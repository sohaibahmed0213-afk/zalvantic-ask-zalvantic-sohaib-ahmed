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
Week 1 done: knowledge base, evaluation questions and a simple command-line search.

## Project structure
- `data/raw/`: cleaned Markdown notes from the public Zalvantic website (home, FAQ, services, about, work, contact)
- `eval/questions.json`: 45 evaluation questions (12 in Roman Urdu) with the expected source file and section
- `src/askz/search_cli.py`: simple command-line search that prints the best matching paragraph

## Run the search (Week 1)
Requires Python 3. No extra packages are needed.

    python src/askz/search_cli.py "How long does a typical project take?"

## Learning log
- Week 1: Collected public text from zalvantic.com and cleaned it (removed menus, footers and duplicate lines). Wrote 45 questions with expected sources. Built a keyword-overlap search. It works well for English questions but is weak for Roman Urdu, because Roman Urdu words do not appear in the English notes. Embeddings in Week 3 should fix this.