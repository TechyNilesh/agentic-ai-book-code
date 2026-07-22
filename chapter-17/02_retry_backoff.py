"""
Chapter 16 -- Deployment and Production

Exponential backoff on rate-limit and server errors, using tenacity
(Section 16.6, "Rate Limiting and Retries").

NOTE: `llm` is illustrative -- point it at your own chat model client
(e.g. a LangChain `ChatOpenAI` instance) before running this file.

Run:
    python 02_retry_backoff.py
"""

from tenacity import retry, wait_exponential, stop_after_attempt


@retry(wait=wait_exponential(min=1, max=16), stop=stop_after_attempt(5))
def safe_call(prompt):
    return llm.invoke(prompt)  # illustrative -- define `llm` yourself


if __name__ == "__main__":
    print(safe_call("Hello, world!"))
