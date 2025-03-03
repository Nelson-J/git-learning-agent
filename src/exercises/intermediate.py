from typing import List
from ..models import Exercise, GitCommand


def create_branch_exercise() -> Exercise:
    commands = [
        GitCommand(name="branch", args=["branching_basics"], expected_output="Branch created", validation_rules={}),
        GitCommand(name="checkout", args=["-b", "branching_basics"], expected_output="Switched to a new branch", validation_rules={})
    ]
    return Exercise(
        exercise_id="branching_basics",
        name="Branching Basics",
        description="Learn to create and manage branches",
        difficulty="intermediate",
        commands=commands,
        expected_output={"status": "success"}
    )


def create_merge_exercise() -> Exercise:
    steps = ["git checkout main", "git merge feature"]
    commands = [
        GitCommand(
            name="merge",
            args=["feature"],
            expected_output="Merged feature branch",
            validation_rules={"branch_merged": "true"}
        )
    ]
    exercise = Exercise(
        exercise_id="merging_changes",
        name="merging_changes",
        description="Learn to merge changes between branches",
        difficulty="intermediate",
        steps=steps,
        expected_output={"status": "success"}
    )
    exercise.commands = commands
    return exercise


def create_collaborative_exercise() -> Exercise:
    steps = ["git remote add origin url", "git push origin main", "git pull origin main"]
    commands = [
        GitCommand(
            name="remote",
            args=["add", "origin"],
            expected_output="Remote added",
            validation_rules={}
        ),
        GitCommand(
            name="pull",
            args=["origin", "main"],
            expected_output="Changes pulled from remote",
            validation_rules={}
        )
    ]
    exercise = Exercise(
        exercise_id="team_collaboration",
        name="team_collaboration",
        description="Practice collaborative Git workflows",
        difficulty="intermediate",
        steps=steps,
        expected_output={"status": "success"}
    )
    exercise.commands = commands
    return exercise


def get_intermediate_exercises() -> List[Exercise]:
    return [
        create_branch_exercise(),
        create_merge_exercise(),
        create_collaborative_exercise(),
    ]
