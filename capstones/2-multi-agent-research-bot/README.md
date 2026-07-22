# Capstone 2: Multi-Agent Research Bot

From Chapter 17 of the book, *Agentic AI: Principles, Patterns, and
Practice*. Suits UG or PG students. Work on it for four to six
weeks, alone or in a team of two or three.

The book gives no starter code for this capstone -- this folder is
README-only. Build the project from scratch using the chapters
listed below.

## Objective

Build a team of agents that together produce a five-page Markdown
research report on any topic the user gives. Each agent has a clear
role.

## Required Concepts (Chapter Map)

- Chapter 4: Planning and task decomposition.
- Chapter 6: Web search and external tools.
- Chapter 9: Multi-agent collaboration.
- Chapter 11: LangGraph state machines.
- Chapter 12: MCP integration.
- Chapter 14: Safety and citation guardrails.

## Architecture

A pipeline of agents: Planner -> Researcher -> Writer -> Citer ->
Editor -> Markdown Report.

## Functional Requirements

1. The Planner splits a topic into five to seven subtopics.
2. The Researcher calls a web search API and collects sources.
3. The Writer drafts each section.
4. The Citer inserts inline references in IEEE or APA style.
5. The Editor checks tone, length, and removes duplicate facts.
6. Final output is a valid Markdown file of about five pages.

## Evaluation Rubric

| Criterion | Marks |
|---|---|
| Planner decomposition quality | 15 |
| Research depth and source variety | 20 |
| Writing quality and coherence | 15 |
| Citation correctness | 15 |
| LangGraph state design | 10 |
| Report (IEEE format) | 15 |
| Demo and viva | 10 |
| **Total** | **100** |

## Submission Checklist

- GitHub repo with clear agent role files.
- Three sample reports on three different topics.
- Log files showing the agent message trace.
- Eight-page IEEE report on your design.
- Live demo on a fresh, unseen topic.

## Extension Ideas

1. Add a fact-checker agent that scores claims.
2. Output to LaTeX as well as Markdown.
3. Support Hindi or regional-language reports.
4. Plug in a local LLM via Ollama for offline use.

## Report Format and Demo Day

See the shared "Report Format" and "Demo Day" sections in the book's
Chapter 17 (also summarised in the capstones-level notes): the
written report follows the IEEE conference template (two-column,
10pt, about eight pages), with Introduction, Related Work, Design,
Implementation, Evaluation, Results, Discussion, and Conclusion and
Future Work sections. Demo day is a ten-minute viva: 0-2 min problem
and architecture, 2-7 min live demo on a fresh input from the
examiner, 7-9 min evaluation table and one failure case, 9-10 min
questions on design choices.
