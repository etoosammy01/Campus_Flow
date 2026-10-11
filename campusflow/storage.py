import json
from pathlib import Path


def save_tickets(tickets, file_path="tickets.json"):
    """Save a list of tickets to a JSON file."""
    path = Path(file_path)

    with path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def load_tickets(file_path="tickets.json"):
    """Load tickets from a JSON file and validate the records."""
    path = Path(file_path)

    # Start with an empty ticket list if the file doesn't exist.
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        tickets = json.load(file)

    # The top-level JSON value must be a list.
    if not isinstance(tickets, list):
        raise ValueError("The ticket file must contain a JSON list.")

    required_fields = {
        "id",
        "title",
        "category",
        "urgency",
        "affected_users",
        "priority",
        "status",
        "assigned_to",
    }

    seen_ids = set()

    for ticket in tickets:
        # Each record must be a dictionary.
        if not isinstance(ticket, dict):
            raise ValueError("Every ticket record must be a JSON object.")

        # Every ticket must contain all required fields.
        if not required_fields.issubset(ticket):
            raise ValueError("A ticket record is missing required fields.")

        ticket_id = ticket["id"]

        # Ticket IDs must be strings.
        if not isinstance(ticket_id, str):
            raise ValueError("Every ticket ID must be a string.")

        # Reject duplicate IDs.
        if ticket_id in seen_ids:
            raise ValueError(f"Duplicate ticket ID found: {ticket_id}")

        seen_ids.add(ticket_id)

    return tickets