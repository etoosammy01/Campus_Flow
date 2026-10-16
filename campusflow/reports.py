"""Summary reports for CampusFlow tickets."""


def generate_report(tickets):
    """Return totals, status/priority/category counts, and resolution metrics."""
    statuses = ("open", "in_progress", "resolved")
    priorities = ("critical", "high", "medium", "low")
    categories = ("Network", "Hardware", "Software", "Other")
    by_status = {status: 0 for status in statuses}
    by_priority = {priority: 0 for priority in priorities}
    by_category = {category: 0 for category in categories}

    for ticket in tickets:
        if ticket.get("status") in by_status:
            by_status[ticket["status"]] += 1
        if ticket.get("priority") in by_priority:
            by_priority[ticket["priority"]] += 1
        if ticket.get("category") in by_category:
            by_category[ticket["category"]] += 1

    total = len(tickets)
    resolved = by_status["resolved"]
    unresolved = by_status["open"] + by_status["in_progress"]
    return {
        "total": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_category": by_category,
        "unresolved": unresolved,
        "resolved": resolved,
        "resolution_rate": (resolved / total * 100) if total else 0.0,
    }
