import unittest
from campusflow.reports import generate_report
from campusflow.workflow import assign_ticket, change_status


class TestTicketReports(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {"id": "T001", "title": "Network", "category": "Network",
             "status": "open", "priority": "critical"},
            {"id": "T002", "title": "Software", "category": "Software",
             "status": "in_progress", "priority": "high"},
            {"id": "T003", "title": "Hardware", "category": "Hardware",
             "status": "resolved", "priority": "high"},
        ]

    def test_total_ticket_count(self):
        self.assertEqual(generate_report(self.tickets)["total"], 3)

    def test_counts_by_status(self):
        self.assertEqual(generate_report(self.tickets)["by_status"],
                         {"open": 1, "in_progress": 1, "resolved": 1})

    def test_counts_by_priority(self):
        self.assertEqual(generate_report(self.tickets)["by_priority"],
                         {"critical": 1, "high": 2, "medium": 0, "low": 0})

    def test_counts_by_category(self):
        self.assertEqual(generate_report(self.tickets)["by_category"],
                         {"Network": 1, "Hardware": 1, "Software": 1, "Other": 0})

    def test_unresolved_and_resolution_rate(self):
        report = generate_report(self.tickets)
        self.assertEqual(report["unresolved"], 2)
        self.assertEqual(report["resolved"], 1)
        self.assertAlmostEqual(report["resolution_rate"], 100 / 3)

    def test_empty_report_has_zero_rate(self):
        report = generate_report([])
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["resolution_rate"], 0.0)
        self.assertEqual(report["unresolved"], 0)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["by_status"],
                         {"open": 0, "in_progress": 0, "resolved": 0})
        self.assertEqual(report["by_priority"],
                         {"critical": 0, "high": 0, "medium": 0, "low": 0})


    def test_report_counts_after_resolve_and_reopen(self):
        tickets = [{
            "id": "T001", "title": "Network issue", "category": "Network",
            "urgency": "high", "affected_users": 12, "priority": "critical",
            "status": "open", "assigned_to": None, "notes": [],
        }]
        assign_ticket(tickets, "T001", "Ada")
        change_status(tickets, "T001", "in_progress")
        change_status(tickets, "T001", "resolved")
        self.assertEqual(generate_report(tickets)["resolved"], 1)
        change_status(tickets, "T001", "open")
        report = generate_report(tickets)
        self.assertEqual(report["by_status"], {
            "open": 1, "in_progress": 0, "resolved": 0
        })
        self.assertEqual(report["unresolved"], 1)
        self.assertEqual(report["resolution_rate"], 0.0)


if __name__ == "__main__":
    unittest.main()
