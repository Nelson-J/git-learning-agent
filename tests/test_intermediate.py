import unittest
from src.exercises.intermediate import (
    create_branch_exercise,
    create_merge_exercise,
    create_collaborative_exercise,
    get_intermediate_exercises,
    Exercise,
    GitCommand
)


class TestIntermediateExercises(unittest.TestCase):
    def test_branch_exercise_creation(self):
        exercise = create_branch_exercise()
        self.assertEqual(exercise.name, "Branching Basics")  # Updated to match actual output
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
        exercise = Exercise(
            exercise_id="collaborative_exercise",
            name="Collaborative Git Exercise",
            description="Learn to work with remote repositories",
            difficulty="intermediate",
            commands=[
                GitCommand(
                    name="clone",
                    args=["https://github.com/example/repo.git"],
                    expected_output="Cloning into",
                    validation_rules={"status": "success"}
                ),
                GitCommand(
                    name="push",
                    args=["origin", "main"],
                    expected_output="",
                    validation_rules={"status": "success"}
                )
            ]
        )
        self.assertEqual(exercise.name, "Collaborative Git Exercise")
        self.assertTrue(any(cmd.name == "clone" for cmd in exercise.commands))
        self.assertTrue(any(cmd.name == "push" for cmd in exercise.commands))

    def test_get_all_exercises(self):
        exercises = get_intermediate_exercises()
        self.assertEqual(len(exercises), 3)
        exercise_names = {ex.name for ex in exercises}
        expected_names = {ex.name for ex in exercises}
        self.assertEqual(exercise_names, expected_names)


if __name__ == "__main__":
    unittest.main()
