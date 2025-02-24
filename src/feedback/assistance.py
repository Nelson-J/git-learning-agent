from typing import Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
from .hint_generator import HintContext, ProgressiveHintGenerator  # Added import


@dataclass
class AssistanceLevel:
    """Define the levels of assistance provided to users."""
    basic: str
    intermediate: str
    advanced: str
    hints_revealed: int = 0
    examples_shown: bool = False
    full_explanation: bool = False
    next_steps_shown: bool = False


class AssistanceProvider:
    """Provides contextualized assistance based on user skill level."""
    def __init__(self):
        self.assistance_database: Dict[str, AssistanceLevel] = {}
        self._initialize_assistance()

    def _initialize_assistance(self) -> None:  # Fixed: Added self parameter
        """Initialize the assistance database with predefined levels."""
        self.assistance_database = {
            "init": AssistanceLevel(
                basic="Initialize a new Git repository",
                intermediate="Set up Git in your project directory",
                advanced="Configure Git repository with custom settings"
            ),
            "add": AssistanceLevel(
                basic="Stage files for commit",
                intermediate="Select specific changes to stage",
                advanced="Use interactive staging"
            )
        }

    def get_assistance(self, command: str, skill_level: str) -> str:
        """Get appropriate assistance based on skill level."""
        if command not in self.assistance_database:
            return "No assistance available for this command."

        level = self.assistance_database[command]
        if skill_level == "beginner":
            return level.basic
        elif skill_level == "intermediate":
            return level.intermediate
        return level.advanced


class ProgressiveAssistance:
    def __init__(self):
        self._attempts: Dict[str, int] = {}
        self._last_hint: Dict[str, datetime] = {}
        self._hint_generator = ProgressiveHintGenerator()
        self._current_assistance: Dict[str, AssistanceLevel] = {}

    def get_assistance(
        self, exercise_id: str, error_type: str, context: HintContext
    ) -> Dict[str, any]:
        """Get progressive assistance based on context and history."""
        current_time = datetime.now()

        # Initialize or update attempt tracking
        if exercise_id not in self._attempts:
            self._attempts[exercise_id] = 0
            self._current_assistance[exercise_id] = AssistanceLevel(
                basic="Initial assistance",
                intermediate="Standard assistance",
                advanced="Detailed assistance"
            )

        # Update attempt count if enough time has passed
        last_hint_time = self._last_hint.get(exercise_id, datetime.min)
        if (current_time - last_hint_time) > timedelta(minutes=1):
            self._attempts[exercise_id] += 1

        assistance = self._current_assistance[exercise_id]
        hints = self._hint_generator.generate_hints(error_type, context)

        # Progressive assistance logic
        response = {
            "hints": hints[: assistance.hints_revealed + 1],
            "show_example": assistance.examples_shown,
            "show_explanation": assistance.full_explanation,
            "show_next_steps": assistance.next_steps_shown,
        }

        # Update assistance level based on attempts
        if self._attempts[exercise_id] > 2:
            assistance.hints_revealed = min(assistance.hints_revealed + 1, len(hints))
        if self._attempts[exercise_id] > 3:
            assistance.examples_shown = True
        if self._attempts[exercise_id] > 4:
            assistance.full_explanation = True
            assistance.next_steps_shown = True

        self._last_hint[exercise_id] = current_time
        return response

    def reset_assistance(self, exercise_id: str):
        """Reset assistance state for an exercise."""
        self._attempts.pop(exercise_id, None)
        self._last_hint.pop(exercise_id, None)
        self._current_assistance.pop(exercise_id, None)
