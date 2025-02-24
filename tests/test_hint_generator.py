import unittest
from src.feedback.hint_generator import (
    ProgressiveHintGenerator,
    HintContext,
    HintLevel
)


class TestHintGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ProgressiveHintGenerator()

    def test_generate_hints(self):
        context = HintContext(
            skill_level="beginner",
            attempts=1,
            command="add",
            error_type="no_files"
        )
        hints = self.generator.generate_hints(context)
        self.assertIsInstance(hints, list)
        self.assertTrue(len(hints) > 0)

    def test_hint_level_progression(self):
        self.assertEqual(
            self.generator.get_hint_level(1),
            HintLevel.BASIC
        )
        self.assertEqual(
            self.generator.get_hint_level(2),
            HintLevel.DETAILED
        )
        self.assertEqual(
            self.generator.get_hint_level(3),
            HintLevel.SPECIFIC
        )
        self.assertEqual(
            self.generator.get_hint_level(4),
            HintLevel.EXAMPLE
        )

    def test_invalid_error_type(self):
        context = HintContext(
            skill_level="beginner",
            attempts=1,
            command="unknown",
            error_type="invalid_type"
        )
        hints = self.generator.generate_hints(context)
        self.assertEqual(hints, ["No hints available for this error"])


def test_hint_generation():
    generator = ProgressiveHintGenerator()
    context = HintContext(
        skill_level="beginner",
        attempts=1,
        command="init",
        error_type="missing_args"
    )
    hints = generator.generate_hints(context)
    assert len(hints) == 1
    assert "required arguments" in hints[0].lower()


def test_progressive_hints():
    generator = ProgressiveHintGenerator()
    context = HintContext(
        skill_level="beginner",
        attempts=1,
        command="add",
        error_type="no_files"
    )
    first_hint = generator.generate_hints(context)
    assert len(first_hint) == 1

    context.attempts = 2
    second_hint = generator.generate_hints(context)
    assert len(second_hint) == 2


if __name__ == "__main__":
    unittest.main()
