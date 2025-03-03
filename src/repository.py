from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import hashlib


@dataclass
class VirtualFile:
    path: str
    content: str
    staged: bool = False

    def get_hash(self) -> str:
        return hashlib.sha1(self.content.encode()).hexdigest()


@dataclass
class Commit:
    hash: str
    message: str
    timestamp: datetime
    parent: Optional[str] = None
    files: Dict[str, str] = None  # path -> hash


class Branch:
    def __init__(self, name: str, commit: Optional[str] = None):
        self.name = name
        self.head = commit


class VirtualRepository:
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        self.files: Dict[str, VirtualFile] = {}
        self.commits: Dict[str, Commit] = {}
        self.branches: Dict[str, Branch] = {}
        self.current_branch = "main"
        self.staged_files: Dict[str, VirtualFile] = {}
        self.initialized = False

    def init(self) -> bool:
        if not self.initialized:
            self.branches["main"] = Branch("main")
            self.initialized = True
            self.current_branch = "main"
            return True
        return False

    def add_file(self, path: str, content: str) -> bool:
        self.files[path] = VirtualFile(path, content)
        return True

    def stage_file(self, path: str) -> bool:
        if not self.initialized or path not in self.files:
            return False
        self.files[path].staged = True
        self.staged_files[path] = self.files[path]
        return True

    def commit(self, message: str) -> Optional[str]:
        if not self.initialized or not self.staged_files:
            return None
        files_snapshot = {
            path: file.get_hash() for path, file in self.staged_files.items()
        }
        timestamp = datetime.now()
        parent = self.branches[self.current_branch].head
        commit_hash = hashlib.sha1(
            f"{timestamp}{message}{parent}".encode()
        ).hexdigest()
        commit = Commit(
            hash=commit_hash,
            message=message,
            timestamp=timestamp,
            parent=parent,
            files=files_snapshot,
        )
        self.commits[commit_hash] = commit
        self.branches[self.current_branch].head = commit_hash
        self.staged_files.clear()
        return commit_hash

    def create_branch(self, name: str) -> bool:
        if name in self.branches:
            return False
        current_commit = self.branches[self.current_branch].head
        self.branches[name] = Branch(name, current_commit)
        return True

    def switch_branch(self, name: str) -> bool:
        if name not in self.branches:
            return False
        self.current_branch = name
        return True

    def merge_branch(self, source_branch: str) -> bool:
        if (
            not self.initialized
            or source_branch not in self.branches
            or source_branch == self.current_branch
        ):
            return False
        source_commit = self.branches[source_branch].head
        target_commit = self.branches[self.current_branch].head
        if not source_commit:
            return False
        if not target_commit:
            self.branches[self.current_branch].head = source_commit
            return True
        merge_message = f"Merge branch '{source_branch}' into {self.current_branch}"
        timestamp = datetime.now()
        merge_hash = hashlib.sha1(
            f"{timestamp}{merge_message}{target_commit}{source_commit}".encode()
        ).hexdigest()
        files_snapshot = {}
        if target_commit in self.commits:
            files_snapshot.update(self.commits[target_commit].files or {})
        if source_commit in self.commits:
            files_snapshot.update(self.commits[source_commit].files or {})
        merge_commit = Commit(
            hash=merge_hash,
            message=merge_message,
            timestamp=timestamp,
            parent=target_commit,
            files=files_snapshot,
        )
        self.commits[merge_hash] = merge_commit
        self.branches[self.current_branch].head = merge_hash
        return True

    def rebase(self, branch_name: str) -> bool:
        if branch_name not in self.branches or not self.initialized:
            return False
        target_commit = self.branches[branch_name].head
        current_commit = self.branches[self.current_branch].head
        if not target_commit or not current_commit:
            return False
        merge_message = f"Rebase {self.current_branch} onto {branch_name}"
        timestamp = datetime.now()
        rebase_hash = hashlib.sha1(
            f"{timestamp}{merge_message}{target_commit}".encode()
        ).hexdigest()
        files_snapshot = {}
        if target_commit in self.commits:
            files_snapshot.update(self.commits[target_commit].files or {})
        if current_commit in self.commits:
            files_snapshot.update(self.commits[current_commit].files or {})
        rebase_commit = Commit(
            hash=rebase_hash,
            message=merge_message,
            timestamp=timestamp,
            parent=target_commit,
            files=files_snapshot,
        )
        self.commits[rebase_hash] = rebase_commit
        self.branches[self.current_branch].head = rebase_hash
        return True

    def configure_hook(self, hook_name: str, script: str) -> bool:
        if not self.initialized:
            return False
        valid_hooks = {"pre-commit", "post-commit", "pre-push", "post-merge"}
        if hook_name not in valid_hooks:
            return False
        return True

    def get_history(self) -> List[Commit]:
        history = []
        current = self.branches[self.current_branch].head
        while current:
            commit = self.commits[current]
            history.append(commit)
            current = commit.parent
        return history
