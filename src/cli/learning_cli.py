"""
Command-line interface for the Git Learning System.

This module provides a CLI for interacting with the Git Learning System,
allowing users to manage their profiles, work on exercises, and track their progress.
"""

import os
import sys
import logging
import argparse
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from src.database.persistence_layer import get_persistence_layer
from src.models.user_profile import UserProfile
from src.models.exercise import Exercise, GitCommand, ComplexScenario
from src.models.progress import Progress

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def parse_command(command_str: str = None) -> Dict[str, Any]:
    """
    Parse the command string into command and arguments.
    
    Args:
        command_str (str, optional): The command string entered by the user. If None, sys.argv is used.
    
    Returns:
        Dict[str, Any]: Parsed command and arguments.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Git Learning System CLI")
    parser.add_argument("command", help="Command to run", nargs="?")
    
    args, unknown = parser.parse_known_args()
    return args

def provide_feedback(message: str, success: bool = True):
    """
    Provide feedback to the user.
    
    Args:
        message (str): The feedback message to display.
        success (bool): Whether the feedback is for a success or failure
    """
    if success:
        print(f"Command '{message}' executed successfully.")
    else:
        print(f"Command '{message}' failed. Please try again.")

class GitLearningCLI:
    """
    Command-line interface for the Git Learning System.
    
    This class provides a CLI for interacting with the Git Learning System,
    allowing users to manage their profiles, work on exercises, and track their progress.
    """
    
    name = "git-learn"  # Required by Click
    
    def __init__(self):
        """
        Initialize the CLI.
        """
        self.persistence = get_persistence_layer()
        self.current_user = None
        self.current_exercise = None
        
        logger.info("GitLearningCLI initialized")
    
    def run(self):
        """
        Run the CLI.
        """
        parser = argparse.ArgumentParser(description="Git Learning System CLI")
        
        # Create subparsers for different commands
        subparsers = parser.add_subparsers(dest="command", help="Command to run")
        
        # User commands
        user_parser = subparsers.add_parser("user", help="User management commands")
        user_subparsers = user_parser.add_subparsers(dest="user_command", help="User command to run")
        
        # Create user
        create_user_parser = user_subparsers.add_parser("create", help="Create a new user")
        create_user_parser.add_argument("username", help="Username")
        create_user_parser.add_argument("--email", help="Email address")
        create_user_parser.add_argument("--skill-level", help="Initial skill level", default="beginner")
        
        # Login
        login_parser = user_subparsers.add_parser("login", help="Login as a user")
        login_parser.add_argument("username", help="Username")
        
        # Show user profile
        profile_parser = user_subparsers.add_parser("profile", help="Show user profile")
        
        # Update user profile
        update_parser = user_subparsers.add_parser("update", help="Update user profile")
        update_parser.add_argument("--email", help="New email address")
        update_parser.add_argument("--skill-level", help="New skill level")
        
        # Exercise commands
        exercise_parser = subparsers.add_parser("exercise", help="Exercise management commands")
        exercise_subparsers = exercise_parser.add_subparsers(dest="exercise_command", help="Exercise command to run")
        
        # List exercises
        list_parser = exercise_subparsers.add_parser("list", help="List exercises")
        list_parser.add_argument("--difficulty", help="Filter by difficulty")
        
        # Show exercise details
        show_parser = exercise_subparsers.add_parser("show", help="Show exercise details")
        show_parser.add_argument("exercise_id", help="Exercise ID")
        
        # Start exercise
        start_parser = exercise_subparsers.add_parser("start", help="Start an exercise")
        start_parser.add_argument("exercise_id", help="Exercise ID")
        
        # Complete exercise
        complete_parser = exercise_subparsers.add_parser("complete", help="Complete an exercise")
        complete_parser.add_argument("exercise_id", help="Exercise ID")
        complete_parser.add_argument("--score", help="Score achieved", type=float, default=1.0)
        
        # Progress commands
        progress_parser = subparsers.add_parser("progress", help="Progress tracking commands")
        progress_subparsers = progress_parser.add_subparsers(dest="progress_command", help="Progress command to run")
        
        # Show progress
        show_progress_parser = progress_subparsers.add_parser("show", help="Show progress")
        
        # Show statistics
        stats_parser = progress_subparsers.add_parser("stats", help="Show statistics")
        
        # Export/Import commands
        data_parser = subparsers.add_parser("data", help="Data management commands")
        data_subparsers = data_parser.add_subparsers(dest="data_command", help="Data command to run")
        
        # Export data
        export_parser = data_subparsers.add_parser("export", help="Export user data")
        export_parser.add_argument("--file", help="Output file path")
        
        # Import data
        import_parser = data_subparsers.add_parser("import", help="Import user data")
        import_parser.add_argument("file", help="Input file path")
        
        # Parse arguments
        args = parser.parse_args()
        
        # Check if a command was specified
        if not args.command:
            parser.print_help()
            return
        
        # Handle user commands
        if args.command == "user":
            self._handle_user_commands(args)
        
        # Handle exercise commands
        elif args.command == "exercise":
            self._handle_exercise_commands(args)
        
        # Handle progress commands
        elif args.command == "progress":
            self._handle_progress_commands(args)
        
        # Handle data commands
        elif args.command == "data":
            self._handle_data_commands(args)
    
    def _handle_user_commands(self, args):
        """
        Handle user management commands.
        
        Args:
            args: Command-line arguments
        """
        if args.user_command == "create":
            self._create_user(args)
        elif args.user_command == "login":
            self._login_user(args)
        elif args.user_command == "profile":
            self._show_user_profile()
        elif args.user_command == "update":
            self._update_user_profile(args)
        else:
            print("Invalid user command")
    
    def _handle_exercise_commands(self, args):
        """
        Handle exercise management commands.
        
        Args:
            args: Command-line arguments
        """
        if args.exercise_command == "list":
            self._list_exercises(args)
        elif args.exercise_command == "show":
            self._show_exercise(args)
        elif args.exercise_command == "start":
            self._start_exercise(args)
        elif args.exercise_command == "complete":
            self._complete_exercise(args)
        else:
            print("Invalid exercise command")
    
    def _handle_progress_commands(self, args):
        """
        Handle progress tracking commands.
        
        Args:
            args: Command-line arguments
        """
        if args.progress_command == "show":
            self._show_progress()
        elif args.progress_command == "stats":
            self._show_statistics()
        else:
            print("Invalid progress command")
    
    def _handle_data_commands(self, args):
        """
        Handle data management commands.
        
        Args:
            args: Command-line arguments
        """
        if args.data_command == "export":
            self._export_data(args)
        elif args.data_command == "import":
            self._import_data(args)
        else:
            print("Invalid data command")
    
    def _create_user(self, args):
        """
        Create a new user.
        
        Args:
            args: Command-line arguments
        """
        username = args.username
        email = args.email
        skill_level = args.skill_level
        
        user = self.persistence.add_user(username, email, skill_level)
        
        if user:
            print(f"User {username} created successfully")
            self.current_user = user
        else:
            provide_feedback(f"create user {username}", success=False)
    
    def _login_user(self, args):
        """
        Login as a user.
        
        Args:
            args: Command-line arguments
        """
        username = args.username
        
        user = self.persistence.get_user_by_username(username)
        
        if user:
            provide_feedback(f"login {username}", success=True)
            self.current_user = user
        else:
            provide_feedback(f"login {username}", success=False)
    
    def _show_user_profile(self):
        """
        Show user profile.
        """
        if not self._check_login():
            return
        
        user = self.current_user
        
        print(f"Username: {user.username}")
        print(f"Email: {user.email or 'Not set'}")
        print(f"Skill Level: {user.skill_level}")
        print(f"Completed Exercises: {user.completed_exercises}")
        
        if user.skill_scores:
            print("\nSkill Scores:")
            for skill, score in user.skill_scores.items():
                print(f"  {skill}: {score:.2f}")
    
    def _update_user_profile(self, args):
        """
        Update user profile.
        
        Args:
            args: Command-line arguments
        """
        if not self._check_login():
            return
        
        user = self.current_user
        
        if args.email:
            user.email = args.email
            provide_feedback(f"update user {user.username} email", success=True)
        
        if args.skill_level:
            user.skill_level = args.skill_level
            provide_feedback(f"update user {user.username} skill level", success=True)
        
        self.persistence.update_user(user)
    
    def _list_exercises(self, args):
        """
        List exercises.
        
        Args:
            args: Command-line arguments
        """
        if args.difficulty:
            exercises = self.persistence.get_exercises_by_difficulty(args.difficulty)
            print(f"Exercises with difficulty '{args.difficulty}':")
        else:
            exercises = self.persistence.get_all(Exercise)
            print("All exercises:")
        
        if not exercises:
            print("No exercises found")
            return
        
        for exercise in exercises:
            print(f"ID: {exercise.exercise_id}, Name: {exercise.name}, Difficulty: {exercise.difficulty}")
    
    def _show_exercise(self, args):
        """
        Show exercise details.
        
        Args:
            args: Command-line arguments
        """
        exercise_id = args.exercise_id
        
        exercise = self.persistence.get_exercise_by_exercise_id(exercise_id)
        
        if not exercise:
            provide_feedback(f"show exercise {exercise_id}", success=False)
            return
        
        print(f"Exercise: {exercise.name}")
        print(f"ID: {exercise.exercise_id}")
        print(f"Difficulty: {exercise.difficulty}")
        print(f"Description: {exercise.description}")
        
        if exercise.tags:
            print(f"Tags: {', '.join(exercise.tags)}")
        
        if exercise.skills:
            print(f"Skills: {', '.join(exercise.skills)}")
        
        if exercise.commands:
            print("\nCommands:")
            for i, command in enumerate(exercise.commands, 1):
                print(f"  {i}. {command.command}")
                if command.description:
                    print(f"     Description: {command.description}")
        
        if exercise.complex_scenario:
            print("\nComplex Scenario:")
            print(f"  Setup: {exercise.complex_scenario.setup}")
            print(f"  Task: {exercise.complex_scenario.task}")
            print(f"  Validation: {exercise.complex_scenario.validation}")
    
    def _start_exercise(self, args):
        """
        Start an exercise.
        
        Args:
            args: Command-line arguments
        """
        if not self._check_login():
            return
        
        exercise_id = args.exercise_id
        
        exercise = self.persistence.get_exercise_by_exercise_id(exercise_id)
        
        if not exercise:
            provide_feedback(f"start exercise {exercise_id}", success=False)
            return
        
        progress = self.persistence.start_exercise(self.current_user.id, exercise.id)
        
        if progress:
            print(f"Exercise {exercise.name} started successfully")
            self.current_exercise = exercise
        else:
            provide_feedback(f"start exercise {exercise.name}", success=False)
    
    def _complete_exercise(self, args):
        """
        Complete an exercise.
        
        Args:
            args: Command-line arguments
        """
        if not self._check_login():
            return
        
        exercise_id = args.exercise_id
        score = args.score
        
        exercise = self.persistence.get_exercise_by_exercise_id(exercise_id)
        
        if not exercise:
            provide_feedback(f"complete exercise {exercise_id}", success=False)
            return
        
        progress = self.persistence.complete_exercise(self.current_user.id, exercise.id, score)
        
        if progress:
            print(f"Exercise {exercise.name} completed successfully")
            
            # Show updated skill levels
            if exercise.skills:
                print("\nUpdated skill levels:")
                for skill in exercise.skills:
                    if skill in self.current_user.skill_scores:
                        print(f"  {skill}: {self.current_user.skill_scores[skill]:.2f}")
        else:
            provide_feedback(f"complete exercise {exercise.name}", success=False)
    
    def _show_progress(self):
        """
        Show progress.
        """
        if not self._check_login():
            return
        
        progress_records = self.persistence.get_user_progress(self.current_user.id)
        
        if not progress_records:
            print("No progress records found")
            return
        
        print(f"Progress for user '{self.current_user.username}':")
        
        for progress in progress_records:
            exercise = self.persistence.get_exercise(progress.exercise_id)
            
            if not exercise:
                continue
            
            status_str = progress.status.replace("_", " ").title()
            
            print(f"Exercise: {exercise.name}")
            print(f"  Status: {status_str}")
            print(f"  Started: {progress.created_at}")
            
            if progress.completed_at:
                print(f"  Completed: {progress.completed_at}")
            
            if progress.score is not None:
                print(f"  Score: {progress.score:.2f}")
            
            if progress.attempts:
                print(f"  Attempts: {progress.attempts}")
            
            if progress.time_spent:
                print(f"  Time Spent: {progress.time_spent} seconds")
            
            print()
    
    def _show_statistics(self):
        """
        Show statistics.
        """
        if not self._check_login():
            return
        
        stats = self.persistence.get_user_statistics(self.current_user.id)
        
        if not stats:
            print("No statistics available")
            return
        
        print(f"Statistics for user '{stats['username']}':")
        print(f"Skill Level: {stats['skill_level']}")
        print(f"Completed Exercises: {stats['completed_count']}")
        print(f"In Progress Exercises: {stats['in_progress_count']}")
        print(f"Failed Exercises: {stats['failed_count']}")
        
        if stats['total_time']:
            print(f"Total Time Spent: {stats['total_time']} seconds")
        
        if stats['avg_score']:
            print(f"Average Score: {stats['avg_score']:.2f}")
        
        print("\nCompleted by Difficulty:")
        print(f"  Beginner: {stats['beginner_completed']}")
        print(f"  Intermediate: {stats['intermediate_completed']}")
        print(f"  Advanced: {stats['advanced_completed']}")
        
        if stats['skill_scores']:
            print("\nSkill Scores:")
            for skill, score in stats['skill_scores'].items():
                print(f"  {skill}: {score:.2f}")
    
    def _export_data(self, args):
        """
        Export user data.
        
        Args:
            args: Command-line arguments
        """
        if not self._check_login():
            return
        
        data = self.persistence.export_user_data(self.current_user.id)
        
        if not data:
            print("No data to export")
            return
        
        if args.file:
            file_path = args.file
        else:
            file_path = f"{self.current_user.username}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        
        provide_feedback(f"export data to {file_path}", success=True)
    
    def _import_data(self, args):
        """
        Import user data.
        
        Args:
            args: Command-line arguments
        """
        file_path = args.file
        
        if not os.path.exists(file_path):
            provide_feedback(f"import data from {file_path}", success=False)
            return
        
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            provide_feedback(f"import data from {file_path}", success=False)
            return
        
        user = self.persistence.import_user_data(data)
        
        if user:
            provide_feedback(f"import data for user {user.username}", success=True)
            self.current_user = user
        else:
            provide_feedback("import data", success=False)
    
    def _check_login(self) -> bool:
        """
        Check if a user is logged in.
        
        Returns:
            bool: True if a user is logged in, False otherwise
        """
        if not self.current_user:
            provide_feedback("login", success=False)
            return False
        
        return True

    def create_user(self, username):
        # Logic to create user and return success message
        user = self.persistence.add_user(username, None, "beginner")
        if user:
            return f"User {username} created successfully"
        else:
            return f"Failed to create user {username}"

    def main(self, *args):
        """
        Main entry point.
        """
        self.run()

if __name__ == "__main__":
    cli = GitLearningCLI()
    cli.main()
