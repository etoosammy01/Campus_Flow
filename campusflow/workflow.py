"""Ticket assignment, status transitions, and the open work queue."""

from campusflow.tickets import STATUSES, validate_existing_tickets


def _find_ticket(tickets, ticket_id):
    validate_existing_tickets(tickets)
    matches = [ticket for ticket in tickets if ticket["id"] == ticket_id]
    if not matches:
        raise ValueError(f"Ticket {ticket_id} not found.")
    return matches[0]


def assign_ticket(tickets, ticket_id, staff_name):
    """Assign an open or in-progress ticket to a nonblank staff label."""
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name cannot be empty.")
    ticket = _find_ticket(tickets, ticket_id)
    if not isinstance(ticket.get("status"), str) or ticket["status"] not in STATUSES:
        raise ValueError("Ticket has an invalid status.")
    if ticket.get("status") == "resolved":
        raise ValueError("Reopen the ticket before modifying it.")
    ticket["assigned_to"] = staff_name.strip()
    return ticket


def change_status(tickets, ticket_id, new_status):
    """Apply a legal workflow transition after validating the request."""
    if not isinstance(new_status, str) or new_status not in STATUSES:
        raise ValueError(f"Invalid status: {new_status}")
    ticket = _find_ticket(tickets, ticket_id)
    current_status = ticket.get("status")
    if not isinstance(current_status, str) or current_status not in STATUSES:
        raise ValueError("Ticket has an invalid status.")

    if current_status == "resolved":
        if new_status != "open":
            raise ValueError(
                "Resolved tickets must be reopened before further changes."
            )
        ticket["status"] = "open"
        return ticket

    if current_status == "open" and new_status == "in_progress":
        if not ticket.get("assigned_to"):
            raise ValueError("Ticket must be assigned before work can begin.")

    transitions = {
        "open": {"in_progress"},
        "in_progress": {"resolved"},
    }
    if new_status not in transitions.get(current_status, set()):
        raise ValueError(
            f"Cannot change status from {current_status} to {new_status}."
        )
    ticket["status"] = new_status
    return ticket


def get_work_queue(tickets):
    """Return only open tickets, sorted by priority and numeric ticket ID."""
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    open_tickets = [ticket for ticket in tickets if ticket.get("status") == "open"]
    return sorted(
        open_tickets,
        key=lambda ticket: (
            priority_order.get(ticket.get("priority"), 4),
            int(ticket["id"][1:]),
        ),
    )
