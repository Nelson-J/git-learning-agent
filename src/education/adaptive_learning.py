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
