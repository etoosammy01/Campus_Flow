import unittest

from campusflow.notes import add_note, get_ticket_notes
from campusflow.tickets import calculate_priority
from campusflow.workflow import assign_ticket, change_status


def ticket(status="open", notes=None):
    return {
        "id": "T001", "title": "Network outage", "category": "Network",
        "urgency": "high", "affected_users": 12,
        "priority": calculate_priority("high", 12),
        "status": status, "assigned_to": None,
        "notes": [] if notes is None else notes,
    }


class TestTicketNotes(unittest.TestCase):
    def setUp(self):
        self.tickets = [ticket()]

    def test_valid_note_and_id(self):
        note = add_note(self.tickets, "T001", " Ada ", " Router restarted ")
        self.assertEqual(note, {
            "note_id": "N001", "author": "Ada", "message": "Router restarted"
        })

    def test_next_note_id_increments_per_ticket(self):
        add_note(self.tickets, "T001", "Ada", "First update")
        self.assertEqual(add_note(self.tickets, "T001", "Ada", "Second update")["note_id"], "N002")

    def test_blank_author_rejected_without_mutation(self):
        before = [dict(self.tickets[0])]
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "  ", "A valid message")
        self.assertEqual(self.tickets, before)

    def test_too_short_note_rejected_without_consuming_id(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Ada", "abcd")
        self.assertEqual(add_note(self.tickets, "T001", "Ada", "valid note")["note_id"], "N001")

    def test_too_long_note_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Ada", "x" * 301)
        self.assertEqual(self.tickets[0]["notes"], [])

    def test_resolved_ticket_rejects_note(self):
        self.tickets[0]["status"] = "resolved"
        before = [dict(self.tickets[0])]
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Ada", "Resolved followup")
        self.assertEqual(self.tickets, before)

    def test_reopen_allows_note_and_preserves_existing_notes(self):
        existing = {"note_id": "N001", "author": "Ada", "message": "First update"}
        self.tickets = [ticket(status="in_progress", notes=[existing])]
        assign_ticket(self.tickets, "T001", "Ada")
        change_status(self.tickets, "T001", "resolved")
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Bo", "Second update")
        change_status(self.tickets, "T001", "open")
        note = add_note(self.tickets, "T001", "Bo", "Second update")
        self.assertEqual(note["note_id"], "N002")
        self.assertEqual(len(self.tickets[0]["notes"]), 2)

    def test_in_progress_ticket_accepts_note(self):
        self.tickets[0]["status"] = "in_progress"
        self.assertEqual(add_note(self.tickets, "T001", "Ada", "Work update")["note_id"], "N001")

    def test_unknown_ticket_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T999", "Ada", "Valid message")

    def test_notes_returned_in_numeric_id_order(self):
        self.tickets[0]["notes"] = [
            {"note_id": "N010", "author": "Bo", "message": "Later update"},
            {"note_id": "N002", "author": "Ada", "message": "Earlier update"},
        ]
        self.assertEqual([n["note_id"] for n in get_ticket_notes(self.tickets, "T001")],
                         ["N002", "N010"])


if __name__ == "__main__":
    unittest.main()
