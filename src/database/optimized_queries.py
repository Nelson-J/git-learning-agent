from typing import List, Dict, Any
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from src.models import Exercise, Progress, UserProfile

class DatabaseOptimizer:
    def __init__(self, connection_string: str):
        self.engine = create_engine(
            connection_string,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=1800
        )
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def batch_insert(self, table: str, records: List[Dict[str, Any]]) -> None:
        """Optimized batch insert operation."""
        with self.session_scope() as session:
            session.execute(
                text(f"INSERT INTO {table} ({','.join(records[0].keys())}) "
                     f"VALUES ({','.join([':' + k for k in records[0].keys()])})")
                ,records
            )

    def bulk_fetch(self, table: str, conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Optimized bulk fetch operation."""
        with self.session_scope() as session:
            query = f"SELECT * FROM {table} WHERE "
            query += " AND ".join([f"{k} = :{k}" for k in conditions.keys()])
            result = session.execute(text(query), conditions)
            return [dict(row) for row in result]

    def get_user_by_username(self, username: str):
        with self.session_scope() as session:
            return session.query(UserProfile).filter(UserProfile.username == username).first()

    def get_by_id(self, model, id):
        with self.session_scope() as session:
            return session.query(model).filter(model.id == id).first()

    def get_user_exercises(self, user_id: str):
        with self.session_scope() as session:
            return session.query(Exercise).join(Progress).filter(Progress.user_id == user_id).all()

def get_db_optimizer(connection_string: str) -> DatabaseOptimizer:
    return DatabaseOptimizer(connection_string)
