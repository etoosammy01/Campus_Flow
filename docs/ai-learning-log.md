# AI Learning Log — Engineer A

## Entry 1: Understanding the Priority Engine

**Task:** Implement the ticket priority calculation rules.

**AI assistance:** I used AI to help translate the assessment's priority rules
into Python conditional statements.

**What I learned:** The order of conditions matters. Critical priority must
be checked before high priority because a ticket with high urgency and at
least 10 affected users must be classified as critical.

I also learned the difference between `and` and `or` when combining conditions.

**Independent verification:** I wrote unit tests for critical, high, medium,
and low priorities and ran them using Python's unittest module. All tests passed.

## Entry 2: Input Validation and Ticket Creation

**Task:** Validate ticket information and create ticket dictionaries.

**AI assistance:** I used AI to understand how to validate titles, categories,
urgency levels, and affected-user counts, and how to create ticket records.

**What I learned:** Raising `ValueError` allows invalid data to be rejected
before the ticket list is modified. I also learned how `list.append()` adds
a new ticket without replacing existing tickets.

**Independent verification:** I wrote tests for valid data, invalid categories,
invalid urgency, empty titles, and invalid affected-user counts. I also tested
that a newly created ticket contains the required fields.

## Entry 3: Improving Ticket ID Generation

**Task:** Generate sequential ticket IDs without duplicating existing IDs.

**AI suggestion and improvement:** The initial approach used
`len(tickets) + 1` to generate the next ID. I learned that this can produce
a duplicate if the existing ticket IDs contain gaps. I improved the approach
to find the highest existing ticket number and increment it.

**What I learned:** Counting records is not always the same as identifying
the next available sequential ID.

**Independent verification:** I added a test with existing IDs `T001` and
`T003` and checked that the next ticket receives `T004`. I ran the unit test
suite to verify the change.


## Engineer B — AI Learning Log

### Interaction 1: Normalizing CLI Input

- **Task:** Make ticket creation accept category and urgency input without requiring exact capitalization.
- **AI assistance:** Suggested normalizing category input with `.strip().title()` and urgency with `.strip().lower()`.
- **My action:** Updated the CLI input handling and tested creating a ticket using lowercase `other`.
- **Outcome:** Ticket creation succeeded with the normalized category.

### Interaction 2: Debugging Storage Tests

- **Task:** Test saving and loading tickets from JSON.
- **AI assistance:** Helped identify that unexpected text after the Python test code caused a syntax error.
- **My action:** Replaced the test file with valid Python test code and reran the suite.
- **Outcome:** The storage tests passed as part of the integrated test suite.

### Interaction 3: Verifying Persistence and Integration

- **Task:** Check that saved tickets remain available after restarting the CLI.
- **AI assistance:** Suggested testing ticket creation, restarting the application, and checking the saved ticket.
- **My action:** Created a ticket, restarted the application, and confirmed the ticket appeared again. I also ran the unit tests.
- **Outcome:** The ticket persisted, and the integrated suite reported 44 passing tests at that stage.

### Independent Verification

I did not treat AI-generated suggestions as automatically correct. I checked the proposed changes by running the application and tests, and corrected the storage test file when it contained invalid Python. I will record any additional issues discovered during final integration review.


## CampusFlow Next — Engineer A implementation cycles (AI-assisted draft)

> Review and personalize these entries before submission. This log records work performed in this assisted implementation; each engineer should be able to explain the decisions and test results independently.

### Cycle 1 — Duplicate IDs and mutation safety

- **Concept gap addressed:** Why validating ID format alone does not guarantee uniqueness, and how to reject an invalid operation before changing a shared list.
- **Exact request in this conversation:** “here is the zip file, just do every then giude to push it and explain later for time sake”
- **AI guidance:** Track previously seen ticket IDs with a set; validate inputs before appending or mutating; raise `ValueError` for invalid business actions.
- **Unrelated tiny experiment:** Ran a separate Python list-comprehension experiment, `print([n * n for n in range(5)])`, which returned `[0, 1, 4, 9, 16]`.
- **Independent verification:** The regression test `test_duplicate_existing_ids_rejected_without_mutation` checks that duplicate IDs raise `ValueError` and the collection remains unchanged. The integrated suite passes.
- **Engineering decision:** Keep ticket IDs generated from the highest existing numeric suffix, and explicitly reject duplicate IDs rather than attempting to repair an ambiguous existing collection.

### Cycle 2 — Safe JSON persistence and note-ID continuity

- **Concept gap addressed:** How to avoid accepting a partially valid JSON collection and how to protect the current in-memory data when reload fails.
- **Exact task discussed:** Implement CampusFlow Next's required JSON validation, note persistence, and ID continuity from the supplied assessment.
- **AI guidance:** Load into a fresh collection, migrate old records by adding `notes: []`, validate the entire collection before returning it, and replace the saved file atomically only after validation.
- **Independent verification:** Tests cover invalid JSON, duplicate ticket IDs, inconsistent priority, old-schema migration, note save/load, and next ticket/note ID generation. The CLI reload test checks that a failed reload returns the original collection unchanged.
- **Changed after evidence:** An initial generated storage implementation wrote a literal backslash-plus-`n` after JSON instead of a newline. The storage round-trip tests failed with `JSONDecodeError: Extra data`. The write was corrected to a real newline, then the complete suite passed.
- **Engineering decision:** Keep JSON as a list for compatibility, validate before saving, and use a temporary file plus `os.replace` to avoid partially written data.

### Verification status

The latest local run reported **80 tests passing, 0 failures, 0 errors**. Before submission, rerun the command in the actual working repository and record its output. Engineer A should be ready to explain `validate_existing_tickets`, `add_note`, `validate_ticket_collection`, and atomic file replacement without relying on this log alone.

## Engineer B — Required personal entries

Engineer B must add two truthful AI-learning cycles with their own exact questions, a concept gap, guidance received, unrelated tiny experiment, independent verification, and final decision. Do not copy Engineer A's experience and present it as Engineer B's own.
