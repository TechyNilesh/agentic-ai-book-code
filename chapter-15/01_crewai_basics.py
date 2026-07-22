"""
Chapter 15 -- Comparative Frameworks: Beyond LangGraph

CrewAI basics: a two-agent crew (Researcher, Writer) that runs two
tasks in sequence (Section 15.2, "CrewAI").

Set your API key (CrewAI defaults to OpenAI models unless you
configure another LLM):

    export OPENAI_API_KEY=sk-...

Run:
    python 01_crewai_basics.py
"""

from crewai import Agent, Task, Crew

researcher = Agent(
    role="Researcher",
    goal="Find five recent papers on agent planning",
    backstory="A careful PhD student who loves arXiv.",
)
writer = Agent(
    role="Writer",
    goal="Turn the notes into a 300-word summary",
    backstory="A patient science communicator.",
)
task1 = Task(description="Search arXiv for 2025 papers", agent=researcher)
task2 = Task(description="Write the summary", agent=writer)
crew = Crew(agents=[researcher, writer], tasks=[task1, task2])

if __name__ == "__main__":
    result = crew.kickoff()
    print(result)
