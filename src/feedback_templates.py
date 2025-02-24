from typing import Dict
from .feedback import FeedbackTemplate, ErrorCategory


class GitFeedbackTemplates:
    @staticmethod
    def get_all_templates() -> Dict[str, FeedbackTemplate]:
        return {
            # Basic Git Operations
            "merge_conflict": FeedbackTemplate(
                error_type="merge_conflict",
                category=ErrorCategory.WORKFLOW,
                message_template="Merge conflict detected in {files}",
                hints=[
                    "Open the conflicted files and look for markers",
                    "Decide which changes to keep",
                    "Stage and commit after resolving"
                ],
                examples={
                    "resolve": (
                        "git add resolved_file.txt\n"
                        'git commit -m "Resolve merge conflict"'
                    )
                }
            ),
            "detached_head": FeedbackTemplate(
                error_type="detached_head",
                category=ErrorCategory.CONCEPTUAL,
                message_template="You are in 'detached HEAD' state",
                hints=[
                    "You are viewing a specific commit rather than a branch",
                    "Create a new branch to make changes",
                    "Or return to an existing branch using 'git checkout branch_name'",
                ],
                examples={"fix": "git checkout -b new_branch\n# or\ngit checkout main"},
            ),
            "rebase_conflict": FeedbackTemplate(
                error_type="rebase_conflict",
                category=ErrorCategory.WORKFLOW,
                message_template="Conflict during rebase operation",
                hints=[
                    "Resolve conflicts in the affected files",
                    "Stage resolved files with 'git add'",
                    "Continue rebase with 'git rebase --continue'",
                ],
                examples={
                    "continue": "git add resolved_file.txt\ngit rebase --continue"
                },
            ),
            # Exercise-specific templates
            "init_repo_success": FeedbackTemplate(
                error_type="init_repo_success",
                category=ErrorCategory.SUCCESS,
                message_template="Successfully initialized Git repository",
                hints=["Try creating and adding a new file next"],
                examples={"next_step": "git add filename.txt"},
            ),
            "first_commit_success": FeedbackTemplate(
                error_type="first_commit_success",
                category=ErrorCategory.SUCCESS,
                message_template="Successfully created your first commit!",
                hints=["You can view your commit history with 'git log'"],
                examples={"view_history": "git log"},
            ),
            "branch_creation_success": FeedbackTemplate(
                error_type="branch_creation_success",
                category=ErrorCategory.SUCCESS,
                message_template="Successfully created branch '{branch_name}'",
                hints=["Switch to your new branch with 'git checkout'"],
                examples={"switch_branch": "git checkout {branch_name}"},
            ),
            "uninitialized_repo": FeedbackTemplate(
                error_type="uninitialized_repo",
                category=ErrorCategory.WORKFLOW,
                message_template="Repository not initialized. Use 'git init' first.",
                hints=[
                    "Initialize a Git repository using 'git init'",
                    "Make sure you're in the correct directory",
                    "Check if .git directory exists",
                ],
                examples={"init": "git init"},
            ),
            "unsupported_command": FeedbackTemplate(
                error_type="unsupported_command",
                category=ErrorCategory.INPUT,
                message_template="Command not supported in current exercise",
                hints=["Check the exercise requirements"],
                examples={},
            ),
            "command_error": FeedbackTemplate(
                error_type="command_error",
                category=ErrorCategory.WORKFLOW,
                message_template="Error executing command: {error}",
                hints=[
                    "Check command syntax",
                    "Verify repository state",
                    "Review prerequisites for this command",
                ],
            ),
        }

    @staticmethod
    def get_merged_templates() -> Dict[str, FeedbackTemplate]:
        """Get merged templates with proper formatting."""
        basic_templates = GitFeedbackTemplates.get_all_templates()
        workflow_templates = GitFeedbackTemplates._get_workflow_templates()
        return {**basic_templates, **workflow_templates}


class ContextualHintGenerator:
    @staticmethod
    def generate_progressive_hints(
        error_type: str, skill_level: str, attempt_count: int
    ) -> list[str]:
        base_hints = {
            "merge_conflict": [
                "Basic: Look for conflict markers in the files",
                "Intermediate: Use git status to see affected files",
                "Advanced: Consider using git mergetool",
            ],
            "detached_head": [
                "Basic: Create a new branch to save changes",
                "Intermediate: Understand HEAD pointer concept",
                "Advanced: Use git reflog to recover commits",
            ],
        }

        hints = base_hints.get(error_type, [])
        if not hints:
            return []

        # Select hints based on skill level and attempts
        if skill_level == "beginner":
            return hints[: min(attempt_count, len(hints))]
        elif skill_level == "intermediate":
            return hints[1 : min(attempt_count + 1, len(hints))]
        else:  # advanced
            return hints[2 : min(attempt_count + 2, len(hints))]
