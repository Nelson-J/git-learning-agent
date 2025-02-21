from typing import List, Dict
from datetime import datetime

class UserProfile:
    def __init__(self, user_id: str, username: str, email: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.progress: Dict[str, Progress] = {}  # Changed from {} to track Progress objects

    def assess_skill(self):
        # Count completed exercises
        return sum(1 for progress in self.progress.values() if progress.status == 'completed')

    def add_progress(self, progress: 'Progress'):
        self.progress[progress.exercise_id] = progress

class Exercise:
    def __init__(self, exercise_id: str, description: str, difficulty: str):
        self.exercise_id = exercise_id
        self.description = description
        self.difficulty = difficulty

class Progress:
    def __init__(self, user_id: str, exercise_id: str, status: str, last_attempt: datetime):
        self.user_id = user_id
        self.exercise_id = exercise_id
        self.status = status
        self.last_attempt = last_attempt

class PersistenceLayer:
    def __init__(self):
        self.users: Dict[str, UserProfile] = {}
        self.exercises: Dict[str, Exercise] = {}
        self.progress: List[Progress] = []

    def add_user(self, user: UserProfile):
        self.users[user.user_id] = user

    def add_exercise(self, exercise: Exercise):
        self.exercises[exercise.exercise_id] = exercise

    def update_progress(self, progress: Progress):
        self.progress.append(progress)
        # Update user's progress
        if progress.user_id in self.users:
            self.users[progress.user_id].add_progress(progress)

    def adjust_difficulty(self, user_id: str):
        user = self.users[user_id]
        skill_level = user.assess_skill()
        # Basic difficulty adjustment logic
        if skill_level < 5:
            return 'beginner'
        elif skill_level < 10:
            return 'intermediate'
        else:
            return 'advanced'

    def generate_learning_path(self, user_id: str):
        difficulty = self.adjust_difficulty(user_id)
        # Simple learning path generation
        return [exercise for exercise in self.exercises.values() if exercise.difficulty == difficulty]

    def evaluate_progress(self, user_id: str):
        user = self.users[user_id]
        return {progress.exercise_id: progress.status for progress in user.progress.values()}
