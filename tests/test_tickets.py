import unittest

from campusflow.tickets import calculate_priority
from campusflow.tickets import validate_ticket_data
from campusflow.tickets import create_ticket
from campusflow.tickets import validate_existing_tickets


class TestCalculatePriority(unittest.TestCase):

    def test_critical_priority(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_priority_from_urgency(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_high_priority_from_affected_users(self):
        self.assertEqual(calculate_priority("low", 10), "high")

    def test_medium_priority_from_urgency(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")

    def test_medium_priority_from_affected_users(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_low_priority(self):
        self.assertEqual(calculate_priority("low", 1), "low")



class TestValidateTicketData(unittest.TestCase):

    def test_valid_ticket_data(self):
        # Valid input should not raise an error.
        validate_ticket_data("Internet is down", "Network", "high", 10)

    def test_empty_title(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("", "Network", "high", 10)

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("Internet is down", "Finance", "high", 10)

    def test_invalid_urgency(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("Internet is down", "Network", "urgent", 10)

    def test_zero_affected_users(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("Internet is down", "Network", "high", 0)

    def test_boolean_affected_users(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("Internet is down", "Network", "high", True)

    def test_category_must_be_a_string(self):
        with self.assertRaisesRegex(ValueError, "category must be a string"):
            validate_ticket_data("Network failure", ["Network"], "high", 5)
    
    def test_urgency_must_be_a_string(self):
        with self.assertRaisesRegex(ValueError, "Urgency must be a string"):
            validate_ticket_data("Network failure", "Network", 123, 5)

class TestCreateTicket(unittest.TestCase):

    def setUp(self):
        # Give every test a fresh ticket list.
        self.tickets = []

    def test_create_ticket_fields(self):
        ticket = create_ticket(
            "Internet is down",
            "Network",
            "high",
            15,
            self.tickets
        )

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["title"], "Internet is down")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["affected_users"], 15)
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

    def test_ticket_id_uses_highest_existing_number(self):
        # Simulate tickets already loaded into the application.
        self.tickets = [
            {"id": "T001"},
            {"id": "T003"}
        ]

        ticket = create_ticket(
            "New network issue",
            "Network",
            "medium",
            3,
            self.tickets
        )

        self.assertEqual(ticket["id"], "T004")

    def test_whitespace_only_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(
                "   ",
                "Network",
                "high",
                10,
                self.tickets
            )

        self.assertEqual(len(self.tickets), 0)

    def test_ticket_is_added_to_list(self):
        ticket = create_ticket(
            "Printer is faulty",
            "Hardware",
            "low",
            2,
            self.tickets
        )

        self.assertEqual(len(self.tickets), 1)
        self.assertIs(self.tickets[0], ticket)

    def test_ticket_ids_are_sequential(self):
        first = create_ticket(
            "Internet is down", "Network", "high", 15, self.tickets
        )
        second = create_ticket(
            "Printer is faulty", "Hardware", "low", 2, self.tickets
        )

        self.assertEqual(first["id"], "T001")
        self.assertEqual(second["id"], "T002")

    def test_invalid_ticket_is_not_added(self):
        with self.assertRaises(ValueError):
            create_ticket(
                "", "Network", "high", 15, self.tickets
            )

        self.assertEqual(len(self.tickets), 0)

    def test_reject_existing_ticket_without_id(self):
        tickets = [{"title": "Malformed record"}]

        with self.assertRaisesRegex(ValueError, "must have a string ID"):
            create_ticket("New ticket", "Network", "high", 5, tickets)

        # Failed creation must not add a new ticket.
        self.assertEqual(len(tickets), 1)

    def test_reject_existing_ticket_with_invalid_id(self):
        tickets = [{"id": "INVALID"}]

        with self.assertRaisesRegex(ValueError, "invalid ID format"):
            create_ticket("New ticket", "Network", "high", 5, tickets)

        self.assertEqual(len(tickets), 1)

if __name__ == "__main__":
    unittest.main()