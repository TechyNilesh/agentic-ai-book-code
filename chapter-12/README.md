# Chapter 12 — Evaluation and Observability

This chapter's lab is about knowing whether your agent is actually
good, and finding out fast when it stops being good. The code here
shows the three building blocks: tracing an agent run so you can see
what it did, running an LLM judge to score open-ended answers, and
watching a stream of scores for drift.

## Files

- `01_langsmith_tracing.py` — traces a function with LangSmith using
  the `@traceable` decorator. Two environment variables turn tracing
  on; nested LangChain calls become child spans automatically.
- `02_opentelemetry_tracing.py` — the vendor-neutral alternative to
  LangSmith. Sets up an OpenTelemetry `TracerProvider` with a console
  exporter and wraps an agent run in nested spans.
- `03_page_hinkley_drift.py` — the Page-Hinkley drift detector from
  the book, plus a small simulated score stream (with a planted drift
  at step 500) so you can see it raise an alarm. No API key needed.
- `04_pairwise_llm_judge.py` — the worked example: an LLM-as-judge
  pairwise evaluator that swaps answer order to reduce position bias,
  then tallies wins, losses, and ties across two systems.
- `requirements.txt` — packages needed for this chapter's labs.

## How to run

1. Create and activate a virtual environment, then install packages:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Export the API keys you need. `03_page_hinkley_drift.py` needs no
   keys at all — start there if you just want to see the drift
   detector work.

   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   export LANGSMITH_API_KEY="ls__..."   # only for 01_langsmith_tracing.py
   ```

3. Run each script:

   ```bash
   python 01_langsmith_tracing.py
   python 02_opentelemetry_tracing.py
   python 03_page_hinkley_drift.py
   python 04_pairwise_llm_judge.py
   ```

## What to expect

`01_langsmith_tracing.py` prints a short summary and, if you open the
LangSmith UI, shows a new trace under the `research-crew` project.

`02_opentelemetry_tracing.py` prints the agent's plan text and also
prints raw span data to the console (that is what `ConsoleSpanExporter`
does).

`03_page_hinkley_drift.py` prints a list of step numbers where the
detector raised an alarm. With the planted drift at step 500, expect
an alarm shortly after that point.

`04_pairwise_llm_judge.py` prints a tuple `(wins_a, wins_b, ties)`
after judging two toy "systems" on two sample questions, with each
question judged twice (order swapped).

## Full lab

For the complete Chapter 12 lab — build a custom evaluator for the
Chapter 8 research crew, log runs to LangSmith, and simulate a model
downgrade to trigger drift — see the `labbox` section in
`ch12-evaluation-observability.tex`. The scripts above give you the
three reusable pieces (tracing, judging, drift detection) needed to
assemble it.
