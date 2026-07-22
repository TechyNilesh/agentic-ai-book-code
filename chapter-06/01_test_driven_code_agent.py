"""
Chapter 6 - Reflection and Self-Improvement
Lab: Test-Driven Code Agent.

The agent writes a Python function for a spec, runs unit tests against
it, and -- if tests fail -- reflects on the error and tries again, up
to max_rounds times. This is reflection at its best: an objective
verifier (the test suite) drives each fix.

Env vars needed:
    ANTHROPIC_API_KEY  -- your Anthropic API key
"""

import os
import subprocess
import tempfile
import textwrap

from anthropic import Anthropic

MODEL = "claude-sonnet-4-5"

SPEC = """
Write a Python function `is_prime(n: int) -> bool` that
returns True if n is a prime number, False otherwise.
Handle n < 2 by returning False.
"""

TESTS = """
from solution import is_prime
assert is_prime(2) == True
assert is_prime(3) == True
assert is_prime(4) == False
assert is_prime(1) == False
assert is_prime(0) == False
assert is_prime(-5) == False
assert is_prime(17) == True
assert is_prime(25) == False
print("ALL PASSED")
"""


def ask(client: Anthropic, prompt: str) -> str:
    msg = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def extract_code(text: str) -> str:
    if "```python" in text:
        return text.split("```python")[1].split("```")[0].strip()
    if "```" in text:
        return text.split("```")[1].split("```")[0].strip()
    return text.strip()


def run_tests(code: str):
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "solution.py"), "w") as f:
            f.write(code)
        with open(os.path.join(d, "test.py"), "w") as f:
            f.write(TESTS)
        r = subprocess.run(
            ["python", "test.py"],
            cwd=d,
            capture_output=True,
            text=True,
            timeout=10,
        )
    ok = r.returncode == 0 and "ALL PASSED" in r.stdout
    return ok, (r.stdout + r.stderr).strip()


def reflect_loop(client: Anthropic, max_rounds: int = 3) -> str:
    code = extract_code(ask(client, f"Write the function. Spec:\n{SPEC}"))
    for i in range(1, max_rounds + 1):
        ok, log = run_tests(code)
        print(f"--- Round {i} ---\n{code}\nResult: {log}\n")
        if ok:
            print(f"Solved in {i} round(s).")
            return code
        critique_prompt = textwrap.dedent(f"""
            Your code failed the tests.
            CODE:
            {code}
            ERROR:
            {log}
            Reflect briefly on what went wrong, then output
            the corrected function in a python code block.
        """)
        code = extract_code(ask(client, critique_prompt))
    print("Failed after max rounds.")
    return code


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set the ANTHROPIC_API_KEY environment variable first.")
    reflect_loop(Anthropic())
