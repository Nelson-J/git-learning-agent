from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, field
import uuid


@dataclass
class GitCommand:
    name: str
    args: List[str]
    expected_output: str
    validation_rules: Dict[str, str]


class Exercise:
    def __init__(
        self,
        exercise_id: str,
        description: str = None,
        steps: list = None,
        expected_output: dict = None,
        name: str = None,
        difficulty: str = "beginner",
    ):
        self.exercise_id = exercise_id
        self.name = name or exercise_id
        self.description = description or ""
        self.difficulty = difficulty
        self.steps = steps or []
        self.expected_output = expected_output or {"status": "success"}
        self.commands = [
            GitCommand(
                name=step.split()[1],
                args=step.split()[2:],
                expected_output="",
                validation_rules={},
            )
            for step in steps
            if step.startswith("git ")
        ] if steps else []

    def add_command(self, command: GitCommand) -> None:
        self.commands.append(command)


@dataclass
class Progress:
    user_id: str
    exercise_id: str
    status: str = "in_progress"
    completed: bool = False
    completed_at: Optional[datetime] = None
    attempts: int = 0
    last_attempt: Optional[datetime] = None

    def assess_skill(self) -> int:
        if self.status == "completed":
            return 10
        return 5


@dataclass
class UserProfile:
    username: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    skill_level: str = "beginner"
    progress: Dict[str, Progress] = field(default_factory=dict)
    user_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    id: str = field(init=False)

    def __post_init__(self):
        self.id = self.user_id

    def assess_skill(self) -> int:
        if not self.progress:
            return 0
        total_skill = sum(p.assess_skill() for p in self.progress.values())
        return total_skill // len(self.progress)


class PersistenceLayer:
    def __init__(self):
        self.users: Dict[str, UserProfile] = {}
        self.exercises: Dict[str, Exercise] = {}
        self.progress: Dict[str, Dict[str, Progress]] = {}

    def add_user(self, user: UserProfile) -> None:
        self.users[user.user_id] = user

    def add_exercise(self, exercise: Exercise):
        self.exercises[exercise.exercise_id] = exercise

    def update_progress(self, progress: Progress) -> None:
        if progress.user_id not in self.progress:
            self.progress[progress.user_id] = {}
        self.progress[progress.user_id][progress.exercise_id] = progress

    def adjust_difficulty(self, user_id: str) -> str:
        if user_id not in self.users:
            return "beginner"
        return "beginner"

    def generate_learning_path(self, user_id: str) -> List[Exercise]:
        if user_id not in self.users:
            return []
        user_difficulty = self.adjust_difficulty(user_id)
        exercises = [
            exercise
            for exercise in self.exercises.values()
            if exercise.difficulty == user_difficulty
        ]
        return exercises or []

    def evaluate_progress(self, user_id: str):
        if user_id not in self.users:
            return {}
        user = self.users[user_id]
        return {
            exercise_id: progress.status
            for exercise_id, progress in user.progress.items()
        }


def models_function():
    # Models code
    pass


# Additional code
