from enum import Enum


class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class CommandCategory(Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    WORKFLOW = "workflow"


class ErrorSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


DEFAULT_HINT_DELAY = 60  # seconds
MAX_HINTS_PER_ERROR = 3
SKILL_PROGRESSION_THRESHOLD = 5
