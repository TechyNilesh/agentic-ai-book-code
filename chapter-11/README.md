# Chapter 11 — Agentic RAG

This chapter moves from naive RAG (chunk, embed, retrieve, generate in
one pass) to agentic RAG, where the agent grades its own retrieval and
loops if the chunks are poor. The chapter lab builds a self-correcting
RAG system over a folder of PDF lecture notes: it retrieves, grades,
rewrites the query when needed, and answers with citations.

## Files

| File | What it shows |
|---|---|
| `01_naive_rag.py` | The textbook naive RAG pipeline: chunk a text file, embed with Chroma, retrieve top-k, generate an answer. |
| `02_chunking_strategies.py` | Recursive chunking with `RecursiveCharacterTextSplitter`. |
| `03_embeddings_vector_store.py` | Creating a Chroma store with on-disk persistence. |
| `04_hybrid_search_reranking.py` | A cross-encoder re-ranker that re-scores retrieved candidates. |
| `05_query_rewriting_hyde.py` | HyDE: write a hypothetical answer first, then retrieve near it. |
| `06_citations.py` | Tagging chunks with citation markers and building a "cite as [n]" prompt. |
| `07_self_correcting_rag_wikipedia.py` | The chapter's worked example: a CRAG-style graph (retrieve, grade, rewrite, generate) over a photosynthesis snippet. |
| `08_lab_agentic_rag_pdf_corpus.py` | **The chapter lab.** Ingests a folder of PDFs, builds the same grade/rewrite/generate graph over them, and answers with citations. |

Note: the book's Solved Problems 1 and 2 in this chapter are
back-of-envelope math questions (estimating chunk counts, reasoning
about hybrid search) with no code to extract, so there is no file for
them here.

## How to run

Most files in this chapter call the OpenAI API for embeddings and
chat completions. Set your key as an environment variable — never
hardcode it in the code:

```bash
export OPENAI_API_KEY=sk-...
```

Install the packages used across this chapter:

```bash
pip install langchain langgraph langchain-chroma langchain-openai \
            langchain-community langchain-text-splitters langchain-core \
            pypdf sentence-transformers
```

Then run any file directly, for example:

```bash
python 01_naive_rag.py                     # needs a notes.txt file in this folder
python 07_self_correcting_rag_wikipedia.py  # self-contained, no extra files needed
python 08_lab_agentic_rag_pdf_corpus.py     # needs a notes/ folder of PDFs
```

`04_hybrid_search_reranking.py` downloads a small cross-encoder model
from Hugging Face the first time it runs, so it needs internet access
but no API key.
