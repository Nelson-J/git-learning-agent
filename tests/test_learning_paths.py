import unittest
from src.learning_paths import PathManager


class TestLearningPaths(unittest.TestCase):
    def setUp(self):
        self.path_manager = PathManager()

    def test_basic_workflow_path(self):
        path = self.path_manager.get_path("basic_git_workflow")
        self.assertIsNotNone(path)
        self.assertEqual(path.difficulty, "beginner")
        self.assertEqual(len(path.exercises), 3)
        self.assertEqual(len(path.prerequisites), 0)

    def test_branching_basics_path(self):
        path = self.path_manager.get_path("branching_basics")
        self.assertIsNotNone(path)
        self.assertEqual(path.difficulty, "beginner")
        self.assertIn("basic_git_workflow", path.prerequisites)

    def test_available_paths(self):
        # New user should only see basic_git_workflow
        available = self.path_manager.get_available_paths([])
        self.assertEqual(len(available), 1)
        self.assertEqual(available[0].name, "basic_git_workflow")

        # After completing basic_workflow, should see branching_basics
        available = self.path_manager.get_available_paths(["basic_git_workflow"])
        self.assertEqual(len(available), 2)

    def test_path_progress(self):
        path_name = "basic_git_workflow"
        self.assertTrue(self.path_manager.start_path(path_name))

        # Complete exercises
        self.assertTrue(self.path_manager.complete_exercise(path_name, "init_repo"))
        self.assertTrue(self.path_manager.complete_exercise(path_name, "first_commit"))
        self.assertTrue(self.path_manager.complete_exercise(path_name, "view_history"))

        # Verify path completion
        self.assertTrue(self.path_manager.is_path_completed(path_name))

    def test_invalid_path_progress(self):
        self.assertFalse(self.path_manager.start_path("nonexistent_path"))
        self.assertFalse(
            self.path_manager.complete_exercise("nonexistent_path", "exercise")
        )
        self.assertFalse(self.path_manager.is_path_completed("nonexistent_path"))


if __name__ == "__main__":
    unittest.main()
