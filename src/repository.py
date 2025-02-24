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
        """Initialize a new virtual repository."""
        if not self.initialized:
            self.branches["main"] = Branch("main")
            self.initialized = True
            self.current_branch = "main"
            return True
        return False

    def add_file(self, path: str, content: str) -> bool:
        """Add or update a file in the working directory."""
        self.files[path] = VirtualFile(path, content)
        return True

    def stage_file(self, path: str) -> bool:
        """Stage a file for commit."""
        if not self.initialized or path not in self.files:
            return False
        self.files[path].staged = True
        self.staged_files[path] = self.files[path]
        return True

    def commit(self, message: str) -> Optional[str]:
        """Create a new commit with staged files."""
        if not self.initialized or not self.staged_files:
            return None

        # Create file snapshot
        files_snapshot = {
            path: file.get_hash() for path, file in self.staged_files.items()
        }

        # Create commit
        timestamp = datetime.now()
        parent = self.branches[self.current_branch].head
        commit_hash = hashlib.sha1(f"{timestamp}{message}{parent}".encode()).hexdigest()

        commit = Commit(
            hash=commit_hash,
            message=message,
            timestamp=timestamp,
            parent=parent,
            files=files_snapshot,
        )

        # Update repository state
        self.commits[commit_hash] = commit
        self.branches[self.current_branch].head = commit_hash
        self.staged_files.clear()

        return commit_hash

    def create_branch(self, name: str) -> bool:
        """Create a new branch at current commit."""
        if name in self.branches:
            return False

        current_commit = self.branches[self.current_branch].head
        self.branches[name] = Branch(name, current_commit)
        return True

    def switch_branch(self, name: str) -> bool:
        """Switch to another branch."""
        if name not in self.branches:
            return False

        self.current_branch = name
        return True

    def merge_branch(self, source_branch: str) -> bool:
        """Merge source branch into current branch."""
        if (
            not self.initialized
            or source_branch not in self.branches
            or source_branch == self.current_branch
        ):
            return False

        source_commit = self.branches[source_branch].head
        target_commit = self.branches[self.current_branch].head

        # Cannot merge if source branch has no commits
        if not source_commit:
            return False

        # Simple fast-forward merge if target has no commits
        if not target_commit:
            self.branches[self.current_branch].head = source_commit
            return True

        # Create merge commit
        merge_message = f"Merge branch '{source_branch}' into {self.current_branch}"
        timestamp = datetime.now()
        merge_hash = hashlib.sha1(
            f"{timestamp}{merge_message}{target_commit}{source_commit}".encode()
        ).hexdigest()

        # Combine files from both branches
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
        """Simulate rebasing current branch onto target branch."""
        if branch_name not in self.branches or not self.initialized:
            return False
            
        target_commit = self.branches[branch_name].head
        current_commit = self.branches[self.current_branch].head
        
        if not target_commit or not current_commit:
            return False
            
        # Create new commit with combined changes
        merge_message = f"Rebase {self.current_branch} onto {branch_name}"
        timestamp = datetime.now()
        rebase_hash = hashlib.sha1(
            f"{timestamp}{merge_message}{target_commit}".encode()
        ).hexdigest()
        
        # Combine files, giving preference to current branch changes
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
            files=files_snapshot
        )
        
        self.commits[rebase_hash] = rebase_commit
        self.branches[self.current_branch].head = rebase_hash
        return True

    def configure_hook(self, hook_name: str, script: str) -> bool:
        """Configure a Git hook with given script content."""
        if not self.initialized:
            return False
        
        valid_hooks = {"pre-commit", "post-commit", "pre-push", "post-merge"}
        if hook_name not in valid_hooks:
            return False
            
        # In real Git this would write to .git/hooks/
        # Here we just simulate hook configuration
        return True

    def get_history(self) -> List[Commit]:
        """Get commit history of current branch."""
        history = []
        current = self.branches[self.current_branch].head

        while current:
            commit = self.commits[current]
            history.append(commit)
            current = commit.parent

        return history
