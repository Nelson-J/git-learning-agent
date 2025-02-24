import unittest
from src.feedback.hint_generator import (
    ProgressiveHintGenerator,
    HintContext,
    HintLevel,
    HintGenerator
)


def test_hint():
    pass


def another_test():
    pass


class TestHintGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ProgressiveHintGenerator()
        self.context = HintContext(
            skill_level="beginner",
            attempts=1,
            command="init",
            error_type="init",
            previous_hints=[]
        )

    def test_generate_hints(self):
        hints = self.generator.generate_hints("init", self.context)
        self.assertIn("Use 'git init' to create a repository", hints)

    def test_hint_level_progression(self):
        self.context.attempts = 2
        hints = self.generator.generate_hints("init", self.context)
        self.assertIn("Consider adding a .gitignore file", hints)

    def test_invalid_error_type(self):
        hints = self.generator.generate_hints("invalid_error", self.context)
        self.assertIn("No specific hints available for this error.", hints)


def test_hint_generation():
    generator = HintGenerator()
    context = HintContext(skill_level="beginner", attempts=1, command="init", error_type="missing_args")
    hints = generator.generate_hints("init_error", context)
    assert len(hints) > 0


def test_progressive_hints():
    generator = HintGenerator()
    context = HintContext(skill_level="beginner", attempts=1, command="add", error_type="no_files")
    hints = generator.generate_hints("add_error", context)
    assert len(hints) > 0


if __name__ == "__main__":
    unittest.main()
