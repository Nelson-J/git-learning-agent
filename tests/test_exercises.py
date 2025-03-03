import os
import shutil
import tempfile
import unittest

from src.models import Exercise, GitCommand
from src.exercises import ExerciseValidator


class TestExercises(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.validator = ExerciseValidator()
        self.validator.set_workspace(self.temp_dir)
        # Ensure clean state
        if self.validator.virtual_repo:
            self.validator.virtual_repo.initialized = False

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_exercise_creation(self):
        exercise = Exercise(
            exercise_id="init_repo",
            name="Initialize a Git repository",
            description="Learn to initialize a Git repository",
            difficulty="beginner",
            commands=[
                GitCommand(
                    name="init",
                    args=[],
                    expected_output="Initialized empty Git repository",
                    validation_rules={"must_exist": ".git"}
                )
            ]
        )

        self.assertEqual(exercise.exercise_id, "init_repo")
        self.assertEqual(len(exercise.commands), 1)

    def test_validate_init_command(self):
        command = GitCommand(
            name="init",
            args=[],
            expected_output="Initialized empty Git repository",
            validation_rules={"must_exist": ".git"},
        )
        os.makedirs(os.path.join(self.temp_dir, ".git"))
        success, message = self.validator.validate_command(command)
        self.assertTrue(success)

    def test_validate_add_command(self):
        # Initialize repository first
        init_command = GitCommand(
            name="init",
            args=[],
            expected_output="Initialized empty Git repository",
            validation_rules={"must_exist": ".git"},
        )
        self.validator.validate_command(init_command)

        # Now test add command
        command = GitCommand(
            name="add",
            args=["test.txt"],
            expected_output="",
            validation_rules={"must_be_staged": "test.txt"},
        )
        self.validator.virtual_repo.add_file("test.txt", "test content")
        success, message = self.validator.validate_command(command)
        self.assertTrue(success)

    def test_validate_commit_command(self):
        # Initialize repository first
        init_cmd = GitCommand(
            name="init",
            args=[],
            expected_output="Initialized empty Git repository",
            validation_rules={"must_exist": ".git"},
        )
        self.validator.validate_command(init_cmd)
        # Prepare test file with proper spacing
        test_file = "test.txt"
        content = "test content"
        self.validator.virtual_repo.add_file(test_file, content)
        self.validator.virtual_repo.stage_file(test_file)
        # Test commit
        cmd = GitCommand(
            name="commit",
            args=["-m", "Initial commit"],
            expected_output="",
            validation_rules={"must_have_commit": "Initial commit"},
        )
        success, _ = self.validator.validate_command(cmd)
        self.assertTrue(success)

    def test_validate_branch_command(self):
        command = GitCommand(
            name="branch",
            args=["feature"],
            expected_output="",
            validation_rules={"branch_exists": "feature"},
        )
        self.validator.virtual_repo.init()
        success, message = self.validator.validate_command(command)
        self.assertTrue(success)

    def test_validate_merge_command(self):
        """Test merge command validation."""
        # Setup initial repository state
        self.validator.virtual_repo.init()

        # Add and commit a file on main branch
        self.validator.virtual_repo.add_file("main.txt", "main content")
        self.validator.virtual_repo.stage_file("main.txt")
        self.validator.virtual_repo.commit("Initial commit")

        # Create and switch to feature branch
        self.validator.virtual_repo.create_branch("feature")
        self.validator.virtual_repo.switch_branch("feature")

        # Add and commit a file on feature branch
        self.validator.virtual_repo.add_file("feature.txt", "feature content")
        self.validator.virtual_repo.stage_file("feature.txt")
        self.validator.virtual_repo.commit("Feature commit")

        # Switch back to main
        self.validator.virtual_repo.switch_branch("main")

        # Test merging
        merge_cmd = GitCommand(
            name="merge",
            args=["feature"],
            expected_output="",
            validation_rules={"branch_merged": "feature"},
        )
        success, message = self.validator.validate_command(merge_cmd)
        self.assertTrue(success)
        self.assertIn("Successfully merged", message)

    def test_validate_checkout_command(self):
        """Test checkout command validation."""
        # Setup repository
        self.validator.virtual_repo.init()
        self.validator.virtual_repo.create_branch("feature")

        # Test checkout
        checkout_cmd = GitCommand(
            name="checkout",
            args=["feature"],
            expected_output="",
            validation_rules={"current_branch": "feature"},
        )
        success, message = self.validator.validate_command(checkout_cmd)
        self.assertTrue(success)
        self.assertEqual(self.validator.virtual_repo.current_branch, "feature")

    def test_exercise_path_integration(self):
        """Test integration between exercises and learning paths."""
        # Start an exercise
        success, message = self.validator.start_exercise(
            "basic_git_workflow", "init_repo"
        )
        self.assertTrue(success)

        # Test init command in exercise context
        command = GitCommand(
            name="init",
            args=[],
            expected_output="Initialized empty Git repository",
            validation_rules={"must_exist": ".git"},
        )
        success, message = self.validator.validate_command(command)
        self.assertTrue(success)
        self.assertTrue(
            self.validator.path_manager.is_exercise_completed(
                "basic_git_workflow", "init_repo"
            )
        )

    def test_exercise_feedback(self):
        """Test exercise-specific feedback."""
        command = GitCommand(
            name="add",
            args=["test.txt"],
            expected_output="",
            validation_rules={"must_be_staged": "test.txt"},
        )
        success, message = self.validator.validate_command(command)
        self.assertFalse(success)
        self.assertIn("Repository not initialized", message)

    def test_exercise(self):
        assert True

    def another_test(self):
        assert True


if __name__ == "__main__":
    unittest.main()
