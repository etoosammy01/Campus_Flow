# CampusFlow — Design Decisions

## 1. Ticket Data Structure

Tickets will initially be represented as Python dictionaries stored in a shared list.

Each ticket contains:
- `id`
- `title`
- `category`
- `urgency`
- `affected_users`
- `priority`
- `status`
- `assigned_to`

## 2. Engineer Responsibilities

- Engineer A: ticket creation, input validation, and priority calculation.
- Engineer B: assignment, lifecycle management, work queue, and reports.

## 3. Ticket Workflow

- New tickets start with status `open`.
- Tickets must be assigned before moving to `in_progress`.
- Tickets can progress from `open` to `in_progress` to `resolved`.
- Resolved tickets must be explicitly reopened to `open` before further modification.

## 4. Error Handling

Invalid operations must be rejected without corrupting ticket data. The team will agree on a consistent error-handling approach before integrating the features.

## 5. Testing

Business logic will be tested independently using Python's standard `unittest` library.

## 6. Persistence

The team will use JSON storage and agree on shared loading and saving interfaces before integration.

## Status

Proposed decisions pending confirmation by both engineers.