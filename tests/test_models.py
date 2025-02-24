import unittest
from datetime import datetime

from src.models import Exercise, Progress, UserProfile, PersistenceLayer


class TestModels(unittest.TestCase):
    def setUp(self):
        self.persistence = PersistenceLayer()
        self.user = UserProfile(
            user_id="1", username="test_user", email="test@example.com"
        )
        self.exercise = Exercise(
            name="test_exercise",
            description="Test Exercise",
            difficulty="beginner",
            exercise_id="1",
        )
        self.progress = Progress(
            user_id="1",
            exercise_id="1",
            status="completed",
            last_attempt=datetime.now(),
        )
        self.user.progress[self.progress.exercise_id] = self.progress

    def test_assess_skill(self):
        skill = self.progress.assess_skill()
        self.assertEqual(skill, 10)

    def test_adjust_difficulty(self):
        self.persistence.add_user(self.user)
        self.persistence.add_exercise(self.exercise)
        self.persistence.update_progress(self.progress)
        difficulty = self.persistence.adjust_difficulty(self.user.user_id)
        self.assertEqual(difficulty, "beginner")

    def test_generate_learning_path(self):
        self.persistence.add_user(self.user)
        self.persistence.add_exercise(self.exercise)
        self.persistence.update_progress(self.progress)
        path = self.persistence.generate_learning_path(self.user.user_id)
        self.assertIn(self.exercise, path)

    def test_evaluate_progress(self):
        self.persistence.add_user(self.user)
        self.persistence.add_exercise(self.exercise)
        self.persistence.update_progress(self.progress)
        progress = self.persistence.evaluate_progress(self.user.user_id)
        self.assertIn("1", progress)


if __name__ == "__main__":
    unittest.main()
