"""
Progress model for the Git Learning System.

This module defines the SQLAlchemy model for tracking user progress on exercises,
including completion status, timestamps, and performance metrics.
""" 

import uuid
from datetime import datetime
from datetime import timezone as tz
from sqlalchemy import Column, String, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
import logging

from src.database.init_db import Base

logger = logging.getLogger(__name__)

class Progress(Base):
    """
    Progress model for tracking user progress on exercises.
    
    Attributes:
        id (str): Unique identifier for the progress record
        user_id (str): ID of the user
        exercise_id (str): ID of the exercise
        status (str): Current status (not_started, in_progress, completed, failed)
        started_at (datetime): When the exercise was started
        completed_at (datetime): When the exercise was completed
        last_attempt (datetime): Timestamp of the last attempt
        attempts (int): Number of attempts made
        time_spent (float): Time spent on the exercise in seconds
        score (float): Score achieved (0.0 to 1.0)
        mistakes (JSON): List of mistakes made during the exercise
        feedback (JSON): Feedback provided for the exercise
    """
    __tablename__ = "progress"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("user_profiles.id"), nullable=False)
    exercise_id = Column(String(36), ForeignKey("exercises.id"), nullable=False)
    status = Column(String(20), default="not_started")
    started_at = Column(DateTime, default=lambda: datetime.now(tz.utc))
    completed_at = Column(DateTime, nullable=True)
    last_attempt = Column(DateTime, default=lambda: datetime.now(tz.utc))
    attempts = Column(Float, default=0)
    time_spent = Column(Float, default=0.0)
    score = Column(Float, default=0.0)
    mistakes = Column(JSON, default=list)
    feedback = Column(JSON, default=dict)
    
    # Relationships
    user = relationship("UserProfile", back_populates="progress", cascade="all, delete-orphan", single_parent=True)
    exercise = relationship("Exercise", back_populates="progress", cascade="all, delete-orphan", single_parent=True)
    
    def __init__(
        self,
        user_id: str,
        exercise_id: str,
        status: str = "not_started",
        last_attempt: datetime = None
    ):
        """
        Initialize a new progress record.
        
        Args:
            user_id (str): ID of the user
            exercise_id (str): ID of the exercise
            status (str, optional): Initial status
            last_attempt (datetime, optional): Timestamp of the last attempt
        """
        logger.info("Initializing Progress mapper")
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.exercise_id = exercise_id
        self.status = status
        self.started_at = datetime.now(tz.utc)
        self.last_attempt = last_attempt or datetime.now(tz.utc)
        self.attempts = 0
        self.time_spent = 0.0
        self.score = 0.0
        self.mistakes = []
        self.feedback = {}
    
    def start_exercise(self):
        """
        Mark the exercise as started.
        
        Returns:
            datetime: The start timestamp
        """
        if self.status == "not_started":
            self.status = "in_progress"
            self.started_at = datetime.now(tz.utc)
        
        self.attempts += 1
        return self.started_at
    
    def complete_exercise(self, score: float = 1.0):
        """
        Mark the exercise as completed.
        
        Args:
            score (float, optional): Score achieved (0.0 to 1.0)
            
        Returns:
            datetime: The completion timestamp
        """
        self.status = "completed"
        self.completed_at = datetime.now(tz.utc)
        self.score = score
        
        # Calculate time spent
        if self.started_at:
            time_diff = self.completed_at - self.started_at
            self.time_spent += time_diff.total_seconds()
        
        return self.completed_at
    
    def fail_exercise(self):
        """
        Mark the exercise as failed.
        
        Returns:
            datetime: The failure timestamp
        """
        self.status = "failed"
        self.completed_at = datetime.now(tz.utc)
        
        # Calculate time spent
        if self.started_at:
            time_diff = self.completed_at - self.started_at
            self.time_spent += time_diff.total_seconds()
        
        return self.completed_at
    
    def add_mistake(self, command: str, error: str, hint: str = None):
        """
        Add a mistake to the progress record.
        
        Args:
            command (str): The command that caused the mistake
            error (str): The error message
            hint (str, optional): A hint for fixing the mistake
            
        Returns:
            list: The updated list of mistakes
        """
        mistake = {
            "command": command,
            "error": error,
            "hint": hint,
            "timestamp": datetime.now(tz.utc).isoformat()
        }
        
        self.mistakes.append(mistake)
        return self.mistakes
    
    def add_feedback(self, category: str, message: str):
        """
        Add feedback to the progress record.
        
        Args:
            category (str): The category of feedback
            message (str): The feedback message
            
        Returns:
            dict: The updated feedback dictionary
        """
        if category not in self.feedback:
            self.feedback[category] = []
        
        self.feedback[category].append({
            "message": message,
            "timestamp": datetime.now(tz.utc).isoformat()
        })
        
        return self.feedback
    
    def is_completed(self) -> bool:
        """
        Check if the exercise is completed.
        
        Returns:
            bool: True if completed, False otherwise
        """
        return self.status == "completed"
    
    def get_duration(self) -> float:
        """
        Get the duration of the exercise in seconds.
        
        Returns:
            float: Duration in seconds
        """
        if self.status == "in_progress" and self.started_at:
            # Calculate current duration for in-progress exercises
            time_diff = datetime.now(tz.utc) - self.started_at
            return self.time_spent + time_diff.total_seconds()
        
        return self.time_spent
    
    def to_dict(self):
        """
        Convert the progress record to a dictionary.
        
        Returns:
            dict: Dictionary representation of the progress record
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "exercise_id": self.exercise_id,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "last_attempt": self.last_attempt.isoformat() if self.last_attempt else None,
            "attempts": self.attempts,
            "time_spent": self.time_spent,
            "score": self.score,
            "mistakes": self.mistakes,
            "feedback": self.feedback
        }
    
    def update_progress(self, completed: bool = False):
        """Update progress status."""
        if completed:
            self.status = "completed"
            self.completed_at = datetime.now(tz.utc)
        else:
            self.status = "in_progress"
    
    def assess_skill(self) -> int:
        if self.status == 'completed':
            return 10
        return 5
    
    def __repr__(self):
        return f"<Progress(user_id='{self.user_id}', exercise_id='{self.exercise_id}', status='{self.status}')>"
