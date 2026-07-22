"""
Chapter 15 -- Comparative Frameworks: Beyond LangGraph

Worked Example: the Chapter 8 research-writing crew (Researcher ->
Writer -> Editor), re-implemented in CrewAI (Section 15.8, "Worked
Example: A 3-Agent Crew in CrewAI"). Compare this ~35-line version
against the ~80-line explicit LangGraph version from Chapter 8.

Set your API key:

    export OPENAI_API_KEY=sk-...

Run:
    python 06_crewai_research_writing_crew.py
"""

from crewai import Agent, Task, Crew, Process

researcher = Agent(
    role="Researcher",
    goal="Collect five key facts about {topic}",
    backstory="A careful library scientist.",
    verbose=True,
)
writer = Agent(
    role="Writer",
    goal="Write a 400-word article from the facts",
    backstory="A clear technical writer.",
    verbose=True,
)
editor = Agent(
    role="Editor",
    goal="Improve clarity and remove jargon",
    backstory="A strict but fair editor.",
    verbose=True,
)

research_task = Task(
    description="Find five facts about {topic}.",
    expected_output="A bulleted list of five facts.",
    agent=researcher,
)
write_task = Task(
    description="Write the article using the facts above.",
    expected_output="A 400-word article.",
    agent=writer,
    context=[research_task],
)
edit_task = Task(
    description="Polish the article.",
    expected_output="The final article.",
    agent=editor,
    context=[write_task],
)

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.sequential,
)

if __name__ == "__main__":
    print(crew.kickoff(inputs={"topic": "agentic AI in education"}))
