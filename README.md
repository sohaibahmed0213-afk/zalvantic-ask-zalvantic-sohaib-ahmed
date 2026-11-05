# Ask Zalvantic

An AI sales and support assistant that answers client questions about Zalvantic, with sources, in English and Roman Urdu.

Built as part of the Zalvantic Internship Programme (AI / ML Engineering).

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