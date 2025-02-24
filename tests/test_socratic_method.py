import unittest
from src.education.socratic_method import (
    SocraticDialogue,
    DialogueManager,
    QuestionType,
    Question,
)


class TestSocraticMethod(unittest.TestCase):
    def setUp(self):
        self.dialogue = SocraticDialogue()
        self.manager = DialogueManager()

    def test_question_selection(self):
        question = self.dialogue.select_question("git_basics", "beginner")
        self.assertIsNotNone(question)
        self.assertEqual(question.difficulty, "beginner")
        self.assertEqual(question.topic, "git_basics")

    def test_response_evaluation(self):
        question = Question(
            id="test_1",
            text="What is git?",
            type=QuestionType.CONCEPTUAL,
            topic="git_basics",
            difficulty="beginner",
            follow_ups=["How does it work?"],
            expected_concepts=["version control", "repository"],
        )

        # Test exact match response
        response = "Git is a version control system that manages repositories"
        score = self.dialogue.evaluate_response(question, response)
        self.assertGreaterEqual(
            score,
            0.7,
            f"Expected score >= 0.7 for response containing all concepts. Got {score}",
        )

        # Test partial match
        partial_response = "Git helps control versions"
        partial_score = self.dialogue.evaluate_response(question, partial_response)
        self.assertLess(
            partial_score,
            0.7,
            f"Expected score < 0.7 for partial response. Got {partial_score}",
        )

    def test_dialogue_flow(self):
        question_text = self.manager.start_dialogue("git_basics", "beginner")
        self.assertIsNotNone(question_text)

        result = self.manager.process_response(
            "Git init creates a new repository with a .git folder"
        )
        self.assertIn("score", result)
        self.assertIsInstance(result["score"], float)

    def test_follow_up_questions(self):
        question = Question(
            id="test_2",
            text="What is git init?",
            type=QuestionType.PRACTICAL,
            topic="git_basics",
            difficulty="beginner",
            follow_ups=["What does it create?"],
            expected_concepts=["repository", "initialization"],
        )

        follow_up = self.dialogue.get_follow_up(question, 0.5)
        self.assertIsNotNone(follow_up)


if __name__ == "__main__":
    unittest.main()
