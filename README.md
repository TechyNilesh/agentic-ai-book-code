# Agentic AI: Principles, Patterns, and Practice — Companion Code

This is the official code repository for the book **Agentic AI: Principles,
Patterns, and Practice** by Nilesh Verma and Dr. Hari Shankar Hota.
Every lab, worked example, and
capstone scaffold from the book lives here, one folder per chapter.

## Quick start

```bash
git clone <REPO_URL>
cd <REPO_NAME>
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file (or export environment variables) with the API keys you
have. Most labs need only one provider:

```bash
OPENAI_API_KEY=...        # or
ANTHROPIC_API_KEY=...
```

Appendix B of the book explains how to get keys, including free options.
Each chapter folder has its own `README.md` with exact run instructions.

## Repository map

| Folder | Book chapter | What you build |
|---|---|---|
| `chapter-01/` | 1. Introduction to Agentic AI | First LLM call, a minimal agent loop |
| `chapter-02/` | 2. LLMs, Prompting, and APIs | Structured-output summarizer with Pydantic |
| `chapter-03/` | 3. Python & LangChain Toolbox | LCEL pipelines, parsers, memory, streaming |
| `chapter-04/` | 4. Reasoning and Planning | ReAct from scratch, then with LangGraph |
| `chapter-05/` | 5. Tool Use and Function Calling | Five-tool research agent |
| `chapter-06/` | 6. Reflection and Self-Improvement | Code agent that fixes itself until tests pass |
| `chapter-07/` | 7. Memory in Agentic Systems | Assistant with long-term memory (LangGraph store + Chroma) |
| `chapter-08/` | 8. Multi-Agent Systems | Research-writing crew (planner → researcher → writer → editor) |
| `chapter-09/` | 9. LangGraph Fundamentals | StateGraph, reducers, `Send`, `Command`, branching |
| `chapter-10/` | 10. Persistence & Human-in-the-Loop | Checkpointers, time-travel, HITL travel-booking agent |
| `chapter-11/` | 11. Agentic RAG | Self-correcting RAG over a PDF corpus |
| `chapter-12/` | 12. Evaluation and Observability | LangSmith/OpenTelemetry tracing, LLM-as-judge, drift detection |
| `chapter-13/` | 13. Model Context Protocol | MCP servers (echo, weather, SQLite) + LangGraph clients |
| `chapter-14/` | 14. Safety and Security | Defense-in-depth guardrails demo |
| `chapter-15/` | 15. Comparative Frameworks | Same crew in CrewAI, AutoGen, OpenAI Agents SDK, Claude Agent SDK, Pydantic AI |
| `chapter-16/` | 16. Inside Real Agent Harnesses | A minimal agent harness, built step by step |
| `chapter-17/` | 17. Deployment and Production | FastAPI wrapper, Docker, Render deploy |
| `capstones/` | 18. Capstone Projects | Smart Study Assistant, Research Bot, Coding Agent with HITL |

## Versions

Library versions are pinned in `requirements.txt` (snapshot: **July 2026**).
Agent frameworks move fast. If an example breaks on a newer library
version, check `versions.md` for the fix, and `errata.md` for corrections
to the book text. The patterns in the book do not change; only the APIs do.

## A tip on practice

Run every lab, even the ones that look easy. Many ideas in the book only
make sense after you watch an agent fail in a surprising way. Failure is
the teacher; the book is only the syllabus.

## License

Code is MIT-licensed (see `LICENSE`). The book text is copyright the author.
