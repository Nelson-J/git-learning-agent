"""
Database optimization module for the Git Learning System.

This module provides optimized database operations for common queries
and transactions, improving performance and resource utilization.
"""

import os
import logging
from typing import List, Dict, Any, Optional, Type, TypeVar
from contextlib import contextmanager
from sqlalchemy import create_engine, text, func, desc
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError

from src.database.init_db import get_db_path, create_connection_string
from src.models.user_profile import UserProfile
from src.models.exercise import Exercise
from src.models.progress import Progress

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Generic type for SQLAlchemy models
T = TypeVar('T')

class DatabaseOptimizer:
    """
    Database optimizer for efficient database operations.
    
    This class provides optimized methods for common database operations,
    including connection pooling, session management, and query optimization.
    """
    
    def __init__(self, connection_string: str = None):
        """
        Initialize the database optimizer.
        
        Args:
            connection_string (str, optional): Database connection string.
                If None, a default connection string will be created.
        """
        if connection_string is None:
            connection_string = create_connection_string()
        
        self.connection_string = connection_string
        self.engine = create_engine(
            connection_string,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=1800,
            connect_args={"check_same_thread": False},  # Allow multi-threading for SQLite
        )
        self.Session = sessionmaker(bind=self.engine)
        
        logger.info(f"DatabaseOptimizer initialized with connection to {get_db_path()}")

    @contextmanager
    def session_scope(self):
        """
        Provide a transactional scope around a series of operations.
        
        Yields:
            Session: SQLAlchemy session
        
        Raises:
            Exception: Any exception that occurs during the transaction
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error in database transaction: {str(e)}")
            raise e
        finally:
            session.close()

    def batch_insert(self, table: str, records: List[Dict[str, Any]]) -> None:
        """
        Optimized batch insert operation.
        
        Args:
            table (str): Table name
            records (List[Dict[str, Any]]): Records to insert
        
        Raises:
            SQLAlchemyError: If the insert operation fails
        """
        if not records:
            return
        
        with self.session_scope() as session:
            columns = ",".join(records[0].keys())
            placeholders = ",".join([f":{k}" for k in records[0].keys()])
            query = (
                f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            )
            session.execute(text(query), records)
            
        logger.info(f"Batch inserted {len(records)} records into {table}")

    def bulk_fetch(self, table: str, conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Optimized bulk fetch operation.
        
        Args:
            table (str): Table name
            conditions (Dict[str, Any]): Query conditions
            
        Returns:
            List[Dict[str, Any]]: Query results
        
        Raises:
            SQLAlchemyError: If the fetch operation fails
        """
        with self.session_scope() as session:
            query = (
                "SELECT * FROM {} WHERE {}".format(
                    table, " AND ".join([f"{k} = :{k}" for k in conditions.keys()])
                )
            )
            result = session.execute(text(query), conditions)
            return [dict(row) for row in result]

    def get_by_id(self, model_class: Type[T], id: str) -> Optional[T]:
        """
        Get a record by ID.
        
        Args:
            model_class (Type[T]): SQLAlchemy model class
            id (str): Record ID
            
        Returns:
            Optional[T]: Record or None if not found
        """
        with self.session_scope() as session:
            return session.query(model_class).filter_by(id=id).first()

    def get_all(self, model_class: Type[T]) -> List[T]:
        """
        Get all records of a model.
        
        Args:
            model_class (Type[T]): SQLAlchemy model class
            
        Returns:
            List[T]: List of records
        """
        with self.session_scope() as session:
            return session.query(model_class).all()

    def add(self, record: T) -> T:
        """
        Add a record to the database.
        
        Args:
            record (T): Record to add
            
        Returns:
            T: Added record
        """
        with self.session_scope() as session:
            session.add(record)
            session.flush()
            session.refresh(record)
            return record

    def update(self, record: T) -> T:
        """
        Update a record in the database.
        
        Args:
            record (T): Record to update
            
        Returns:
            T: Updated record
        """
        with self.session_scope() as session:
            session.merge(record)
            session.flush()
            session.refresh(record)
            return record

    def delete(self, record: T) -> None:
        """
        Delete a record from the database.
        
        Args:
            record (T): Record to delete
        """
        with self.session_scope() as session:
            session.delete(record)

    def get_user_by_username(self, username: str) -> Optional[UserProfile]:
        """Get a user by username."""
        with self.session_scope() as session:
            return session.query(UserProfile).filter_by(username=username).first()

    def get_exercise_by_exercise_id(self, exercise_id: str) -> Optional[Exercise]:
        """Get an exercise by exercise_id."""
        with self.session_scope() as session:
            return session.query(Exercise).filter_by(exercise_id=exercise_id).first()

    def get_exercises_by_difficulty(self, difficulty: str) -> List[Exercise]:
        """Get exercises by difficulty level."""
        with self.session_scope() as session:
            return session.query(Exercise).filter_by(difficulty=difficulty).all()

    def get_user_progress(self, user_id: str) -> List[Progress]:
        """Get all progress records for a user."""
        with self.session_scope() as session:
            return session.query(Progress).filter_by(user_id=user_id).all()

    def get_exercise_progress(self, user_id: str, exercise_id: str) -> Optional[Progress]:
        """Get progress for a specific exercise and user."""
        with self.session_scope() as session:
            return session.query(Progress).filter_by(
                user_id=user_id, exercise_id=exercise_id
            ).first()

    def get_completed_exercises(self, user_id: str) -> List[Exercise]:
        """Get all completed exercises for a user."""
        with self.session_scope() as session:
            completed_progress = session.query(Progress).filter_by(
                user_id=user_id, status="completed"
            ).all()
            exercise_ids = [p.exercise_id for p in completed_progress]
            if not exercise_ids:
                return []
            return session.query(Exercise).filter(
                Exercise.id.in_(exercise_ids)
            ).all()

    def get_next_exercises(self, user_id: str, count: int = 3) -> List[Exercise]:
        """Get recommended next exercises for a user."""
        with self.session_scope() as session:
            user = session.query(UserProfile).filter_by(id=user_id).first()
            if not user:
                return []
            completed_progress = session.query(Progress).filter_by(
                user_id=user_id, status="completed"
            ).all()
            completed_exercise_ids = [p.exercise_id for p in completed_progress]
            query = session.query(Exercise).filter_by(
                difficulty=user.skill_level
            )
            if completed_exercise_ids:
                query = query.filter(~Exercise.id.in_(completed_exercise_ids))
            return query.order_by(Exercise.order).limit(count).all()

    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get statistics for a user."""
        with self.session_scope() as session:
            user = session.query(UserProfile).filter_by(id=user_id).first()
            if not user:
                return {}
            progress_records = session.query(Progress).filter_by(user_id=user_id).all()
            completed_count = sum(1 for p in progress_records if p.status == "completed")
            in_progress_count = sum(1 for p in progress_records if p.status == "in_progress")
            failed_count = sum(1 for p in progress_records if p.status == "failed")
            total_time = sum(p.time_spent for p in progress_records)
            avg_score = sum(p.score for p in progress_records if p.status == "completed")
            if completed_count > 0:
                avg_score /= completed_count
            else:
                avg_score = 0.0
            beginner_count = session.query(func.count(Progress.id)).join(Exercise).filter(
                Progress.user_id == user_id,
                Progress.status == "completed",
                Exercise.difficulty == "beginner"
            ).scalar() or 0
            intermediate_count = session.query(func.count(Progress.id)).join(Exercise).filter(
                Progress.user_id == user_id,
                Progress.status == "completed",
                Exercise.difficulty == "intermediate"
            ).scalar() or 0
            advanced_count = session.query(func.count(Progress.id)).join(Exercise).filter(
                Progress.user_id == user_id,
                Progress.status == "completed",
                Exercise.difficulty == "advanced"
            ).scalar() or 0
            return {
                "user_id": user_id,
                "username": user.username,
                "skill_level": user.skill_level,
                "completed_count": completed_count,
                "in_progress_count": in_progress_count,
                "failed_count": failed_count,
                "total_time": total_time,
                "avg_score": avg_score,
                "beginner_completed": beginner_count,
                "intermediate_completed": intermediate_count,
                "advanced_completed": advanced_count,
                "skill_scores": user.skill_scores
            }

def get_db_optimizer() -> DatabaseOptimizer:
    """Get a database optimizer instance."""
    return DatabaseOptimizer()
