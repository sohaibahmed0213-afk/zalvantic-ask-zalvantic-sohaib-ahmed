# Ask Zalvantic

An AI sales and support assistant that answers client questions about Zalvantic, with sources, in English and Roman Urdu.

Built as part of the Zalvantic Internship Programme (AI / ML Engineering).

## Where the project is

| Week | What gets built | Finish by | Status |
|---|---|---|---|
| 1 | Collect and structure what Zalvantic knows about itself | 08/11/2026 | Done |
| 2 | Split the knowledge into chunks and search it with BM25 | 15/11/2026 | Done |
| 3 | Search by meaning, not only keywords | 22/11/2026 | Not started |
| 4 | Combine keyword and vector search and pick a winner | 29/11/2026 | Not started |
| 5 | Generate answers that stay inside the sources | 06/12/2026 | Not started |
| 6 | Make failure safe | 13/12/2026 | Not started |
| 7 | Turn the pipeline into a service | 20/12/2026 | Not started |
| 8 | Make it deployable by someone else | 27/12/2026 | Not started |

## Status
- Week 1 done: knowledge base, evaluation questions and a simple command-line search.
- Week 2 done: two chunking strategies, BM25 search and a hit@3 report for each strategy.

## Project structure
- `data/raw/`: cleaned Markdown notes from the public Zalvantic website (home, FAQ, services, about, work, contact)
- `eval/questions.json`: 45 evaluation questions (12 in Roman Urdu) with the expected source file and section
- `src/askz/search_cli.py`: simple command-line search that prints the best matching paragraph (Week 1)
- `src/askz/chunk.py`: two chunking strategies, by heading and fixed size with overlap (Week 2)
- `src/askz/bm25.py`: BM25 search over chunks using rank-bm25 (Week 2)
- `src/askz/evaluate.py`: reports hit@3 for each chunking strategy (Week 2)
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

## Week 2 results (hit@3 on eval/questions.json)

| Chunking strategy | Chunks | hit@3 overall | English (33) | Roman Urdu (12) |
|---|---|---|---|---|
| By heading | 51 | 38/45 (0.84) | 28/33 (0.85) | 10/12 (0.83) |
| Fixed size with overlap | 15 | 38/45 (0.84) | 27/33 (0.82) | 11/12 (0.92) |

The two strategies tie overall. The per-language gap is one question each way, which is too small to call a winner.

The tie is not equal in practice. Fixed size has only 15 chunks, so the top 3 cover about 20% of the knowledge base and hit@3 is easier to reach. Heading has 51 chunks, so the top 3 cover about 6%. Heading chunks are also one topic each, so a source can be cited by section.

For now I use **heading chunking**. I will re-check this in Weeks 3 and 4 with recall@5 and MRR.

## Learning log
- Week 1: Collected public text from zalvantic.com and cleaned it (removed menus, footers and duplicate lines). Wrote 45 questions with expected sources. Built a keyword-overlap search. It works well for English questions but is weak for Roman Urdu, because Roman Urdu words do not appear in the English notes. Embeddings in Week 3 should fix this.
- Week 2: Split the notes into chunks in two ways (by heading, and fixed size with overlap) and added BM25 search with rank-bm25. Wrote `evaluate.py` to measure hit@3 for each strategy, with unit tests. Both strategies scored 38/45. I learned that fewer, larger chunks make hit@3 easier, so a tie favours the strategy with more chunks. BM25 only matches exact words, so Roman Urdu is still weak. Embeddings in Week 3 should help.
