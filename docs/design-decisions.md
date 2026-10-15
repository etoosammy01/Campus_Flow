# CampusFlow Next — Design Decisions

## 1. Ticket data

Tickets remain dictionaries in a list, preserving the original JSON list format. The original fields remain and each ticket now has `notes`, initially an empty list. Each note contains `note_id`, `author`, and `message`.

## 2. Validation and errors

Business/data-layer functions raise `ValueError` for invalid user actions. The CLI catches these errors and displays a friendly message. Validation occurs before a mutation is applied. Ticket IDs and note IDs are checked for valid format and uniqueness.

## 3. Workflow

Tickets start `open`; assigned tickets can move to `in_progress`, then `resolved`. Resolved tickets must be reopened to `open` before reassignment or adding notes. Existing notes are retained through these transitions.

## 4. Search and queue

Search is a case-insensitive substring match on the title. Supplied category, status, and priority filters are combined with AND. Search results are sorted by priority then numeric ticket ID. The original queue remains limited to `open` tickets.

## 5. Reporting

The report includes totals by status, priority, and category, unresolved count (`open` + `in_progress`), resolved count, and resolution rate. An empty collection has a 0% resolution rate.

## 6. Persistence and migration

JSON remains a list of ticket objects. The loader migrates older records by adding `notes: []`, validates the complete collection, and returns a new collection only when every record is valid. Reload assigns the new collection only after successful loading. Saving validates first and uses a temporary file plus atomic replacement to avoid leaving a partially written JSON file.

## 7. Testing

Tests use the standard-library `unittest` module and temporary files. They cover original behaviour and new requirements including invalid actions leaving state unchanged, note ID continuity, corrupt JSON, duplicate IDs, search filters, reporting, and the understanding check.

## 8. Collaboration boundaries

Engineer A owns validation, mutation safety, notes, persistence, and related tests. Engineer B owns CLI experience, search, reports, and the shared understanding check. Both engineers must verify the integrated diff and tests before approving a pull request. Actual PR review/approval evidence must be recorded from GitHub.
