

def assign_ticket(tickets, ticket_id, staff_name):
    """Assign an existing ticket to a staff member."""

    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name cannot be empty.")

    for ticket in tickets:
        if ticket["id"] == ticket_id:

            if ticket["status"] == "resolved":
                raise ValueError(
                    "Reopen the ticket before modifying it."
                )

            ticket["assigned_to"] = staff_name.strip()
            return ticket

    raise ValueError(f"Ticket {ticket_id} not found.")


def change_status(tickets, ticket_id, new_status):
    """Change a ticket's status while enforcing workflow rules."""

    allowed_statuses = {"open", "in_progress", "resolved"}

    if new_status not in allowed_statuses:
        raise ValueError(f"Invalid status: {new_status}")

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            current_status = ticket["status"]

            if current_status == "resolved":
                if new_status != "open":
                    raise ValueError(
                        "Resolved tickets must be reopened before further changes."
                    )
                ticket["status"] = "open"
                return ticket

            if current_status == "open" and new_status == "in_progress":
                if not ticket["assigned_to"]:
                    raise ValueError(
                        "Ticket must be assigned before work can begin."
                    )

            valid_transitions = {
                "open": {"in_progress"},
                "in_progress": {"resolved"},
            }

            if new_status not in valid_transitions.get(current_status, set()):
                raise ValueError(
                    f"Cannot change status from {current_status} to {new_status}."
                )

            ticket["status"] = new_status
            return ticket

    raise ValueError(f"Ticket {ticket_id} not found.")


def get_work_queue(tickets):
    """Return open tickets ordered by priority and ticket ID."""

    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    open_tickets = [
        ticket for ticket in tickets
        if ticket["status"] == "open"
    ]

    return sorted(
        open_tickets,
        key=lambda ticket: (
            priority_order.get(ticket["priority"], 4),
            int(ticket["id"][1:]),
        ),
    )
