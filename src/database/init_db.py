"""
Database initialization module for the Git Learning System.

This module handles the creation and initialization of the SQLite database,
including schema creation, migrations, and initial data setup.
"""

import os
import sys
import logging
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Define base model class
Base = declarative_base()

def get_db_path():
    """
    Determine the appropriate database path based on the environment.
    
    For development: Use a local SQLite database in the project directory.
    For production: Use a SQLite database in the user's home directory.
    
    Returns:
        str: Path to the SQLite database file
    """
    # Check if running in development mode
    if os.environ.get("GIT_LEARNING_ENV") == "development":
        # Use a database in the project directory
        db_path = Path(__file__).parent.parent.parent / "data" / "git_learning.db"
    else:
        # Use a database in the user's home directory
        home_dir = Path.home()
        app_dir = home_dir / ".git-learning-agent"
        
        # Create the directory if it doesn't exist
        app_dir.mkdir(exist_ok=True)
        
        db_path = app_dir / "git_learning.db"
    
    # Ensure the parent directory exists
    db_path.parent.mkdir(exist_ok=True)
    
    return str(db_path)

def create_connection_string():
    """
    Create a SQLAlchemy connection string for the SQLite database.
    
    Returns:
        str: SQLAlchemy connection string
    """
    db_path = get_db_path()
    return f"sqlite:///{db_path}"

def optimize_sqlite_connection(dbapi_connection, connection_record):
    """
    Optimize SQLite connection settings for better performance.
    
    Args:
        dbapi_connection: The database connection
        connection_record: Connection record
    """
    # Enable foreign key constraints
    dbapi_connection.execute("PRAGMA foreign_keys=ON")
    
    # Set journal mode to WAL for better concurrency
    dbapi_connection.execute("PRAGMA journal_mode=WAL")
    
    # Set synchronous mode to NORMAL for better performance
    dbapi_connection.execute("PRAGMA synchronous=NORMAL")
    
    # Enable memory-mapped I/O for the database file
    dbapi_connection.execute("PRAGMA mmap_size=30000000000")

def init_db(connection_string=None):
    """
    Initialize the database, creating tables if they don't exist.
    
    Args:
        connection_string (str, optional): Database connection string.
            If None, a default connection string will be created.
    
    Returns:
        tuple: (engine, session_maker) - SQLAlchemy engine and session maker
    """
    if connection_string is None:
        connection_string = create_connection_string()
    
    # Create engine with connection pooling
    engine = create_engine(
        connection_string,
        connect_args={"check_same_thread": False},  # Allow multi-threading for SQLite
        echo=False,  # Set to True for SQL debugging
    )
    
    # Register optimization function for SQLite connections
    event.listen(engine, "connect", optimize_sqlite_connection)
    
    # Import models to ensure they're registered with Base
    from src.models.user_profile import UserProfile
    from src.models.exercise import Exercise
    from src.models.progress import Progress
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create session maker
    Session = sessionmaker(bind=engine)
    
    logger.info(f"Database initialized at {get_db_path()}")
    
    return engine, Session

def reset_db():
    """
    Reset the database by dropping all tables and recreating them.
    WARNING: This will delete all data in the database.
    
    Returns:
        tuple: (engine, session_maker) - SQLAlchemy engine and session maker
    """
    connection_string = create_connection_string()
    
    # Create engine
    engine = create_engine(connection_string)
    
    # Import models to ensure they're registered with Base
    from src.models.user_profile import UserProfile
    from src.models.exercise import Exercise
    from src.models.progress import Progress
    
    # Drop all tables
    Base.metadata.drop_all(engine)
    
    logger.warning("All database tables have been dropped")
    
    # Recreate all tables
    Base.metadata.create_all(engine)
    
    # Create session maker
    Session = sessionmaker(bind=engine)
    
    logger.info("Database has been reset")
    
    return engine, Session

def backup_db():
    """
    Create a backup of the database file.
    
    Returns:
        str: Path to the backup file
    """
    import shutil
    from datetime import datetime
    
    # Get the database path
    db_path = get_db_path()
    
    # Create a timestamp for the backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create the backup path
    backup_path = f"{db_path}.backup_{timestamp}"
    
    # Copy the database file to the backup path
    shutil.copy2(db_path, backup_path)
    
    logger.info(f"Database backup created at {backup_path}")
    
    return backup_path

def main():
    """
    Main function to initialize the database when run as a script.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize the Git Learning System database")
    parser.add_argument("--reset", action="store_true", help="Reset the database (WARNING: This will delete all data)")
    parser.add_argument("--backup", action="store_true", help="Create a backup of the database")
    
    args = parser.parse_args()
    
    if args.backup:
        backup_path = backup_db()
        print(f"Database backup created at {backup_path}")
    elif args.reset:
        confirm = input("WARNING: This will delete all data in the database. Are you sure? (y/N): ")
        if confirm.lower() == "y":
            engine, Session = reset_db()
            print("Database has been reset")
        else:
            print("Database reset cancelled")
    else:
        engine, Session = init_db()
        print(f"Database initialized at {get_db_path()}")

if __name__ == "__main__":
    main()
