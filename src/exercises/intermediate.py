from typing import List
from ..models import Exercise, GitCommand


def create_branch_exercise() -> Exercise:
    exercise = Exercise(
        name="branching_basics",
        description="Learn to create and manage branches",
        difficulty="intermediate",
    )

    commands = [
        GitCommand(
            name="branch",
            args=["feature"],
            expected_output="",
            validation_rules={"branch_exists": "feature"},
        ),
        GitCommand(
            name="checkout",
            args=["feature"],
            expected_output="Switched to branch 'feature'",
            validation_rules={"current_branch": "feature"},
        ),
    ]

    for cmd in commands:
        exercise.add_command(cmd)
    return exercise


def create_merge_exercise() -> Exercise:
    exercise = Exercise(
        name="merging_changes",
        description="Learn to merge changes between branches",
        difficulty="intermediate",
    )

    setup_commands = [
        GitCommand(
            name="checkout",
            args=["main"],
            expected_output="Switched to branch 'main'",
            validation_rules={"current_branch": "main"},
        ),
        GitCommand(
            name="commit",
            args=["-m", "Update main branch"],
            expected_output="[main] Update main branch",
            validation_rules={"has_commit_message": "Update main branch"},
        ),
        GitCommand(
            name="checkout",
            args=["feature"],
            expected_output="Switched to branch 'feature'",
            validation_rules={"current_branch": "feature"},
        ),
        GitCommand(
            name="commit",
            args=["-m", "Add feature changes"],
            expected_output="[feature] Add feature changes",
            validation_rules={"has_commit_message": "Add feature changes"},
        ),
    ]

    merge_command = GitCommand(
        name="merge",
        args=["main"],
        expected_output="Merge successful",
        validation_rules={"branch_merged": "main", "has_merge_commit": True},
    )

    exercise.commands = setup_commands + [merge_command]
    return exercise


def create_collaborative_exercise() -> Exercise:
    exercise = Exercise(
        name="team_collaboration",
        description="Practice collaborative Git workflows",
        difficulty="intermediate",
    )

    commands = [
        GitCommand(
            name="remote",
            args=["add", "origin", "https://github.com/example/repo.git"],
            expected_output="remote 'origin' added",
            validation_rules={"has_remote": "origin"},
        ),
        GitCommand(
            name="fetch",
            args=["origin"],
            expected_output="Fetching origin",
            validation_rules={"remote_fetched": "origin"},
        ),
        GitCommand(
            name="pull",
            args=["origin", "main"],
            expected_output="Successfully pulled changes",
            validation_rules={"branch_updated": "main"},
        ),
    ]

    exercise.commands = commands
    return exercise


def get_intermediate_exercises() -> List[Exercise]:
    return [
        create_branch_exercise(),
        create_merge_exercise(),
        create_collaborative_exercise(),
    ]
