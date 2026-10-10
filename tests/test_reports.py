
import unittest
from campusflow.reports import generate_report


class TestTicketReports(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "status": "open",
                "priority": "critical",
            },
            {
                "id": "T002",
                "status": "in_progress",
                "priority": "high",
            },
            {
                "id": "T003",
                "status": "resolved",
                "priority": "high",
            },
        ]

    def test_total_ticket_count(self):
        report = generate_report(self.tickets)
        self.assertEqual(report["total"], 3)

    def test_counts_by_status(self):
        report = generate_report(self.tickets)
        self.assertEqual(
            report["by_status"],
            {"open": 1, "in_progress": 1, "resolved": 1},
        )

    def test_counts_by_priority(self):
        report = generate_report(self.tickets)
        self.assertEqual(
            report["by_priority"],
            {"critical": 1, "high": 2, "medium": 0, "low": 0},
        )

    def test_empty_ticket_list(self):
        report = generate_report([])
        self.assertEqual(report["total"], 0)
        self.assertEqual(
            report["by_status"],
            {"open": 0, "in_progress": 0, "resolved": 0},
        )
        self.assertEqual(
            report["by_priority"],
            {"critical": 0, "high": 0, "medium": 0, "low": 0},
        )


if __name__ == "__main__":
    unittest.main()

