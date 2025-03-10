import pytest
import tempfile
import shutil
from typing import Generator
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.models import Exercise, GitCommand, UserProfile, Base
from src.exercises import ExerciseValidator


@pytest.fixture
def temp_workspace() -> Generator[str, None, None]:
    """Create a temporary workspace for tests."""
    workspace = tempfile.mkdtemp()
    yield workspace
    shutil.rmtree(workspace)


@pytest.fixture
def validator(temp_workspace: str) -> ExerciseValidator:
    """Create an exercise validator with temp workspace."""
    validator = ExerciseValidator()
    validator.set_workspace(temp_workspace)
    return validator


@pytest.fixture
def basic_exercise() -> Exercise:
    """Create a basic exercise for testing."""
    exercise = Exercise(
        name="init_repo",
        description="Initialize a Git repository",
        difficulty="beginner",
    )
    command = GitCommand(
        name="init",
        args=[],
        expected_output="Initialized empty Git repository",
        validation_rules={"must_exist": ".git"},
    )
    exercise.add_command(command)
    return exercise


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: mark test as an integration test"
    )


@pytest.fixture(scope='session')
def db_engine():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def mock_exercise():
    """Create a mock exercise for testing."""
    return Exercise(
        exercise_id="ex_001",
        name="Basic Git Init",
        difficulty="beginner",
        description="Initialize a new Git repository",
        steps=["git init"],
        expected_output="Initialized empty Git repository",
        created_at=datetime.now()
    )


@pytest.fixture
def mock_user_profile():
    """Create a mock user profile for testing."""
    return UserProfile(
        user_id="test_user",
        username="testuser",
        email="test@example.com",
        skill_level="beginner",
        created_at=datetime.now()
    )
