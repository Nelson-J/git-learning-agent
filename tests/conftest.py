import pytest
import tempfile
import shutil
from typing import Generator

from src.models import Exercise, GitCommand
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
        difficulty="beginner"
    )
    command = GitCommand(
        name="init",
        args=[],
        expected_output="Initialized empty Git repository",
        validation_rules={"must_exist": ".git"}
    )
    exercise.add_command(command)
    return exercise
