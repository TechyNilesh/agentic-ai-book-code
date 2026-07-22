# Chapter 7 -- Memory in Agentic Systems

This lab covers memory building blocks used in the chapter: a
summarising buffer for working memory, a Chroma vector store for
semantic recall, LangGraph's built-in store API, and a full personal
assistant that remembers facts about the user across turns and across
runs.

## Files

- `01_summary_buffer_memory.py` -- `ConversationSummaryBufferMemory`, which keeps recent turns verbatim and summarises older ones.
- `02_chroma_vector_memory.py` -- embeds text and stores/searches it in a local Chroma vector store.
- `03_langgraph_store_api.py` -- LangGraph's `BaseStore` / `InMemoryStore` for put and search of memory items. No API key needed.
- `04_personal_assistant_long_term_memory.py` -- Lab 7.1: an assistant that saves every turn as an episode in Chroma and retrieves the top-3 relevant past episodes before each reply. Memory persists to `./assistant_mem` on disk.

## How to run

Install the packages:

```bash
pip install langgraph langchain-openai langchain-chroma chromadb langchain
```

Set your API key (not needed for `03_langgraph_store_api.py`):

```bash
export OPENAI_API_KEY=sk-...
```

Then run any file:

```bash
python 01_summary_buffer_memory.py
python 02_chroma_vector_memory.py
python 03_langgraph_store_api.py
python 04_personal_assistant_long_term_memory.py
```

`02_chroma_vector_memory.py` and `04_personal_assistant_long_term_memory.py`
write a local Chroma database folder (`./mem_db` and `./assistant_mem`).
Delete these folders if you want to start with a clean memory.
