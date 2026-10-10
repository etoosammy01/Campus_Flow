
import json
import tempfile
import unittest
from pathlib import Path

from campusflow.storage import load_tickets, save_tickets


class TestTicketStorage(unittest.TestCase):

    def test_save_and_load_tickets(self):
        tickets = [
            {
                "id": "T001",
                "title": "Network is down",
                "category": "Network",
                "urgency": "high",
                "affected_users": 12,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            }
        ]

        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "tickets.json"

            save_tickets(tickets, file_path)
            loaded = load_tickets(file_path)

            self.assertEqual(loaded, tickets)

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "missing.json"

            self.assertEqual(load_tickets(file_path), [])

    def test_saved_file_contains_valid_json(self):
        tickets = [{"id": "T001"}]

        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "tickets.json"

            save_tickets(tickets, file_path)

            with open(file_path, encoding="utf-8") as file:
                self.assertEqual(json.load(file), tickets)


if __name__ == "__main__":
    unittest.main()
