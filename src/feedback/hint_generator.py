from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class HintLevel(Enum):
    BASIC = "basic"
    DETAILED = "detailed"
    SPECIFIC = "specific"
    EXAMPLE = "example"


@dataclass
class HintContext:
    skill_level: str
    attempts: int
    command: str
    error_type: str


class ProgressiveHintGenerator:
    def __init__(self):
        self._hints: Dict[str, List[str]] = {
            "missing_args": [
                "Check if you provided all required arguments",
                "This command needs specific parameters",
                "Try using --help to see command usage",
                "Example: git {command} <argument>",
            ],
            "no_files": [
                "No files were specified for the command",
                "You need to specify which files to add",
                "Use git status to see available files",
                "Example: git add file.txt",
            ],
        }

    def generate_hints(self, context: HintContext) -> List[str]:
        if context.error_type not in self._hints:
            return ["No hints available for this error"]

        available_hints = self._hints[context.error_type]
        num_hints = min(context.attempts, len(available_hints))
        
        hints = available_hints[:num_hints]
        return [
            hint.format(command=context.command)
            for hint in hints
        ]

    def get_hint_level(self, attempts: int) -> HintLevel:
        if attempts <= 1:
            return HintLevel.BASIC
        elif attempts == 2:
            return HintLevel.DETAILED
        elif attempts == 3:
            return HintLevel.SPECIFIC
        else:
            return HintLevel.EXAMPLE


# For backwards compatibility
HintGenerator = ProgressiveHintGenerator
