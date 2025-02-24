import unittest
from src.education.adaptive_learning import (
    KnowledgeSpace,
    SkillMatrix,
    LearningPatternRecognizer,
    AdaptiveLearning
)

class TestAdaptiveLearning(unittest.TestCase):
    def setUp(self):
        self.adaptive_learning = AdaptiveLearning()
        self.knowledge_space = KnowledgeSpace()
        self.skill_matrix = SkillMatrix(self.knowledge_space)
        self.pattern_recognizer = LearningPatternRecognizer()

    def test_knowledge_space_update(self):
        self.knowledge_space.update_mastery("init", 0.8)
        node = self.knowledge_space._knowledge_graph.get("init")
        self.assertIsNotNone(node)
        self.assertAlmostEqual(node.mastery_level, 0.08)

    def test_skill_matrix_calculation(self):
        performance = {"init": 0.8, "add": 0.7}
        skill_vector = self.skill_matrix.calculate_skill_vector(performance)
        self.assertEqual(len(skill_vector), 3)  # Three skill dimensions

    def test_learning_pattern_recognition(self):
        events = [
            {"init": 0.5, "add": 0.4},
            {"init": 0.6, "add": 0.5},
            {"init": 0.7, "add": 0.6},
        ]
        for event in events:
            self.pattern_recognizer.add_learning_event(event)
        patterns = self.pattern_recognizer.identify_patterns()
        self.assertIn("learning_rate", patterns)

    def test_skill_level_progression(self):
        performance = {"init": 0.9, "add": 0.85, "commit": 0.8}
        skill_vector = self.skill_matrix.calculate_skill_vector(performance)
        self.assertGreater(skill_vector[0], 0.8)


if __name__ == "__main__":
    unittest.main()
