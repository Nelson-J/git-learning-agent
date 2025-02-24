from dataclasses import dataclass
from typing import List, Dict, Optional
from .models import Exercise

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
                Exercise("init_repo", "Initialize your first Git repository", "beginner"),
                Exercise("first_commit", "Make your first commit", "beginner"),
                Exercise("view_history", "View your commit history", "beginner")
            ],
            completion_criteria={"exercises_completed": 3}
        )

    @staticmethod
    def create_branching_basics_path() -> LearningPath:
        return LearningPath(
            name="branching_basics",
            description="Learn how to work with branches in Git",
            difficulty="beginner",
            prerequisites=["basic_git_workflow"],
            exercises=[
                Exercise("create_branch", "Create your first branch", "beginner"),
                Exercise("switch_branch", "Switch between branches", "beginner"),
                Exercise("merge_branch", "Merge your first branch", "beginner")
            ],
            completion_criteria={"exercises_completed": 3}
        )

class PathManager:
    def __init__(self):
        self.paths: Dict[str, LearningPath] = {}
        self.path_progress: Dict[str, List[str]] = {}
        self._initialize_paths()

    def _initialize_paths(self):
        beginner = BeginnerPaths()
        paths = [
            beginner.create_basic_workflow_path(),
            beginner.create_branching_basics_path()
        ]
        for path in paths:
            self.paths[path.name] = path

    def get_path(self, name: str) -> Optional[LearningPath]:
        return self.paths.get(name)

    def get_available_paths(self, completed_paths: List[str]) -> List['LearningPath']:
        return [
            path for path in self.paths.values()
            if all(prereq in completed_paths for prereq in path.prerequisites)
        ]

    def start_path(self, path_name: str) -> bool:
        """Start tracking progress for a path."""
        if path_name not in self.paths:
            return False
        if path_name not in self.path_progress:
            self.path_progress[path_name] = []
        return True

    def complete_exercise(self, path_name: str, exercise_name: str) -> bool:
        """Mark an exercise as completed in a path."""
        if path_name not in self.paths:
            return False
            
        # Initialize progress tracking for path if not exists
        if path_name not in self.path_progress:
            self.path_progress[path_name] = []
            
        if exercise_name not in self.path_progress[path_name]:
            self.path_progress[path_name].append(exercise_name)
            return True
        return False

    def is_path_completed(self, path_name: str) -> bool:
        """Check if a path is completed based on its criteria."""
        if path_name not in self.paths or path_name not in self.path_progress:
            return False
        path = self.paths[path_name]
        completed = len(self.path_progress[path_name])
        required = path.completion_criteria.get('exercises_completed', 0)
        return completed >= required

    def is_exercise_completed(self, path_name: str, exercise_name: str) -> bool:
        """Check if a specific exercise in a path is completed."""
        return (path_name in self.path_progress and 
                exercise_name in self.path_progress[path_name])

    def get_exercise_progress(self, path_name: str) -> List[str]:
        """Get list of completed exercises for a path."""
        return self.path_progress.get(path_name, [])
