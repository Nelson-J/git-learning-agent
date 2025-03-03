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
        self._user_data = {}
        self._review_schedule = {}
        self._minimum_interval = 1
        self._maximum_interval = 365
        self.initial_interval = timedelta(days=1)
        self.ease_factor = 2.5
        self.items = {}

    def initialize_user(self, user_id: str) -> None:
        """Initialize a new user in the spaced repetition system."""
        if user_id not in self._user_data:
            self._user_data[user_id] = {
                "reviews": {},
                "last_review": None,
                "next_review": None
            }
            self._review_schedule[user_id] = []

    def add_item(self, concept_id: str) -> None:
        """Add a new item to the spaced repetition system."""
        now = datetime.now()
        self._review_items[concept_id] = ReviewItem(
            concept_id=concept_id,
            last_review=now,
            next_review=now
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
        
        # Check review items instead of schedule
        for concept_id, item in self._review_items.items():
            if item.next_review <= now:
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

    def schedule_review(self, item_id: str) -> Optional[datetime]:
        """Schedule next review for an item using SuperMemo2 algorithm."""
        if item_id not in self.items:
            self.items[item_id] = {
                "interval": self.initial_interval,
                "ease_factor": self.ease_factor,
                "repetitions": 0
            }
            return datetime.now() + self.initial_interval

        item = self.items[item_id]
        next_interval = item["interval"] * item["ease_factor"]
        return datetime.now() + next_interval

    def process_response(self, item_id: str, quality: int) -> datetime:
        """Process response quality (0-5) and return next review date."""
        if quality < 0 or quality > 5:
            raise ValueError("Quality must be between 0 and 5")

        if item_id not in self.items:
            self.items[item_id] = {
                "interval": self.initial_interval,
                "ease_factor": self.ease_factor,
                "repetitions": 0
            }

        item = self.items[item_id]
        
        # Update ease factor
        item["ease_factor"] = max(1.3, item["ease_factor"] + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        
        # Calculate next interval
        if quality < 3:
            item["repetitions"] = 0
            item["interval"] = self.initial_interval
        else:
            item["repetitions"] += 1
            if item["repetitions"] == 1:
                item["interval"] = self.initial_interval * 1
            elif item["repetitions"] == 2:
                item["interval"] = self.initial_interval * 6
            else:
                item["interval"] = timedelta(days=math.ceil(item["interval"].days * item["ease_factor"]))

        return datetime.now() + item["interval"]


def spaced_repetition_function():
    # Spaced repetition code
    pass


# Additional code
