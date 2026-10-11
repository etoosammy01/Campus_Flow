
import json
from campusflow.tickets import create_ticket
from campusflow.workflow import (
    assign_ticket,
    change_status,
    get_work_queue,
)
from campusflow.reports import generate_report
from campusflow.storage import load_tickets, save_tickets


DATA_FILE = "tickets.json"


def display_tickets(tickets):
    """Display all tickets."""
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



def create_new_ticket(tickets):
    """Collect details and create a ticket."""
    title = input("Ticket title: ").strip()
    category = input(
        "Category (Network/Hardware/Software/Other): "
    ).strip().title()
    urgency = input("Urgency (low/medium/high): ").strip().lower()

    try:
        affected_users = int(input("Number of affected users: "))

        ticket = create_ticket(
            title, category, urgency, affected_users, tickets
        )
        save_tickets(tickets, DATA_FILE)
        print(f"Ticket {ticket['id']} created successfully.")

    except ValueError as error:
        print(f"Could not create ticket: {error}")



def assign_existing_ticket(tickets):
    ticket_id = input("Ticket ID: ").strip()
    staff_name = input("Staff member's name: ")

    try:
        assign_ticket(tickets, ticket_id, staff_name)
        save_tickets(tickets, DATA_FILE)
        print("Ticket assigned successfully.")
    except ValueError as error:
        print(f"Could not assign ticket: {error}")


def update_ticket_status(tickets):
    ticket_id = input("Ticket ID: ").strip()
    print("Statuses: in_progress, resolved, open (reopen)")
    new_status = input("New status: ").strip()

    try:
        change_status(tickets, ticket_id, new_status)
        save_tickets(tickets, DATA_FILE)
        print("Ticket status updated successfully.")
    except ValueError as error:
        print(f"Could not update status: {error}")


def show_work_queue(tickets):
    queue = get_work_queue(tickets)
    print("\n=== Open Ticket Work Queue ===")
    display_tickets(queue)


def show_report(tickets):
    report = generate_report(tickets)

    print("\n=== Ticket Report ===")
    print(f"Total tickets: {report['total']}")

    print("\nBy status:")
    for status, count in report["by_status"].items():
        print(f"  {status}: {count}")

    print("\nBy priority:")
    for priority, count in report["by_priority"].items():
        print(f"  {priority}: {count}")


def main():
    """Run the CampusFlow command-line application."""
    try:
        tickets = load_tickets(DATA_FILE)
    except json.JSONDecodeError as error:
        print(f"Ticket file contains invalid JSON: {error}")
        return
    except (ValueError, OSError) as error:
        print(f"Could not load tickets: {error}")
        return

    while True:
        print("\n====== CampusFlow ======")
        print("1. Create ticket")
        print("2. View all tickets")
        print("3. Assign ticket")
        print("4. Change ticket status")
        print("5. View work queue")
        print("6. View reports")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_new_ticket(tickets)
        elif choice == "2":
            display_tickets(tickets)
        elif choice == "3":
            assign_existing_ticket(tickets)
        elif choice == "4":
            update_ticket_status(tickets)
        elif choice == "5":
            show_work_queue(tickets)
        elif choice == "6":
            show_report(tickets)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a listed option.")


if __name__ == "__main__":
    main()
