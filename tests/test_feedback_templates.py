import unittest
from src.feedback import FeedbackTemplate, ErrorCategory
from src.feedback_templates import GitFeedbackTemplates


class TestGitFeedbackTemplates(unittest.TestCase):
    def setUp(self):
        self.templates = GitFeedbackTemplates.get_all_templates()

    def test_template_structure(self):
        """Test that all templates have required attributes."""
        for name, template in self.templates.items():
            self.assertIsInstance(template, FeedbackTemplate)
            self.assertIsInstance(template.error_type, str)
            self.assertIsInstance(template.category, ErrorCategory)
            self.assertIsInstance(template.message_template, str)
            self.assertIsInstance(template.hints, list)

    def test_merge_conflict_template(self):
        """Test specific merge conflict template."""
        template = self.templates.get("merge_conflict")
        self.assertIsNotNone(template)
        self.assertEqual(template.category, ErrorCategory.WORKFLOW)
        self.assertIn("conflict", template.message_template.lower())

    def test_template_hints(self):
        """Test that templates provide helpful hints."""
        for template in self.templates.values():
            if template.hints:  # Some templates might not need hints
                self.assertGreater(len(template.hints), 0)
                self.assertTrue(all(isinstance(hint, str) for hint in template.hints))


if __name__ == "__main__":
    unittest.main()
