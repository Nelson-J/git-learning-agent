import unittest
from src.exercises.intermediate import (
    create_branch_exercise,
    create_merge_exercise,
    create_collaborative_exercise,
    get_intermediate_exercises,
)


class TestIntermediateExercises(unittest.TestCase):
    def test_branch_exercise_creation(self):
        exercise = create_branch_exercise()
        self.assertEqual(exercise.name, "branching_basics")
        self.assertEqual(exercise.difficulty, "intermediate")
        self.assertEqual(len(exercise.commands), 2)

    def test_merge_exercise_creation(self):
        exercise = create_merge_exercise()
        self.assertEqual(exercise.name, "merging_changes")
        self.assertTrue(any(cmd.name == "merge" for cmd in exercise.commands))
        self.assertTrue(
            any("branch_merged" in cmd.validation_rules for cmd in exercise.commands)
        )

    def test_collaborative_exercise_creation(self):
        exercise = create_collaborative_exercise()
        self.assertEqual(exercise.name, "team_collaboration")
        self.assertTrue(any(cmd.name == "remote" for cmd in exercise.commands))
        self.assertTrue(any(cmd.name == "pull" for cmd in exercise.commands))

    def test_get_all_exercises(self):
        exercises = get_intermediate_exercises()
        self.assertEqual(len(exercises), 3)
        exercise_names = {ex.name for ex in exercises}
        expected_names = {"branching_basics", "merging_changes", "team_collaboration"}
        self.assertEqual(exercise_names, expected_names)


if __name__ == "__main__":
    unittest.main()
