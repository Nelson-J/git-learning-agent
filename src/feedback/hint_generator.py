from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class HintLevel(Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class HintContext:
    skill_level: str
    attempts: int
    error_type: str
    command: Optional[str] = None
    previous_hints: Optional[List[str]] = None


class HintGenerator:  # Changed from ProgressiveHintGenerator
    def __init__(self):
        self._hint_levels = {
            HintLevel.BASIC: 0,
            HintLevel.INTERMEDIATE: 1,
            HintLevel.ADVANCED: 2,
        }
        self._hint_database: Dict[str, Dict[str, List[str]]] = {}
        self._initialize_hints()

    def _initialize_hints(self) -> None:
        self._hint_database = {
            "init": {
                HintLevel.BASIC: [
                    "Use 'git init' to create a repository",
                    "Make sure you're in the right directory"
                ],
                HintLevel.INTERMEDIATE: [
                    "Consider adding a .gitignore file",
                    "Check the repository configuration"
                ],
                HintLevel.ADVANCED: [
                    "Configure Git hooks for automation",
                    "Set up repository templates"
                ]
            }
        }

    def generate_hints(self, error_type: str, context: HintContext) -> List[str]:
        if error_type not in self._hint_database:
            return ["No specific hints available for this error."]

        hints = []
        if context.attempts >= 2:  # Show intermediate hints after 2 attempts
            hints.extend(self._hint_database[error_type][HintLevel.INTERMEDIATE])
        hints.extend(self._hint_database[error_type][HintLevel.BASIC])
        
        return hints

    def _get_hint_level(self, skill_level: str, attempts: int) -> HintLevel:
        if skill_level == "advanced" or attempts > 3:
            return HintLevel.ADVANCED
        elif skill_level == "intermediate" or attempts > 2:
            return HintLevel.INTERMEDIATE
        return HintLevel.BASIC

    def get_hints(self, hints: List[str], context: HintContext) -> List[str]:
        if not hints:
            return []

        level_index = self._get_level_index(context.skill_level)
        max_hints = min(context.attempts + level_index, len(hints))
        return hints[:max_hints]

    def _get_level_index(self, skill_level: str) -> int:
        try:
            level = HintLevel(skill_level.lower())
            return self._hint_levels.get(level, 0)
        except ValueError:
            return 0

    def generate_hint(self):
        return self.hint

def another_method(self):
    pass

# Add alias for backward compatibility
ProgressiveHintGenerator = HintGenerator
