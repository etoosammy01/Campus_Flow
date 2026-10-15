"""Validated, atomic JSON persistence for ticket collections."""

import json
import os
import tempfile
from pathlib import Path

from campusflow.tickets import (
    STATUSES, calculate_priority,
    validate_existing_tickets, validate_ticket_data,
)

BASE_FIELDS = {
    "id", "title", "category", "urgency", "affected_users",
    "priority", "status", "assigned_to",
}
NOTE_FIELDS = {"note_id", "author", "message"}


def validate_ticket_collection(tickets):
    """Validate the full collection before saving or accepting loaded data."""
    validate_existing_tickets(tickets)
    for ticket in tickets:
        missing = BASE_FIELDS - ticket.keys()
        if missing:
            raise ValueError(
                f"Ticket {ticket.get('id', '<unknown>')} is missing fields: "
                f"{', '.join(sorted(missing))}"
            )
        validate_ticket_data(
            ticket["title"], ticket["category"], ticket["urgency"],
            ticket["affected_users"],
        )
        expected_priority = calculate_priority(
            ticket["urgency"], ticket["affected_users"]
        )
        if ticket["priority"] != expected_priority:
            raise ValueError(f"Ticket {ticket['id']} has inconsistent priority.")
        if not isinstance(ticket["status"], str) or ticket["status"] not in STATUSES:
            raise ValueError(f"Ticket {ticket['id']} has an invalid status.")
        assigned = ticket["assigned_to"]
        if assigned is not None and (
            not isinstance(assigned, str) or not assigned.strip()
        ):
            raise ValueError(f"Ticket {ticket['id']} has an invalid assignee.")
        if ticket["status"] == "in_progress" and not assigned:
            raise ValueError(
                f"Ticket {ticket['id']} is in progress but has no assignee."
            )

        notes = ticket.get("notes")
        if not isinstance(notes, list):
            raise ValueError(f"Ticket {ticket['id']} notes must be a list.")
        note_ids = set()
        for note in notes:
            if not isinstance(note, dict) or not NOTE_FIELDS.issubset(note):
                raise ValueError(f"Ticket {ticket['id']} has an invalid note record.")
            note_id = note["note_id"]
            if (not isinstance(note_id, str) or len(note_id) < 2
                    or note_id[0] != "N" or not note_id[1:].isdigit()
                    or int(note_id[1:]) < 1):
                raise ValueError(f"Ticket {ticket['id']} has an invalid note ID.")
            if note_id in note_ids:
                raise ValueError(
                    f"Ticket {ticket['id']} has duplicate note ID {note_id}."
                )
            note_ids.add(note_id)
            if not isinstance(note["author"], str) or not note["author"].strip():
                raise ValueError(f"Ticket {ticket['id']} has a blank note author.")
            message = note["message"]
            if not isinstance(message, str) or not 5 <= len(message.strip()) <= 300:
                raise ValueError(f"Ticket {ticket['id']} has an invalid note message.")


def save_tickets(tickets, file_path="tickets.json"):
    """Validate and atomically save tickets as a JSON list."""
    validate_ticket_collection(tickets)
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False
        ) as file:
            temp_name = file.name
            json.dump(tickets, file, indent=4)
            file.write("\n")
        os.replace(temp_name, path)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def load_tickets(file_path="tickets.json"):
    """Load and fully validate JSON; migrate older tickets by adding notes=[]."""
    path = Path(file_path)
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            loaded = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Ticket file contains invalid JSON: {error}") from error

    if not isinstance(loaded, list):
        raise ValueError("The ticket file must contain a JSON list.")

    # Work on a fresh collection so invalid data never partially mutates app state.
    tickets = []
    for record in loaded:
        if not isinstance(record, dict):
            raise ValueError("Every ticket record must be a JSON object.")
        migrated = dict(record)
        # Backward-compatible migration from the original eight-field schema.
        migrated.setdefault("notes", [])
        tickets.append(migrated)

    validate_ticket_collection(tickets)
    return tickets
