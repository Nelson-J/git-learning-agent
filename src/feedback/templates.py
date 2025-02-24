from dataclasses import dataclass
from typing import Dict, List, Optional
from .categories import FeedbackCategory, ErrorLevel

@dataclass
class DetailedFeedback:
    category: FeedbackCategory
    level: ErrorLevel
    message: str
    explanation: str
    hints: List[str]
    examples: Dict[str, str]
    next_steps: List[str]
    common_mistakes: List[str]

class DetailedFeedbackTemplates:
    def __init__(self):
        self.templates: Dict[str, DetailedFeedback] = {
            "uninitialized_repo": DetailedFeedback(
                category=FeedbackCategory.STATE,
                level=ErrorLevel.ERROR,
                message="Git repository not initialized",
                explanation="Before using Git commands, you need to initialize a repository using 'git init'.",
                hints=[
                    "Make sure you're in the correct directory",
                    "Check if .git directory exists",
                    "Run 'git init' to create a new repository"
                ],
                examples={"init": "git init"},
                next_steps=[
                    "Initialize the repository",
                    "Add some files",
                    "Make your first commit"
                ],
                common_mistakes=[
                    "Running Git commands outside a repository",
                    "Trying to initialize inside another Git repository",
                    "Wrong working directory"
                ]
            ),
            # Add more templates as needed
        }

    def get_template(self, error_type: str, skill_level: str = "beginner") -> Optional[DetailedFeedback]:
        template = self.templates.get(error_type)
        if template:
            # Adjust feedback detail based on skill level
            if skill_level == "beginner":
                return template
            elif skill_level == "intermediate":
                # Remove basic hints and examples
                template.hints = template.hints[1:]
                template.common_mistakes = []
            else:  # advanced
                # Keep only advanced hints
                template.hints = template.hints[-1:]
                template.explanation = ""
                template.common_mistakes = []
        return template
