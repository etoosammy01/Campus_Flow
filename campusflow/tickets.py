"""Ticket validation, priority calculation, and creation."""

CATEGORIES = {"Network", "Hardware", "Software", "Other"}
URGENCY_LEVELS = {"low", "medium", "high"}
STATUSES = {"open", "in_progress", "resolved"}
PRIORITIES = {"critical", "high", "medium", "low"}


def calculate_priority(urgency, affected_users):
    """Calculate priority using the CampusFlow assessment rules."""
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def validate_ticket_data(title, category, urgency, affected_users):
    """Validate the information required to create a ticket."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be empty.")
    if not isinstance(category, str):
        raise ValueError("Ticket category must be a string.")
    if category not in CATEGORIES:
        raise ValueError("Invalid ticket category.")
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be a string.")
    if urgency not in URGENCY_LEVELS:
        raise ValueError("Invalid urgency level.")
    if (isinstance(affected_users, bool)
            or not isinstance(affected_users, int)
            or affected_users <= 0):
        raise ValueError("Affected users must be a positive integer.")


def validate_existing_tickets(tickets):
    """Validate unique, well-formed ticket IDs in a collection."""
    if not isinstance(tickets, list):
        raise ValueError("Tickets must be stored in a list.")

    seen_ids = set()
    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Existing ticket record must be a dictionary.")
        ticket_id = ticket.get("id")
        if (not isinstance(ticket_id, str) or len(ticket_id) < 2
                or ticket_id[0] != "T" or not ticket_id[1:].isdigit()
                or int(ticket_id[1:]) < 1):
            raise ValueError("Existing ticket has an invalid ID format.")
        if ticket_id in seen_ids:
            raise ValueError(f"Duplicate ticket ID found: {ticket_id}")
        seen_ids.add(ticket_id)


def create_ticket(title, category, urgency, affected_users, tickets):
    """Validate, create, and append a ticket without partial mutation."""
    validate_ticket_data(title, category, urgency, affected_users)
    validate_existing_tickets(tickets)

    existing_numbers = [
        int(ticket["id"][1:]) for ticket in tickets
    ]
    ticket_id = f"T{max(existing_numbers, default=0) + 1:03d}"
    ticket = {
        "id": ticket_id,
        "title": title.strip(),
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": calculate_priority(urgency, affected_users),
        "status": "open",
        "assigned_to": None,
        "notes": [],
    }
    tickets.append(ticket)
    return ticket
