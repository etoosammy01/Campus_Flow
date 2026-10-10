
import unittest

from campusflow.workflow import assign_ticket

from campusflow.workflow import assign_ticket, change_status

from campusflow.workflow import (
    assign_ticket,
    change_status,
    get_work_queue,
)

class TestTicketAssignment(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "status": "open",
                "assigned_to": None,
            }
        ]

    def test_assign_ticket_successfully(self):
        ticket = assign_ticket(self.tickets, "T001", "Ada")

        self.assertEqual(ticket["assigned_to"], "Ada")
        self.assertEqual(ticket["status"], "open")

    def test_unknown_ticket_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "Ada")

    def test_blank_staff_name_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "   ")

    def test_staff_name_is_trimmed(self):
        ticket = assign_ticket(self.tickets, "T001", "  Ada  ")

        self.assertEqual(ticket["assigned_to"], "Ada")



    def test_unassigned_ticket_cannot_start_work(self):
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "in_progress")

    def test_assigned_ticket_can_start_work(self):
        assign_ticket(self.tickets, "T001", "Ada")

        ticket = change_status(self.tickets, "T001", "in_progress")

        self.assertEqual(ticket["status"], "in_progress")

    def test_ticket_can_be_resolved(self):
        assign_ticket(self.tickets, "T001", "Ada")
        change_status(self.tickets, "T001", "in_progress")

        ticket = change_status(self.tickets, "T001", "resolved")

        self.assertEqual(ticket["status"], "resolved")

    def test_resolved_ticket_can_be_reopened(self):
        assign_ticket(self.tickets, "T001", "Ada")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")

        ticket = change_status(self.tickets, "T001", "open")

        self.assertEqual(ticket["status"], "open")

    def test_open_ticket_cannot_skip_to_resolved(self):
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "resolved")


    def test_resolved_ticket_cannot_be_reassigned(self):
        self.tickets[0]["status"] = "resolved"

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "Ada")


class TestWorkQueue(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {
                "id": "T003",
                "status": "open",
                "priority": "low",
            },
            {
                "id": "T002",
                "status": "open",
                "priority": "critical",
            },
            {
                "id": "T001",
                "status": "open",
                "priority": "critical",
            },
            {
                "id": "T004",
                "status": "resolved",
                "priority": "critical",
            },
        ]

    def test_critical_tickets_come_first(self):
        queue = get_work_queue(self.tickets)
        self.assertEqual(queue[0]["priority"], "critical")

    def test_same_priority_uses_numeric_id(self):
        queue = get_work_queue(self.tickets)
        self.assertEqual(queue[0]["id"], "T001")
        self.assertEqual(queue[1]["id"], "T002")

    def test_resolved_tickets_are_excluded(self):
        queue = get_work_queue(self.tickets)
        ids = [ticket["id"] for ticket in queue]
        self.assertNotIn("T004", ids)

    def test_original_list_is_not_reordered(self):
        original_ids = [ticket["id"] for ticket in self.tickets]
        get_work_queue(self.tickets)
        self.assertEqual(
            [ticket["id"] for ticket in self.tickets],
            original_ids,
        )

    def test_empty_queue(self):
        self.assertEqual(get_work_queue([]), [])


if __name__ == "__main__":
    unittest.main()
