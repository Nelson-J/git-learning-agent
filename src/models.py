from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GitCommand(Base):
    __tablename__ = 'git_commands'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    args = Column(String)
    expected_output = Column(String)
    validation_rules = Column(String)
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    exercise = relationship('Exercise', backref='commands')

class Exercise(Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True)
    exercise_id = Column(String, unique=True)
    name = Column(String)
    description = Column(String)
    difficulty = Column(String)

class Progress(Base):
    __tablename__ = 'progress'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('user_profiles.user_id'))
    exercise_id = Column(String, ForeignKey('exercises.exercise_id'))
    status = Column(String, default='in_progress')
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    attempts = Column(Integer, default=0)
    last_attempt = Column(DateTime)
    user = relationship('UserProfile', backref='progress')
    exercise = relationship('Exercise', backref='progress')

    def assess_skill(self) -> int:
        if self.status == 'completed':
            return 10
        elif self.attempts > 0:
            return min(5 + self.attempts, 9)
        return 0

    def __repr__(self):
        return f'<Progress(user_id={self.user_id}, exercise_id={self.exercise_id}, status={self.status})>'

class UserProfile(Base):
    __tablename__ = 'user_profiles'
    user_id = Column(String, primary_key=True)
    username = Column(String)
    email = Column(String)
    created_at = Column(DateTime)
    skill_level = Column(String)

class PersistenceLayer:
    def __init__(self, session):
        self.session = session

    def add_user(self, user: UserProfile) -> None:
        self.session.add(user)
        self.session.commit()

    def add_exercise(self, exercise: Exercise):
        self.session.add(exercise)
        self.session.commit()

    def update_progress(self, progress: Progress) -> None:
        self.session.add(progress)
        self.session.commit()

    def adjust_difficulty(self, user_id: str) -> str:
        if self.session.query(UserProfile).filter_by(user_id=user_id).first() is None:
            return "beginner"
        return "beginner"

    def generate_learning_path(self, user_id: str) -> List[Exercise]:
        if self.session.query(UserProfile).filter_by(user_id=user_id).first() is None:
            return []
        user_difficulty = self.adjust_difficulty(user_id)
        exercises = self.session.query(Exercise).filter_by(difficulty=user_difficulty).all()
        return exercises or []

    def evaluate_progress(self, user_id: str):
        if self.session.query(UserProfile).filter_by(user_id=user_id).first() is None:
            return {}
        user = self.session.query(UserProfile).filter_by(user_id=user_id).first()
        return {
            progress.exercise_id: progress.assess_skill()
            for progress in user.progress
        }

def models_function():
    # Models code
    pass

# Additional code
