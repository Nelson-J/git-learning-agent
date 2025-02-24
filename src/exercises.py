from typing import List, Dict, Optional, Tuple
import os
from .repository import VirtualRepository
from .feedback import FeedbackManager
from .learning_paths import PathManager
from .feedback_templates import GitFeedbackTemplates
from .models import Exercise, GitCommand

class ExerciseValidator:
    def __init__(self):
        self.workspace_path: Optional[str] = None
        self.virtual_repo: Optional[VirtualRepository] = None
        self.feedback_manager = FeedbackManager()
        self.path_manager = PathManager()
        self.current_path: Optional[str] = None
        self.current_exercise: Optional[str] = None
        self._path_progress: Dict[str, List[str]] = {}

    def set_workspace(self, path: str):
        self.workspace_path = path
        self.virtual_repo = VirtualRepository(path)
        if not os.path.exists(path):
            os.makedirs(path)

    def start_exercise(self, path_name: str, exercise_name: str) -> Tuple[bool, str]:
        """Initialize an exercise from a learning path."""
        if not self.path_manager.start_path(path_name):
            return False, "Invalid learning path"
        
        self.current_path = path_name
        self.current_exercise = exercise_name
        # Initialize a fresh repository state
        self.virtual_repo = VirtualRepository(self.workspace_path)
        return True, f"Started exercise: {exercise_name}"

    def validate_command(self, command: GitCommand) -> tuple[bool, str]:
        if not self.virtual_repo:
            return False, self._get_feedback("workspace_not_initialized")

        # Check if repository needs initialization
        if command.name != "init" and not self.virtual_repo.initialized:
            return False, "Repository not initialized"  # Changed to match test expectations

        # Validate command and track completion
        success, message = self._validate_command_impl(command)
        
        # If command successful and we're in an exercise context, mark progress
        if success and self.current_path and self.current_exercise:
            self.path_manager.complete_exercise(self.current_path, self.current_exercise)
        
        return success, message

    def _validate_command_impl(self, command: GitCommand) -> tuple[bool, str]:
        if command.name == "init":
            return self._validate_init(command)
        elif command.name == "add":
            return self._validate_add(command)
        elif command.name == "commit":
            return self._validate_commit(command)
        elif command.name == "branch":
            return self._validate_branch(command)
        return False, self._get_feedback("unsupported_command")

    def _get_feedback(self, error_type: str, context: Dict = None) -> str:
        """Get formatted feedback from templates."""
        return self.feedback_manager.get_feedback(error_type, context or {})

    def _validate_init(self, command: GitCommand) -> tuple[bool, str]:
        success = self.virtual_repo.init()
        return success, "Repository initialized successfully" if success else "Repository already initialized"

    def _validate_add(self, command: GitCommand) -> tuple[bool, str]:
        if not command.args:
            return False, self._get_feedback("no_files_specified")
        
        if not self.virtual_repo.initialized:
            return False, "Repository not initialized"
            
        # First add file to repo if it exists in workspace
        for file_path in command.args:
            full_path = os.path.join(self.workspace_path, file_path)
            if os.path.exists(full_path):
                with open(full_path, 'r') as f:
                    content = f.read()
                self.virtual_repo.add_file(file_path, content)
        
        # Then stage the files
        all_staged = all(self.virtual_repo.stage_file(file) for file in command.args)
        if all_staged:
            return True, "Files staged successfully"
        return False, "Failed to stage files"

    def _validate_commit(self, command: GitCommand) -> tuple[bool, str]:
        if not command.args or len(command.args) < 2 or command.args[0] != "-m":
            return False, self._get_feedback("invalid_commit_format")
            
        commit_hash = self.virtual_repo.commit(command.args[1])
        
        if commit_hash and self.current_path and self.current_exercise:
            self.path_manager.complete_exercise(self.current_path, self.current_exercise)
            
        return bool(commit_hash), (
            self._get_feedback("commit_success") if commit_hash 
            else self._get_feedback("nothing_to_commit")
        )

    def _validate_branch(self, command: GitCommand) -> tuple[bool, str]:
        if not command.args:
            return False, "Branch name not specified"
            
        success = self.virtual_repo.create_branch(command.args[0])
        return success, f"Branch '{command.args[0]}' created" if success else "Failed to create branch"

    def get_hints(self, error_type: str) -> List[str]:
        """Get progressive hints for an error type."""
        if not hasattr(self, 'hint_generator'):
            return [self.feedback_manager.get_feedback(error_type)]
        
        current_exercise = self.path_manager.get_path(self.current_path)
        skill_level = current_exercise.difficulty if current_exercise else "beginner"
        
        return self.feedback_manager.get_feedback(
            error_type,
            {"skill_level": skill_level}
        ).split('\n')

    def init(self) -> bool:
        """Initialize the validator's virtual repository."""
        if self.virtual_repo:
            return self.virtual_repo.init()
        return False

    def get_current_exercise(self, path_name: str, exercise_name: str) -> Optional[Exercise]:
        # Simplified exercise lookup
        return None  # TODO: Implement proper exercise lookup
