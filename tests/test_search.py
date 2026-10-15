import unittest

from campusflow.search import search_tickets


TICKETS = [
    {"id": "T003", "title": "Network outage in Lab", "category": "Network",
     "status": "open", "priority": "critical"},
    {"id": "T002", "title": "network cable broken", "category": "Hardware",
     "status": "in_progress", "priority": "high"},
    {"id": "T001", "title": "Printer offline", "category": "Hardware",
     "status": "resolved", "priority": "low"},
]


class TestTicketSearch(unittest.TestCase):
    def test_case_insensitive_substring_search(self):
        results = search_tickets(TICKETS, query="NETWORK")
        self.assertEqual({ticket["id"] for ticket in results}, {"T002", "T003"})

    def test_combined_filters_use_and(self):
        results = search_tickets(
            TICKETS, query="network", category="Hardware",
            status="in_progress", priority="high",
        )
        self.assertEqual([ticket["id"] for ticket in results], ["T002"])

    def test_nonmatching_combined_filters_return_empty(self):
        self.assertEqual(search_tickets(
            TICKETS, query="network", category="Network", status="resolved"
        ), [])

    def test_results_sorted_by_priority_then_numeric_id(self):
        results = search_tickets(TICKETS)
        self.assertEqual([ticket["id"] for ticket in results], ["T003", "T002", "T001"])

    def test_invalid_filter_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(TICKETS, status="closed")


if __name__ == "__main__":
    unittest.main()
