import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.persistence_layer import PersistenceLayer
from src.models.user_profile import UserProfile
from src.models.exercise import Exercise, GitCommand
from src.models.progress import Progress

@pytest.fixture(scope='module')
def test_db():
    """Create a test database connection."""
    engine = create_engine('sqlite:///:memory:')
    # Create all tables in the in-memory database
    UserProfile.metadata.create_all(engine)
    Exercise.metadata.create_all(engine)
    Progress.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

@pytest.fixture
def persistence_layer(test_db):
    """Create a persistence layer instance with test database."""
    return PersistenceLayer(test_db)

def test_add_user(persistence_layer):
    """Test adding a new user."""
    user = UserProfile(username="test_user", email="test@example.com")
    result = persistence_layer.add_user(user)
    assert result.username == "test_user"
    assert result.email == "test@example.com"

def test_get_user(persistence_layer):
    """Test retrieving a user."""
    user = UserProfile(username="test_user", email="test@example.com")
    persistence_layer.add_user(user)
    result = persistence_layer.get_user("test_user")
    assert result is not None
    assert result.username == "test_user"

def test_update_user_progress(persistence_layer):
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
    persistence_layer.add_user(user)
    persistence_layer.add_exercise(exercise)
    
    progress = Progress(user=user, exercise=exercise, status="completed")
    result = persistence_layer.update_progress(progress)
    assert result.status == "completed"

def test_get_user_exercises(persistence_layer):
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
    persistence_layer.add_user(user)
    persistence_layer.add_exercise(exercise)
    
    exercises = persistence_layer.get_user_exercises(user.id)
    assert len(exercises) > 0
    assert exercises[0].name == "Initialize Git Repository"
