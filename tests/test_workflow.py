import unittest

from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status, get_work_queue


def make_ticket(ticket_id="T001", status="open", assigned_to=None,
                priority="high", title="Network issue", category="Network",
                urgency="high", affected_users=5, notes=None):
    return {
        "id": ticket_id, "title": title, "category": category,
        "urgency": urgency, "affected_users": affected_users,
        "priority": priority, "status": status, "assigned_to": assigned_to,
        "notes": [] if notes is None else notes,
    }


class TestTicketAssignment(unittest.TestCase):
    def setUp(self):
        self.tickets = [make_ticket()]

    def test_assign_ticket_successfully(self):
        self.assertEqual(assign_ticket(self.tickets, "T001", "Ada")["assigned_to"], "Ada")

    def test_unknown_ticket_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "Ada")

    def test_blank_staff_name_is_rejected_without_mutation(self):
        before = [dict(self.tickets[0])]
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "   ")
        self.assertEqual(self.tickets, before)

    def test_staff_name_is_trimmed(self):
        self.assertEqual(assign_ticket(self.tickets, "T001", " Ada ")["assigned_to"], "Ada")

    def test_resolved_ticket_cannot_be_reassigned_without_mutation(self):
        self.tickets[0]["status"] = "resolved"
        before = [dict(self.tickets[0])]
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "Ada")
        self.assertEqual(self.tickets, before)

    def test_unassigned_open_ticket_cannot_start_work_without_mutation(self):
        before = [dict(self.tickets[0])]
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "in_progress")
        self.assertEqual(self.tickets, before)

    def test_assigned_ticket_can_start_work(self):
        assign_ticket(self.tickets, "T001", "Ada")
        self.assertEqual(change_status(self.tickets, "T001", "in_progress")["status"], "in_progress")

    def test_ticket_can_be_resolved(self):
        assign_ticket(self.tickets, "T001", "Ada")
        change_status(self.tickets, "T001", "in_progress")
        self.assertEqual(change_status(self.tickets, "T001", "resolved")["status"], "resolved")

    def test_resolved_ticket_can_be_reopened(self):
        self.tickets[0]["status"] = "resolved"
        self.assertEqual(change_status(self.tickets, "T001", "open")["status"], "open")

    def test_open_ticket_cannot_skip_to_resolved(self):
        before = [dict(self.tickets[0])]
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "resolved")
        self.assertEqual(self.tickets, before)

    def test_invalid_unhashable_status_is_value_error_and_unchanged(self):
        before = [dict(self.tickets[0])]
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", [])
        self.assertEqual(self.tickets, before)


class TestWorkQueue(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            make_ticket("T003", priority="low"),
            make_ticket("T002", priority="critical"),
            make_ticket("T001", priority="critical"),
            make_ticket("T004", status="resolved", priority="critical"),
            make_ticket("T005", status="in_progress", priority="critical"),
        ]

    def test_critical_tickets_come_first(self):
        self.assertEqual(get_work_queue(self.tickets)[0]["priority"], "critical")

    def test_same_priority_uses_numeric_id(self):
        queue = get_work_queue(self.tickets)
        self.assertEqual([queue[0]["id"], queue[1]["id"]], ["T001", "T002"])

    def test_resolved_and_in_progress_excluded(self):
        ids = [ticket["id"] for ticket in get_work_queue(self.tickets)]
        self.assertNotIn("T004", ids)
        self.assertNotIn("T005", ids)

    def test_original_list_is_not_reordered(self):
        before = [ticket["id"] for ticket in self.tickets]
        get_work_queue(self.tickets)
        self.assertEqual([ticket["id"] for ticket in self.tickets], before)

    def test_empty_queue(self):
        self.assertEqual(get_work_queue([]), [])


if __name__ == "__main__":
    unittest.main()
