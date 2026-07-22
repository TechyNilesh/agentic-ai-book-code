# Capstone 3: Coding Agent with HITL

From Chapter 17 of the book, *Agentic AI: Principles, Patterns, and
Practice*. Best for PG students or strong UG teams. Work on it for
four to six weeks, alone or in a team of two or three.

The book gives no starter code for this capstone -- this folder is
README-only. Build the project from scratch using the chapters
listed below.

## Objective

Build an agent that fixes Python bugs. The agent reads failing
tests, edits code, and re-runs tests in a loop. A human must approve
every patch before it is applied.

## Required Concepts (Chapter Map)

- Chapter 5: Tool use (shell, file edit, test runner).
- Chapter 9: ReAct loops.
- Chapter 11: LangGraph control flow.
- Chapter 12: MCP for code tools.
- Chapter 14: Human-in-the-loop (HITL) gates.
- Chapter 15: Sandboxing and safety.

## Architecture

A loop: Test Runner (fail log) -> Code Generator -> Patch -> HITL
Approval -> (on approve) Apply Patch -> back to Test Runner. On
reject, HITL Approval sends control back to the Code Generator.

## Functional Requirements

1. Accept a Git repository and a failing `pytest` command.
2. Read test output and locate the buggy file.
3. Propose a diff in unified `patch` format.
4. Show the diff to the human and wait for `approve` or `reject`.
5. On approval, apply the patch and re-run tests.
6. Stop after tests pass or after five failed attempts.

## Evaluation Rubric

| Criterion | Marks |
|---|---|
| Bug-fix success rate on 10 sample bugs | 25 |
| Quality of generated diffs | 15 |
| HITL workflow design | 15 |
| Sandbox and safety controls | 10 |
| Code quality and tests | 10 |
| Report (IEEE format) | 15 |
| Demo and viva | 10 |
| **Total** | **100** |

## Submission Checklist

- GitHub repo with a `bugs/` folder of test cases.
- Logs of all agent attempts and human decisions.
- Safety notes: what the sandbox does and does not allow.
- Eight-page IEEE report.
- Live demo: fix at least one unseen bug during the viva.

## Extension Ideas

1. Add a static analyzer (e.g. `ruff`) as an extra tool.
2. Auto-write missing tests before fixing.
3. Support JavaScript or Java in addition to Python.
4. Compare your agent against SWE-bench-lite scores.

## Report Format and Demo Day

The written report follows the IEEE conference template (two-column,
10pt, about eight pages), with Introduction, Related Work, Design,
Implementation, Evaluation, Results, Discussion, and Conclusion and
Future Work sections. Demo day is a ten-minute viva: 0-2 min problem
and architecture, 2-7 min live demo on a fresh input from the
examiner, 7-9 min evaluation table and one failure case, 9-10 min
questions on design choices.
