# Chapter 2 — Foundations: LLMs, Prompting, and APIs

This chapter shows how to call an LLM through a chat API and how to
turn its reply into data your program can trust, using Pydantic
schemas instead of free-form text. The main lab (Lab 2.1) builds a
command-line news summariser that reads an article from a file and
prints a structured JSON summary.

## Files

- `01_hello_chat_model.py` — the simplest chat call using
  `init_chat_model`, with a system and a user message.
- `02_structured_sentiment.py` — classifies one review into a typed
  `Sentiment` object (label, confidence, reason) using
  `with_structured_output`.
- `03_review_extractor.py` — the chapter's worked example: turns a
  free-text product review into a structured `ReviewInfo` object
  with complaints and compliments as lists.
- `04_news_summary.py` — Lab 2.1: reads a news article from a text
  file and prints a structured `NewsSummary` (headline, summary, key
  entities, sentiment, topic).
- `sample_article.txt` — a short placeholder article so you can run
  `04_news_summary.py` immediately. Swap it for a real article for
  your lab submission.
- `requirements.txt` — packages needed for this chapter's labs.

## How to run

1. Set up your environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

2. Run any script:

   ```bash
   python 01_hello_chat_model.py
   python 02_structured_sentiment.py
   python 03_review_extractor.py
   python 04_news_summary.py sample_article.txt
   ```

## What to expect

Each structured-output script prints a typed object, not raw text.
For example, `04_news_summary.py` prints JSON with a `headline`,
`summary`, `key_entities` list, `sentiment`, and `topic` field —
ready to store in a database.
