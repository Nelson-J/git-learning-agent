from dataclasses import dataclass
from typing import List, Dict, Optional
from .models import Exercise, GitCommand, ComplexScenario
from collections import defaultdict

@dataclass
class LearningPath:
    name: str
    description: str
    difficulty: str
    prerequisites: List[str]
    exercises: List[Exercise]
    completion_criteria: Dict[str, int]


class BeginnerPaths:
    @staticmethod
    def create_basic_workflow_path() -> LearningPath:
        return LearningPath(
            name="basic_git_workflow",
            description="Learn the fundamental Git workflow with init, add, and commit",
            difficulty="beginner",
            prerequisites=[],
            exercises=[
                Exercise(
                    exercise_id="init_repo",
                    name="Initialize your first Git repository",
                    description="Learn how to initialize a Git repository",
                    difficulty="beginner",
                    commands=[GitCommand(
                        name="init",
                        args=[],
                        expected_output="Initialized empty Git repository",
                        validation_rules={"status": "success"}
                    )]
                ),
                Exercise(
                    exercise_id="first_commit",
                    name="Make your first commit",
                    description="Learn how to commit changes",
                    difficulty="beginner",
                    commands=[
                        GitCommand(
                            name="add",
                            args=["."],
                            expected_output="",
                            validation_rules={"status": "success"}
                        ),
                        GitCommand(
                            name="commit",
                            args=["-m", "Initial commit"],
                            expected_output="",
                            validation_rules={"status": "success"}
                        )
                    ]
                ),
                Exercise(
                    exercise_id="view_history",
                    name="View your commit history",
                    description="Learn how to view commit history",
                    difficulty="beginner",
                    commands=[GitCommand(
                        name="log",
                        args=[],
                        expected_output="commit",
                        validation_rules={"status": "success"}
                    )]
                ),
            ],
            completion_criteria={"exercises_completed": 3},
        )

    @staticmethod
    def create_branching_basics_path() -> LearningPath:
        return LearningPath(
            name="branching_basics",
            description="Learn how to work with branches in Git",
            difficulty="beginner",
            prerequisites=["basic_git_workflow"],
            exercises=[
                Exercise(
                    exercise_id="create_branch",
                    name="Create your first branch",
                    description="Learn to create a new branch",
                    difficulty="beginner",
                    commands=[
                        GitCommand(
                            name="branch",
                            args=["feature"],
                            expected_output="",
                            validation_rules={"status": "success"}
                        ),
                        GitCommand(
                            name="checkout",
                            args=["feature"],
                            expected_output="Switched to branch 'feature'",
                            validation_rules={"status": "success"}
                        )
                    ]
                ),
                Exercise(
                    exercise_id="switch_branch",
                    name="Switch between branches",
                    description="Learn to switch branches",
                    difficulty="beginner",
                    commands=[
                        GitCommand(
                            name="checkout",
                            args=["main"],
                            expected_output="Switched to branch 'main'",
                            validation_rules={"status": "success"}
                        ),
                        GitCommand(
                            name="checkout",
                            args=["feature"],
                            expected_output="Switched to branch 'feature'",
                            validation_rules={"status": "success"}
                        )
                    ]
                ),
                Exercise(
                    exercise_id="merge_branch",
                    name="Merge your first branch",
                    description="Learn to merge branches",
                    difficulty="beginner",
                    commands=[
                        GitCommand(
                            name="checkout",
                            args=["main"],
                            expected_output="Switched to branch 'main'",
                            validation_rules={"status": "success"}
                        ),
                        GitCommand(
                            name="merge",
                            args=["feature"],
                            expected_output="Fast-forward",
                            validation_rules={"status": "success"}
                        )
                    ]
                ),
            ],
            completion_criteria={"exercises_completed": 3},
        )


class IntermediatePaths:
    @staticmethod
    def create_intermediate_workflow_path() -> LearningPath:
        return LearningPath(
            name="intermediate_git_workflow",
            description="Learn the intermediate Git workflow with rebase and merge",
            difficulty="intermediate",
            prerequisites=["branching_basics"],
            exercises=[
                Exercise(
                    exercise_id="rebase_workflow",
                    name="Rebase workflow exercise",
                    description="Practice interactive rebasing",
                    difficulty="intermediate",
                    commands=[
                        GitCommand(
                            name="rebase",
                            args=["-i", "HEAD~3"],
                            expected_output="Successfully rebased",
                            validation_rules={"status": "success"}
                        )
                    ],
                    complex_scenario=ComplexScenario(
                        name="rebase_conflict",
                        setup_commands=[
                            GitCommand("commit", ["-m", "Commit 1"], "", {}),
                            GitCommand("commit", ["-m", "Commit 2"], "", {})
                        ],
                        expected_resolution=[
                            GitCommand("rebase", ["--continue"], "", {})
                        ]
                    )
                ),
            ],
            completion_criteria={"exercises_completed": 1},
        )


class PathManager:
    def __init__(self):
        self.paths: Dict[str, LearningPath] = {}
        self.path_progress = defaultdict(list)
        self._initialize_paths()

    def _initialize_paths(self):
        beginner = BeginnerPaths()
        intermediate = IntermediatePaths()
        paths = [
            beginner.create_basic_workflow_path(),
            beginner.create_branching_basics_path(),
            intermediate.create_intermediate_workflow_path(),
        ]
        for path in paths:
            self.add_path(path.name, path)

    def add_path(self, path_name: str, path: LearningPath):
        self.paths[path_name] = path
        self.path_progress[path_name] = []  # Explicit initialization

    def get_path(self, name: str) -> Optional[LearningPath]:
        return self.paths.get(name)

    def get_available_paths(self, completed_paths: List[str]) -> List[LearningPath]:
        return [
            path
            for path in self.paths.values()
            if all(prereq in completed_paths for prereq in path.prerequisites)
        ]

    def start_path(self, path_name: str) -> bool:
        if path_name not in self.paths:
            return False
        if path_name not in self.path_progress:
            self.path_progress[path_name] = []
        return True

    def complete_exercise(self, path_name: str, exercise_name: str) -> bool:
        if path_name not in self.paths:
            return False
        if path_name not in self.path_progress:
            self.path_progress[path_name] = []
        if exercise_name not in self.path_progress[path_name]:
            self.path_progress[path_name].append(exercise_name)
            return True
        return False

    def is_path_completed(self, path_name: str) -> bool:
        if path_name not in self.paths or path_name not in self.path_progress:
            return False
        path = self.paths[path_name]
        completed = len(self.path_progress[path_name])
        required = path.completion_criteria.get("exercises_completed", 0)
        return completed >= required

    def is_exercise_completed(self, path_name: str, exercise_name: str) -> bool:
        return (
            path_name in self.path_progress
            and exercise_name in self.path_progress[path_name]
        )

    def get_exercise_progress(self, path_name: str) -> List[str]:
        return self.path_progress.get(path_name, [])


def learning_paths_function():
    # Learning paths code
    pass


# Additional code
