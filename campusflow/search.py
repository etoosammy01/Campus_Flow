"""Read-only ticket search. Nothing here modifies a ticket."""

CATEGORY_OPTIONS = ("Network", "Hardware", "Software", "Other")
STATUS_OPTIONS = ("open", "in_progress", "resolved")
PRIORITY_OPTIONS = ("critical", "high", "medium", "low")
PRIORITY_ORDER = {name: rank for rank, name in enumerate(PRIORITY_OPTIONS)}


def normalize_filter(value, allowed, label):
    """Turn raw filter text into an official option, or None for 'no filter'.

    Blank text means "do not filter". Matching ignores case and surrounding
    spaces. Anything else raises ValueError so the CLI can re-prompt.
    """
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{label} filter must be text.")
    wanted = value.strip().casefold()
    if not wanted:
        return None
    for option in allowed:
        if wanted == option.casefold():
            return option
    raise ValueError(f"{label} must be one of: {', '.join(allowed)} (or leave blank).")


def search_tickets(tickets, query="", category=None, status=None, priority=None):
    """Return tickets matching ALL supplied filters, in their stored order.

    The title test is a case-insensitive substring match. A filter that is
    None is ignored. The tickets themselves are never changed.
    """
    if not isinstance(query, str):
        raise ValueError("Search query must be text.")
    if category is not None and category not in CATEGORY_OPTIONS:
        raise ValueError("Invalid category filter.")
    if status is not None and status not in STATUS_OPTIONS:
        raise ValueError("Invalid status filter.")
    if priority is not None and priority not in PRIORITY_OPTIONS:
        raise ValueError("Invalid priority filter.")

    needle = query.strip().casefold()
    return [
        ticket for ticket in tickets
        if needle in str(ticket.get("title", "")).casefold()
        and (category is None or ticket.get("category") == category)
        and (status is None or ticket.get("status") == status)
        and (priority is None or ticket.get("priority") == priority)
    ]


def sort_by_priority(tickets):
    """Return a NEW list: critical -> low, ties by numeric ticket ID."""
    return sorted(
        tickets,
        key=lambda ticket: (
            PRIORITY_ORDER.get(ticket.get("priority"), len(PRIORITY_ORDER)),
            int(ticket["id"][1:]),
        ),
    )