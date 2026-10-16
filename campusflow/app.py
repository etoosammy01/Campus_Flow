"""Interactive command-line interface for CampusFlow."""

import json

from campusflow.assessment import QUESTIONS, run_check
from campusflow.notes import add_note, get_ticket_notes
from campusflow.reports import format_report, generate_report
from campusflow.search import (
    CATEGORY_OPTIONS, PRIORITY_OPTIONS, STATUS_OPTIONS,
    normalize_filter, search_tickets, sort_by_priority,
)
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status, get_work_queue

DATA_FILE = "tickets.json"
CHECK_RESULTS_FILE = "engineering_check_results.json"


def ask_ticket_id():
    """Read a ticket ID; 't001' and ' T001 ' both become 'T001'."""
    return input("Ticket ID: ").strip().upper()


def ask_filter(prompt, allowed, label):
    """Re-prompt until the filter is blank (no filter) or a valid option."""
    while True:
        try:
            return normalize_filter(input(prompt), allowed, label)
        except ValueError as error:
            print(f"  {error}")


def display_tickets(tickets):
    """Display ticket details and ordered follow-up notes."""
    if not tickets:
        print("\nNo tickets found.")
        return
    for ticket in tickets:
        print(
            f"\n{ticket['id']} | {ticket['title']}"
            f"\n  Category: {ticket['category']}"
            f"\n  Urgency: {ticket['urgency']}"
            f"\n  Priority: {ticket['priority']}"
            f"\n  Status: {ticket['status']}"
            f"\n  Assigned to: {ticket['assigned_to'] or 'Unassigned'}"
            f"\n  Affected users: {ticket['affected_users']}"
        )
        notes = sorted(
            ticket.get("notes", []),
            key=lambda item: int(item["note_id"][1:]),
        )
        if notes:
            print("  Notes:")
            for note in notes:
                print(f"    {note['note_id']} — {note['author']}: {note['message']}")


def create_new_ticket(tickets):
    """Collect details and create a ticket."""
    title = input("Ticket title: ")
    category = input("Category (Network/Hardware/Software/Other): ").strip().title()
    urgency = input("Urgency (low/medium/high): ").strip().lower()
    raw_users = input("Number of affected users: ").strip()
    try:
        if not (raw_users.isascii() and raw_users.isdigit()):
            raise ValueError("Affected users must be a positive whole number.")
        affected_users = int(raw_users)
        ticket = create_ticket(title, category, urgency, affected_users, tickets)
        save_tickets(tickets, DATA_FILE)
        print(f"Ticket {ticket['id']} created successfully.")
    except ValueError as error:
        print(f"Could not create ticket: {error}")
    except OSError as error:
        print(f"Ticket was created in memory but could not be saved: {error}")


def assign_existing_ticket(tickets):
    ticket_id = ask_ticket_id()
    staff_name = input("Staff member's name: ")
    try:
        assign_ticket(tickets, ticket_id, staff_name)
        save_tickets(tickets, DATA_FILE)
        print("Ticket assigned successfully.")
    except (ValueError, OSError) as error:
        print(f"Could not assign ticket: {error}")


def update_ticket_status(tickets):
    ticket_id = ask_ticket_id()
    print("Statuses: in_progress, resolved, open (reopen)")
    new_status = input("New status: ").strip()
    try:
        change_status(tickets, ticket_id, new_status)
        save_tickets(tickets, DATA_FILE)
        print("Ticket status updated successfully.")
    except (ValueError, OSError) as error:
        print(f"Could not update status: {error}")


def add_ticket_note(tickets):
    ticket_id = ask_ticket_id()
    author = input("Note author: ")
    message = input("Note (5–300 characters): ")
    try:
        note = add_note(tickets, ticket_id, author, message)
        save_tickets(tickets, DATA_FILE)
        print(f"Added note {note['note_id']} to {ticket_id}.")
    except (ValueError, OSError) as error:
        print(f"Could not add note: {error}")


def show_notes(tickets):
    ticket_id = ask_ticket_id()
    try:
        notes = get_ticket_notes(tickets, ticket_id)
        if not notes:
            print("This ticket has no notes.")
        for note in notes:
            print(f"{note['note_id']} — {note['author']}: {note['message']}")
    except ValueError as error:
        print(error)


def ask_search_criteria():
    """Collect search inputs. Invalid filters re-prompt instead of aborting."""
    query = input("Title contains (leave blank for all titles): ")
    category = ask_filter("Category filter (blank for any): ", CATEGORY_OPTIONS, "Category")
    status = ask_filter("Status filter (blank for any): ", STATUS_OPTIONS, "Status")
    priority = ask_filter("Priority filter (blank for any): ", PRIORITY_OPTIONS, "Priority")
    return query, category, status, priority


def search_ticket_list(tickets, sort=False):
    """Read-only search view. With sort=True, order by priority then ID."""
    query, category, status, priority = ask_search_criteria()
    results = search_tickets(tickets, query, category, status, priority)
    if sort:
        results = sort_by_priority(results)
    print(f"\nSearch results: {len(results)}")
    display_tickets(results)


def show_work_queue(tickets):
    print("\n=== Open Ticket Work Queue ===")
    display_tickets(get_work_queue(tickets))


def show_report(tickets):
    print("\n=== Ticket Report ===")
    print(format_report(generate_report(tickets)))


def run_understanding_check():
    """Run the six-question check, then save the score and explanations."""
    print("\n=== Engineering Understanding Check ===")
    result = run_check(QUESTIONS, input, print)
    print(f"\nScore: {result['score']}/{result['out_of']}")
    try:
        with open(CHECK_RESULTS_FILE, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=2)
            file.write("\n")
        print(f"Answers and explanations saved to {CHECK_RESULTS_FILE}.")
    except OSError as error:
        print(f"Could not save results: {error}")


def reload_ticket_data(current_tickets):
    """Replace in-memory data only after a complete successful load."""
    try:
        reloaded = load_tickets(DATA_FILE)
    except (ValueError, OSError) as error:
        print(f"Reload rejected; current in-memory tickets were kept: {error}")
        return current_tickets
    print(f"Reloaded {len(reloaded)} ticket(s).")
    return reloaded


def main():
    """Run the CampusFlow command-line application."""
    try:
        tickets = load_tickets(DATA_FILE)
    except (ValueError, OSError) as error:
        print(f"Could not load tickets: {error}")
        return

    actions = {
        "1": ("Create ticket", lambda: create_new_ticket(tickets)),
        "2": ("View all tickets", lambda: display_tickets(tickets)),
        "3": ("Assign ticket", lambda: assign_existing_ticket(tickets)),
        "4": ("Change ticket status", lambda: update_ticket_status(tickets)),
        "5": ("View open work queue", lambda: show_work_queue(tickets)),
        "6": ("View reports", lambda: show_report(tickets)),
        "7": ("Add a note", lambda: add_ticket_note(tickets)),
        "8": ("View ticket notes", lambda: show_notes(tickets)),
        "9": ("Search tickets", lambda: search_ticket_list(tickets)),
        "10": ("Reload tickets from JSON", None),
        "11": ("Engineering Understanding Check", run_understanding_check),
        "12": ("Search tickets (sorted by priority)",
               lambda: search_ticket_list(tickets, sort=True)),
    }
    while True:
        print("\n====== CampusFlow Next ======")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            return
        if choice not in actions:
            print("Invalid choice. Please select a listed option.")
            continue
        if choice == "10":
            tickets = reload_ticket_data(tickets)
        else:
            actions[choice][1]()


if __name__ == "__main__":
    main()