from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class ErrorCategory(Enum):
    SYNTAX = "syntax"
    WORKFLOW = "workflow"
    CONCEPTUAL = "conceptual"
    CONFIGURATION = "configuration"
    INPUT = "input"
    SUCCESS = "success"


@dataclass
class FeedbackTemplate:
    error_type: str
    category: ErrorCategory
    message_template: str
    hints: List[str]
    examples: Optional[Dict[str, str]] = None

    def format_message(self, context: Dict[str, str] = None) -> str:
        try:
            context = context or {}
            return self.message_template.format(**context)
        except KeyError as e:
            return f"Error: Missing context parameter: {str(e)}"

    def get_hints(self, attempt: int) -> List[str]:
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
                    message_template="The command '{command}' is not valid.",
                    hints=[
                        "Check the command spelling",
                        "Use 'git help' to see available commands",
                    ],
                ),
                "invalid_commit_format": FeedbackTemplate(
                    error_type="invalid_commit_format",
                    category=ErrorCategory.SYNTAX,
                    message_template="Invalid commit message format.",
                    hints=[
                        "Use -m flag followed by your message in quotes",
                        "Keep the message clear and descriptive",
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
            message = template.format_message(context)
            self.attempt_count[error_type] = self.attempt_count.get(error_type, 0) + 1

            if self.attempt_count[error_type] > 1:
                hints = template.get_hints(self.attempt_count[error_type])
                if hints:
                    formatted_hints = [f"- {hint}" for hint in hints]
                    message = f"{message}\n\nHints:\n{chr(10).join(formatted_hints)}"
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
        template = self._templates.get(error_type)
        if not template:
            return "An unknown error occurred."

        message = template.format_message(context)
        hints = template.get_hints(attempt_count)

        if hints:
            if user_skill_level == "beginner":
                formatted_hints = [f"- {hint}" for hint in hints]
                message = f"{message}\n\nHints:\n{chr(10).join(formatted_hints)}"
            elif user_skill_level == "intermediate" and attempt_count > 1:
                formatted_hints = [f"- {hint}" for hint in hints[1:]]
                message = f"{message}\n\nHints:\n{chr(10).join(formatted_hints)}"
            elif user_skill_level == "advanced" and attempt_count > 2:
                formatted_hints = [f"- {hint}" for hint in hints[-1:]]
                message = f"{message}\n\nHints:\n{chr(10).join(formatted_hints)}"

        return message

    def reset_attempts(self, error_type: str = None):
        if error_type:
            self.attempt_count.pop(error_type, None)
        else:
            self.attempt_count.clear()

    def get_feedback_template(self, error_type):
        return self.templates.get(
            error_type,
            self.default_template
        )
