from typing import List, Dict, Optional
from dataclasses import dataclass
from .categories import FeedbackCategory, ErrorLevel

@dataclass
class HintContext:
    skill_level: str
    attempt_count: int
    error_history: List[str]
    command_history: List[str]

class ProgressiveHintGenerator:
    def __init__(self):
        self._hint_levels: Dict[str, List[List[str]]] = {
            "init": [
                ["First, initialize a Git repository using 'git init'"],
                ["Make sure you're in the correct directory", "Check if .git folder exists"],
                ["Consider using 'git status' to verify repository state"]
            ],
            "add": [
                ["Use 'git add <filename>' to stage files"],
                ["Try 'git status' to see which files can be staged"],
                ["Consider using 'git add .' to stage all changes"]
            ],
            # Add more commands
        }

    def generate_hints(self, command: str, context: HintContext) -> List[str]:
        """Generate progressive hints based on context."""
        hints = self._hint_levels.get(command, [[]])[:]
        
        # Adjust hints based on skill level and attempts
        if context.skill_level == "beginner":
            max_hints = min(context.attempt_count, len(hints))
            return [h for level in hints[:max_hints] for h in level]
        elif context.skill_level == "intermediate":
            return [h for level in hints[1:] for h in level]
        else:  # advanced
            return hints[-1] if hints else []

    def analyze_error_pattern(self, context: HintContext) -> Optional[str]:
        """Analyze error history to identify patterns and provide specific guidance."""
        if len(context.error_history) >= 3:
            recent_errors = context.error_history[-3:]
            if all(error == recent_errors[0] for error in recent_errors):
                return "You seem to be stuck. Consider reviewing the Git documentation or trying a different approach."
        return None
