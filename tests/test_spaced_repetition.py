import unittest
from datetime import datetime, timedelta
from src.education.spaced_repetition import SpacedRepetitionSystem, RecallQuality  # Added RecallQuality import


class TestSpacedRepetition(unittest.TestCase):
    def setUp(self):
        self.srs = SpacedRepetitionSystem()
        self.concept_id = "git_init"

    def test_add_item(self):
        self.srs.add_item(self.concept_id)
        item_status = self.srs.get_item_status(self.concept_id)  # Renamed to item_status
        self.assertIsNotNone(item_status)
        self.assertEqual(item_status["interval"], 1)

    def test_review_progression(self):
        self.srs.add_item(self.concept_id)

        # First perfect review
        interval = self.srs.review_item(
            self.concept_id, 
            RecallQuality.CORRECT_PERFECT
        )
        self.assertEqual(interval.days, 1)

        # Second perfect review
        interval = self.srs.review_item(
            self.concept_id,
            RecallQuality.CORRECT_PERFECT
        )
        self.assertEqual(interval.days, 6)

        # Third perfect review
        interval = self.srs.review_item(
            self.concept_id,
            RecallQuality.CORRECT_PERFECT
        )
        self.assertGreater(interval.days, 6)

    def test_retention_calculation(self):
        self.srs.add_item(self.concept_id)
        initial_retention = self.srs.calculate_retention(self.concept_id)
        self.assertEqual(initial_retention, 1.0)

        # Simulate time passage
        item = self.srs._review_items[self.concept_id]
        item.last_review = datetime.now() - timedelta(days=5)

        retention = self.srs.calculate_retention(self.concept_id)
        self.assertLess(retention, 1.0)
        self.assertGreater(retention, 0.0)

    def test_due_items(self):
        self.srs.add_item(self.concept_id)

        # New item should be due immediately
        due_items = self.srs.get_due_items()
        self.assertIn(self.concept_id, due_items)

        # After review, item should not be due
        self.srs.review_item(self.concept_id, RecallQuality.CORRECT_PERFECT)
        due_items = self.srs.get_due_items()
        self.assertNotIn(self.concept_id, due_items)

    def test_review_scheduling(self):
        item_id = "test_item"
        next_review = self.srs.schedule_review(item_id)
        self.assertIsInstance(next_review, datetime)
        self.assertTrue(next_review > datetime.now())

    def test_response_processing(self):
        item_id = "test_item"
        next_review = self.srs.process_response(item_id, 5)
        self.assertIsInstance(next_review, datetime)
        self.assertTrue(next_review > datetime.now())


if __name__ == "__main__":
    unittest.main()
