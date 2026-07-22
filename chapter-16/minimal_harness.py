import json, subprocess
from my_llm import call_model      # returns text + optional tool_calls

TOOLS = {
    "read_file": lambda path: open(path).read(),
    "run_bash":  lambda cmd: subprocess.run(
        cmd, shell=True, capture_output=True, text=True).stdout,
}
def build_system_prompt(soul: str, memory: str) -> str:
    return (f"{soul}\n\n"
            f"# What I remember\n{memory}\n\n"
            f"# Tools\n{list(TOOLS)}")

def approve(call) -> bool:
    # the permission gate: ask the user before a risky call
    if call.name == "run_bash":
        return input(f"Run `{call.args}`? [y/N] ") == "y"
    return True                      # reads are auto-allowed
def run(user_msg, soul, memory, max_steps=12):
    messages = [
        {"role": "system", "content": build_system_prompt(soul, memory)},
        {"role": "user",   "content": user_msg},
    ]
    for _ in range(max_steps):                 # 1. the loop
        reply = call_model(messages)           # 2. call the model
        messages.append({"role": "assistant", "content": reply.text})
        if not reply.tool_calls:               # 5. stop: no tools asked
            return reply.text
        for call in reply.tool_calls:          # 3. permission gate
            if not approve(call):
                result = "Denied by user."
            else:
                result = TOOLS[call.name](**call.args)  # 4. execute
            messages.append({"role": "tool", "content": str(result)})
    return "Stopped: step limit reached."
