import pytest
from src.progress_visualization import ProgressVisualizer
from src.learning_paths import PathManager, LearningPath

class TestProgressVisualization:
    @pytest.fixture
    def path_manager(self):
        manager = PathManager()
        manager.add_path('basic_git_workflow', LearningPath(
            name='Basic Git Workflow',
            description='Learn the fundamental Git workflow with init, add, and commit',
            difficulty='beginner',
            prerequisites=[],
            exercises=[],
            completion_criteria={'exercises_completed': 5}
        ))
        manager.path_progress['basic_git_workflow'].extend([True, True, False])
        return manager

    def test_initialization(self, path_manager):
        visualizer = ProgressVisualizer(path_manager)
        assert visualizer is not None

    def test_skill_graph_generation(self, path_manager):
        visualizer = ProgressVisualizer(path_manager)
        visualizer.generate_visualizations()
        # Add actual assertions based on output
