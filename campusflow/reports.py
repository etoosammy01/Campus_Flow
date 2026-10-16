"""Summary reports for CampusFlow tickets."""

STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")
CATEGORIES = ("Network", "Hardware", "Software", "Other")


def generate_report(tickets):
    """Return totals, status/priority/category counts, and resolution metrics.

    Every count comes from the tickets' CURRENT values, so a reopened ticket
    is counted once, under its current status.
    """
    by_status = {status: 0 for status in STATUSES}
    by_priority = {priority: 0 for priority in PRIORITIES}
    by_category = {category: 0 for category in CATEGORIES}

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


def format_report(report):
    """Return the report as text. Pure function: no print(), easy to test."""
    lines = [
        f"Total tickets: {report['total']}",
        f"Unresolved (open + in progress): {report['unresolved']}",
        f"Resolved: {report['resolved']}",
        f"Resolution rate: {report['resolution_rate']:.1f}%",
    ]
    for key, label in (("by_status", "By status"),
                       ("by_priority", "By priority"),
                       ("by_category", "By category")):
        lines.append(f"\n{label}:")
        lines += [f"  {name}: {count}" for name, count in report[key].items()]
    return "\n".join(lines)