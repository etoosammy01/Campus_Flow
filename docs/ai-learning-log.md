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