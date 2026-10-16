# CampusFlow Next

CampusFlow Next is a dependency-free Python command-line helpdesk application for creating, prioritizing, assigning, searching, and tracking support tickets.

## Features

- Create validated tickets with unique sequential IDs (`T001`, `T002`, ...).
- Calculate critical/high/medium/low priority using the original precedence rules.
- Assign staff and enforce the open → in_progress → resolved workflow, including reopening.
- Add structured follow-up notes to open or in-progress tickets (`N001`, `N002`, ... per ticket).
- Display notes in numeric ID order and preserve them through resolution/reopening.
- Search title text using a case-insensitive substring and combine optional category, status, and priority filters with AND.
- Keep the original open-only work queue, sorted by priority and numeric ticket ID.
- Report totals, status/priority/category counts, unresolved/resolved counts, and resolution rate.
- Validate the entire JSON collection before saving/loading; use atomic saves and reject corrupt records without replacing in-memory state.
- Migrate older ticket records by adding an empty `notes` list.
- Run a six-question Engineering Understanding Check with validated A/B/C/D answers, a score out of six, two short explanations, and a local results file.

## Ticket rules

### Categories and urgency
Categories: `Network`, `Hardware`, `Software`, `Other`.
Urgency: `low`, `medium`, `high`.
The title must not be blank, and `affected_users` must be a positive integer (booleans, floats, and numeric strings are rejected).

### Priority
1. **Critical:** high urgency AND at least 10 affected users.
2. **High:** high urgency OR at least 10 affected users.
3. **Medium:** medium urgency OR at least 3 affected users.
4. **Low:** all other valid cases.

Rules are evaluated from highest to lowest priority.

### Workflow
- `open` → `in_progress` → `resolved`
- `resolved` → `open` to reopen.
- A ticket must be assigned before moving from `open` to `in_progress`.
- Resolved tickets cannot be reassigned or receive notes until reopened.
- Notes require a nonblank author and a trimmed message of 5–300 characters.

## Running the app

Python 3.10+ is required. No third-party packages are needed.

From the repository root:

```bash
python3 -m campusflow.app
```

The JSON data file `tickets.json` is created in the current working directory when the first change is saved. The application validates and loads it on startup. Menu option 10 reloads from disk; a failed reload leaves the current in-memory collection unchanged.

The Engineering Understanding Check writes `engineering_check_results.json` to the current working directory. Both runtime files are ignored by Git.

## Running tests

```bash
python3 -m unittest discover -v
```

The suite covers priority precedence, ticket validation, safe workflow mutations, notes and note-ID continuity, JSON validation/migration, search, reporting, and the understanding check.

## Project structure

```text
campusflow/
  app.py
  assessment.py
  notes.py
  reports.py
  search.py
  storage.py
  tickets.py
  workflow.py
tests/
  test_assessment.py
  test_notes.py
  test_reports.py
  test_search.py
  test_storage.py
  test_tickets.py
  test_workflow.py
docs/
  baseline-check.md
  design-decisions.md
  ai-learning-log.md
  edge-case-tests.md
  final-cli-demo.md
```

## Collaboration and submission

See `docs/baseline-check.md` for the pre-change baseline and `docs/edge-case-tests.md` for the documented additional test. Peer review, PR links, final `main` SHA, team names, and personal reflections must be filled in by the team from the real GitHub workflow; do not invent them.
