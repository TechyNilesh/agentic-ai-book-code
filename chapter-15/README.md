# Chapter 15 -- Comparative Frameworks: Beyond LangGraph

This chapter is a map of the agent-framework landscape. It shows the
same kind of small example in five different frameworks -- CrewAI,
AutoGen / Microsoft Agent Framework, the OpenAI Agents SDK, the
Claude Agent SDK, and Pydantic AI -- so you can compare their mental
models side by side. Lab 15.1 asks you to port the Chapter 8
research-writing crew from LangGraph to CrewAI; file `06` is the
CrewAI half of that comparison.

## Files

- `01_crewai_basics.py` -- a two-agent CrewAI crew (Researcher, Writer) running two tasks in order.
- `02_autogen_groupchat.py` -- an AutoGen group chat between a Coder agent, a Reviewer agent, and a user-proxy agent.
- `03_openai_agents_sdk.py` -- an OpenAI Agents SDK triage agent that hands off to a weather agent with one tool.
- `04_claude_agent_sdk.py` -- a Claude Agent SDK agent that reads files with the `Read` and `Grep` tools.
- `05_pydantic_ai.py` -- a Pydantic AI agent whose output is validated against a typed `Answer` model.
- `06_crewai_research_writing_crew.py` -- the Worked Example: a 3-agent CrewAI crew (Researcher, Writer, Editor) that reimplements the Chapter 8 LangGraph pipeline.

## How to run

Each file uses a different framework, so install only the package(s)
you need for the file you want to run:

```bash
pip install crewai              # for 01 and 06
pip install pyautogen           # for 02
pip install openai-agents       # for 03
pip install claude-agent-sdk    # for 04
pip install pydantic-ai         # for 05
```

Set the matching API key as an environment variable. Never hard-code
keys in the source files.

```bash
export OPENAI_API_KEY=sk-...        # CrewAI, AutoGen, OpenAI Agents SDK, Pydantic AI
export ANTHROPIC_API_KEY=sk-ant-... # Claude Agent SDK
```

Then run any file directly:

```bash
python 01_crewai_basics.py
python 02_autogen_groupchat.py
python 03_openai_agents_sdk.py
python 04_claude_agent_sdk.py
python 05_pydantic_ai.py
python 06_crewai_research_writing_crew.py
```

For Lab 15.1, run `06_crewai_research_writing_crew.py` next to your
Chapter 8 LangGraph project, then compare line count, wall-clock
time, token usage, and output quality as described in the lab.
