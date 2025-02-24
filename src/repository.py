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

    def get_history(self) -> List[Commit]:
        """Get commit history of current branch."""
        history = []
        current = self.branches[self.current_branch].head

        while current:
            commit = self.commits[current]
            history.append(commit)
            current = commit.parent

        return history
