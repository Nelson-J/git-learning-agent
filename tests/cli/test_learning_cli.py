import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from src.cli.learning_cli import cli
from src.models.user_profile import UserProfile
from src.models.exercise import Exercise
from src.models.git_command import GitCommand
from src.database.persistence_layer import PersistenceLayer

Base = declarative_base()

@pytest.fixture
def runner():
    return CliRunner()

class TestLearningCLI:
    def setup_method(self):
        self.runner = CliRunner()
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
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
            commands=[
                GitCommand(
                    name="init",
                    args=[],
                    expected_output="Initialized empty Git repository",
                    validation_rules={"status": "success"}
                )
            ]
        )
        self.persistence.add_user(self.user)
        self.persistence.add_exercise(self.exercise)
        self.mock_auth = MagicMock()
        self.mock_auth.get_current_user.return_value = self.user
        self.mock_auth.is_authenticated.return_value = True
        self.mock_auth.login.return_value = True
        self.mock_auth.logout.return_value = True

    @patch('src.cli.learning_cli.get_persistence_layer')
    @patch('src.cli.learning_cli.get_auth')
    def test_create_user_command(self, mock_auth, mock_persistence):
        """Test user creation command."""
        mock_persistence.return_value = self.persistence
        mock_auth.return_value = self.mock_auth
        result = self.runner.invoke(cli, ['create-user', 'test_user'])
        assert 'Created user test_user' in result.output

    @patch('src.cli.learning_cli.get_persistence_layer')
    @patch('src.cli.learning_cli.get_auth')
    def test_start_exercise_command(self, mock_auth, mock_persistence):
        """Test starting an exercise."""
        mock_persistence.return_value = self.persistence
        mock_auth.return_value = self.mock_auth
        result = self.runner.invoke(cli, ['start-exercise', 'git_init'])
        assert 'Starting exercise git_init' in result.output

    @patch('src.cli.learning_cli.get_persistence_layer')
    @patch('src.cli.learning_cli.get_auth')
    def test_start_exercise_command_unauthenticated(self, mock_auth, mock_persistence):
        """Test starting an exercise without authentication."""
        mock_persistence.return_value = self.persistence
        mock_auth.return_value = self.mock_auth
        self.mock_auth.is_authenticated.return_value = False
        result = self.runner.invoke(cli, ['start-exercise', 'git_init'])
        assert 'Please login first' in result.output
        assert result.exit_code == 1

    @patch('src.cli.learning_cli.get_persistence_layer')
    @patch('src.cli.learning_cli.get_auth')
    def test_show_progress_command(self, mock_auth, mock_persistence):
        """Test progress display command."""
        mock_persistence.return_value = self.persistence
        mock_auth.return_value = self.mock_auth
        result = self.runner.invoke(cli, ['show-progress'])
        assert 'Showing progress' in result.output

    @patch('src.cli.learning_cli.get_persistence_layer')
    @patch('src.cli.learning_cli.get_auth')
    def test_show_progress_command_unauthenticated(self, mock_auth, mock_persistence):
        """Test showing progress without authentication."""
        mock_persistence.return_value = self.persistence
        mock_auth.return_value = self.mock_auth
        self.mock_auth.is_authenticated.return_value = False
        result = self.runner.invoke(cli, ['show-progress'])
        assert 'Please login first' in result.output
        assert result.exit_code == 1

    @patch('src.cli.learning_cli.get_persistence_layer')
    @patch('src.cli.learning_cli.get_auth')
    def test_help_command(self, mock_auth, mock_persistence):
        """Test help system."""
        mock_persistence.return_value = self.persistence
        mock_auth.return_value = self.mock_auth
        result = self.runner.invoke(cli, ['--help'])
        assert 'Usage:' in result.output

def get_auth(self):
    return AuthHandler()
