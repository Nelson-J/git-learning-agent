import unittest
import sys
sys.path.insert(0, './src')
from datetime import datetime
from models import UserProfile, Exercise, Progress, PersistenceLayer

class TestModels(unittest.TestCase):

    def setUp(self):
        self.persistence = PersistenceLayer()
        self.user = UserProfile(user_id="1", username="test_user", email="test@example.com")
        self.exercise = Exercise(
            name="test_exercise",
            description="Test Exercise",
            difficulty="beginner",
            exercise_id="1"
        )
        self.progress = Progress(user_id="1", exercise_id="1", status="completed", last_attempt=datetime.now())
        self.persistence.add_user(self.user)
        self.persistence.add_exercise(self.exercise)
        self.persistence.update_progress(self.progress)

    def test_assess_skill(self):
        skill = self.user.assess_skill()
        self.assertEqual(skill, 1)

    def test_adjust_difficulty(self):
        difficulty = self.persistence.adjust_difficulty("1")
        self.assertEqual(difficulty, "beginner")

    def test_generate_learning_path(self):
        learning_path = self.persistence.generate_learning_path("1")
        self.assertEqual(len(learning_path), 1)
        self.assertEqual(learning_path[0].exercise_id, "1")

    def test_evaluate_progress(self):
        progress = self.persistence.evaluate_progress("1")
        self.assertEqual(progress["1"], "completed")

if __name__ == '__main__':
    unittest.main()
