from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
import math


class RecallQuality(Enum):
    COMPLETE_BLACKOUT = 0  # Complete forgetting
    INCORRECT_REMEMBER = 1  # Wrong answer but remembered learning
    INCORRECT_EASY = 2  # Wrong answer but easy to remember
    CORRECT_DIFFICULT = 3  # Correct but required effort
    CORRECT_HESITANT = 4  # Correct with some hesitation
    CORRECT_PERFECT = 5  # Perfect recall


@dataclass
class ReviewItem:
    concept_id: str
    last_review: datetime
    next_review: datetime
    easiness: float = 2.5
    interval: int = 1
    repetitions: int = 0


class SpacedRepetitionSystem:
    def __init__(self):
        self._review_items: Dict[str, ReviewItem] = {}
        self._minimum_interval = 1  # day
        self._maximum_interval = 365  # days

    def add_item(self, concept_id: str) -> None:
        """Add a new item to the spaced repetition system."""
        now = datetime.now()
        self._review_items[concept_id] = ReviewItem(
            concept_id=concept_id,
            last_review=now,
            next_review=now,  # Set next_review to now to make it immediately due
        )

    def review_item(self, concept_id: str, quality: RecallQuality) -> timedelta:
        """
        Process a review using SuperMemo2 algorithm.
        Returns the next review interval.
        """
        if concept_id not in self._review_items:
            self.add_item(concept_id)

        item = self._review_items[concept_id]

        # Update item parameters based on SuperMemo2 algorithm
        if quality.value < 3:
            item.repetitions = 0
            item.interval = 1
        else:
            if item.repetitions == 0:
                item.interval = 1
            elif item.repetitions == 1:
                item.interval = 6
            else:
                item.interval = round(item.interval * item.easiness)

            item.repetitions += 1

        # Update easiness factor
        item.easiness = max(1.3, item.easiness + 0.1 - (5 - quality.value) * 0.08)

        # Calculate next review date
        interval_days = min(
            self._maximum_interval, max(self._minimum_interval, item.interval)
        )
        item.last_review = datetime.now()
        item.next_review = item.last_review + timedelta(days=interval_days)

        return timedelta(days=interval_days)

    def get_due_items(self) -> List[str]:
        """Get items due for review."""
        now = datetime.now()
        due_items = []

        for concept_id, item in self._review_items.items():
            # An item is due if:
            # 1. It's the first review (last_review == next_review)
            # 2. Its next review time has passed
            if item.last_review == item.next_review or item.next_review <= now:
                due_items.append(concept_id)

        return due_items

    def calculate_retention(self, concept_id: str) -> float:
        """Calculate estimated retention rate for an item."""
        if concept_id not in self._review_items:
            return 0.0

        item = self._review_items[concept_id]
        days_since_review = (datetime.now() - item.last_review).days

        # Use exponential decay formula: R = e^(-t/τ)
        # where τ (tau) is the decay constant based on item's easiness
        tau = item.easiness * 10  # Scale factor for decay rate
        retention = math.exp(-days_since_review / tau)

        return max(0.0, min(1.0, retention))

    def get_item_status(self, concept_id: str) -> Optional[Dict[str, any]]:
        """Get current status of a review item."""
        if concept_id not in self._review_items:
            return None

        item = self._review_items[concept_id]
        return {
            "last_review": item.last_review,
            "next_review": item.next_review,
            "easiness": item.easiness,
            "interval": item.interval,
            "repetitions": item.repetitions,
            "estimated_retention": self.calculate_retention(concept_id),
        }
