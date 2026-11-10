import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bm25 import build_index, search  # noqa: E402
from chunk import load_chunks  # noqa: E402

QUESTIONS_FILE = Path("eval/questions.json")


def is_hit(chunk, question):
    """A chunk is correct if it comes from the expected file and contains
    the expected section heading."""
    return (chunk["source"] == question["expected_source"]
            and question["expected_section"] in chunk["text"])


def hit_at_k(questions, chunks, index, k=3):
    """Return (hits, results) where results is a list of (question, hit)."""
    results = []
    for q in questions:
        top = search(q["question"], chunks, index, k=k)
        hit = any(is_hit(chunk, q) for _score, chunk in top)
        results.append((q, hit))
    hits = sum(1 for _q, hit in results if hit)
    return hits, results


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    verbose = "--verbose" in sys.argv
    k = 3
    if "--k" in sys.argv:
        k = int(sys.argv[sys.argv.index("--k") + 1])
    questions = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))
    total = len(questions)

    for strategy in ("heading", "fixed"):
        chunks = load_chunks(strategy)
        index = build_index(chunks)
        hits, results = hit_at_k(questions, chunks, index, k=k)
        print(f"Chunking: {strategy} ({len(chunks)} chunks)")
        print(f"  hit@{k} overall: {hits}/{total} = {hits / total:.2f}")
        for lang, label in (("en", "English"), ("ur-roman", "Roman Urdu")):
            group = [hit for q, hit in results if q["lang"] == lang]
            if group:
                print(f"  hit@{k} {label}: {sum(group)}/{len(group)} = {sum(group) / len(group):.2f}")
        if verbose:
            missed = [q["id"] for q, hit in results if not hit]
            print(f"  missed question ids: {missed}")
        print()


if __name__ == "__main__":
    main()