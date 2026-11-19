import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bm25 as bm25_mod  # noqa: E402
import embed as embed_mod  # noqa: E402
from chunk import load_chunks  # noqa: E402
from evaluate import QUESTIONS_FILE, is_hit  # noqa: E402

OUT_FILE = Path("docs/benchmark.md")
LANGUAGES = (("all", "All"), ("en", "English"), ("ur-roman", "Roman Urdu"))


def first_hit_rank(top, question):
    for rank, (_score, chunk) in enumerate(top, start=1):
        if is_hit(chunk, question):
            return rank
    return None


def metrics(ranks):
    n = len(ranks)
    recall = sum(1 for r in ranks if r is not None) / n
    mrr = sum(1 / r for r in ranks if r is not None) / n
    return recall, mrr


def rank_all(search_fn, questions):
    return [(q, first_hit_rank(search_fn(q["question"]), q)) for q in questions]


def systems(chunks, k):
    bm25_index = bm25_mod.build_index(chunks)
    yield "BM25", lambda text: bm25_mod.search(text, chunks, bm25_index, k=k)
    for key, model_name in embed_mod.MODELS.items():
        model, index = embed_mod.build_index(chunks, model_name)
        yield (
            f"Embeddings: {key}",
            lambda text, model=model, index=index: embed_mod.search(
                text, model, index, chunks, k=k
            ),
        )


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    verbose = "--verbose" in sys.argv
    k = 5
    if "--k" in sys.argv:
        k = int(sys.argv[sys.argv.index("--k") + 1])

    questions = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))
    counts = {lang: sum(1 for q in questions if lang == "all" or q["lang"] == lang)
              for lang, _label in LANGUAGES}

    header = ["System", "Chunking"]
    for _lang, label in LANGUAGES:
        header += [f"recall@{k} {label}", f"MRR {label}"]
    rows = []

    for strategy in ("heading", "fixed"):
        chunks = load_chunks(strategy)
        for name, search_fn in systems(chunks, k):
            results = rank_all(search_fn, questions)
            row = [name, f"{strategy} ({len(chunks)} chunks)"]
            for lang, _label in LANGUAGES:
                ranks = [r for q, r in results if lang == "all" or q["lang"] == lang]
                recall, mrr = metrics(ranks)
                row += [f"{recall:.2f}", f"{mrr:.2f}"]
            rows.append(row)
            if verbose:
                missed = [q["id"] for q, r in results if r is None]
                print(f"{name} / {strategy}: missed {missed}")

    lines = [
        "# Week 3 benchmark",
        "",
        f"Questions: {counts['all']} ({counts['en']} English, {counts['ur-roman']} Roman Urdu). "
        f"Each system returns its top {k} chunks.",
        "",
        f"- recall@{k}: share of questions where a correct chunk is in the top {k}.",
        f"- MRR: average of 1/rank of the first correct chunk (0 if it is not in the top {k}).",
        "",
        "| " + " | ".join(header) + " |",
        "|" + "---|" * len(header),
    ]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    text = "\n".join(lines) + "\n"

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(text, encoding="utf-8")
    print(text)
    print(f"Saved to {OUT_FILE}")


if __name__ == "__main__":
    main()