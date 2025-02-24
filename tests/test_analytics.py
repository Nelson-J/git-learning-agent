import unittest
import numpy as np
from src.education.analytics import LearningAnalytics

class TestLearningAnalytics(unittest.TestCase):
    def setUp(self):
        self.analytics = LearningAnalytics()
        self.user_id = "test_user"

    def test_skill_matrix_calculation(self):
        performance_data = {
            "basic": 0.8,
            "intermediate": 0.6,
            "advanced": 0.4
        }
        matrix = self.analytics.calculate_skill_matrix(self.user_id, performance_data)
        self.assertEqual(matrix.shape, (3, 3))
        self.assertTrue(isinstance(matrix, np.ndarray))

    def test_learning_velocity_calculation(self):
        recent_scores = [0.5, 0.6, 0.7, 0.8, 0.85]
        velocity = self.analytics.calculate_learning_velocity(self.user_id, recent_scores)
        self.assertGreater(velocity, 0)

    def test_performance_prediction(self):
        prediction = self.analytics.predict_performance(self.user_id, 0.7)
        self.assertGreaterEqual(prediction, 0.0)
        self.assertLessEqual(prediction, 1.0)

    def test_retention_visualization(self):
        retention_data = {
            "2023-01-01": 0.9,
            "2023-01-02": 0.85,
            "2023-01-03": 0.82
        }
        visualization = self.analytics.visualize_retention(self.user_id, retention_data)
        self.assertIn("labels", visualization)
        self.assertIn("values", visualization)
        self.assertIn("trend", visualization)
        self.assertEqual(len(visualization["labels"]), 3)

if __name__ == '__main__':
    unittest.main()
