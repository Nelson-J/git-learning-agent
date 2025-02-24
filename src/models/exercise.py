from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class GitCommand:
    name: str
    args: List[str]
    expected_output: str
    validation_rules: Dict[str, str]


@dataclass
class Exercise:
    name: str
    description: str
    difficulty: str
    exercise_id: str = field(default="")
    commands: List[GitCommand] = field(default_factory=list)

    def add_command(self, command: GitCommand) -> None:
        """Add a command to the exercise."""
        self.commands.append(command)

    def validate_sequence(self, commands: List[GitCommand]) -> bool:
        """Validate a sequence of commands against the exercise."""
        if len(commands) != len(self.commands):
            return False
        return all(
            c1.name == c2.name and c1.args == c2.args
            for c1, c2 in zip(commands, self.commands)
        )
