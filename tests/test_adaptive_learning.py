import unittest
from src.education.adaptive_learning import AdaptiveLearning

class TestAdaptiveLearning(unittest.TestCase):
    def setUp(self):
        self.adaptive = AdaptiveLearning()

    def test_knowledge_space_update(self):
        self.knowledge_space.update_mastery("init", 0.8)
        node = self.knowledge_space._knowledge_graph["init"]
        self.assertGreater(node.mastery_level, 0)
        self.assertIsNotNone(node.last_practiced)

    def test_skill_matrix_calculation(self):
        performance = {"init": 0.8, "add": 0.7}
        skill_vector = self.skill_matrix.calculate_skill_vector(performance)
        self.assertEqual(len(skill_vector), 3)  # Three skill dimensions
        self.assertTrue(all(0 <= score <= 1 for score in skill_vector))

    def test_learning_pattern_recognition(self):
        # Add some learning events
        events = [
            {"init": 0.5, "add": 0.4},
            {"init": 0.6, "add": 0.5},
            {"init": 0.7, "add": 0.6},
        ]

        for event in events:
            self.pattern_recognizer.add_learning_event(event)

        patterns = self.pattern_recognizer.identify_patterns()

        self.assertIn("learning_rate", patterns)
        self.assertIn("struggle_areas", patterns)
        self.assertIn("mastery_concepts", patterns)
        self.assertGreater(patterns["learning_rate"], 0)

    def test_skill_level_progression(self):
        # Test progression through skill levels
        performance = {"init": 0.9, "add": 0.85, "commit": 0.8}

        skill_vector = self.skill_matrix.calculate_skill_vector(performance)
        self.assertTrue(all(score > 0.7 for score in skill_vector))


if __name__ == "__main__":
    unittest.main()
