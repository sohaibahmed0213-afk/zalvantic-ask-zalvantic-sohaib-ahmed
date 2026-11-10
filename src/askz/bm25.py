import re
import sys
from pathlib import Path

from rank_bm25 import BM25Okapi

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chunk import load_chunks  # noqa: E402

STOPWORDS = {
    "the", "a", "an", "is", "are", "do", "does", "you", "your", "we", "i", "of",
    "to", "in", "for", "and", "or", "can", "what", "how", "which", "who", "my",
    "it", "on", "with", "at", "by", "be", "this", "that", "have", "has",
    "zalvantic", "me", "our", "us", "from", "as", "about",
}


def tokenize(text):
    """Lowercase, keep letters and numbers, drop very common words."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w for w in words if w not in STOPWORDS]


def build_index(chunks):
    """Build a BM25 index. Each chunk becomes a list of tokens."""
    return BM25Okapi([tokenize(c["text"]) for c in chunks])


def search(question, chunks, index, k=3):
    """Return the top k chunks as (score, chunk), best first."""
    scores = index.get_scores(tokenize(question))
    ranked = sorted(zip(scores, chunks), key=lambda pair: pair[0], reverse=True)
    return ranked[:k]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print('Usage: python src/askz/bm25.py "your question" [heading|fixed]')
        return
    question = sys.argv[1]
    strategy = sys.argv[2] if len(sys.argv) > 2 else "heading"
    chunks = load_chunks(strategy)
    index = build_index(chunks)
    print(f"Strategy: {strategy} | Question: {question}\n")
    for rank, (score, chunk) in enumerate(search(question, chunks, index), start=1):
        preview = chunk["text"][:160].replace("\n", " ")
        print(f"{rank}. {chunk['id']} ({chunk['source']}) score={score:.2f}")
        print(f"   {preview}...\n")


if __name__ == "__main__":
    main()