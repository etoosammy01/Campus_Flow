import json
import tempfile
import unittest
from pathlib import Path

from campusflow.storage import load_tickets, save_tickets, validate_ticket_collection
from campusflow.tickets import create_ticket


def valid_ticket(ticket_id="T001", status="open", assigned_to=None,
                 urgency="high", affected_users=12, notes=None):
    from campusflow.tickets import calculate_priority
    return {
        "id": ticket_id, "title": "Network outage", "category": "Network",
        "urgency": urgency, "affected_users": affected_users,
        "priority": calculate_priority(urgency, affected_users),
        "status": status, "assigned_to": assigned_to,
        "notes": [] if notes is None else notes,
    }


class TestTicketStorage(unittest.TestCase):
    def test_save_and_load_tickets_with_notes(self):
        tickets = [valid_ticket(notes=[
            {"note_id": "N001", "author": "Ada", "message": "Restarted the router"}
        ])]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            save_tickets(tickets, path)
            self.assertEqual(load_tickets(path), tickets)

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(load_tickets(Path(directory) / "missing.json"), [])

    def test_saved_file_contains_valid_json(self):
        tickets = [valid_ticket()]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            save_tickets(tickets, path)
            with path.open(encoding="utf-8") as file:
                self.assertEqual(json.load(file), tickets)

    def test_old_schema_migrates_notes_to_empty_list(self):
        old = valid_ticket()
        del old["notes"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text(json.dumps([old]), encoding="utf-8")
            self.assertEqual(load_tickets(path)[0]["notes"], [])

    def test_duplicate_ticket_ids_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text(json.dumps([valid_ticket(), valid_ticket()]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate ticket ID"):
                load_tickets(path)

    def test_invalid_json_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text("{broken", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid JSON"):
                load_tickets(path)

    def test_invalid_priority_rejected(self):
        bad = valid_ticket()
        bad["priority"] = "low"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text(json.dumps([bad]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "inconsistent priority"):
                load_tickets(path)

    def test_invalid_note_shape_rejected(self):
        bad = valid_ticket(notes=[{"note_id": "N001"}])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text(json.dumps([bad]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid note record"):
                load_tickets(path)

    def test_save_rejects_invalid_collection_before_replacing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            original = [valid_ticket()]
            save_tickets(original, path)
            before = path.read_text(encoding="utf-8")
            with self.assertRaises(ValueError):
                save_tickets([{"id": "T001"}], path)
            self.assertEqual(path.read_text(encoding="utf-8"), before)

    def test_ticket_id_continues_after_load(self):
        tickets = [valid_ticket("T004")]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            save_tickets(tickets, path)
            loaded = load_tickets(path)
            created = create_ticket("Printer", "Hardware", "low", 1, loaded)
            self.assertEqual(created["id"], "T005")

    def test_note_id_continues_after_load(self):
        from campusflow.notes import add_note
        ticket = valid_ticket(notes=[
            {"note_id": "N003", "author": "Ada", "message": "Previous update"}
        ])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            save_tickets([ticket], path)
            loaded = load_tickets(path)
            self.assertEqual(add_note(loaded, "T001", "Bo", "New update")["note_id"], "N004")


if __name__ == "__main__":
    unittest.main()
