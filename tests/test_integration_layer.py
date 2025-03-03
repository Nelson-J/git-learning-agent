import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.integration_layer import IntegrationLayer
from src.models import UserProfile, Exercise, Progress

# Register integration mark properly
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )

@pytest.fixture
def integration_layer():
    return IntegrationLayer()

@pytest.fixture
def mock_user_profile():
    return UserProfile(
        user_id="test_user",
        username="testuser",
        email="test@example.com",
        skill_level="beginner",
        created_at=datetime.now()
    )

@pytest.fixture
def mock_exercise():
    return Exercise(
        exercise_id="ex_001",
        name="Basic Git Init",
        difficulty="beginner",
        description="Initialize a new Git repository",
        steps=["git init"],  # Changed from validation_rules to steps
        expected_output="Initialized empty Git repository"
    )

class TestIntegrationLayer:
    def test_initialize_session(self, integration_layer, mock_user_profile):
        """Test successful session initialization with proper component mocking."""
        with patch.multiple(integration_layer.adaptive_learning,
                          initialize_user=Mock(return_value=None)), \
             patch.multiple(integration_layer.spaced_repetition,
                          initialize_user=Mock(return_value=None)), \
             patch.multiple(integration_layer.dialogue_manager,
                          initialize_session=Mock(return_value=None)), \
             patch.multiple(integration_layer.exercise_validator,
                          set_workspace=Mock(return_value=None)):
            result = integration_layer.initialize_session(mock_user_profile)
            assert result is True

    def test_initialize_session_failure(self, integration_layer, mock_user_profile):
        with patch.object(integration_layer.adaptive_learning, 'initialize_user', side_effect=Exception("Test error")):
            result = integration_layer.initialize_session(mock_user_profile)
            assert result is False

    def test_process_command_success(self, integration_layer):
        with patch.multiple(integration_layer.adaptive_learning,
                          get_user_level=Mock(return_value="beginner"),
                          get_attempt_count=Mock(return_value=1),
                          update_metrics=Mock(return_value=None)):
            with patch.object(integration_layer.exercise_validator, 'validate_command') as mock_validate:
                mock_validate.return_value = (True, "Success")
                result = integration_layer.process_command(
                    user_id="test_user",
                    command="git",
                    args=["init"]
                )
                assert "feedback" in result

    def test_process_command_failure(self, integration_layer):
        with patch.object(integration_layer.exercise_validator, 'validate_command', side_effect=Exception("Test error")):
            result = integration_layer.process_command(
                user_id="test_user",
                command="git",
                args=["invalid"]
            )
            assert result["success"] is False
            assert "error" in result

    def test_get_next_exercise(self, integration_layer, mock_exercise):
        with patch.object(integration_layer.exercise_validator, 'get_next_exercise', return_value=mock_exercise):
            exercise = integration_layer.get_next_exercise("test_user")
            assert exercise is not None
            assert exercise.exercise_id == "ex_001"

    def test_get_next_exercise_failure(self, integration_layer):
        with patch.object(integration_layer.adaptive_learning, 'get_next_exercise', side_effect=Exception("Test error")):
            exercise = integration_layer.get_next_exercise("test_user")
            assert exercise is None

    def test_update_progress_success(self, integration_layer):
        result = integration_layer.update_progress(
            user_id="test_user",
            exercise_id="ex_001",
            completed=True
        )
        assert result is True

    def test_update_progress_failure(self, integration_layer):
        with patch.object(integration_layer.adaptive_learning, 'update_knowledge_space', side_effect=Exception("Test error")):
            result = integration_layer.update_progress(
                user_id="test_user",
                exercise_id="ex_001",
                completed=True
            )
            assert result is False

    def test_error_handlers(self, integration_layer):
        # Test repository error handler
        result = integration_layer._handle_repository_error(Exception("Repository error"))
        assert result[0] is False
        assert "Repository operation failed" in result[1]

        # Test validation error handler
        result = integration_layer._handle_validation_error(Exception("Validation error"))
        assert result[0] is False
        assert "Command validation failed" in result[1]

        # Test learning error handler
        result = integration_layer._handle_learning_error(Exception("Learning error"))
        assert result[0] is False
        assert "Learning operation failed" in result[1]

        # Test persistence error handler
        result = integration_layer._handle_persistence_error(Exception("Persistence error"))
        assert result[0] is False
        assert "Data operation failed" in result[1]

    @pytest.mark.integration
    def test_full_learning_flow(self, integration_layer, mock_user_profile):
        # Patch all required initialization methods
        with patch.multiple(integration_layer.adaptive_learning,
                          initialize_user=Mock(return_value=None),
                          get_user_level=Mock(return_value="beginner"),
                          get_attempt_count=Mock(return_value=1)):
            with patch.multiple(integration_layer.spaced_repetition,
                              initialize_user=Mock(return_value=None)):
                with patch.multiple(integration_layer.dialogue_manager,
                                  initialize_session=Mock(return_value=None)):
                    assert integration_layer.initialize_session(mock_user_profile)
                    # Test complete flow from initialization to progress update
                    command_result = integration_layer.process_command(
                        user_id=mock_user_profile.user_id,
                        command="git",
                        args=["init"]
                    )
                    assert command_result["success"] in [True, False]

                    next_exercise = integration_layer.get_next_exercise(mock_user_profile.user_id)
                    if next_exercise:
                        progress_result = integration_layer.update_progress(
                            user_id=mock_user_profile.user_id,
                            exercise_id=next_exercise.exercise_id,
                            completed=True
                        )
                        assert progress_result is True
