from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Union
from enum import Enum
from datetime import datetime
import warnings

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
            "init": KnowledgeNode(
                concept="git_init", prerequisites=set(), difficulty=SkillLevel.BEGINNER
            ),
            "add": KnowledgeNode(
                concept="git_add",
                prerequisites={"git_init"},
                difficulty=SkillLevel.BEGINNER,
            ),
            "commit": KnowledgeNode(
                concept="git_commit",
                prerequisites={"git_add"},
                difficulty=SkillLevel.BEGINNER,
            ),
            "branch": KnowledgeNode(
                concept="git_branch",
                prerequisites={"git_commit"},
                difficulty=SkillLevel.INTERMEDIATE,
            ),
            "merge": KnowledgeNode(
                concept="git_merge",
                prerequisites={"git_branch"},
                difficulty=SkillLevel.INTERMEDIATE,
            ),
        }

    def update_mastery(self, concept: str, performance: float) -> None:
        if concept in self._knowledge_graph:
            node = self._knowledge_graph[concept]
            node.mastery_level = min(1.0, node.mastery_level + performance * 0.1)
            node.last_practiced = datetime.now()


class SkillMatrix:
    def __init__(self, knowledge_space: KnowledgeSpace):
        self.knowledge_space = knowledge_space
        self.skill_dimensions = [
            "concept_understanding",
            "practical_application",
            "problem_solving",
        ]
        self._difficulty_weights = {
            SkillLevel.BEGINNER: 1.0,
            SkillLevel.INTERMEDIATE: 1.5,
            SkillLevel.ADVANCED: 2.0,
        }

    def _get_difficulty_weight(self, difficulty: SkillLevel) -> float:
        return self._difficulty_weights.get(difficulty, 1.0)

    def calculate_skill_vector(
        self, user_performance: Dict[str, float]
    ) -> Union[np.ndarray, List[float]]:
        if not user_performance:
            return (
                np.zeros(len(self.skill_dimensions))
                if NUMPY_AVAILABLE
                else [0.0] * len(self.skill_dimensions)
            )

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
                skill_vector += np.array(
                    [
                        performance * weight,
                        performance * weight,  # Remove reduction factor
                        performance * weight * 0.9,  # Reduce penalty
                    ]
                )

        return skill_vector / total_weight if total_weight > 0 else skill_vector

    def _calculate_without_numpy(
        self, user_performance: Dict[str, float]
    ) -> List[float]:
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

        return [
            score / total_weight if total_weight > 0 else score
            for score in skill_vector
        ]


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

        performances = [
            sum(event.values()) / len(event) for event in self.pattern_history
        ]

        # Calculate the average improvement between consecutive performances
        improvements = [b - a for a, b in zip(performances[:-1], performances[1:])]

        return sum(improvements) / len(improvements) if improvements else 0.0

    def _identify_struggle_areas(self) -> List[str]:
        if not self.pattern_history:
            return []

        # Aggregate performance by concept
        concept_performance = {}
        for event in self.pattern_history:
            for concept, score in event.items():
                if concept not in concept_performance:
                    concept_performance[concept] = []
                concept_performance[concept].append(score)

        # Identify concepts with consistently low performance
        struggle_areas = [
            concept
            for concept, scores in concept_performance.items()
            if sum(scores) / len(scores) < 0.6  # threshold for struggling
        ]

        return struggle_areas

    def _identify_mastery_concepts(self) -> List[str]:
        if not self.pattern_history:
            return []

        # Aggregate performance by concept
        concept_performance = {}
        for event in self.pattern_history:
            for concept, score in event.items():
                if concept not in concept_performance:
                    concept_performance[concept] = []
                concept_performance[concept].append(score)

        # Identify concepts with consistently high performance
        mastery_concepts = [
            concept
            for concept, scores in concept_performance.items()
            if sum(scores) / len(scores) > 0.85  # threshold for mastery
        ]

        return mastery_concepts


from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


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

    def update_metrics(self, user_id: str, command: str, success: bool, time_taken: float) -> None:
        """Update user metrics based on their latest exercise attempt."""
        if user_id not in self.skill_metrics:
            self.skill_metrics[user_id] = SkillMetrics()

        metrics = self.skill_metrics[user_id]
        
        # Update success rate
        total_attempts = sum(metrics.error_frequency.values()) + 1
        if success:
            metrics.command_success_rate = (
                (metrics.command_success_rate * (total_attempts - 1) + 1) / total_attempts
            )
        else:
            metrics.command_success_rate = (
                metrics.command_success_rate * (total_attempts - 1) / total_attempts
            )
            metrics.error_frequency[command] = metrics.error_frequency.get(command, 0) + 1

        # Update completion time
        metrics.average_completion_time = (
            (metrics.average_completion_time * (total_attempts - 1) + time_taken)
            / total_attempts
        )

    def adjust_difficulty(self, user_id: str) -> Optional[DifficultyLevel]:
        """Adjust difficulty based on user performance."""
        if user_id not in self.skill_metrics:
            return None

        metrics = self.skill_metrics[user_id]
        
        # Consider advancing difficulty
        if (metrics.command_success_rate >= self.threshold_to_advance and
            self.current_difficulty != DifficultyLevel.ADVANCED):
            if self.current_difficulty == DifficultyLevel.BEGINNER:
                self.current_difficulty = DifficultyLevel.INTERMEDIATE
            else:
                self.current_difficulty = DifficultyLevel.ADVANCED
            return self.current_difficulty

        # Consider reducing difficulty
        if (metrics.command_success_rate <= self.threshold_to_fallback and
            self.current_difficulty != DifficultyLevel.BEGINNER):
            if self.current_difficulty == DifficultyLevel.ADVANCED:
                self.current_difficulty = DifficultyLevel.INTERMEDIATE
            else:
                self.current_difficulty = DifficultyLevel.BEGINNER
            return self.current_difficulty

        return None

    def get_next_exercise(self, user_id: str) -> Dict[str, str]:
        """Get the next appropriate exercise based on user's performance."""
        difficulty = self.current_difficulty.value
        metrics = self.skill_metrics.get(user_id, SkillMetrics())
        
        # Identify areas needing improvement
        weak_areas = sorted(
            metrics.error_frequency.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            "difficulty": difficulty,
            "focus_areas": [cmd for cmd, _ in weak_areas[:3]],
            "recommended_practice": self._get_practice_recommendations(metrics)
        }

    def _get_practice_recommendations(self, metrics: SkillMetrics) -> List[str]:
        """Generate practice recommendations based on user metrics."""
        recommendations = []
        
        if metrics.command_success_rate < 0.6:
            recommendations.append("Practice basic commands more")
        if any(err > 3 for err in metrics.error_frequency.values()):
            recommendations.append("Focus on error-prone commands")
        if metrics.average_completion_time > 120:  # 2 minutes
            recommendations.append("Work on speed improvement")
            
        return recommendations or ["Continue with current difficulty level"]

    def get_skill_vector(self, user_id: str) -> Union[np.ndarray, List[float]]:
        """Get the skill vector for a user."""
        if user_id not in self.skill_metrics:
            return []
        
        metrics = self.skill_metrics[user_id]
        performance = {
            cmd: 1.0 - (count / sum(metrics.error_frequency.values()))
            for cmd, count in metrics.error_frequency.items()
        }
        
        return self.skill_matrix.calculate_skill_vector(performance)

    def update_knowledge_space(self, user_id: str, concept: str, performance: float) -> None:
        """Update the knowledge space for a user."""
        self.knowledge_space.update_mastery(concept, performance)
        self.pattern_recognizer.add_learning_event({concept: performance})
