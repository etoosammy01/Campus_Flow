# CampusFlow

CampusFlow is a command-line helpdesk ticket management system
that helps an organization record, prioritize, assign, and track
technical support requests.

## Features

- Create support tickets with unique IDs.
- Validate ticket information.
- Automatically calculate ticket priorities.
- Assign tickets to staff members.
- Track ticket status and enforce workflow rules.
- Display tickets in a priority-based work queue.
- Generate reports by ticket status and priority.
- Save and load ticket data using JSON.
- Run automated tests using Python's unittest framework.

## Ticket Categories

- Network
- Hardware
- Software
- Other

## Priority Rules

- Critical: High urgency AND at least 10 affected users.
- High: High urgency OR at least 10 affected users.
- Medium: Medium urgency OR at least 3 affected users.
- Low: All other valid cases.

Rules are evaluated from highest priority to lowest priority.

## Ticket Workflow

Tickets follow these status transitions:

- Open -> In Progress
- In Progress -> Resolved
- Resolved -> Open (reopening)

A ticket must be assigned before work can begin.
A resolved ticket must be reopened before further status changes.

## Project Structure

campusflow/
    __init__.py
    app.py
    tickets.py
    workflow.py
    reports.py
    storage.py

tests/
    test_tickets.py
    test_workflow.py
    test_reports.py
    test_storage.py

README.md

## Requirements

- Python 3.10 or later

## Running the Application

From the project root, run:

    python3 -m campusflow.app

## Running Tests

Run the automated test suite with:

    python3 -m unittest discover -s tests -v

## Data Storage

Ticket records are stored in a JSON file named tickets.json.
If the file does not exist, the application starts with an empty
ticket list.

## Author

CampusFlow was developed as a Python engineering assessment project.
