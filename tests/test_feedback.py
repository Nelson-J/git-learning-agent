import unittest
from src.feedback import FeedbackManager


class TestFeedback(unittest.TestCase):
    def setUp(self):
        self.feedback_manager = FeedbackManager()

    def test_basic_feedback(self):
        feedback = self.feedback_manager.get_feedback(
            "invalid_command", {"command": "git comit"}
        )
        self.assertIn("command 'git comit' is not valid", feedback.lower())
        self.assertNotIn("hint", feedback.lower())  # No hints on first attempt

    def test_progressive_feedback(self):
        # First attempt
        feedback1 = self.feedback_manager.get_feedback("uninitialized_repo")
        self.assertNotIn("hint", feedback1.lower())

        # Second attempt - should show first hint
        feedback2 = self.feedback_manager.get_feedback("uninitialized_repo")
        self.assertIn("hint", feedback2.lower())

    def test_reset_attempts(self):
        # First attempt - provide required context
        self.feedback_manager.get_feedback("invalid_command", {"command": "test"})
        self.feedback_manager.reset_attempts("invalid_command")
        # Second attempt - provide required context again
        feedback = self.feedback_manager.get_feedback(
            "invalid_command", {"command": "test"}
        )
        self.assertNotIn("hint", feedback.lower())  # Should be like first attempt

    def test_contextual_feedback(self):
        # Test beginner feedback
        beginner_feedback = self.feedback_manager.get_feedback_with_context(
            "invalid_commit_format", "beginner", 1
        )
        self.assertIn("Invalid commit message format", beginner_feedback)

        # Test intermediate feedback with multiple attempts
        intermediate_feedback = self.feedback_manager.get_feedback_with_context(
            "invalid_commit_format", "intermediate", 2
        )
        self.assertIn("hint", intermediate_feedback.lower())
        self.assertIn("Keep the message clear", intermediate_feedback)

        # Test advanced feedback
        advanced_feedback = self.feedback_manager.get_feedback_with_context(
            "invalid_commit_format", "advanced", 1
        )
        self.assertNotIn(
            "Use -m flag", advanced_feedback
        )  # Basic hints should be omitted


if __name__ == "__main__":
    unittest.main()
