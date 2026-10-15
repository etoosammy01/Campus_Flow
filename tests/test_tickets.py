import unittest

from campusflow.tickets import (
    calculate_priority, create_ticket, validate_existing_tickets,
    validate_ticket_data,
)


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
        validate_ticket_data("Internet is down", "Network", "high", 10)

    def test_empty_title(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("", "Network", "high", 10)

    def test_whitespace_title(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("   ", "Network", "high", 10)

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("Internet is down", "Finance", "high", 10)

    def test_category_must_be_string(self):
        with self.assertRaisesRegex(ValueError, "category must be a string"):
            validate_ticket_data("Issue", ["Network"], "high", 5)

    def test_invalid_urgency(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("Issue", "Network", "urgent", 10)

    def test_urgency_must_be_string(self):
        with self.assertRaisesRegex(ValueError, "Urgency must be a string"):
            validate_ticket_data("Issue", "Network", 123, 5)

    def test_zero_affected_users(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("Issue", "Network", "high", 0)

    def test_negative_affected_users(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("Issue", "Network", "high", -1)

    def test_float_affected_users(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("Issue", "Network", "high", 2.5)

    def test_string_affected_users(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("Issue", "Network", "high", "2")

    def test_boolean_affected_users(self):
        with self.assertRaises(ValueError):
            validate_ticket_data("Issue", "Network", "high", True)


class TestCreateTicket(unittest.TestCase):
    def setUp(self):
        self.tickets = []

    def test_create_ticket_fields_and_empty_notes(self):
        ticket = create_ticket("Internet down", "Network", "high", 15, self.tickets)
        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertEqual(ticket["notes"], [])

    def test_ticket_id_uses_highest_existing_number(self):
        self.tickets = [
            {"id": "T001"}, {"id": "T003"}
        ]
        ticket = create_ticket("Issue", "Network", "medium", 3, self.tickets)
        self.assertEqual(ticket["id"], "T004")

    def test_ticket_ids_are_sequential(self):
        first = create_ticket("First", "Network", "high", 15, self.tickets)
        second = create_ticket("Second", "Hardware", "low", 2, self.tickets)
        self.assertEqual((first["id"], second["id"]), ("T001", "T002"))

    def test_title_is_trimmed(self):
        ticket = create_ticket("  Printer issue  ", "Hardware", "low", 2, self.tickets)
        self.assertEqual(ticket["title"], "Printer issue")

    def test_invalid_ticket_is_not_added(self):
        before = list(self.tickets)
        with self.assertRaises(ValueError):
            create_ticket("", "Network", "high", 15, self.tickets)
        self.assertEqual(self.tickets, before)

    def test_reject_existing_ticket_without_id(self):
        tickets = [{"title": "Malformed"}]
        with self.assertRaises(ValueError):
            create_ticket("New", "Network", "high", 5, tickets)
        self.assertEqual(tickets, [{"title": "Malformed"}])

    def test_reject_existing_ticket_with_invalid_id(self):
        tickets = [{"id": "INVALID"}]
        with self.assertRaises(ValueError):
            create_ticket("New", "Network", "high", 5, tickets)
        self.assertEqual(tickets, [{"id": "INVALID"}])

    def test_duplicate_existing_ids_rejected_without_mutation(self):
        tickets = [{"id": "T001"}, {"id": "T001"}]
        before = [dict(ticket) for ticket in tickets]
        with self.assertRaisesRegex(ValueError, "Duplicate ticket ID"):
            create_ticket("New", "Network", "high", 5, tickets)
        self.assertEqual(tickets, before)

    def test_non_list_collection_rejected(self):
        with self.assertRaises(ValueError):
            validate_existing_tickets({})


if __name__ == "__main__":
    unittest.main()
