from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum
import random


class QuestionType(Enum):
    CONCEPTUAL = "conceptual"
    PRACTICAL = "practical"
    REFLECTIVE = "reflective"
    ANALYTICAL = "analytical"


@dataclass
class Question:
    id: str
    text: str
    type: QuestionType
    topic: str
    difficulty: str
    follow_ups: List[str]
    expected_concepts: List[str]


class SocraticDialogue:
    def __init__(self):
        self._question_bank: Dict[str, Question] = {}
        self._initialize_question_bank()

    def _initialize_question_bank(self):
        self._question_bank = {
            "git_init_1": Question(
                id="git_init_1",
                text="What do you think happens when you run 'git init'?",
                type=QuestionType.CONCEPTUAL,
                topic="git_basics",
                difficulty="beginner",
                follow_ups=["What files does it create?", "Why is .git hidden?"],
                expected_concepts=["repository", "initialization", "version control"],
            ),
            "git_commit_1": Question(
                id="git_commit_1",
                text="How would you describe the difference between working directory and staging area?",
                type=QuestionType.ANALYTICAL,
                topic="git_basics",
                difficulty="beginner",
                follow_ups=["Why do we need a staging area?"],
                expected_concepts=["staging", "working directory", "git add"],
            ),
        }

    def select_question(
        self, topic: str, difficulty: str, previous_questions: List[str] = None
    ) -> Optional[Question]:
        if previous_questions is None:
            previous_questions = []

        eligible_questions = [
            q
            for q in self._question_bank.values()
            if q.topic == topic
            and q.difficulty == difficulty
            and q.id not in previous_questions
        ]

        return random.choice(eligible_questions) if eligible_questions else None

    def evaluate_response(self, question: Question, response: str) -> float:
        response_lower = response.lower()

        def check_word_match(concept: str) -> bool:
            # Clean up and normalize strings
            concept = concept.lower().strip()

            # Direct match check
            if concept in response_lower:
                return True

            # Handle plural/singular variations
            plural_forms = [
                f"{concept}s",  # Simple plural
                f"{concept}es",  # Complex plural
                f"{concept[:-1]}ies" if concept.endswith("y") else "",  # y -> ies
            ]

            singular_forms = [
                concept.rstrip("s"),  # Simple singular
                concept.rstrip("es"),  # Complex singular
                f"{concept.rstrip('ies')}y",  # ies -> y
            ]

            # Check all variations
            all_forms = [concept] + plural_forms + singular_forms
            return any(
                form in response_lower
                for form in all_forms
                if form  # Skip empty strings
            )

        # Count matched concepts
        matched_concepts = sum(
            1 for concept in question.expected_concepts if check_word_match(concept)
        )

        # Award points based on matches
        if matched_concepts == len(question.expected_concepts):
            score = 0.7  # Base passing score

            # Quality bonuses
            if len(response_lower.split()) >= 5:
                score += 0.15
            if any(word in response_lower for word in ["system", "manages", "using"]):
                score += 0.15

            return min(1.0, score)

        return 0.3

    def get_follow_up(self, question: Question, response_score: float) -> Optional[str]:
        if (
            response_score < 0.7 and question.follow_ups
        ):  # If score is low, provide follow-up
            return random.choice(question.follow_ups)
        return None


class DialogueManager:
    def __init__(self):
        self.socratic = SocraticDialogue()
        self.current_question: Optional[Question] = None
        self.previous_questions: List[str] = []
        self.current_context: Dict[str, Any] = {}

    def start_dialogue(self, topic: str, difficulty: str) -> Optional[str]:
        self.current_question = self.socratic.select_question(
            topic, difficulty, self.previous_questions
        )
        if self.current_question:
            self.previous_questions.append(self.current_question.id)
            return self.current_question.text
        return None

    def process_response(self, response: str) -> Dict[str, Any]:
        if not self.current_question:
            return {"error": "No active question"}

        score = self.socratic.evaluate_response(self.current_question, response)
        follow_up = self.socratic.get_follow_up(self.current_question, score)

        # Fixed: Using proper variable names and adding context
        response_analysis = self.analyze_response(
            self.current_question.id,
            response,
            self.current_context
        )

        return {
            "score": score,
            "follow_up": follow_up,
            "complete": score >= 0.7 and not follow_up,
            "analysis": response_analysis
        }

    def analyze_response(self, question_id: str, student_response: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze student response and provide detailed feedback."""
        return {
            "question_id": question_id,
            "response_length": len(student_response.split()),
            "key_concepts_found": [
                concept for concept in self.current_question.expected_concepts
                if concept.lower() in student_response.lower()
            ],
            "context": context
        }
