from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from .categories import FeedbackCategory, ErrorLevel
from .hint_generator import HintContext, ProgressiveHintGenerator

@dataclass
class AssistanceLevel:
    level: int
    hints_revealed: int
    examples_shown: bool
    full_explanation: bool
    next_steps_shown: bool

class ProgressiveAssistance:
    def __init__(self):
        self._attempts: Dict[str, int] = {}
        self._last_hint: Dict[str, datetime] = {}
        self._hint_generator = ProgressiveHintGenerator()
        self._current_assistance: Dict[str, AssistanceLevel] = {}

    def get_assistance(self, exercise_id: str, error_type: str, 
                      context: HintContext) -> Dict[str, any]:
        """Get progressive assistance based on context and history."""
        current_time = datetime.now()
        
        # Initialize or update attempt tracking
        if exercise_id not in self._attempts:
            self._attempts[exercise_id] = 0
            self._current_assistance[exercise_id] = AssistanceLevel(
                level=0, hints_revealed=0, examples_shown=False,
                full_explanation=False, next_steps_shown=False
            )

        # Update attempt count if enough time has passed
        last_hint_time = self._last_hint.get(exercise_id, datetime.min)
        if (current_time - last_hint_time) > timedelta(minutes=1):
            self._attempts[exercise_id] += 1

        assistance = self._current_assistance[exercise_id]
        hints = self._hint_generator.generate_hints(error_type, context)

        # Progressive assistance logic
        response = {
            "hints": hints[:assistance.hints_revealed + 1],
            "show_example": assistance.examples_shown,
            "show_explanation": assistance.full_explanation,
            "show_next_steps": assistance.next_steps_shown
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
