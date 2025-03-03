"""
User profile model for the Git Learning System.

This module defines the SQLAlchemy model for user profiles,
including user information, skill level, and preferences.
"""

import uuid
from datetime import datetime
import pytz
from sqlalchemy import Column, String, DateTime, Integer, Float, Boolean, JSON
from sqlalchemy.orm import relationship

from src.database.init_db import Base

class UserProfile(Base):
    """
    User profile model for storing user information and learning progress.
    
    Attributes:
        id (str): Unique identifier for the user
        username (str): User's chosen username
        email (str): User's email address (optional)
        created_at (datetime): When the user profile was created
        last_login (datetime): When the user last logged in
        skill_level (str): User's current skill level (beginner, intermediate, advanced)
        completed_exercises (int): Number of exercises completed
        skill_scores (dict): Dictionary of skill scores for different Git concepts
        preferences (dict): User preferences for the learning system
    """
    __tablename__ = "user_profiles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    last_login = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    skill_level = Column(String(20), default="beginner")
    completed_exercises = Column(Integer, default=0)
    skill_scores = Column(JSON, default=lambda: {
        "basic_commands": 0.0,
        "branching": 0.0,
        "merging": 0.0,
        "remote_operations": 0.0,
        "advanced_workflows": 0.0
    })
    preferences = Column(JSON, default=lambda: {
        "difficulty_preference": "adaptive",
        "feedback_level": "detailed",
        "exercise_type_preference": "guided",
        "theme": "default"
    })
    
    # Relationships
    progress = relationship("Progress", back_populates="user", cascade="save-update, merge, delete")
    
    def __init__(self, username, email=None, skill_level="beginner"):
        """
        Initialize a new user profile.
        
        Args:
            username (str): User's chosen username
            email (str, optional): User's email address
            skill_level (str, optional): Initial skill level
        """
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.skill_level = skill_level
        self.created_at = datetime.now(pytz.utc)
        self.last_login = datetime.now(pytz.utc)
        self.completed_exercises = 0
        self.skill_scores = {
            "basic_commands": 0.0,
            "branching": 0.0,
            "merging": 0.0,
            "remote_operations": 0.0,
            "advanced_workflows": 0.0
        }
        self.preferences = {
            "difficulty_preference": "adaptive",
            "feedback_level": "detailed",
            "exercise_type_preference": "guided",
            "theme": "default"
        }
    
    @property
    def user_id(self) -> str:
        """Get the user ID."""
        return self.id
    
    def update_skill_level(self):
        """
        Update the user's skill level based on their skill scores.
        
        Returns:
            str: The updated skill level
        """
        avg_score = sum(self.skill_scores.values()) / len(self.skill_scores)
        
        if avg_score < 0.3:
            self.skill_level = "beginner"
        elif avg_score < 0.7:
            self.skill_level = "intermediate"
        else:
            self.skill_level = "advanced"
        
        return self.skill_level
    
    def update_skill_score(self, skill_name, score):
        """
        Update a specific skill score.
        
        Args:
            skill_name (str): Name of the skill to update
            score (float): New score value (0.0 to 1.0)
            
        Returns:
            float: The updated skill score
        """
        if skill_name in self.skill_scores:
            # Use a weighted average to gradually update scores
            current_score = self.skill_scores[skill_name]
            # 70% weight to previous score, 30% to new score
            updated_score = (current_score * 0.7) + (score * 0.3)
            self.skill_scores[skill_name] = updated_score
            
            # Update overall skill level
            self.update_skill_level()
            
            return updated_score
        return None
    
    def increment_completed_exercises(self):
        """
        Increment the count of completed exercises.
        
        Returns:
            int: The updated count of completed exercises
        """
        self.completed_exercises += 1
        return self.completed_exercises
    
    def update_last_login(self):
        """
        Update the last login timestamp to the current time.
        
        Returns:
            datetime: The updated last login timestamp
        """
        self.last_login = datetime.now(pytz.utc)
        return self.last_login
    
    def update_preference(self, preference_name, value):
        """
        Update a user preference.
        
        Args:
            preference_name (str): Name of the preference to update
            value: New value for the preference
            
        Returns:
            dict: The updated preferences dictionary
        """
        if preference_name in self.preferences:
            self.preferences[preference_name] = value
        return self.preferences
    
    def assess_skill(self, skill_list):
        # Correct logic to assess skill
        for skill in skill_list:
            if skill in self.skill_scores:
                # Assess the skill
                pass

    def adjust_difficulty(self, user_id, difficulty_list):
        # Correct logic to adjust difficulty
        for difficulty in difficulty_list:
            if difficulty in self.preferences:
                # Adjust the difficulty
                pass

    def to_dict(self):
        """
        Convert the user profile to a dictionary.
        
        Returns:
            dict: Dictionary representation of the user profile
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat(),
            "skill_level": self.skill_level,
            "completed_exercises": self.completed_exercises,
            "skill_scores": self.skill_scores,
            "preferences": self.preferences
        }
    
    def __repr__(self):
        return f"<UserProfile(username='{self.username}', skill_level='{self.skill_level}')>"
