"""Interactive command-line interface for CampusFlow."""

import json

from campusflow.assessment import QUESTIONS, score_answers
from campusflow.notes import add_note, get_ticket_notes
from campusflow.reports import generate_report
from campusflow.search import search_tickets
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status, get_work_queue

DATA_FILE = "tickets.json"
CHECK_RESULTS_FILE = "engineering_check_results.json"


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
    try:
        affected_users = int(input("Number of affected users: "))
        ticket = create_ticket(title, category, urgency, affected_users, tickets)
        save_tickets(tickets, DATA_FILE)
        print(f"Ticket {ticket['id']} created successfully.")
    except ValueError as error:
        print(f"Could not create ticket: {error}")
    except OSError as error:
        print(f"Ticket was created in memory but could not be saved: {error}")


def assign_existing_ticket(tickets):
    ticket_id = input("Ticket ID: ").strip()
    staff_name = input("Staff member's name: ")
    try:
        assign_ticket(tickets, ticket_id, staff_name)
        save_tickets(tickets, DATA_FILE)
        print("Ticket assigned successfully.")
    except (ValueError, OSError) as error:
        print(f"Could not assign ticket: {error}")


def update_ticket_status(tickets):
    ticket_id = input("Ticket ID: ").strip()
    print("Statuses: in_progress, resolved, open (reopen)")
    new_status = input("New status: ").strip()
    try:
        change_status(tickets, ticket_id, new_status)
        save_tickets(tickets, DATA_FILE)
        print("Ticket status updated successfully.")
    except (ValueError, OSError) as error:
        print(f"Could not update status: {error}")


def add_ticket_note(tickets):
    ticket_id = input("Ticket ID: ").strip()
    author = input("Note author: ")
    message = input("Note (5–300 characters): ")
    try:
        note = add_note(tickets, ticket_id, author, message)
        save_tickets(tickets, DATA_FILE)
        print(f"Added note {note['note_id']} to {ticket_id}.")
    except (ValueError, OSError) as error:
        print(f"Could not add note: {error}")


def show_notes(tickets):
    ticket_id = input("Ticket ID: ").strip()
    try:
        notes = get_ticket_notes(tickets, ticket_id)
        if not notes:
            print("This ticket has no notes.")
        for note in notes:
            print(f"{note['note_id']} — {note['author']}: {note['message']}")
    except ValueError as error:
        print(error)


def search_ticket_list(tickets):
    query = input("Title contains (leave blank for all titles): ")
    category = input("Category filter (blank for any): ").strip()
    status = input("Status filter (blank for any): ").strip()
    priority = input("Priority filter (blank for any): ").strip()
    try:
        results = search_tickets(
            tickets,
            query=query,
            category=category or None,
            status=status or None,
            priority=priority or None,
        )
        print(f"\nSearch results: {len(results)}")
        display_tickets(results)
    except ValueError as error:
        print(f"Search failed: {error}")


def show_work_queue(tickets):
    print("\n=== Open Ticket Work Queue ===")
    display_tickets(get_work_queue(tickets))


def show_report(tickets):
    report = generate_report(tickets)
    print("\n=== Ticket Report ===")
    print(f"Total tickets: {report['total']}")
    print(f"Unresolved (open + in progress): {report['unresolved']}")
    print(f"Resolved: {report['resolved']}")
    print(f"Resolution rate: {report['resolution_rate']:.1f}%")
    for key, label in (
        ("by_status", "By status"),
        ("by_priority", "By priority"),
        ("by_category", "By category"),
    ):
        print(f"\n{label}:")
        for name, count in report[key].items():
            print(f"  {name}: {count}")


def run_understanding_check():
    """Run the six-question check, retry invalid answers, and save explanations."""
    answers = []
    explanations = []
    print("\n=== Engineering Understanding Check ===")
    for number, question in enumerate(QUESTIONS, start=1):
        print(f"\n{number}. {question['question']}")
        for letter, option in question["options"].items():
            print(f"  {letter}. {option}")
        while True:
            answer = input("Answer (A/B/C/D): ").strip().upper()
            if answer in {"A", "B", "C", "D"}:
                break
            print("Please enter A, B, C, or D.")
        answers.append(answer)
        if number in {1, 2, 3, 4, 5, 6} and number in {1, 2}:
            explanations.append({
                "question": number,
                "answer": answer,
                "explanation": input("Briefly explain your answer: ").strip(),
            })
    score = score_answers(answers)
    result = {"score": score, "out_of": len(QUESTIONS),
              "answers": answers, "explanations": explanations}
    try:
        with open(CHECK_RESULTS_FILE, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=2)
            file.write("\n")
        print(f"Score: {score}/{len(QUESTIONS)}")
        print(f"Answers and explanations saved to {CHECK_RESULTS_FILE}.")
        for entry in explanations:
            print(f"Explanation for Q{entry['question']}: {entry['explanation']}")
    except OSError as error:
        print(f"Score: {score}/{len(QUESTIONS)} (could not save results: {error})")


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
