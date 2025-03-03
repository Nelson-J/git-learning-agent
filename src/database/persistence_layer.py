"""
Persistence layer for the Git Learning System.

This module provides a high-level interface for data persistence operations,
abstracting away the database implementation details from the rest of the application.
"""

import os
import logging
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

from src.models.user_profile import UserProfile
from src.models.exercise import Exercise, GitCommand, ComplexScenario
from src.models.progress import Progress
from src.database.optimized_queries import get_db_optimizer, DatabaseOptimizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class PersistenceLayer:
    """
    Persistence layer for the Git Learning System.
    
    This class provides a high-level interface for data persistence operations,
    abstracting away the database implementation details from the rest of the application.
    """
    
    def __init__(self):
        """
        Initialize the persistence layer.
        """
        self.db = get_db_optimizer()
        logger.info("PersistenceLayer initialized")
    
    # User Profile Operations
    
    def add_user(self, username: str, email: str = None, skill_level: str = "beginner") -> UserProfile:
        """
        Add a new user to the database.
        
        Args:
            username (str): User's username
            email (str, optional): User's email
            skill_level (str, optional): User's initial skill level
            
        Returns:
            UserProfile: The created user profile
        """
        # Check if user already exists
        existing_user = self.db.get_user_by_username(username)
        if existing_user:
            logger.warning(f"User {username} already exists")
            return existing_user
        
        # Create new user
        user = UserProfile(username=username, email=email, skill_level=skill_level)
        self.db.add(user)
        
        logger.info(f"Added new user: {username}")
        return user
    
    def get_user(self, user_id: str) -> Optional[UserProfile]:
        """
        Get a user by ID.
        
        Args:
            user_id (str): User ID
            
        Returns:
            Optional[UserProfile]: User profile or None if not found
        """
        return self.db.get_by_id(UserProfile, user_id)
    
    def get_user_by_username(self, username: str) -> Optional[UserProfile]:
        """
        Get a user by username.
        
        Args:
            username (str): Username
            
        Returns:
            Optional[UserProfile]: User profile or None if not found
        """
        return self.db.get_user_by_username(username)
    
    def update_user(self, user: UserProfile) -> UserProfile:
        """
        Update a user profile.
        
        Args:
            user (UserProfile): User profile to update
            
        Returns:
            UserProfile: Updated user profile
        """
        return self.db.update(user)
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user by ID.
        
        Args:
            user_id (str): User ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        user = self.get_user(user_id)
        if user:
            self.db.delete(user)
            logger.info(f"Deleted user: {user.username}")
            return True
        
        logger.warning(f"User with ID {user_id} not found for deletion")
        return False
    
    def update_user_skill_level(self, user_id: str, skill_name: str, score: float) -> Optional[str]:
        """
        Update a user's skill level based on a new skill score.
        
        Args:
            user_id (str): User ID
            skill_name (str): Name of the skill to update
            score (float): New score value (0.0 to 1.0)
            
        Returns:
            Optional[str]: Updated skill level or None if user not found
        """
        user = self.get_user(user_id)
        if not user:
            logger.warning(f"User with ID {user_id} not found for skill update")
            return None
        
        user.update_skill_score(skill_name, score)
        self.update_user(user)
        
        logger.info(f"Updated skill {skill_name} for user {user.username} to {score}")
        return user.skill_level
    
    # Exercise Operations
    
    def add_exercise(self, 
                    name: str, 
                    description: str, 
                    difficulty: str,
                    exercise_id: str = None,
                    commands: List[GitCommand] = None,
                    complex_scenario: ComplexScenario = None,
                    tags: List[str] = None,
                    skills: List[str] = None,
                    order: int = 0) -> Exercise:
        """
        Add a new exercise to the database.
        
        Args:
            name (str): Name of the exercise
            description (str): Description of the exercise
            difficulty (str): Difficulty level
            exercise_id (str, optional): Unique identifier for the exercise
            commands (List[GitCommand], optional): List of Git commands
            complex_scenario (ComplexScenario, optional): Complex scenario data
            tags (List[str], optional): Tags for categorizing the exercise
            skills (List[str], optional): Skills practiced in this exercise
            order (int, optional): Order in the learning path
            
        Returns:
            Exercise: The created exercise
        """
        # Check if exercise already exists
        if exercise_id:
            existing_exercise = self.db.get_exercise_by_exercise_id(exercise_id)
            if existing_exercise:
                logger.warning(f"Exercise {exercise_id} already exists")
                return existing_exercise
        
        # Create new exercise
        exercise = Exercise(
            name=name,
            description=description,
            difficulty=difficulty,
            exercise_id=exercise_id,
            commands=commands or [],
            complex_scenario=complex_scenario,
            tags=tags or [],
            skills=skills or [],
            order=order
        )
        
        self.db.add(exercise)
        
        logger.info(f"Added new exercise: {name}")
        return exercise
    
    def get_exercise(self, exercise_id: str) -> Optional[Exercise]:
        """
        Get an exercise by ID.
        
        Args:
            exercise_id (str): Exercise ID
            
        Returns:
            Optional[Exercise]: Exercise or None if not found
        """
        return self.db.get_by_id(Exercise, exercise_id)
    
    def get_exercise_by_exercise_id(self, exercise_id: str) -> Optional[Exercise]:
        """
        Get an exercise by exercise_id.
        
        Args:
            exercise_id (str): Exercise ID
            
        Returns:
            Optional[Exercise]: Exercise or None if not found
        """
        return self.db.get_exercise_by_exercise_id(exercise_id)
    
    def get_exercises_by_difficulty(self, difficulty: str) -> List[Exercise]:
        """
        Get exercises by difficulty level.
        
        Args:
            difficulty (str): Difficulty level
            
        Returns:
            List[Exercise]: List of exercises
        """
        return self.db.get_exercises_by_difficulty(difficulty)
    
    def update_exercise(self, exercise: Exercise) -> Exercise:
        """
        Update an exercise.
        
        Args:
            exercise (Exercise): Exercise to update
            
        Returns:
            Exercise: Updated exercise
        """
        return self.db.update(exercise)
    
    def delete_exercise(self, exercise_id: str) -> bool:
        """
        Delete an exercise by ID.
        
        Args:
            exercise_id (str): Exercise ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        exercise = self.get_exercise(exercise_id)
        if exercise:
            self.db.delete(exercise)
            logger.info(f"Deleted exercise: {exercise.name}")
            return True
        
        logger.warning(f"Exercise with ID {exercise_id} not found for deletion")
        return False
    
    # Progress Operations
    
    def add_progress(self, user_id: str, exercise_id: str, status: str = "not_started") -> Optional[Progress]:
        """
        Add a new progress record.
        
        Args:
            user_id (str): User ID
            exercise_id (str): Exercise ID
            status (str, optional): Initial status
            
        Returns:
            Optional[Progress]: The created progress record or None if user or exercise not found
        """
        # Check if user and exercise exist
        user = self.get_user(user_id)
        exercise = self.get_exercise(exercise_id)
        
        if not user or not exercise:
            logger.warning(f"User {user_id} or exercise {exercise_id} not found")
            return None
        
        # Check if progress already exists
        existing_progress = self.db.get_exercise_progress(user_id, exercise_id)
        if existing_progress:
            logger.warning(f"Progress for user {user_id} and exercise {exercise_id} already exists")
            return existing_progress
        
        # Create new progress
        progress = Progress(user_id=user_id, exercise_id=exercise_id, status=status)
        self.db.add(progress)
        
        logger.info(f"Added new progress for user {user.username} and exercise {exercise.name}")
        return progress
    
    def get_progress(self, progress_id: str) -> Optional[Progress]:
        """
        Get a progress record by ID.
        
        Args:
            progress_id (str): Progress ID
            
        Returns:
            Optional[Progress]: Progress record or None if not found
        """
        return self.db.get_by_id(Progress, progress_id)
    
    def get_user_progress(self, user_id: str) -> List[Progress]:
        """
        Get all progress records for a user.
        
        Args:
            user_id (str): User ID
            
        Returns:
            List[Progress]: List of progress records
        """
        return self.db.get_user_progress(user_id)
    
    def get_exercise_progress(self, user_id: str, exercise_id: str) -> Optional[Progress]:
        """
        Get progress for a specific exercise and user.
        
        Args:
            user_id (str): User ID
            exercise_id (str): Exercise ID
            
        Returns:
            Optional[Progress]: Progress record or None if not found
        """
        return self.db.get_exercise_progress(user_id, exercise_id)
    
    def update_progress(self, progress: Progress) -> Progress:
        """
        Update a progress record.
        
        Args:
            progress (Progress): Progress record to update
            
        Returns:
            Progress: Updated progress record
        """
        return self.db.update(progress)
    
    def delete_progress(self, progress_id: str) -> bool:
        """
        Delete a progress record by ID.
        
        Args:
            progress_id (str): Progress ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        progress = self.get_progress(progress_id)
        if progress:
            self.db.delete(progress)
            logger.info(f"Deleted progress record {progress_id}")
            return True
        
        logger.warning(f"Progress with ID {progress_id} not found for deletion")
        return False
    
    def start_exercise(self, user_id: str, exercise_id: str) -> Optional[Progress]:
        """
        Start an exercise for a user.
        
        Args:
            user_id (str): User ID
            exercise_id (str): Exercise ID
            
        Returns:
            Optional[Progress]: Updated progress record or None if not found
        """
        progress = self.get_exercise_progress(user_id, exercise_id)
        
        if not progress:
            # Create new progress record
            progress = self.add_progress(user_id, exercise_id, "in_progress")
            if not progress:
                return None
        else:
            # Update existing progress record
            progress.start_exercise()
            self.update_progress(progress)
        
        logger.info(f"Started exercise {exercise_id} for user {user_id}")
        return progress
    
    def complete_exercise(self, user_id: str, exercise_id: str, score: float = 1.0) -> Optional[Progress]:
        """
        Complete an exercise for a user.
        
        Args:
            user_id (str): User ID
            exercise_id (str): Exercise ID
            score (float, optional): Score achieved (0.0 to 1.0)
            
        Returns:
            Optional[Progress]: Updated progress record or None if not found
        """
        progress = self.get_exercise_progress(user_id, exercise_id)
        
        if not progress:
            logger.warning(f"No progress found for user {user_id} and exercise {exercise_id}")
            return None
        
        # Complete the exercise
        progress.complete_exercise(score)
        self.update_progress(progress)
        
        # Update user's completed exercises count
        user = self.get_user(user_id)
        if user:
            user.increment_completed_exercises()
            
            # Update user's skill scores based on the exercise
            exercise = self.get_exercise(exercise_id)
            if exercise and exercise.skills:
                for skill in exercise.skills:
                    if skill in user.skill_scores:
                        user.update_skill_score(skill, score)
            
            self.update_user(user)
        
        logger.info(f"Completed exercise {exercise_id} for user {user_id} with score {score}")
        return progress
    
    # Learning Path Operations
    
    def get_next_exercises(self, user_id: str, count: int = 3) -> List[Exercise]:
        """
        Get recommended next exercises for a user.
        
        Args:
            user_id (str): User ID
            count (int, optional): Number of exercises to recommend
            
        Returns:
            List[Exercise]: List of recommended exercises
        """
        return self.db.get_next_exercises(user_id, count)
    
    def get_completed_exercises(self, user_id: str) -> List[Exercise]:
        """
        Get all completed exercises for a user.
        
        Args:
            user_id (str): User ID
            
        Returns:
            List[Exercise]: List of completed exercises
        """
        return self.db.get_completed_exercises(user_id)
    
    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        Get statistics for a user.
        
        Args:
            user_id (str): User ID
            
        Returns:
            Dict[str, Any]: User statistics
        """
        return self.db.get_user_statistics(user_id)
    
    # Data Export/Import Operations
    
    def export_user_data(self, user_id: str) -> Dict[str, Any]:
        """
        Export all data for a user.
        
        Args:
            user_id (str): User ID
            
        Returns:
            Dict[str, Any]: User data export
        """
        user = self.get_user(user_id)
        if not user:
            logger.warning(f"User {user_id} not found for data export")
            return {}
        
        progress_records = self.get_user_progress(user_id)
        
        # Convert progress records to dictionaries
        progress_dicts = [p.to_dict() for p in progress_records]
        
        # Get completed exercises
        completed_exercises = self.get_completed_exercises(user_id)
        exercise_dicts = [e.to_dict() for e in completed_exercises]
        
        # Get statistics
        statistics = self.get_user_statistics(user_id)
        
        export_data = {
            "user": user.to_dict(),
            "progress": progress_dicts,
            "completed_exercises": exercise_dicts,
            "statistics": statistics,
            "export_date": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Exported data for user {user.username}")
        return export_data
    
    def import_user_data(self, data: Dict[str, Any]) -> Optional[UserProfile]:
        """
        Import user data.
        
        Args:
            data (Dict[str, Any]): User data to import
            
        Returns:
            Optional[UserProfile]: Imported user profile or None if import failed
        """
        if "user" not in data:
            logger.error("Invalid user data format for import")
            return None
        
        user_data = data["user"]
        
        # Check if user already exists
        existing_user = self.get_user_by_username(user_data["username"])
        if existing_user:
            logger.warning(f"User {user_data['username']} already exists, updating")
            user = existing_user
        else:
            # Create new user
            user = self.add_user(
                username=user_data["username"],
                email=user_data.get("email"),
                skill_level=user_data.get("skill_level", "beginner")
            )
        
        # Update user attributes
        user.skill_scores = user_data.get("skill_scores", user.skill_scores)
        user.preferences = user_data.get("preferences", user.preferences)
        user.completed_exercises = user_data.get("completed_exercises", user.completed_exercises)
        
        self.update_user(user)
        
        # Import progress records if present
        if "progress" in data:
            for progress_data in data["progress"]:
                exercise_id = progress_data["exercise_id"]
                
                # Check if exercise exists
                exercise = self.get_exercise(exercise_id)
                if not exercise and "completed_exercises" in data:
                    # Try to find exercise in completed_exercises
                    for exercise_data in data["completed_exercises"]:
                        if exercise_data["id"] == exercise_id:
                            # Create the exercise
                            exercise = self.add_exercise(
                                name=exercise_data["name"],
                                description=exercise_data["description"],
                                difficulty=exercise_data["difficulty"],
                                exercise_id=exercise_data["exercise_id"],
                                tags=exercise_data.get("tags", []),
                                skills=exercise_data.get("skills", []),
                                order=exercise_data.get("order", 0)
                            )
                            break
                
                if exercise:
                    # Create or update progress
                    progress = self.get_exercise_progress(user.id, exercise.id)
                    
                    if not progress:
                        progress = self.add_progress(user.id, exercise.id, progress_data["status"])
                    
                    if progress:
                        # Update progress attributes
                        if progress_data.get("completed_at"):
                            progress.completed_at = datetime.fromisoformat(progress_data["completed_at"])
                        
                        progress.status = progress_data["status"]
                        progress.attempts = progress_data.get("attempts", progress.attempts)
                        progress.time_spent = progress_data.get("time_spent", progress.time_spent)
                        progress.score = progress_data.get("score", progress.score)
                        progress.mistakes = progress_data.get("mistakes", progress.mistakes)
                        progress.feedback = progress_data.get("feedback", progress.feedback)
                        
                        self.update_progress(progress)
        
        logger.info(f"Imported data for user {user.username}")
        return user

# Singleton instance
_persistence_layer = None

def get_persistence_layer() -> PersistenceLayer:
    """
    Get the persistence layer singleton instance.
    
    Returns:
        PersistenceLayer: Persistence layer instance
    """
    global _persistence_layer
    if _persistence_layer is None:
        _persistence_layer = PersistenceLayer()
    return _persistence_layer
