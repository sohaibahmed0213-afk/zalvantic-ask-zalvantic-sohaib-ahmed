# Ask Zalvantic

An AI sales and support assistant that answers client questions about Zalvantic, with sources, in English and Roman Urdu.

Built as part of the Zalvantic Internship Programme (AI / ML Engineering).

## Where the project is

| Week | What gets built | Finish by | Status |
|---|---|---|---|
| 1 | Collect and structure what Zalvantic knows about itself | 08/11/2026 | Done |
| 2 | Split the knowledge into chunks and search it with BM25 | 15/11/2026 | Done |
| 3 | Search by meaning, not only keywords | 22/11/2026 | Done |
| 4 | Combine keyword and vector search and pick a winner | 29/11/2026 | Not started |
| 5 | Generate answers that stay inside the sources | 06/12/2026 | Not started |
| 6 | Make failure safe | 13/12/2026 | Not started |
| 7 | Turn the pipeline into a service | 20/12/2026 | Not started |
| 8 | Make it deployable by someone else | 27/12/2026 | Not started |

## Status

Week 1 done: knowledge base, evaluation questions and a simple command-line search.

Week 2 done: two chunking strategies, BM25 search and a hit@3 evaluation script.

Week 3 done: embeddings with two models, a FAISS index, and a benchmark of BM25 against both models.

## Project structure

- `data/raw/`: cleaned Markdown notes from the public Zalvantic website (home, FAQ, services, about, work, contact)
- `eval/questions.json`: 45 evaluation questions (12 in Roman Urdu) with the expected source file and section
- `src/askz/search_cli.py`: simple command-line search that prints the best matching paragraph (Week 1)
- `src/askz/chunk.py`: two chunking strategies, by heading and fixed size with overlap (Week 2)
- `src/askz/bm25.py`: BM25 search over chunks using rank-bm25 (Week 2)
- `src/askz/evaluate.py`: reports hit@3 for each chunking strategy (Week 2)
- `src/askz/embed.py`: embeds the chunks with a sentence-transformers model and searches them with a FAISS index (Week 3)
- `src/askz/benchmark.py`: compares BM25 and both embedding models with recall@5 and MRR, and writes `docs/benchmark.md` (Week 3)
- `docs/benchmark.md`: the benchmark results table and notes (Week 3)
- `tests/`: unit tests for chunking and the hit@k metric (Week 2)

## Run the search (Week 1)

Requires Python 3. No extra packages are needed.

    python src/askz/search_cli.py "How long does a typical project take?"

## Run the evaluation and tests (Week 2)

Install the packages first:

    pip install rank-bm25 pytest

Print hit@3 for each chunking strategy:

    python src/askz/evaluate.py

Run the unit tests:

    pytest -q

## Run the benchmark (Week 3)

Use Python 3.11 (FAISS and PyTorch do not support Python 3.15 yet). Install the packages:

    pip install sentence-transformers faiss-cpu rank-bm25

Build the chunks and run the benchmark:

    python src/askz/chunk.py
    python src/askz/benchmark.py

The first run downloads two embedding models.

## Learning log

- Week 1: Collected public text from zalvantic.com and cleaned it (removed menus, footers and duplicate lines). Wrote 45 questions with expected sources. Built a keyword-overlap search. It works well for English questions but is weak for Roman Urdu, because Roman Urdu words do not appear in the English notes. Embeddings in Week 3 should fix this.
- Week 2: Split the notes into chunks in two ways (by heading: 51 chunks, fixed size with overlap: 15 chunks) and added BM25 search. Both strategies scored hit@3 = 38/45. Fixed size has fewer, larger chunks, which makes hit@3 easier, so I use heading chunking for now. BM25 only matches exact words, so Roman Urdu is still weak. Embeddings in Week 3 should help.
- Week 3: Embedded the chunks with two models (multilingual and English-only) and built a FAISS index for each. Compared them with BM25 using recall@5 and MRR. On heading chunks BM25 was best overall (recall@5 0.84), the multilingual model was close (0.82), and the English-only model was weaker (0.69). On Roman Urdu the multilingual model (0.67) beat the English-only one (0.42) but stayed behind BM25 (0.83). In Week 4 I will combine BM25 and embeddings.