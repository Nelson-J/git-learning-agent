from enum import Enum
from typing import Dict, List, Optional

class FeedbackCategory(Enum):
    SYNTAX = "syntax"         # Command syntax and format issues
    WORKFLOW = "workflow"     # Git workflow and process issues
    CONCEPTUAL = "concept"    # Understanding Git concepts
    STATE = "state"          # Repository state issues
    SYSTEM = "system"        # System-level issues
    SUCCESS = "success"      # Successful operations

class ErrorLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class FeedbackClassifier:
    def __init__(self):
        self._error_patterns: Dict[str, tuple[FeedbackCategory, ErrorLevel]] = {
            "not initialized": (FeedbackCategory.STATE, ErrorLevel.ERROR),
            "already exists": (FeedbackCategory.STATE, ErrorLevel.WARNING),
            "invalid syntax": (FeedbackCategory.SYNTAX, ErrorLevel.ERROR),
            "not found": (FeedbackCategory.SYSTEM, ErrorLevel.ERROR),
            "merge conflict": (FeedbackCategory.WORKFLOW, ErrorLevel.WARNING),
            "detached HEAD": (FeedbackCategory.CONCEPTUAL, ErrorLevel.WARNING),
        }

    def classify_error(self, error_message: str) -> tuple[FeedbackCategory, ErrorLevel]:
        """Classify an error message into a category and severity level."""
        for pattern, (category, level) in self._error_patterns.items():
            if pattern.lower() in error_message.lower():
                return category, level
        return FeedbackCategory.SYSTEM, ErrorLevel.ERROR
