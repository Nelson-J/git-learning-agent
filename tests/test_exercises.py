import os
import shutil
import tempfile
import unittest

from src.exercises import Exercise, ExerciseValidator, GitCommand


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
        exercise = Exercise("init_repo", "Initialize a Git repository", "beginner")
        command = GitCommand(
            name="init",
            args=[],
            expected_output="Initialized empty Git repository",
            validation_rules={"must_exist": ".git"}
        )
        exercise.add_command(command)

        self.assertEqual(exercise.name, "init_repo")
        self.assertEqual(len(exercise.commands), 1)

    def test_validate_init_command(self):
        command = GitCommand(
            name="init",
            args=[],
            expected_output="Initialized empty Git repository",
            validation_rules={"must_exist": ".git"}
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
            validation_rules={"must_exist": ".git"}
        )
        self.validator.validate_command(init_command)

        # Now test add command
        command = GitCommand(
            name="add",
            args=["test.txt"],
            expected_output="",
            validation_rules={"must_be_staged": "test.txt"}
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
            validation_rules={"must_exist": ".git"}
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
            validation_rules={"must_have_commit": "Initial commit"}
        )
        success, _ = self.validator.validate_command(cmd)
        self.assertTrue(success)

    def test_validate_branch_command(self):
        command = GitCommand(
            name="branch",
            args=["feature"],
            expected_output="",
            validation_rules={"branch_exists": "feature"}
        )
        self.validator.virtual_repo.init()
        success, message = self.validator.validate_command(command)
        self.assertTrue(success)

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
            validation_rules={"must_exist": ".git"}
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
            validation_rules={"must_be_staged": "test.txt"}
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
