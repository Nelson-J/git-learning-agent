from typing import Dict, List, Set, Optional, Union, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import warnings
from ..models import UserProfile

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    warnings.warn("NumPy is not available. Using fallback implementation.")
    NUMPY_AVAILABLE = False


class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class KnowledgeNode:
    concept: str
    prerequisites: Set[str]
    difficulty: SkillLevel
    mastery_level: float = 0.0
    last_practiced: Optional[datetime] = None


class KnowledgeSpace:
    def __init__(self):
        self._knowledge_graph: Dict[str, KnowledgeNode] = {}
        self._initialize_git_knowledge_space()

    def _initialize_git_knowledge_space(self):
        self._knowledge_graph = {
            "init": KnowledgeNode(concept="git_init", prerequisites=set(), difficulty=SkillLevel.BEGINNER),
            "add": KnowledgeNode(concept="git_add", prerequisites={"git_init"}, difficulty=SkillLevel.BEGINNER),
            "commit": KnowledgeNode(concept="git_commit", prerequisites={"git_add"}, difficulty=SkillLevel.BEGINNER),
            "branch": KnowledgeNode(concept="git_branch", prerequisites={"git_commit"}, difficulty=SkillLevel.INTERMEDIATE),
            "merge": KnowledgeNode(concept="git_merge", prerequisites={"git_branch"}, difficulty=SkillLevel.INTERMEDIATE),
        }

    def update_mastery(self, concept: str, performance: float) -> None:
        if concept in self._knowledge_graph:
            node = self._knowledge_graph[concept]
            node.mastery_level = min(1.0, node.mastery_level + performance * 0.1)
            node.last_practiced = datetime.now()


class SkillMatrix:
    def __init__(self, knowledge_space: KnowledgeSpace):
        self.knowledge_space = knowledge_space
        self.skill_dimensions = ["concept_understanding", "practical_application", "problem_solving"]
        self._difficulty_weights = {SkillLevel.BEGINNER: 1.0, SkillLevel.INTERMEDIATE: 1.5, SkillLevel.ADVANCED: 2.0}

    def _get_difficulty_weight(self, difficulty: SkillLevel) -> float:
        return self._difficulty_weights.get(difficulty, 1.0)

    def calculate_skill_vector(self, user_performance: Dict[str, float]) -> Union[np.ndarray, List[float]]:
        if not user_performance:
            return np.zeros(len(self.skill_dimensions)) if NUMPY_AVAILABLE else [0.0] * len(self.skill_dimensions)

        if NUMPY_AVAILABLE:
            return self._calculate_with_numpy(user_performance)
        return self._calculate_without_numpy(user_performance)

    def _calculate_with_numpy(self, user_performance: Dict[str, float]) -> np.ndarray:
        skill_vector = np.zeros(len(self.skill_dimensions))
        total_weight = 0

        for concept, performance in user_performance.items():
            if concept in self.knowledge_space._knowledge_graph:
                node = self.knowledge_space._knowledge_graph[concept]
                weight = self._get_difficulty_weight(node.difficulty)
                total_weight += weight
                skill_vector += np.array([
                    performance * weight,
                    performance * weight,
                    performance * weight * 0.9
                ])

        return skill_vector / total_weight if total_weight > 0 else skill_vector

    def _calculate_without_numpy(self, user_performance: Dict[str, float]) -> List[float]:
        skill_vector = [0.0] * len(self.skill_dimensions)
        total_weight = 0

        for concept, performance in user_performance.items():
            if concept in self.knowledge_space._knowledge_graph:
                node = self.knowledge_space._knowledge_graph[concept]
                weight = self._get_difficulty_weight(node.difficulty)
                total_weight += weight
                skill_vector[0] += performance * weight
                skill_vector[1] += performance * weight
                skill_vector[2] += performance * weight * 0.9

        return [score / total_weight if total_weight > 0 else score for score in skill_vector]


