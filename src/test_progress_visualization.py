import matplotlib.pyplot as plt
from progress_visualization import visualize_progress
from learning_paths import PathManager, LearningPath
from models import Exercise


def test_visualize_progress():
    # Create a mock PathManager instance
    path_manager = PathManager()

    # Mock data for testing
    basic_workflow_path = LearningPath(
        name="basic_git_workflow",
        description="Learn the fundamental Git workflow with init, add, and commit",
        difficulty="beginner",
        prerequisites=[],
        exercises=[],
        completion_criteria={"exercises_completed": 3},
    )

    branching_basics_path = LearningPath(
        name="branching_basics",
        description="Learn how to work with branches in Git",
        difficulty="beginner",
        prerequisites=["basic_git_workflow"],
        exercises=[],
        completion_criteria={"exercises_completed": 3},
    )

    path_manager.paths[basic_workflow_path.name] = basic_workflow_path
    path_manager.paths[branching_basics_path.name] = branching_basics_path

    # Simulate user progress
    path_manager.path_progress[basic_workflow_path.name] = ["init_repo", "first_commit"]
    path_manager.path_progress[branching_basics_path.name] = ["create_branch"]

    # Call the visualization function
    visualize_progress(path_manager)


if __name__ == "__main__":
    test_visualize_progress()
