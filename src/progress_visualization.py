from .learning_paths import PathManager
from .education.analytics import LearningAnalytics
import matplotlib.pyplot as plt


class ProgressVisualizer:
    def __init__(self, path_manager: PathManager):
        self.path_manager = path_manager

    def generate_visualizations(self):
        """Public method to generate all visualizations"""
        visualize_progress(self.path_manager)


def visualize_progress(path_manager: PathManager):
    """Visualize user progress through learning paths."""

    analytics = LearningAnalytics()
    path_names = list(path_manager.paths.keys())

    completed_counts = [
        len(path_manager.path_progress.get(path_name, []))
        for path_name in path_names
    ]
    required_counts = [
        path.completion_criteria.get('exercises_completed', 0)
        for path in path_manager.paths.values()
    ]

    skill_matrices = [
        analytics.calculate_skill_matrix(user_id='user_1', performance_data={})
        for path_name in path_names
    ]
    skill_matrix = skill_matrices[0] if skill_matrices else None

    accuracy_scores = [
        analytics.calculate_accuracy_score(user_id='user_1', performance_data={})
        for path_name in path_names
    ]
    time_spent = [
        analytics.calculate_time_spent(user_id='user_1', performance_data={})
        for path_name in path_names
    ]

    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    index = range(len(path_names))

    plt.bar(index, completed_counts, bar_width, label='Completed Exercises')
    plt.bar(
        [i + bar_width for i in index], required_counts, bar_width,
        label='Required Exercises'
    )
    plt.xlabel('Learning Paths')
    plt.ylabel('Number of Exercises')
    plt.title('User Progress in Learning Paths')
    plt.xticks([i + bar_width / 2 for i in index], path_names)
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(index, accuracy_scores, marker='o')
    plt.xlabel('Learning Paths')
    plt.ylabel('Accuracy Score')
    plt.title('User Accuracy Scores in Learning Paths')
    plt.xticks(index, path_names)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.bar(index, time_spent)
    plt.xlabel('Learning Paths')
    plt.ylabel('Time Spent (minutes)')
    plt.title('User Time Spent in Learning Paths')
    plt.xticks(index, path_names)
    plt.tight_layout()
    plt.show()

    if skill_matrix is not None:
        plt.figure(figsize=(8, 6))
        plt.imshow(skill_matrix, cmap='hot', interpolation='nearest')
        plt.title('Skill Matrix Visualization')
        plt.colorbar()
        plt.show()


def progress_visualization_function():
    # Progress visualization code
    pass


# Additional code
