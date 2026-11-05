import re
import sys
from pathlib import Path

STOPWORDS = {
    "the", "a", "an", "is", "are", "do", "does", "you", "your", "we", "i", "of",
    "to", "in", "for", "and", "or", "can", "what", "how", "which", "who", "my",
    "it", "on", "with", "at", "by", "be", "this", "that", "have", "has",
    "zalvantic", "me", "our", "us", "from", "as", "about",
}


def tokens(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if w not in STOPWORDS}


def load_paragraphs(raw_dir="data/raw"):
    paragraphs = []
    for file in sorted(Path(raw_dir).glob("*.md")):
        heading = ""
        text = file.read_text(encoding="utf-8")
        for block in re.split(r"\n\s*\n", text):
            block = block.strip()
            if not block:
                continue
            if block.startswith("#"):
                first_line, _, rest = block.partition("\n")
                heading = first_line.lstrip("# ").strip()
                block = rest.strip()
                if not block:
                    continue
            if len(block.split()) >= 8:
                paragraphs.append((file.name, heading, block))
    return paragraphs


def search(question, paragraphs):
    q = tokens(question)
    best_score, best = 0, None
    for source, heading, text in paragraphs:
        score = len(q & tokens(heading + " " + text))
        if score > best_score:
            best_score, best = score, (source, heading, text)
    return best_score, best


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print('Usage: python src/askz/search_cli.py "your question"')
        return
    question = " ".join(sys.argv[1:])
    paragraphs = load_paragraphs()
    score, best = search(question, paragraphs)
    if best is None:
        print("No matching paragraph found.")
        return
    source, heading, text = best
    print(f"Source: {source} | Section: {heading} | Score: {score}\n")
    print(text)


if __name__ == "__main__":
    main()