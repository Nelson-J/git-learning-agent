from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class ErrorCategory(Enum):
    SYNTAX = "syntax"
    WORKFLOW = "workflow"
    CONCEPTUAL = "conceptual"
    CONFIGURATION = "configuration"
    INPUT = "input"
    SUCCESS = "success"  # Add this value


@dataclass
class FeedbackTemplate:
    error_type: str
    category: ErrorCategory
    message_template: str
    hints: List[str]
    examples: Optional[Dict[str, str]] = None

    def format_message(self, context: Dict[str, str] = None) -> str:
        """Format message with proper spacing."""
        try:
            context = context or {}
            return self.message_template.format(**context)
        except KeyError as e:
            return f"Error: Missing context parameter: {str(e)}"

    def get_hints(self, attempt: int) -> List[str]:
        """Get hints with proper spacing."""
        if not self.hints:
            return []
        return self.hints[: min(len(self.hints), attempt)]


class FeedbackManager:
    def __init__(self):
        self._templates: Dict[str, FeedbackTemplate] = {}
        self._initialize_templates()
        self.attempt_count: Dict[str, int] = {}

    def _initialize_templates(self):
        self._templates.update(
            {
                "invalid_command": FeedbackTemplate(
                    error_type="invalid_command",
                    category=ErrorCategory.SYNTAX,
                    message_template=("The command '{command}' is not valid."),
                    hints=[
                        "Check the command spelling",
                        "Use 'git help' to see available commands",
                    ],
                ),
                "uninitialized_repo": FeedbackTemplate(
                    error_type="uninitialized_repo",
                    category=ErrorCategory.WORKFLOW,
                    message_template="You need to initialize a repository first.",
                    hints=[
                        "Use 'git init' to create a new repository",
                        "Make sure you're in the right directory",
                    ],
                    examples={"init": "git init"},
                ),
                "no_files_specified": FeedbackTemplate(
                    error_type="no_files_specified",
                    category=ErrorCategory.SYNTAX,
                    message_template="No files specified for staging.",
                    hints=[
                        "Use 'git add <filename>' to stage specific files",
                        "Use 'git add .' to stage all changes",
                        "Use 'git status' to see which files can be staged",
                    ],
                    examples={"add": "git add example.txt"},
                ),
                "files_staged_success": FeedbackTemplate(
                    error_type="files_staged_success",
                    category=ErrorCategory.WORKFLOW,
                    message_template="Files staged successfully.",
                    hints=[
                        "Next, commit your changes using 'git commit -m \"your message\"'",
                        "Use 'git status' to verify staged changes",
                    ],
                    examples={"commit": 'git commit -m "Add new feature"'},
                ),
                "invalid_commit_format": FeedbackTemplate(
                    error_type="invalid_commit_format",
                    category=ErrorCategory.SYNTAX,
                    message_template="Invalid commit message format.",
                    hints=[
                        "Use -m flag followed by your message in quotes",
                        "Keep the message clear and descriptive",
                        "Start with a verb (Add, Fix, Update, etc.)",
                    ],
                    examples={"commit": 'git commit -m "Fix login bug"'},
                ),
                "nothing_to_commit": FeedbackTemplate(
                    error_type="nothing_to_commit",
                    category=ErrorCategory.WORKFLOW,
                    message_template="Nothing to commit. Working tree clean.",
                    hints=[
                        "Stage changes first using 'git add'",
                        "Check staged files with 'git status'",
                        "Make sure you have modified files",
                    ],
                ),
            }
        )

    def get_feedback(self, error_type: str, context: Dict[str, str] = None) -> str:
        template = self._templates.get(error_type)
        if not template:
            return "An unknown error occurred."

        try:
            context = context or {}
            if template.error_type == "invalid_command" and "command" not in context:
                context["command"] = "unknown"

            message = template.message_template.format(**context)
            self.attempt_count[error_type] = self.attempt_count.get(error_type, 0) + 1

            # Progressive hints based on attempt count
            if self.attempt_count[error_type] > 1:
                hints = template.get_hints(self.attempt_count[error_type])
                formatted_hints = [f"- {hint}" for hint in hints]
                message = f"{message}\n\n" f"Hints:\n{chr(10).join(formatted_hints)}"

            return message
        except KeyError as e:
            return f"Error: Missing required context parameter: {str(e)}"

    def get_feedback_with_context(
        self,
        error_type: str,
        user_skill_level: str,
        attempt_count: int,
        context: Dict[str, str] = None,
    ) -> str:
        """Generate contextual feedback based on user's skill level and attempt count."""
        template = self._templates.get(error_type)
        if not template:
            return "An unknown error occurred."

        message = template.format_message(context)
        hints = []

        # Adjust feedback based on skill level
        if user_skill_level == "beginner":
            hints = template.hints
        elif user_skill_level == "intermediate":
            # Skip basic hints for intermediate users
            hints = template.hints[1:] if len(template.hints) > 1 else template.hints
        else:  # advanced
            # Only show advanced hints for advanced users
            hints = template.hints[-1:] if template.hints else []

        # Add progressive hints based on attempt count
        if attempt_count > 1:
            formatted_hints = [
                f"- {hint}" for hint in hints[: min(len(hints), attempt_count)]
            ]
            message = f"{message}\n\n" f"Hints:\n{chr(10).join(formatted_hints)}"

        # Add examples after multiple attempts
        if attempt_count > 2 and template.examples:
            message += "\n\nExample:\n" + next(iter(template.examples.values()))

        return message

    def reset_attempts(self, error_type: str = None):
        """Reset attempt counter for specific or all error types."""
        if error_type:
            self.attempt_count.pop(error_type, None)
        else:
            self.attempt_count.clear()

    def process_feedback(self):
        feedback_msg = "Long line split into " "multiple parts for better readability"
        if self.validation_needed():
            self.process_something(parameter="value")
        return feedback_msg

    def generate_feedback(self, context, error_type):
        # Break long lines into multiple lines
        template = self.feedback_templates.get(
            error_type,
            self.default_template
        )
        
    def format_message(self, template, context):
        # Break long line into multiple lines
        return template.format(
            **context
        ) if context else template
