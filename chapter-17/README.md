# Chapter 16 -- Deployment and Production

This chapter takes an agent out of the notebook and into production:
wrapping it in FastAPI, packing it into Docker, deploying it to a
free-tier host such as Render, cutting cost with caching and
batching, adding retries for rate limits, and running fully local
with Ollama or vLLM. The main lab deploys the Chapter 7
personal-assistant agent to Render behind a public HTTPS URL.

## Files

- `01_fastapi_wrapper.py` -- minimal FastAPI wrapper around a compiled LangGraph object, with a `/chat` and a `/health` endpoint (Section 16.2).
- `Dockerfile` -- generic Dockerfile for a FastAPI agent app (Section 16.3).
- `render.yaml` -- Render.com service definition used in the chapter's main lab (Section 16.10).
- `02_retry_backoff.py` -- exponential backoff around an LLM call using `tenacity` (Section 16.6).
- `03_local_ollama_llm.py` -- points a LangChain `ChatOpenAI` client at a local Ollama server for offline deployment (Section 16.7).
- `worked_example/main.py` -- the chapter's Worked Example: a 2-tool (calculator + Wikipedia search) LangGraph ReAct agent wrapped in FastAPI (Section 16.9).
- `worked_example/Dockerfile` -- Dockerfile for the worked example above.

Two files are marked illustrative because the book does not print
their full source, and the instructions ask us not to invent
substantial code:

- `01_fastapi_wrapper.py` imports `graph` from a module named
  `my_agent` -- point this at your own compiled LangGraph graph
  (e.g. your Chapter 4 or Chapter 7 agent).
- `worked_example/main.py` imports `calculator` and `wiki_search`
  from a `tools.py` you must write yourself, following the
  `@tool`-decorator pattern from Chapter 5.

## How to run

Install the packages used across this chapter's examples:

```bash
pip install fastapi uvicorn langgraph langchain-openai tenacity
```

Set your API key as an environment variable -- never hard-code it in
source or bake it into a Docker image:

```bash
export OPENAI_API_KEY=sk-...
```

Run the FastAPI wrapper locally (after supplying your own `my_agent.py`):

```bash
uvicorn 01_fastapi_wrapper:app --reload
```

Run the retry example directly:

```bash
python 02_retry_backoff.py
```

For local, offline deployment, start Ollama first, then run the
local-LLM example:

```bash
ollama pull llama3.1:8b
ollama serve   # exposes an OpenAI-compatible API on :11434
python 03_local_ollama_llm.py
```

Build and run the generic Docker image (from this folder, after
adding your own `requirements.txt` and `main.py`):

```bash
docker build -t my-agent .
docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY my-agent
```

Build and run the worked-example two-tool agent (from
`worked_example/`, after adding your own `tools.py` and
`requirements.txt`):

```bash
cd worked_example
docker build -t two-tool-agent .
docker run -p 8000:8000 -e OPENAI_API_KEY=$KEY two-tool-agent
curl -X POST localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"q": "What is 13*19?"}'
```

To follow the chapter's main lab, copy `render.yaml` into your own
deployment repo alongside a `requirements.txt` listing `fastapi`,
`uvicorn`, `langgraph`, and `langchain-openai`, push to GitHub, and
connect the repo at render.com as described in Section 16.10.
