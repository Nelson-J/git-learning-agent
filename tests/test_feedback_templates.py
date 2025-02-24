import unittest
from src.feedback_templates import GitFeedbackTemplates, ContextualHintGenerator

class TestFeedbackTemplates(unittest.TestCase):
    def setUp(self):
        self.templates = GitFeedbackTemplates.get_all_templates()
        self.hint_generator = ContextualHintGenerator()

    def test_merge_conflict_template(self):
        template = self.templates["merge_conflict"]
        feedback = template.message_template.format(files="example.txt")
        self.assertIn("Merge conflict detected in example.txt", feedback)
        self.assertTrue(len(template.hints) >= 3)
        self.assertIn("resolve", template.examples)

    def test_progressive_hints(self):
        hints = self.hint_generator.generate_progressive_hints(
            "merge_conflict", "beginner", 1
        )
        self.assertEqual(len(hints), 1)
        
        hints = self.hint_generator.generate_progressive_hints(
            "merge_conflict", "intermediate", 2
        )
        self.assertEqual(len(hints), 2)
        self.assertNotIn("Basic:", hints[0])

    def test_skill_level_appropriate_hints(self):
        # Test beginner hints
        beginner_hints = self.hint_generator.generate_progressive_hints(
            "detached_head", "beginner", 1
        )
        self.assertIn("Basic:", beginner_hints[0])

        # Test advanced hints
        advanced_hints = self.hint_generator.generate_progressive_hints(
            "detached_head", "advanced", 1
        )
        self.assertIn("Advanced:", advanced_hints[0])

if __name__ == '__main__':
    unittest.main()
