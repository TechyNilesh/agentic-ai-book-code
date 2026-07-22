# Chapter 6 -- Reflection and Self-Improvement

This lab shows the reflection pattern: generate, evaluate, reflect,
regenerate. The main lab builds a code-writing agent that runs its own
output against unit tests and fixes itself when a test fails, up to
three rounds. A second, smaller file replays the chapter's SQL
worked example, showing the same loop with a database error as the
verifier.

## Files

- `01_test_driven_code_agent.py` -- the chapter lab. Asks Claude to write `is_prime`, runs unit tests, and reflects on failures for up to 3 rounds.
- `02_sql_reflection_worked_example.py` -- illustrative replay of the chapter's SQL trace (ambiguous column name fixed on the second try). Not a full agent; it prints the two queries and the trace from the book.

## How to run

Install the package:

```bash
pip install anthropic
```

Set your API key:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Then run:

```bash
python 01_test_driven_code_agent.py
python 02_sql_reflection_worked_example.py
```

`02_sql_reflection_worked_example.py` needs no API key -- it just
prints the worked-example trace from the chapter. `01_test_driven_code_agent.py`
sandboxes every test run in a temporary directory with a 10-second
timeout; do not remove that when you extend it to run untrusted code.
