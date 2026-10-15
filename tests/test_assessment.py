import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from campusflow import app
from campusflow.assessment import QUESTIONS, score_answers


class TestEngineeringCheck(unittest.TestCase):
    def test_score_is_correct(self):
        answers = [question["answer"] for question in QUESTIONS]
        self.assertEqual(score_answers(answers), 6)

    def test_wrong_answers_are_not_counted(self):
        self.assertEqual(score_answers(["A"] * 6), sum(q["answer"] == "A" for q in QUESTIONS))

    def test_invalid_answer_retries_and_score_is_saved(self):
        valid_answers = [q["answer"] for q in QUESTIONS]
        responses = ["X", *valid_answers, "Reason one", "Reason two"]
        # The first two explanations are prompted immediately after answers 1 and 2.
        responses = ["X", valid_answers[0], "Reason one",
                     valid_answers[1], "Reason two", *valid_answers[2:]]
        with tempfile.TemporaryDirectory() as directory:
            target = str(Path(directory) / "results.json")
            with patch.object(app, "CHECK_RESULTS_FILE", target):
                with patch("builtins.input", side_effect=responses):
                    app.run_understanding_check()
            self.assertTrue(Path(target).exists())


    def test_failed_reload_keeps_current_collection_unchanged(self):
        current = [{"id": "T001", "title": "Keep me"}]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text("{broken", encoding="utf-8")
            with patch.object(app, "DATA_FILE", str(path)):
                returned = app.reload_ticket_data(current)
        self.assertIs(returned, current)
        self.assertEqual(current, [{"id": "T001", "title": "Keep me"}])


if __name__ == "__main__":
    unittest.main()
