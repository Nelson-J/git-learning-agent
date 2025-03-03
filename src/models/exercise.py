from dataclasses import dataclass, field
from typing import List, Dict, Optional


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


@dataclass
class Exercise:
    name: str
    description: str
    difficulty: str
    exercise_id: str = field(default="")
    commands: List[GitCommand] = field(default_factory=list)
    complex_scenario: Optional[ComplexScenario] = None

    def add_command(self, command: GitCommand) -> None:
        self.commands.append(command)

    def validate_sequence(self, commands: List[GitCommand]) -> bool:
        if len(commands) != len(self.commands):
            return False
        return all(
            c1.name == c2.name and c1.args == c2.args
            for c1, c2 in zip(commands, self.commands)
        )

    def is_advanced_exercise(self) -> bool:
        advanced_commands = {"rebase", "config", "cherry-pick", "bisect"}
        return any(cmd.name in advanced_commands for cmd in self.commands)

    def setup_complex_scenario(self) -> bool:
        if not self.complex_scenario:
            return False
        return all(
            cmd.validate_advanced_command()
            for cmd in self.complex_scenario.setup_commands
        )

    def validate_scenario_resolution(self, commands: List[GitCommand]) -> bool:
        if not self.complex_scenario:
            return False
        return all(
            c1.name == c2.name and c1.args == c2.args
            for c1, c2 in zip(commands, self.complex_scenario.expected_resolution)
        )


def exercise_function():
    # Exercise code
    pass


# Additional code
