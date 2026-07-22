# Chapter 3 — The Python and LangChain Toolbox

This chapter teaches the LangChain building blocks you will reuse for
the rest of the book: model loading, prompt templates, output parsers,
LCEL (the `|` pipe operator), streaming, memory, and callbacks. The
main lab (Lab 3) asks you to chain several of these pieces into a
four-stage content pipeline that ends in a Hindi summary.

## Files

- `01_load_models.py` — loads chat models from four providers
  (Anthropic, OpenAI, Google, Groq) with the single `init_chat_model`
  helper. Only Anthropic is actually called by default.
- `02_prompt_templates.py` — builds a reusable `ChatPromptTemplate`
  with placeholders, and shows `partial()` to fix one variable.
- `03_output_parsers.py` — three ways to turn a model reply into
  data: plain string, free-form JSON, and a typed Pydantic object.
- `04_lcel_chain.py` — composes prompt, model, and parser with the
  `|` operator, then runs the chain on a batch of inputs in parallel.
- `05_streaming.py` — shows `.stream()` for synchronous code and
  `.astream()` inside an `asyncio` program.
- `06_memory.py` — adds per-session chat memory with
  `RunnableWithMessageHistory` (the LangChain 1.0 replacement for the
  deprecated `ConversationBufferMemory`).
- `07_callbacks.py` — a small callback handler that prints events
  when an LLM call starts and ends; also shows the LangSmith env vars
  for hosted tracing.
- `08_four_stage_pipeline.py` — the chapter's worked example: outline
  -> write -> critique -> finalise, four small chains glued together
  in plain Python. This is the pattern Lab 3 asks you to extend with
  a translate-to-Hindi and summarise stage.
- `09_translate_summarise.py` — Solved Problem 3.1: a two-stage chain
  that translates English to Hindi and then summarises it into three
  Hindi bullets, using `RunnableLambda` to reshape data between
  stages.
- `requirements.txt` — packages needed for this chapter's labs.

## How to run

1. Set up your environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Create a `.env` file with the keys you plan to use, for example:

   ```
   ANTHROPIC_API_KEY=sk-ant-...
   OPENAI_API_KEY=sk-...
   GOOGLE_API_KEY=...
   GROQ_API_KEY=...
   ```

3. Run any script:

   ```bash
   python 01_load_models.py
   python 08_four_stage_pipeline.py
   ```

## Building Lab 3 yourself

Lab 3 asks for a four-stage pipeline: outline -> expand -> translate
-> summarise. Start from `08_four_stage_pipeline.py` for the
outline/write pattern and `09_translate_summarise.py` for the
translate/summarise pattern, then combine the two into a single
`pipeline.py` as described in the book.
