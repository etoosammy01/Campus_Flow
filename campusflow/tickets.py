def calculate_priority(urgency, affected_users):
    """Calculate a ticket's priority using the assessment rules."""

    # Rule 1: High urgency and at least 10 affected users
    if urgency == "high" and affected_users >= 10:
        return "critical"

    # Rule 2: High urgency or at least 10 affected users
    if urgency == "high" or affected_users >= 10:
        return "high"

    # Rule 3: Medium urgency or at least 3 affected users
    if urgency == "medium" or affected_users >= 3:
        return "medium"

    # Rule 4: Everything else
    return "low"


def validate_ticket_data(title, category, urgency, affected_users):
    """Validate the information required to create a ticket."""

    # A ticket must have a title.
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be empty.")

    # Only these categories are allowed.
    if category not in ["Network", "Hardware", "Software", "Other"]:
        raise ValueError("Invalid ticket category.")

    # Only these urgency levels are allowed.
    if urgency not in ["low", "medium", "high"]:
        raise ValueError("Invalid urgency level.")

    # Affected users must be a positive integer, not a boolean.
    if isinstance(affected_users, bool) or not isinstance(affected_users, int) or affected_users <= 0:
        raise ValueError("Affected users must be a positive integer.")

def create_ticket(title, category, urgency, affected_users, tickets):
    """Validate, create, and store a new ticket."""

    # Reject invalid information before changing the ticket list.
    validate_ticket_data(title, category, urgency, affected_users)

    # Find the highest existing ticket number.
    existing_numbers = [
        int(ticket["id"][1:])
        for ticket in tickets
    ]

    # Generate the next ID.
    next_number = max(existing_numbers, default=0) + 1
    ticket_id = f"T{next_number:03d}"

    # Build the ticket using the shared structure.
    ticket = {
        "id": ticket_id,
        "title": title.strip(),
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": calculate_priority(urgency, affected_users),
        "status": "open",
        "assigned_to": None,
    }

    # Save the new ticket in the supplied list.
    tickets.append(ticket)

    return ticket