# CampusFlow Design Decisions

## 1. Ticket Representation

Tickets will be stored as a list of dictionaries.

Each ticket contains:
- id
- title
- category
- urgency
- affected_users
- priority
- status
- assigned_to

## 2. Input Validation

Functions will validate input before changing application state.

Invalid input will raise ValueError with a helpful message.

## 3. Ticket Creation

The ticket creation function will validate the ticket details,
calculate priority, generate a unique ID, and add the ticket
to the shared ticket collection.

## 4. Priority Calculation

Priority will be calculated using the assessment rules in order:
1. High urgency and at least 10 affected users: critical.
2. High urgency or at least 10 affected users: high.
3. Medium urgency or at least 3 affected users: medium.
4. Otherwise: low.

## 5. Testing

Automated tests will use Python's unittest module.
Business logic will be tested independently of terminal input.

## 6. Persistence

Tickets will eventually be saved to and loaded from a JSON file.

## 7. Collaboration

Engineer A owns ticket creation, validation, priority calculation,
and related tests.

Engineer B owns assignment, workflow, queue, reports,
and related tests.

Both engineers will coordinate interfaces, persistence,
integration, and code reviews.