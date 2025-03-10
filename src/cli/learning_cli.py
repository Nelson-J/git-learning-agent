"""
Command-line interface for the Git Learning System.

This module provides a CLI for interacting with the Git Learning System,
allowing users to manage their profiles, work on exercises, and track their progress.
"""

import os
import logging
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import click

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

@click.group()
@click.pass_context
def cli(ctx):
    """Git Learning System CLI"""
    ctx.obj = GitLearningCLI()

@cli.command()
def init():
    """Initialize a new repository."""
    click.echo("Initialized new repository")
    return 0

@cli.command()
@click.argument('username')
@click.option('--email', help="User's email address")
@click.option('--skill-level', default="beginner", help="Initial skill level")
def create_user(username, email, skill_level):
    """Create a new user."""
    cli = GitLearningCLI()
    cli._create_user(username, email, skill_level)
    click.echo(f"Created user {username}")

@cli.command()
@click.argument('username')
def login(username):
    """Login as a user."""
    cli = GitLearningCLI()
    cli._login_user(username)
    click.echo(f"Logged in as {username}")

@cli.command()
def profile():
    """Show user profile."""
    cli = GitLearningCLI()
    cli._show_user_profile()

@cli.command()
@click.option('--email', help="New email address")
@click.option('--skill-level', help="New skill level")
def update_profile(email, skill_level):
    """Update user profile."""
    cli = GitLearningCLI()
    cli._update_user_profile(email, skill_level)

@cli.command()
@click.option('--difficulty', help="Filter by difficulty")
def list_exercises(difficulty):
    """List exercises."""
    cli = GitLearningCLI()
    cli._list_exercises(difficulty)

@cli.command()
@click.argument('exercise_id')
def show_exercise(exercise_id):
    """Show exercise details."""
    cli = GitLearningCLI()
    cli._show_exercise(exercise_id)

@cli.command()
@click.argument('exercise_id')
def start_exercise(exercise_id):
    """Start an exercise."""
    cli = GitLearningCLI()
    cli._start_exercise(exercise_id)

@cli.command()
@click.argument('exercise_id')
@click.option('--score', help="Score achieved", type=float, default=1.0)
def complete_exercise(exercise_id, score):
    """Complete an exercise."""
    cli = GitLearningCLI()
    cli._complete_exercise(exercise_id, score)

@cli.command()
def show_progress():
    """Show progress."""
    cli = GitLearningCLI()
    cli._show_progress()

@cli.command()
def show_statistics():
    """Show statistics."""
    cli = GitLearningCLI()
    cli._show_statistics()

@cli.command()
@click.option('--file', help="Output file path")
def export_data(file):
    """Export user data."""
    cli = GitLearningCLI()
    cli._export_data(file)

@cli.command()
@click.argument('file')
def import_data(file):
    """Import user data."""
    cli = GitLearningCLI()
    cli._import_data(file)

def get_auth():
    from src.auth.auth_handler import AuthHandler
    return AuthHandler()

