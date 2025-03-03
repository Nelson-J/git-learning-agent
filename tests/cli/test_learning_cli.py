import pytest
from src.cli.learning_cli import GitLearningCLI
from src.database.persistence_layer import PersistenceLayer
from click.testing import CliRunner

@pytest.fixture
def cli():
    """Create a CLI instance for testing."""
    return GitLearningCLI()

def test_create_user_command(cli):
    """Test user creation command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["create-user", "--username", "test_user"])
    assert "User created successfully" in result.output
    assert "test_user" in result.output

def test_start_exercise_command(cli):
    """Test starting an exercise."""
    # First create a user
    runner = CliRunner()
    runner.invoke(cli, ["create-user", "--username", "test_user"])
    # Then start an exercise
    result = runner.invoke(cli, ["start-exercise", "--name", "git_init"])
    assert "Exercise started" in result.output

def test_show_progress_command(cli):
    """Test progress display command."""
    # Setup user and complete an exercise
    runner = CliRunner()
    runner.invoke(cli, ["create-user", "--username", "test_user"])
    runner.invoke(cli, ["start-exercise", "--name", "git_init"])
    runner.invoke(cli, ["complete-exercise", "--name", "git_init"])
    
    result = runner.invoke(cli, ["show-progress"])
    assert "git_init" in result.output
    assert "completed" in result.output

def test_help_command(cli):
    """Test help system."""
    runner = CliRunner()
    result = runner.invoke(cli, ["help"])
    assert "Available commands" in result.output
    assert "create-user" in result.output
    assert "start-exercise" in result.output
