"""Question bank and scoring for the Engineering Understanding Check."""

QUESTIONS = [
    {
        "question": "A ticket has high urgency and 12 affected users. What is its priority?",
        "options": {"A": "low", "B": "medium", "C": "high", "D": "critical"},
        "answer": "D",
        "explanation": "The critical rule is checked first: high urgency AND at least 10 affected users.",
    },
    {
        "question": "Which transition is allowed for an open, assigned ticket?",
        "options": {"A": "open to resolved", "B": "open to in_progress",
                    "C": "open to closed", "D": "open to archived"},
        "answer": "B",
        "explanation": "Work begins by moving an assigned open ticket to in_progress.",
    },
    {
        "question": "A note message has only four non-space characters. What should happen?",
        "options": {"A": "Accept it", "B": "Pad it automatically",
                    "C": "Reject it without consuming an ID", "D": "Resolve the ticket"},
        "answer": "C",
        "explanation": "A trimmed message must contain 5–300 characters, and rejected notes do not use IDs.",
    },
    {
        "question": "What does combining category and status filters with AND mean?",
        "options": {"A": "Either filter may match", "B": "Both filters must match",
                    "C": "Only category is used", "D": "Only status is used"},
        "answer": "B",
        "explanation": "A result must satisfy every supplied filter.",
    },
    {
        "question": "What should loading do if one record in the JSON file is invalid?",
        "options": {"A": "Load the valid records only", "B": "Delete the file",
                    "C": "Reject the entire load", "D": "Skip the record silently"},
        "answer": "C",
        "explanation": "The whole collection is validated before the caller replaces current memory.",
    },
    {
        "question": "If there are zero tickets, what is the resolution rate?",
        "options": {"A": "0%", "B": "100%", "C": "Undefined text only", "D": "Crash"},
        "answer": "A",
        "explanation": "An empty collection reports 0% instead of dividing by zero.",
    },
]


def score_answers(answers, questions=None):
    """Return the number of correct answers for a supplied answer sequence."""
    bank = QUESTIONS if questions is None else questions
    return sum(
        1 for question, answer in zip(bank, answers)
        if isinstance(answer, str) and answer.upper() == question["answer"]
    )
