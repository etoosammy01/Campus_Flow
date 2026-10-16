# Additional Edge-Case Test Record

## Engineer A — duplicate ticket IDs rejected without mutation

- **Test name:** `test_duplicate_existing_ids_rejected_without_mutation`
- **Initial state:** Two existing dictionaries in the ticket list both have ID `T001`.
- **Input/action:** Attempt to create a new valid Network ticket.
- **Expected:** Raise `ValueError`; the list remains byte-for-byte equivalent at the dictionary/value level to its pre-action state.
- **Actual:** The test passes; duplicate IDs are rejected and the list is unchanged.
- **Code change:** `validate_existing_tickets()` tracks IDs in a set and rejects duplicates before ticket creation.

## Engineer A — invalid note does not consume an ID

- **Test name:** `test_too_short_note_rejected_without_consuming_id`
- **Initial state:** One open ticket with an empty notes list.
- **Input/action:** Attempt to add a four-character trimmed message, then add a valid message.
- **Expected:** First action raises `ValueError`; the valid note receives `N001`.
- **Actual:** The test passes; invalid input does not append a note or consume an ID.
- **Code change:** `add_note()` validates the author/message before generating and appending a note.

## Engineer B — additional edge case to confirm

The combined-filter and invalid-filter cases are covered by `tests/test_search.py`. Engineer B should confirm one additional test as their own contribution, record the initial state/input/expected/actual result here, and commit it from their feature branch. Do not claim this section as peer-authored until Engineer B confirms it.
