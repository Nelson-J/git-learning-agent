"""
Main entry point for the Git Learning System.

This module initializes the database and starts the CLI.
"""

import os
import sys
import logging
from pathlib import Path

from src.database.init_db import initialize_database
from src.cli.learning_cli import GitLearningCLI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def main():
    """
    Main entry point.
    """
    logger.info("Starting Git Learning System")
    
    # Initialize database
    initialize_database()
    
    # Start CLI
    cli = GitLearningCLI()
    cli.run()

if __name__ == "__main__":
    main()
