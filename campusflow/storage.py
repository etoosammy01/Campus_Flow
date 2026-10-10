
import json
from pathlib import Path


def save_tickets(tickets, file_path="tickets.json"):
    """Save a list of tickets to a JSON file."""
    path = Path(file_path)

    with path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def load_tickets(file_path="tickets.json"):
    """Load tickets from a JSON file."""
    path = Path(file_path)

    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        tickets = json.load(file)

    if not isinstance(tickets, list):
        raise ValueError("The ticket file must contain a JSON list.")

    return tickets
