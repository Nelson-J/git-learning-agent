import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.database.persistence_layer import PersistenceLayer
from src.models.user_profile import UserProfile
from src.models.exercise import Exercise, GitCommand
from src.models.progress import Progress

class TestPersistenceLayer(unittest.TestCase):
    def setup_method(self, method):
        engine = create_engine('sqlite:///:memory:')
        Base = declarative_base()
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.persistence = PersistenceLayer(self.session)

    def test_add_user(self):
        """Test adding a new user."""
        user = UserProfile(username="test_user", email="test@example.com")
        result = self.persistence.add_user(user)
        assert result.username == "test_user"
        assert result.email == "test@example.com"

    def test_get_user(self):
        """Test retrieving a user."""
        user = UserProfile(username="test_user", email="test@example.com")
        self.persistence.add_user(user)
        result = self.persistence.get_user("test_user")
        assert result is not None
        assert result.username == "test_user"

    def test_update_user_progress(self):
        """Test updating user progress."""
        user = UserProfile(username="test_user", email="test@example.com")
        exercise = Exercise(
            exercise_id="git_init",
            name="Initialize Git Repository",
            description="Learn to initialize a Git repository",
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
        self.persistence.add_user(user)
        self.persistence.add_exercise(exercise)
        
        progress = Progress(
            user_id=user.id,
            exercise_id=exercise.id,
            status="completed"
        )
        result = self.persistence.update_progress(progress)
        assert result.status == "completed"

    def test_get_user_exercises(self):
        """Test retrieving user exercises."""
        user = UserProfile(username="test_user", email="test@example.com")
        exercise = Exercise(
            exercise_id="git_init",
            name="Initialize Git Repository",
            description="Learn to initialize a Git repository",
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
        self.persistence.add_user(user)
        self.persistence.add_exercise(exercise)
        
        exercises = self.persistence.get_user_exercises(user.id)
        assert len(exercises) > 0
        assert exercises[0].name == "Initialize Git Repository"
