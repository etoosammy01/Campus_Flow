
def generate_report(tickets):
    """Generate summary counts for ticket status and priority."""

    report = {
        "total": len(tickets),
        "by_status": {
            "open": 0,
            "in_progress": 0,
            "resolved": 0,
        },
        "by_priority": {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        },
    }

    for ticket in tickets:
        status = ticket["status"]
        priority = ticket["priority"]

        if status in report["by_status"]:
            report["by_status"][status] += 1

        if priority in report["by_priority"]:
            report["by_priority"][priority] += 1

    return report
