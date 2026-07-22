# Capstone 1: Smart Study Assistant

From Chapter 17 of the book, *Agentic AI: Principles, Patterns, and
Practice*. Friendly for UG students. Work on it for four to six
weeks, alone or in a team of two or three.

## Objective

Build an agent that reads your textbook PDFs and helps you study.
The agent should answer questions, generate quizzes, and remind you
to revise weak topics using spaced repetition.

## Required Concepts (Chapter Map)

- Chapter 3: LLM basics and prompt design.
- Chapter 5: Tools and function calling.
- Chapter 7: Retrieval-Augmented Generation (RAG).
- Chapter 8: Vector stores and embeddings.
- Chapter 10: Memory and state.
- Chapter 13: Evaluation of agents.

## Architecture

A PDF Loader feeds a Vector Store, which a Retriever queries. The
Retriever and Quiz Generator call each other. The Quiz Generator
feeds the Spaced Repetition scheduler, which drives the User UI. The
User UI feeds new material back into the PDF Loader.

## Functional Requirements

1. Load at least three PDFs of a subject and index them in a vector store.
2. Answer free-text questions with citations to page numbers.
3. Generate a quiz of five MCQs from a chosen topic.
4. Record which questions the user gets wrong.
5. Schedule the next review using a simple SM-2 or Leitner algorithm.
6. Provide a CLI or Streamlit UI.

## Evaluation Rubric

| Criterion | Marks |
|---|---|
| Correct RAG pipeline with citations | 20 |
| Quiz quality and variety | 15 |
| Spaced repetition logic | 15 |
| UI and user experience | 10 |
| Code quality and tests | 15 |
| Report (IEEE format) | 15 |
| Demo and viva | 10 |
| **Total** | **100** |

## Submission Checklist

- GitHub repo with README and license.
- `requirements.txt` or `pyproject.toml`.
- Sample PDFs (or links) used for testing.
- Eval script that measures retrieval accuracy on 20 hand-written questions.
- Eight-page IEEE report.
- Two-minute screencast plus a ten-minute live demo.

## Extension Ideas

1. Add voice input using Whisper.
2. Support handwritten notes via OCR.
3. Generate flashcards as Anki decks.
4. Add a mobile-friendly web UI.

## Starter Scaffold

The book gives a starter folder layout and a skeleton `app.py`
(Chapter 17, Lab "Starter scaffold for Capstone 1"). This folder
already has that scaffold in place:

```
1-smart-study-assistant/
|-- README.md
|-- requirements.txt
|-- data/
|   `-- pdfs/            # drop your textbook PDFs here
|-- src/
|   `-- capstone1/
|       |-- __init__.py
|       |-- app.py       # entry point
|       |-- loader.py    # PDF loading + chunking
|       |-- index.py     # vector store build
|       |-- retriever.py
|       |-- quiz.py
|       |-- scheduler.py # SM-2 / Leitner logic
|       `-- prompts/
|           |-- qa.txt
|           `-- quiz.txt
|-- tests/
|   `-- test_retriever.py
`-- eval/
    `-- questions.jsonl  # 20 hand-written Q/A pairs
```

`app.py` is filled in exactly as printed in the book. All the other
Python files (`loader.py`, `index.py`, `retriever.py`, `quiz.py`,
`scheduler.py`) are stubs with `TODO` markers -- the book does not
print their implementation. Fill in the TODOs one by one and commit
after each, as the book instructs.

## How to run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...

# from this folder:
python -m capstone1 build          # after implementing index.py
python -m capstone1 ask "..."      # after implementing retriever.py
python -m capstone1 quiz "topic"   # after implementing quiz.py
python -m capstone1 run            # after implementing a src/capstone1/ui.py Streamlit UI
```
