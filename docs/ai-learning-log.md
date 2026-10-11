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
