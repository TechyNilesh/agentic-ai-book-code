"""
Chapter 15 -- Comparative Frameworks: Beyond LangGraph

OpenAI Agents SDK: a triage agent that hands off to a weather agent
with one tool (Section 15.4, "OpenAI Agents SDK (March 2025)").

Set your API key:

    export OPENAI_API_KEY=sk-...

Run:
    python 03_openai_agents_sdk.py
"""

from agents import Agent, Runner, function_tool


@function_tool
def get_weather(city: str) -> str:
    return f"It is 32 C in {city}."


triage = Agent(name="Triage", instructions="Route to the right agent.")
weather = Agent(
    name="Weather",
    instructions="Answer weather questions.",
    tools=[get_weather],
)
triage.handoffs = [weather]

if __name__ == "__main__":
    result = Runner.run_sync(triage, "What is the weather in Pune?")
    print(result.final_output)