class LearningPatternRecognizer:
    def __init__(self):
        self.pattern_history: List[Dict[str, float]] = []
        self.min_pattern_length = 3

    def add_learning_event(self, event: Dict[str, float]) -> None:
        self.pattern_history.append(event)

    def identify_patterns(self) -> Dict[str, any]:
        if len(self.pattern_history) < self.min_pattern_length:
            return {"status": "insufficient_data"}

        patterns = {
            "learning_rate": self._calculate_learning_rate(),
            "struggle_areas": self._identify_struggle_areas(),
            "mastery_concepts": self._identify_mastery_concepts(),
        }

        return patterns

    def _calculate_learning_rate(self) -> float:
        if not self.pattern_history:
            return 0.0

        performances = [sum(event.values()) / len(event) for event in self.pattern_history]

        improvements = [b - a for a, b in zip(performances[:-1], performances[1:])]

        return sum(improvements) / len(improvements) if improvements else 0.0

    def _identify_struggle_areas(self) -> List[str]:
        if not self.pattern_history:
            return []

        concept_performance = {}
        for event in self.pattern_history:
            for concept, score in event.items():
                if concept not in concept_performance:
                    concept_performance[concept] = []
                concept_performance[concept].append(score)

        struggle_areas = [
            concept
            for concept, scores in concept_performance.items()
            if sum(scores) / len(scores) < 0.6
        ]

        return struggle_areas

    def _identify_mastery_concepts(self) -> List[str]:
        if not self.pattern_history:
            return []

        concept_performance = {}
        for event in self.pattern_history:
            for concept, score in event.items():
                if concept not in concept_performance:
                    concept_performance[concept] = []
                concept_performance[concept].append(score)

        mastery_concepts = [
            concept
            for concept, scores in concept_performance.items()
            if sum(scores) / len(scores) > 0.85
        ]

        return mastery_concepts


class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class SkillMetrics:
    command_success_rate: float = 0.0
    average_completion_time: float = 0.0
    error_frequency: Dict[str, int] = None
    concepts_mastered: List[str] = None

    def __post_init__(self):
        self.error_frequency = self.error_frequency or {}
        self.concepts_mastered = self.concepts_mastered or []


