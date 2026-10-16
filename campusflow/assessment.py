"""Question bank, scoring, and quiz loop for the Engineering Understanding Check.

The question bank (QUESTIONS) and scoring (score_answers) contain no input()
or print(). run_check takes input_fn/output_fn so tests can script it.
"""

VALID_CHOICES = ("A", "B", "C", "D")
EXPLAIN_QUESTIONS = (1, 2)      # question numbers that also ask for an explanation

QUESTIONS = [
    {
        "question": "Ticket T001 is open and unassigned. A user tries to move it to in_progress.",
        "options": {"A": "Accept", "B": "Reject and preserve all data",
                    "C": "Resolve it automatically", "D": "Remove ticket"},
        "answer": "B",
        "explanation": "An unassigned ticket has no owner, so the move is rejected and nothing changes.",
    },
    {
        "question": "The app has zero tickets. What should resolution percentage display?",
        "options": {"A": "Crash", "B": "100%", "C": "0%",
                    "D": "Divide by one without explanation"},
        "answer": "C",
        "explanation": "The division is skipped when total is 0, so the rate is reported as 0%.",
    },
    {
        "question": "Filter title='wifi', category='Network', status='open'. Which records should match?",
        "options": {"A": "Any record matching one filter",
                    "B": "Only records matching all supplied filters",
                    "C": "All network records", "D": "All open records"},
        "answer": "B",
        "explanation": "Supplied filters are combined with AND: every one must match.",
    },
    {
        "question": "A resolved ticket receives 'Add note'. What should happen?",
        "options": {"A": "Append anyway", "B": "Delete old notes",
                    "C": "Reject until reopened", "D": "Change status silently"},
        "answer": "C",
        "explanation": "Resolved tickets are locked until they are reopened through the workflow.",
    },
    {
        "question": "The JSON file includes two tickets with the same ID. What should load do?",
        "options": {"A": "Keep both", "B": "Replace memory with duplicates",
                    "C": "Reject the load without changing current memory",
                    "D": "Rename IDs silently"},
        "answer": "C",
        "explanation": "The whole file is validated first; memory is replaced only if it is all valid.",
    },
    {
        "question": "A PR changes validation but has no negative-case tests. Best review action?",
        "options": {"A": "Approve because it runs", "B": "Request focused tests and reasoning",
                    "C": "Merge immediately", "D": "Ask AI to approve it"},
        "answer": "B",
        "explanation": "A review should name the missing edge cases and ask for tests that prove them.",
    },
]


def normalize_choice(raw):
    """' b ' -> 'B'. Non-text becomes '' (which is never valid)."""
    return raw.strip().upper() if isinstance(raw, str) else ""


def is_valid_choice(choice):
    return choice in VALID_CHOICES


def score_answers(answers, questions=None):
    """Return the number of correct answers for a supplied answer sequence."""
    bank = QUESTIONS if questions is None else questions
    return sum(
        1 for question, answer in zip(bank, answers)
        if isinstance(answer, str) and answer.upper() == question["answer"]
    )


def ask_choice(question, input_fn=input, output_fn=print):
    """Show one question and re-prompt until the answer is A, B, C or D."""
    output_fn(question["question"])
    for letter, option in question["options"].items():
        output_fn(f"  {letter}. {option}")
    while True:
        choice = normalize_choice(input_fn("Answer (A/B/C/D): "))
        if is_valid_choice(choice):
            return choice
        output_fn("Please enter A, B, C, or D.")


def ask_explanation(input_fn=input, output_fn=print):
    """Ask for a non-blank explanation. It is stored, never auto-graded."""
    while True:
        text = input_fn("Briefly explain your answer: ").strip()
        if text:
            return text
        output_fn("Please write a short explanation.")


def run_check(questions=None, input_fn=input, output_fn=print):
    """Run the quiz. The FIRST valid choice for each question is what scores."""
    bank = QUESTIONS if questions is None else questions
    answers, explanations = [], []
    for number, question in enumerate(bank, start=1):
        output_fn(f"\nQuestion {number} of {len(bank)}")
        choice = ask_choice(question, input_fn, output_fn)
        answers.append(choice)                        # recorded BEFORE any feedback
        if number in EXPLAIN_QUESTIONS:
            explanations.append({"question": number, "answer": choice,
                                 "explanation": ask_explanation(input_fn, output_fn)})
        if choice == question["answer"]:
            output_fn("Correct. " + question.get("explanation", ""))
        else:
            output_fn(f"Not quite. Correct answer: {question['answer']}. "
                      + question.get("explanation", ""))
    return {"score": score_answers(answers, bank), "out_of": len(bank),
            "answers": answers, "explanations": explanations}