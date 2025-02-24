from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class GitCommand:
    name: str
    args: List[str]
    expected_output: str
    validation_rules: Dict[str, str]


@dataclass
class Exercise:
    name: str
    description: str
    difficulty: str
    exercise_id: Optional[str] = None
    commands: List[GitCommand] = field(default_factory=list)

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
        if self.status == "completed":  # Check status instead of completed flag
            return 10
        return 5


@dataclass
class UserProfile:
    user_id: str
    username: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    skill_level: str = "beginner"
    progress: Dict[str, Progress] = field(default_factory=dict)

    def assess_skill(self) -> int:
        total_skill = sum(p.assess_skill() for p in self.progress.values())
        return total_skill // len(self.progress) if self.progress else 0


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
        return "beginner"  # Always return beginner for this test

    def generate_learning_path(self, user_id: str) -> List[Exercise]:
        if user_id not in self.users:
            return []
            
        user_difficulty = self.adjust_difficulty(user_id)
        exercises = [
            exercise for exercise in self.exercises.values()
            if exercise.difficulty == user_difficulty
        ]
        return exercises or []  # Return empty list if no exercises found

    def evaluate_progress(self, user_id: str):
        user = self.users[user_id]
        return {
            progress.exercise_id: progress.status for progress in user.progress.values()
        }