class AdaptiveLearning:
    def __init__(self):
        self.current_difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
        self.skill_metrics: Dict[str, SkillMetrics] = {}
        self.threshold_to_advance: float = 0.8
        self.threshold_to_fallback: float = 0.4
        self.knowledge_space = KnowledgeSpace()
        self.skill_matrix = SkillMatrix(self.knowledge_space)
        self.pattern_recognizer = LearningPatternRecognizer()
        self._user_data = {}

    def initialize_user(self, user_profile: UserProfile) -> None:
        self._user_data[user_profile.user_id] = {
            "skill_level": user_profile.skill_level,
            "attempts": {},
            "metrics": {},
            "knowledge_space": {}
        }

    def get_user_level(self, user_id: str) -> str:
        return self._user_data.get(user_id, {}).get("skill_level", "beginner")

    def get_attempt_count(self, user_id: str) -> int:
        return len(self._user_data.get(user_id, {}).get("attempts", {}))

    def update_metrics(self, user_id: str, command: str, success: bool, time_taken: float) -> None:
        metrics = self.skill_metrics.setdefault(user_id, SkillMetrics())
        total_attempts = sum(metrics.error_frequency.values()) + 1

        # Calculate success rate
        if success:
            metrics.command_success_rate = (
                metrics.command_success_rate * (total_attempts - 1) + 1
            ) / total_attempts
        else:
            metrics.command_success_rate = (
                metrics.command_success_rate * (total_attempts - 1)
            ) / total_attempts
            metrics.error_frequency[command] = metrics.error_frequency.get(command, 0) + 1

        # Update completion time average
        metrics.average_completion_time = (
            metrics.average_completion_time * (total_attempts - 1) + time_taken
        ) / total_attempts

        if user_id in self._user_data:
            if "metrics" not in self._user_data[user_id]:
                self._user_data[user_id]["metrics"] = {}
            self._user_data[user_id]["metrics"][command] = {
                "success": success,
                "time_taken": time_taken
            }

    def adjust_difficulty(self, user_id: str) -> Optional[DifficultyLevel]:
        if user_id not in self.skill_metrics:
            return None

        metrics = self.skill_metrics[user_id]
        if (
            metrics.command_success_rate >= self.threshold_to_advance
            and self.current_difficulty != DifficultyLevel.ADVANCED
        ):
            if self.current_difficulty == DifficultyLevel.BEGINNER:
                self.current_difficulty = DifficultyLevel.INTERMEDIATE
            else:
                self.current_difficulty = DifficultyLevel.ADVANCED
            return self.current_difficulty

        if (
            metrics.command_success_rate <= self.threshold_to_fallback
            and self.current_difficulty != DifficultyLevel.BEGINNER
        ):
            if self.current_difficulty == DifficultyLevel.ADVANCED:
                self.current_difficulty = DifficultyLevel.INTERMEDIATE
            else:
                self.current_difficulty = DifficultyLevel.BEGINNER
            return self.current_difficulty

        return None

    def get_next_exercise(self, user_id: str) -> Dict[str, Any]:
        difficulty = self.get_user_level(user_id)
        metrics = self.skill_metrics.get(user_id, SkillMetrics())
        weak_areas = sorted(metrics.error_frequency.items(), key=lambda x: x[1], reverse=True)

        return {
            "difficulty": difficulty,
            "focus_areas": [cmd for cmd, _ in weak_areas[:3]],
            "recommended_practice": self._get_practice_recommendations(metrics)
        }

    def get_skill_vector(self, user_id: str) -> Dict[str, float]:
        if user_id not in self.skill_metrics:
            return {"git_basics": 0.0, "branching": 0.0, "collaboration": 0.0}

        metrics = self.skill_metrics[user_id]
        total_commands = sum(metrics.error_frequency.values())
        if total_commands == 0:
            return {"git_basics": 0.0, "branching": 0.0, "collaboration": 0.0}

        performance = {
            cmd: 1.0 - (count / total_commands) for cmd, count in metrics.error_frequency.items()
        }
        vector = self.skill_matrix.calculate_skill_vector(performance)
        if isinstance(vector, list):
            return {"git_basics": vector[0], "branching": vector[1], "collaboration": vector[2]}
        return {
            "git_basics": float(vector[0]),
            "branching": float(vector[1]),
            "collaboration": float(vector[2])
        }

    def update_knowledge_space(self, user_id: str, exercise_id: str, score: float) -> None:
        if user_id in self._user_data:
            if "knowledge_space" not in self._user_data[user_id]:
                self._user_data[user_id]["knowledge_space"] = {}
            self._user_data[user_id]["knowledge_space"][exercise_id] = score

            self.pattern_recognizer.add_learning_event({exercise_id: score})
            self.knowledge_space.update_mastery(exercise_id, score)

    def _get_practice_recommendations(self, metrics: SkillMetrics) -> List[str]:
        recommendations = []
        if metrics.command_success_rate < 0.6:
            recommendations.append("Practice basic commands more")
        if any(err > 3 for err in metrics.error_frequency.values()):
            recommendations.append("Focus on error-prone commands")
        if metrics.average_completion_time > 120:
            recommendations.append("Work on speed improvement")

        return recommendations or ["Continue with current difficulty level"]

    def calculate_difficulty_score(
        self,
        user_id: str,
        exercise_type: str,
        historical_performance: Dict[str, float],
        current_skill_level: float
    ) -> float:
        base_difficulty = 1.0
        skill_deviation = 0.5
        error_rate = 0.2
        self.skill_deviation_weight = 0.3
        self.error_rate_weight = 0.2

        adjusted_difficulty = (
            base_difficulty * (
                1 + (skill_deviation * self.skill_deviation_weight)
                + (error_rate * self.error_rate_weight)
            )
        )

        self.learning_parameters = {
            'base_learning_rate': 0.1,
            'skill_decay_factor': 0.95,
            'max_learning_rate': 0.5,
            'min_learning_rate': 0.01
        }

        return adjusted_difficulty


def adaptive_learning_function():
    # Adaptive learning code
    pass
