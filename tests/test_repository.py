import unittest
from src.repository import VirtualRepository


class TestVirtualRepository(unittest.TestCase):
    def setUp(self):
        self.repo = VirtualRepository("/test/workspace")

    def test_init(self):
        self.assertTrue(self.repo.init())
        self.assertIn("main", self.repo.branches)

    def test_add_and_stage_file(self):
        self.repo.init()
        self.assertTrue(self.repo.add_file("test.txt", "content"))
        self.assertTrue(self.repo.stage_file("test.txt"))
        self.assertIn("test.txt", self.repo.staged_files)

    def test_commit(self):
        # Ensure repository is initialized first
        self.assertTrue(self.repo.init())

        # Now test commit functionality
        self.repo.add_file("test.txt", "content")
        self.repo.stage_file("test.txt")

        commit_hash = self.repo.commit("Initial commit")
        self.assertIsNotNone(commit_hash)
        self.assertIn(commit_hash, self.repo.commits)
        self.assertEqual(self.repo.branches["main"].head, commit_hash)

    def test_branch_operations(self):
        self.repo.init()
        self.assertTrue(self.repo.create_branch("feature"))
        self.assertTrue(self.repo.switch_branch("feature"))
        self.assertEqual(self.repo.current_branch, "feature")


if __name__ == "__main__":
    unittest.main()
