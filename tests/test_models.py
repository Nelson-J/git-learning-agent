import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.models import Exercise, Progress, UserProfile, GitCommand
from src.database.persistence_layer import PersistenceLayer

Base = declarative_base()

class TestModels(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        self.persistence = PersistenceLayer(session)
        self.user = UserProfile(
            username="test_user",
            email="test@example.com"
        )
        self.exercise = Exercise(
            exercise_id="1",
            name="test_exercise",
            description="Test Exercise",
            difficulty="beginner",
            commands=[
                GitCommand(
                    name="init",
                    args=[],
                    expected_output="Initialized empty Git repository",
                    validation_rules={"status": "success"}
                )
            ]
        )
        self.progress = Progress(
            user_id=self.user.user_id,
            exercise_id=self.exercise.exercise_id,
            status="completed",
            last_attempt=datetime.now(),
        )
        self.user.progress = {self.exercise.exercise_id: self.progress}

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
        self.assertIn(self.progress, progress)


if __name__ == "__main__":
    unittest.main()
