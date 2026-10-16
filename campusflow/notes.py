"""Business-layer operations for structured ticket notes."""


def add_note(tickets, ticket_id, author, message):
    """Add a note to a non-resolved ticket and return the new note.

    Args:
        tickets: The shared list of ticket dictionaries.
        ticket_id: ID of the ticket receiving the note.
        author: Nonblank staff/user label.
        message: Trimmed note text of 5 to 300 characters.

    Raises:
        ValueError: If the ticket, author, message, or workflow state is invalid.

    Note IDs are generated per ticket (N001, N002, ...) and are not consumed
    by rejected operations.
    """
    if not isinstance(author, str) or not author.strip():
        raise ValueError("Note author cannot be empty.")
    if not isinstance(message, str):
        raise ValueError("Note message must be text.")
    clean_message = message.strip()
    if not 5 <= len(clean_message) <= 300:
        raise ValueError("Note message must be 5 to 300 characters long.")

    if not isinstance(tickets, list):
        raise ValueError("Tickets must be stored in a list.")
    matches = [ticket for ticket in tickets
               if isinstance(ticket, dict) and ticket.get("id") == ticket_id]
    if not matches:
        raise ValueError(f"Ticket {ticket_id} not found.")
    if len(matches) > 1:
        raise ValueError(f"Duplicate ticket ID found: {ticket_id}")

    ticket = matches[0]
    status = ticket.get("status")
    if not isinstance(status, str) or status not in {"open", "in_progress", "resolved"}:
        raise ValueError("Ticket has an invalid status.")
    if ticket["status"] == "resolved":
        raise ValueError("Reopen the ticket before adding notes.")

    existing_notes = ticket.get("notes", [])
    if not isinstance(existing_notes, list):
        raise ValueError("Ticket notes must be stored in a list.")

    note_numbers = []
    seen = set()
    for note in existing_notes:
        if not isinstance(note, dict):
            raise ValueError("Existing note record must be a dictionary.")
        note_id = note.get("note_id")
        if (not isinstance(note_id, str) or len(note_id) < 2
                or note_id[0] != "N" or not note_id[1:].isdigit()
                or int(note_id[1:]) < 1):
            raise ValueError("Existing note has an invalid ID format.")
        if note_id in seen:
            raise ValueError(f"Duplicate note ID found: {note_id}")
        seen.add(note_id)
        note_numbers.append(int(note_id[1:]))

    note = {
        "note_id": f"N{max(note_numbers, default=0) + 1:03d}",
        "author": author.strip(),
        "message": clean_message,
    }
    # Only mutate after every validation succeeds.
    if "notes" not in ticket:
        ticket["notes"] = []
    ticket["notes"].append(note)
    ticket["notes"].sort(key=lambda item: int(item["note_id"][1:]))
    return note


def get_ticket_notes(tickets, ticket_id):
    """Return a ticket's notes in numeric note-ID order."""
    for ticket in tickets:
        if isinstance(ticket, dict) and ticket.get("id") == ticket_id:
            notes = ticket.get("notes", [])
            if not isinstance(notes, list):
                raise ValueError("Ticket notes must be stored in a list.")
            return sorted(notes, key=lambda item: int(item["note_id"][1:]))
    raise ValueError(f"Ticket {ticket_id} not found.")
