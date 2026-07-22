"""
Chapter 15 -- Comparative Frameworks: Beyond LangGraph

AutoGen / Microsoft Agent Framework: a group chat between a Coder
agent, a Reviewer agent, and a user-proxy agent (Section 15.3,
"AutoGen / Microsoft Agent Framework v1.0").

Set your API key:

    export OPENAI_API_KEY=sk-...

Run:
    python 02_autogen_groupchat.py
"""

from autogen import AssistantAgent, UserProxyAgent, GroupChat

coder = AssistantAgent(name="Coder", llm_config={"model": "gpt-4o"})
reviewer = AssistantAgent(name="Reviewer", llm_config={"model": "gpt-4o"})
user = UserProxyAgent(name="User", human_input_mode="NEVER")

chat = GroupChat(agents=[user, coder, reviewer], messages=[], max_round=8)

if __name__ == "__main__":
    user.initiate_chat(
        chat, message="Write a Python script that reverses a string."
    )