class GitLearningCLI:
    """
    Command-line interface for the Git Learning System.
    """
    name = 'git-learning-cli'
    def __init__(self):
        self.persistence = get_persistence_layer()
        self.current_user = None
        self.current_exercise = None
        logger.info("GitLearningCLI initialized")

    def _create_user(self, username, email, skill_level):
        """Create a new user."""
        user = UserProfile(username, email, skill_level)
        self.persistence.add_user(user)
        self.current_user = user
        return user

    def _login_user(self, username):
        """Login as a user."""
        user = self.persistence.get_user_by_username(username)
        if user:
            self.current_user = user
        else:
            click.echo(f"User {username} not found")

    def _show_user_profile(self):
        """Show user profile."""
        if not self.current_user:
            click.echo("You are not logged in")
            return
        click.echo(f"Username: {self.current_user.username}")
        click.echo(f"Email: {self.current_user.email or 'Not set'}")
        click.echo(f"Skill Level: {self.current_user.skill_level}")
        click.echo(f"Completed Exercises: {self.current_user.completed_exercises}")

    def _update_user_profile(self, email, skill_level):
        """Update user profile."""
        if not self.current_user:
            click.echo("You are not logged in")
            return
        if email:
            self.current_user.email = email
        if skill_level:
            self.current_user.skill_level = skill_level
        self.persistence.update_user(self.current_user)

    def _list_exercises(self, difficulty):
        """List exercises."""
        if difficulty:
            exercises = self.persistence.get_exercises_by_difficulty(difficulty)
            click.echo(f"Exercises with difficulty '{difficulty}':")
        else:
            exercises = self.persistence.get_all(Exercise)
            click.echo("All exercises:")
        for exercise in exercises:
            click.echo(f"ID: {exercise.exercise_id}, Name: {exercise.name}, Difficulty: {exercise.difficulty}")

    def _show_exercise(self, exercise_id):
        """Show exercise details."""
        exercise = self.persistence.get_exercise_by_exercise_id(exercise_id)
        if not exercise:
            click.echo(f"Exercise {exercise_id} not found")
            return
        click.echo(f"Exercise: {exercise.name}")
        click.echo(f"ID: {exercise.exercise_id}")
        click.echo(f"Difficulty: {exercise.difficulty}")
        click.echo(f"Description: {exercise.description}")

    def _start_exercise(self, exercise_id):
        """Start an exercise."""
        if not self.current_user:
            click.echo("You are not logged in")
            return
        exercise = self.persistence.get_exercise_by_exercise_id(exercise_id)
        if not exercise:
            click.echo(f"Exercise {exercise_id} not found")
            return
        progress = self.persistence.start_exercise(self.current_user.id, exercise.id)
        if progress:
            click.echo(f"Exercise {exercise.name} started successfully")
            self.current_exercise = exercise

    def _complete_exercise(self, exercise_id, score):
        """Complete an exercise."""
        if not self.current_user:
            click.echo("You are not logged in")
            return
        exercise = self.persistence.get_exercise_by_exercise_id(exercise_id)
        if not exercise:
            click.echo(f"Exercise {exercise_id} not found")
            return
        progress = self.persistence.complete_exercise(self.current_user.id, exercise.id, score)
        if progress:
            click.echo(f"Exercise {exercise.name} completed successfully")

    def _show_progress(self):
        """Show progress."""
        if not self.current_user:
            click.echo("You are not logged in")
            return
        progress_records = self.persistence.get_user_progress(self.current_user.id)
        if not progress_records:
            click.echo("No progress records found")
            return
        click.echo(f"Progress for user '{self.current_user.username}':")
        for progress in progress_records:
            exercise = self.persistence.get_exercise(progress.exercise_id)
            if not exercise:
                continue
            click.echo(f"Exercise: {exercise.name}")
            click.echo(f"  Status: {progress.status.replace('_', ' ').title()}")
            click.echo(f"  Started: {progress.created_at}")
            if progress.completed_at:
                click.echo(f"  Completed: {progress.completed_at}")
            if progress.score is not None:
                click.echo(f"  Score: {progress.score:.2f}")
            if progress.attempts:
                click.echo(f"  Attempts: {progress.attempts}")
            if progress.time_spent:
                click.echo(f"  Time Spent: {progress.time_spent} seconds")

    def _show_statistics(self):
        """Show statistics."""
        if not self.current_user:
            click.echo("You are not logged in")
            return
        stats = self.persistence.get_user_statistics(self.current_user.id)
        if not stats:
            click.echo("No statistics available")
            return
        click.echo(f"Statistics for user '{stats['username']}':")
        click.echo(f"Skill Level: {stats['skill_level']}")
        click.echo(f"Completed Exercises: {stats['completed_count']}")
        click.echo(f"In Progress Exercises: {stats['in_progress_count']}")
        click.echo(f"Failed Exercises: {stats['failed_count']}")
        if stats['total_time']:
            click.echo(f"Total Time Spent: {stats['total_time']} seconds")
        if stats['avg_score']:
            click.echo(f"Average Score: {stats['avg_score']:.2f}")
        click.echo("\nCompleted by Difficulty:")
        click.echo(f"  Beginner: {stats['beginner_completed']}")
        click.echo(f"  Intermediate: {stats['intermediate_completed']}")
        click.echo(f"  Advanced: {stats['advanced_completed']}")

    def _export_data(self, file):
        """Export user data."""
        if not self.current_user:
            click.echo("You are not logged in")
            return
        data = self.persistence.export_user_data(self.current_user.id)
        if not data:
            click.echo("No data to export")
            return
        if file:
            file_path = file
        else:
            file_path = f"{self.current_user.username}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        click.echo(f"Data exported to {file_path}")

    def _import_data(self, file):
        """Import user data."""
        if not os.path.exists(file):
            click.echo(f"File {file} not found")
            return
        try:
            with open(file, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            click.echo(f"Invalid JSON in file {file}")
            return
        user = self.persistence.import_user_data(data)
        if user:
            click.echo(f"Data imported for user {user.username}")
            self.current_user = user

    def parse_command(self, command_str: str = None) -> Dict[str, Any]:
        """
        Parse the command string into command and arguments.
        
        Args:
            command_str (str, optional): The command string entered by the user. If None, sys.argv is used.
        
        Returns:
            Dict[str, Any]: Parsed command and arguments.
        """
        import click
        from click.testing import CliRunner
        
        runner = CliRunner()
        result = runner.invoke(cli, command_str.split() if command_str else None)
        
        return {
            'command': result.command,
            'args': result.args,
            'output': result.output
        }

if __name__ == "__main__":
    cli()
