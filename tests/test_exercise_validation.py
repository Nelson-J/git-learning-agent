import unittest
import tempfile
import shutil
import os
from src.models import GitCommand
from src.exercises import ExerciseValidator
from src.repository import VirtualRepository


class TestExerciseValidation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.validator = ExerciseValidator()
        self.validator.set_workspace(self.temp_dir)
        # Remove automatic initialization
        self.validator.virtual_repo.initialized = False

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_command_sequence_validation(self):
        """Test a complete sequence of Git commands in an exercise."""
        # Start with a clean repository state
        self.validator.virtual_repo = VirtualRepository(self.temp_dir)

        # Create and add a file first
        with open(os.path.join(self.temp_dir, "test.txt"), "w") as f:
            f.write("test content")

        # Then test the commands
        init_cmd = GitCommand(
            name="init",
            args=[],
            expected_output="",
            validation_rules={"must_exist": ".git"},
        )
        success, message = self.validator.validate_command(init_cmd)
        self.assertTrue(success, f"Init failed: {message}")

        # Create and add a file
        with open(os.path.join(self.temp_dir, "test.txt"), "w") as f:
            f.write("test content")

        add_cmd = GitCommand(
            name="add",
            args=["test.txt"],
            expected_output="",
            validation_rules={"must_be_staged": "test.txt"},
        )
        success, message = self.validator.validate_command(add_cmd)
        self.assertTrue(success, f"Add failed: {message}")

        # Make a commit
        commit_cmd = GitCommand(
            name="commit",
            args=["-m", "Initial commit"],
            expected_output="",
            validation_rules={"must_have_commit": "Initial commit"},
        )
        success, message = self.validator.validate_command(commit_cmd)
        self.assertTrue(success, f"Commit failed: {message}")

    def test_invalid_command_sequence(self):
        """Test validation of incorrect command sequences."""
        # Try to commit before init
        commit_cmd = GitCommand(
            name="commit", args=["-m", "test"], expected_output="", validation_rules={}
        )
        success, message = self.validator.validate_command(commit_cmd)
        self.assertFalse(success)
        self.assertIn("Repository not initialized", message)

    def test_exercise_state_tracking(self):
        """Test if exercise state is properly tracked."""
        self.validator.start_exercise("basic_git_workflow", "init_repo")

        # Complete the init exercise
        init_cmd = GitCommand(
            name="init",
            args=[],
            expected_output="",
            validation_rules={"must_exist": ".git"},
        )
        success, _ = self.validator.validate_command(init_cmd)
        self.assertTrue(success)
        self.assertTrue(
            self.validator.path_manager.is_exercise_completed(
                "basic_git_workflow", "init_repo"
            )
        )

    def test_feedback_quality(self):
        """Test the quality and relevance of feedback messages."""
        # Test unintialized repo feedback
        add_cmd = GitCommand(
            name="add", args=["test.txt"], expected_output="", validation_rules={}
        )
        success, message = self.validator.validate_command(add_cmd)
        self.assertFalse(success)
        self.assertIn("Repository not initialized", message)

        # Test progressive hints
        self.validator.init()
        success, message = self.validator.validate_command(add_cmd)
        self.assertFalse(success)
        hints = self.validator.get_hints("add_nonexistent")
        self.assertTrue(len(hints) > 0)


if __name__ == "__main__":
    unittest.main()
