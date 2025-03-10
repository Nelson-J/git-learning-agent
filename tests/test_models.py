import unittest
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.models import Base, Exercise, Progress, UserProfile, GitCommand
from src.database.persistence_layer import PersistenceLayer

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)

    def setUp(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.session.execute(text('PRAGMA foreign_keys=ON'))
        self.persistence = PersistenceLayer(self.session)
        self.user = UserProfile(
            username="test_user",
            email="test@example.com"
        )
        self.exercise = Exercise(
            exercise_id="1",
            name="test_exercise",
            description="test_description",
            difficulty="beginner",
        )
        self.command = GitCommand(
            name="init",
            args=[],
            expected_output="Initialized empty Git repository",
            validation_rules={"status": "success"}
        )
        self.exercise.commands.append(self.command)
        self.progress = Progress(
            user_id=self.user.user_id,
            exercise_id=self.exercise.exercise_id,
            status="completed",
            last_attempt=datetime.now(),
        )
        self.user.progress.append(self.progress)
        self.persistence.add_user(self.user)
        self.persistence.add_exercise(self.exercise)

    def test_assess_skill(self):
        skill = self.progress.assess_skill()
        self.assertEqual(skill, 10)

    def test_adjust_difficulty(self):
        self.persistence.update_progress(self.progress)
        difficulty = self.persistence.adjust_difficulty(self.user.user_id)
        self.assertEqual(difficulty, "beginner")

    def test_generate_learning_path(self):
        self.persistence.update_progress(self.progress)
        path = self.persistence.generate_learning_path(self.user.user_id)
        self.assertIn(self.exercise, path)

    def test_evaluate_progress(self):
        self.persistence.update_progress(self.progress)
        progress = self.persistence.evaluate_progress(self.user.user_id)
        self.assertIn(self.progress, progress)


if __name__ == "__main__":
    unittest.main()
