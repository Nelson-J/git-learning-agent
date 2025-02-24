from typing import List, Dict, Optional, Tuple
import os
from ..repository import VirtualRepository
from ..feedback import FeedbackManager
from ..learning_paths import PathManager
from ..models import Exercise, GitCommand


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
        if not self.path_manager.start_path(path_name):
            return False, "Invalid learning path"

        self.current_path = path_name
        self.current_exercise = exercise_name
        self.virtual_repo = VirtualRepository(self.workspace_path)
        return True, f"Started exercise: {exercise_name}"

    def validate_command(self, command: GitCommand) -> Tuple[bool, str]:
        if not self.virtual_repo:
            return False, self._get_feedback("workspace_not_initialized")

        if command.name != "init" and not self.virtual_repo.initialized:
            return False, "Repository not initialized"

        validators = {
            "init": self._validate_init,
            "add": self._validate_add,
            "commit": self._validate_commit,
            "branch": self._validate_branch,
            "merge": self._validate_merge,
            "checkout": self._validate_checkout,
            "rebase": self._validate_rebase,
            "config": self._validate_hook,
        }
        validator = validators.get(command.name)
        if not validator:
            return False, self._get_feedback("unsupported_command")

        success, message = validator(command)
        if success and self.current_path and self.current_exercise:
            self.path_manager.complete_exercise(
                self.current_path,
                self.current_exercise
            )
        return success, message

    def _get_feedback(self, error_type: str, context: Dict = None) -> str:
        return self.feedback_manager.get_feedback(error_type, context or {})

    def _validate_init(self, command: GitCommand) -> Tuple[bool, str]:
        success = self.virtual_repo.init()
        return (
            success,
            "Repository initialized successfully"
            if success
            else "Repository already initialized",
        )

    def _validate_add(self, command: GitCommand) -> Tuple[bool, str]:
        if not command.args:
            return False, self._get_feedback("no_files_specified")

        # First add file to repo if it exists in workspace
        for file_path in command.args:
            full_path = os.path.join(self.workspace_path, file_path)
            if os.path.exists(full_path):
                with open(full_path, "r") as f:
                    content = f.read()
                self.virtual_repo.add_file(file_path, content)

        # Then stage the files
        all_staged = all(self.virtual_repo.stage_file(file) for file in command.args)
        return (
            (True, "Files staged successfully")
            if all_staged
            else (False, "Failed to stage files")
        )

    def _validate_commit(self, command: GitCommand) -> Tuple[bool, str]:
        if not command.args or len(command.args) < 2 or command.args[0] != "-m":
            return False, self._get_feedback("invalid_commit_format")

        commit_hash = self.virtual_repo.commit(command.args[1])
        return bool(commit_hash), (
            self._get_feedback("commit_success")
            if commit_hash
            else self._get_feedback("nothing_to_commit")
        )

    def _validate_branch(self, command: GitCommand) -> Tuple[bool, str]:
        if not command.args:
            return False, "Branch name not specified"

        success = self.virtual_repo.create_branch(command.args[0])
        return (
            success,
            f"Branch '{command.args[0]}' created"
            if success
            else "Failed to create branch",
        )

    def _validate_merge(self, command: GitCommand) -> Tuple[bool, str]:
        if not command.args:
            return False, "Branch name not specified"

        source_branch = command.args[0]
        if source_branch not in self.virtual_repo.branches:
            return False, f"Branch '{source_branch}' does not exist"

        success = self.virtual_repo.merge_branch(source_branch)
        if success:
            message = f"Successfully merged '{source_branch}' into '{self.virtual_repo.current_branch}'"
        else:
            message = "Merge failed - ensure branches have commits and no conflicts"
        return success, message

    def _validate_checkout(self, command: GitCommand) -> Tuple[bool, str]:
        if not command.args:
            return False, "Branch name not specified"

        branch_name = command.args[0]
        success = self.virtual_repo.switch_branch(branch_name)
        return success, (
            f"Switched to branch '{branch_name}'"
            if success
            else f"Failed to switch to branch '{branch_name}'"
        )

    def _validate_rebase(self, command: GitCommand) -> Tuple[bool, str]:
        """Validate rebase command."""
        if not command.args:
            return False, "Target branch name required for rebase"
            
        success = self.virtual_repo.rebase(command.args[0])
        return success, (
            f"Successfully rebased onto {command.args[0]}"
            if success
            else "Rebase failed - ensure branches exist and have commits"
        )

    def _validate_hook(self, command: GitCommand) -> Tuple[bool, str]:
        """Validate hook configuration command."""
        if len(command.args) < 2 or not command.args[0].startswith("hooks."):
            return False, "Invalid hook configuration format"
            
        hook_name = command.args[0].split(".")[1]
        script_content = command.args[1]
        success = self.virtual_repo.configure_hook(hook_name, script_content)
        return success, (
            f"Successfully configured {hook_name} hook"
            if success
            else "Failed to configure hook"
        )

    def setup_complex_scenario(self, exercise: Exercise) -> Tuple[bool, str]:
        """Set up a complex scenario for validation."""
        if not exercise.complex_scenario:
            return False, "No complex scenario defined"
            
        # Run setup commands
        for cmd in exercise.complex_scenario.setup_commands:
            success, _ = self.validate_command(cmd)
            if not success:
                return False, "Failed to set up scenario"
                
        # Create conflicts if defined
        for file_path, versions in exercise.complex_scenario.conflict_files.items():
            self.virtual_repo.simulate_conflict(file_path, versions)
            
        return True, "Complex scenario set up successfully"

    def validate_scenario_resolution(self, exercise: Exercise, commands: List[GitCommand]) -> Tuple[bool, str]:
        """Validate the resolution of a complex scenario."""
        if not exercise.complex_scenario:
            return False, "No complex scenario to validate"
            
        if self.virtual_repo.is_in_conflict():
            return False, "Conflicts not fully resolved"
            
        is_valid = exercise.validate_scenario_resolution(commands)
        return is_valid, (
            "Scenario resolved correctly" if is_valid 
            else "Scenario not resolved as expected"
        )

    def get_hints(self, error_type: str) -> List[str]:
        if not hasattr(self, "hint_generator"):
            return [self.feedback_manager.get_feedback(error_type)]

        current_exercise = self.path_manager.get_path(self.current_path)
        skill_level = current_exercise.difficulty if current_exercise else "beginner"

        return self.feedback_manager.get_feedback(
            error_type, {"skill_level": skill_level}
        ).split("\n")

    def init(self) -> bool:
        if self.virtual_repo:
            return self.virtual_repo.init()
        return False

    def get_current_exercise(
        self, path_name: str, exercise_name: str
    ) -> Optional[Exercise]:
        return None  # TODO: Implement proper exercise lookup
