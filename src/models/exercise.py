"""
Exercise model for the Git Learning System.

This module defines the SQLAlchemy model for exercises,
including commands, validation rules, and complex scenarios.
"""

import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from sqlalchemy import Column, String, JSON, Integer
from sqlalchemy.orm import relationship

from src.database.init_db import Base


@dataclass
class GitCommand:
    name: str
    args: List[str]
    expected_output: str
    validation_rules: Dict[str, str]

    def validate_advanced_command(self) -> bool:
        if self.name == "rebase":
            return (
                "--continue" in self.args
                or "--abort" in self.args
                or len(self.args) == 1
            )
        elif self.name == "config":
            return len(self.args) >= 2 and self.args[0].startswith("hook.")
        return True


@dataclass
class ComplexScenario:
    name: str
    setup_commands: List[GitCommand]
    expected_resolution: List[GitCommand]
    conflict_files: Dict[str, List[str]] = field(default_factory=dict)


class Exercise(Base):
    """
    SQLAlchemy model for exercises in the Git Learning System.
    
    Attributes:
        id (str): Unique identifier for the exercise
        name (str): Name of the exercise
        description (str): Description of the exercise
        difficulty (str): Difficulty level (beginner, intermediate, advanced)
        commands (JSON): List of Git commands in the exercise
        complex_scenario (JSON): Complex scenario data if applicable
        tags (JSON): Tags for categorizing the exercise
        skills (JSON): Skills practiced in this exercise
    """
    __tablename__ = "exercises"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    exercise_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    difficulty = Column(String(20), nullable=False)
    commands_data = Column(JSON, default=list)
    complex_scenario_data = Column(JSON, nullable=True)
    tags = Column(JSON, default=list)
    skills = Column(JSON, default=list)
    order = Column(Integer, default=0)  # For ordering exercises in learning paths
    
    # Relationships
    progress = relationship("Progress", back_populates="exercise", cascade="all, delete-orphan")
    
    def __init__(
        self,
        name: str,
        description: str,
        difficulty: str,
        exercise_id: str = None,
        commands: List[GitCommand] = None,
        complex_scenario: Optional[ComplexScenario] = None,
        tags: List[str] = None,
        skills: List[str] = None,
        order: int = 0
    ):
        """
        Initialize a new exercise.
        
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
        """
        self.id = str(uuid.uuid4())
        self.exercise_id = exercise_id or self.id
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.commands_data = self._serialize_commands(commands or [])
        self.complex_scenario_data = self._serialize_complex_scenario(complex_scenario)
        self.tags = tags or []
        self.skills = skills or []
        self.order = order
    
    @property
    def commands(self) -> List[GitCommand]:
        """
        Get the list of Git commands for this exercise.
        
        Returns:
            List[GitCommand]: List of Git commands
        """
        return self._deserialize_commands(self.commands_data)
    
    @commands.setter
    def commands(self, commands: List[GitCommand]):
        """
        Set the list of Git commands for this exercise.
        
        Args:
            commands (List[GitCommand]): List of Git commands
        """
        self.commands_data = self._serialize_commands(commands)
    
    @property
    def complex_scenario(self) -> Optional[ComplexScenario]:
        """
        Get the complex scenario for this exercise.
        
        Returns:
            Optional[ComplexScenario]: Complex scenario or None
        """
        return self._deserialize_complex_scenario(self.complex_scenario_data)
    
    @complex_scenario.setter
    def complex_scenario(self, scenario: Optional[ComplexScenario]):
        """
        Set the complex scenario for this exercise.
        
        Args:
            scenario (Optional[ComplexScenario]): Complex scenario or None
        """
        self.complex_scenario_data = self._serialize_complex_scenario(scenario)
    
    def add_command(self, command: GitCommand) -> None:
        """
        Add a Git command to this exercise.
        
        Args:
            command (GitCommand): Git command to add
        """
        commands = self.commands
        commands.append(command)
        self.commands = commands
    
    def validate_sequence(self, commands: List[GitCommand]) -> bool:
        """
        Validate a sequence of Git commands against this exercise.
        
        Args:
            commands (List[GitCommand]): Sequence of Git commands to validate
            
        Returns:
            bool: True if the sequence is valid, False otherwise
        """
        exercise_commands = self.commands
        if len(commands) != len(exercise_commands):
            return False
        return all(
            c1.name == c2.name and c1.args == c2.args
            for c1, c2 in zip(commands, exercise_commands)
        )
    
    def _serialize_commands(self, commands: List[GitCommand]) -> List[Dict]:
        """
        Serialize Git commands to JSON-compatible format.
        
        Args:
            commands (List[GitCommand]): List of Git commands
            
        Returns:
            List[Dict]: JSON-compatible representation of Git commands
        """
        return [
            {
                "name": cmd.name,
                "args": cmd.args,
                "expected_output": cmd.expected_output,
                "validation_rules": cmd.validation_rules
            }
            for cmd in commands
        ]
    
    def _deserialize_commands(self, data: List[Dict]) -> List[GitCommand]:
        """
        Deserialize Git commands from JSON-compatible format.
        
        Args:
            data (List[Dict]): JSON-compatible representation of Git commands
            
        Returns:
            List[GitCommand]: List of Git commands
        """
        return [
            GitCommand(
                name=cmd["name"],
                args=cmd["args"],
                expected_output=cmd["expected_output"],
                validation_rules=cmd["validation_rules"]
            )
            for cmd in data
        ]
    
    def _serialize_complex_scenario(self, scenario: Optional[ComplexScenario]) -> Optional[Dict]:
        """
        Serialize a complex scenario to JSON-compatible format.
        
        Args:
            scenario (Optional[ComplexScenario]): Complex scenario or None
            
        Returns:
            Optional[Dict]: JSON-compatible representation of the complex scenario
        """
        if scenario is None:
            return None
        
        return {
            "name": scenario.name,
            "setup_commands": self._serialize_commands(scenario.setup_commands),
            "expected_resolution": self._serialize_commands(scenario.expected_resolution),
            "conflict_files": scenario.conflict_files
        }
    
    def _deserialize_complex_scenario(self, data: Optional[Dict]) -> Optional[ComplexScenario]:
        """
        Deserialize a complex scenario from JSON-compatible format.
        
        Args:
            data (Optional[Dict]): JSON-compatible representation of the complex scenario
            
        Returns:
            Optional[ComplexScenario]: Complex scenario or None
        """
        if data is None:
            return None
        
        return ComplexScenario(
            name=data["name"],
            setup_commands=self._deserialize_commands(data["setup_commands"]),
            expected_resolution=self._deserialize_commands(data["expected_resolution"]),
            conflict_files=data["conflict_files"]
        )
    
    def to_dict(self) -> Dict:
        """
        Convert the exercise to a dictionary.
        
        Returns:
            Dict: Dictionary representation of the exercise
        """
        return {
            "id": self.id,
            "exercise_id": self.exercise_id,
            "name": self.name,
            "description": self.description,
            "difficulty": self.difficulty,
            "commands": self.commands_data,
            "complex_scenario": self.complex_scenario_data,
            "tags": self.tags,
            "skills": self.skills,
            "order": self.order
        }
    
    def __repr__(self):
        return f"<Exercise(name='{self.name}', difficulty='{self.difficulty}')>"


def exercise_function():
    # Exercise code
    pass


# Additional code
