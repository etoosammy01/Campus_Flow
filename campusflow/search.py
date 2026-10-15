"""Ticket search with optional AND-combined filters."""


def search_tickets(tickets, query="", category=None, status=None, priority=None):
    """Search title substrings case-insensitively and combine filters with AND."""
    if not isinstance(query, str):
        raise ValueError("Search query must be text.")
    if category is not None and (
        not isinstance(category, str)
        or category not in {"Network", "Hardware", "Software", "Other"}
    ):
        raise ValueError("Invalid category filter.")
    if status is not None and (
        not isinstance(status, str)
        or status not in {"open", "in_progress", "resolved"}
    ):
        raise ValueError("Invalid status filter.")
    if priority is not None and (
        not isinstance(priority, str)
        or priority not in {"critical", "high", "medium", "low"}
    ):
        raise ValueError("Invalid priority filter.")

    needle = query.strip().casefold()
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    matches = [
        ticket for ticket in tickets
        if needle in ticket.get("title", "").casefold()
        and (category is None or ticket.get("category") == category)
        and (status is None or ticket.get("status") == status)
        and (priority is None or ticket.get("priority") == priority)
    ]
    return sorted(matches, key=lambda ticket: (
        order.get(ticket.get("priority"), 4),
        int(ticket["id"][1:]),
    ))
