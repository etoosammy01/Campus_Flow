# Git Push and Pull Request Guide

These commands assume the existing local repository is `Campus_Flow` and the current branch is `feat/21-validation-and-notes`.

## 1. Copy the updated source files into the existing repository

Extract the supplied source ZIP to a temporary folder. It intentionally does not include `.git/` or `tickets.json` so your repository history and local ticket data are not overwritten.

From the directory containing both folders, copy the updated source:

```bash
cp -r Campus_Flow_Next_EngineerA/campusflow/. Campus_Flow/campusflow/
cp -r Campus_Flow_Next_EngineerA/tests/. Campus_Flow/tests/
cp -r Campus_Flow_Next_EngineerA/docs/. Campus_Flow/docs/
cp Campus_Flow_Next_EngineerA/README.md Campus_Flow/README.md
cp Campus_Flow_Next_EngineerA/.gitignore Campus_Flow/.gitignore
```

Adjust `Campus_Flow_Next_EngineerA` to the extracted folder name if your unzip tool chose another name. These commands do not copy or replace your `tickets.json`.

## 2. Test before committing

```bash
cd Campus_Flow
python3 -m unittest discover -v
git diff --check
git status
```

The implementation ZIP was tested with 80 passing tests. Re-run the tests in your actual repository; do not rely only on the ZIP's results.

## 3. Commit Engineer A's changes

Review the changed files and stage the validation, workflow, notes, persistence, and corresponding tests first:

```bash
git add campusflow/tickets.py campusflow/workflow.py campusflow/notes.py campusflow/storage.py
git add tests/test_tickets.py tests/test_workflow.py tests/test_notes.py tests/test_storage.py
git commit -m "feat: add safe validation notes and persistence"
```

Then stage the CLI/search/report/understanding-check integration and shared documentation in a second focused commit if the team has agreed that these changes belong on this branch:

```bash
git add campusflow/app.py campusflow/search.py campusflow/reports.py campusflow/assessment.py
git add tests/test_search.py tests/test_reports.py tests/test_assessment.py
git add README.md .gitignore docs/
git commit -m "feat: add search insights and engineering check"
```

If Engineer B is responsible for the second group, coordinate with them before committing it to Engineer A's branch. Do not claim their authorship or review on their behalf.

## 4. Push the feature branch

```bash
git push -u origin feat/21-validation-and-notes
```

If Git reports that authentication is required, complete the GitHub authentication flow. Do not put a password or token directly into a command.

## 5. Open a pull request

On GitHub, open the repository and create a PR from `feat/21-validation-and-notes` into `main`. Include:
- What changed and why.
- The test command and actual output.
- Any known limitations.
- A request for Engineer B to review the diff.

Do not merge your own PR if the assessment requires peer approval. Engineer B must inspect the real diff, leave specific review observations/questions, and approve before merge. Address blocking feedback, rerun tests, and only then merge according to the team instructions.

## 6. Complete the team process honestly

The following cannot be established by a source ZIP alone and must be completed in GitHub by the team:
- Actual issue IDs and PR URLs.
- Engineer B's independent implementation/ownership and review comments.
- Two specific review observations/questions and their resolution.
- The final merged `main` SHA.
- Each engineer's full name, personal reflection, and independently completed understanding check.

After merging, synchronize branches and rerun `python3 -m unittest discover -v`. Never invent a PR URL, approval, review, test result, or final SHA.
