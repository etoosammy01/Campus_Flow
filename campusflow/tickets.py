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

    # Category must be a string.
    if not isinstance(category, str):
        raise ValueError("Ticket category must be a string.")

    # The category must be one of the allowed values.
    if category not in ["Network", "Hardware", "Software", "Other"]:
        raise ValueError("Invalid ticket category.")

    # Urgency must be a string.
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be a string.")

    # The urgency must be one of the allowed values.
    if urgency not in ["low", "medium", "high"]:
        raise ValueError("Invalid urgency level.")

    # Affected users must be a positive integer, not a boolean.
    if isinstance(affected_users, bool) or not isinstance(affected_users, int) or affected_users <= 0:
        raise ValueError("Affected users must be a positive integer.")

def validate_existing_tickets(tickets):
    """Ensure existing ticket records have valid IDs."""

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Existing ticket record must be a dictionary.")

        ticket_id = ticket.get("id")

        if not isinstance(ticket_id, str):
            raise ValueError("Existing ticket must have a string ID.")

        if (
            len(ticket_id) < 2
            or ticket_id[0] != "T"
            or not ticket_id[1:].isdigit()
        ):
            raise ValueError("Existing ticket has an invalid ID format.")

def create_ticket(title, category, urgency, affected_users, tickets):
    """Validate, create, and store a new ticket."""

    # Validate the new ticket information first.
    validate_ticket_data(title, category, urgency, affected_users)

    # Reject malformed existing records before generating an ID.
    validate_existing_tickets(tickets)

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