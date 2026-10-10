
import unittest

from campusflow.workflow import assign_ticket


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


if __name__ == "__main__":
    unittest.main()
