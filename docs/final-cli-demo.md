# Final CLI Demonstration

The application was smoke-tested in an isolated temporary directory with the following sequence:

1. Create `Campus Wi-Fi outage`, category `Network`, urgency `high`, 12 affected users.
2. Assign `T001` to `Ada`.
3. Move `T001` to `in_progress`.
4. Add note `Router restarted successfully` by `Ada`.
5. View the report.
6. Exit.

Observed results:
- Ticket `T001` was created with `critical` priority.
- Assignment and status update succeeded.
- Note `N001` was added successfully.
- Report showed total 1, unresolved 1, resolved 0, resolution rate 0.0%, and one critical Network ticket.
- The CLI exited normally.

For a live demonstration from the repository root, run `python3 -m campusflow.app` and repeat the sequence above. Avoid sharing a real `tickets.json` if it contains private support data.
