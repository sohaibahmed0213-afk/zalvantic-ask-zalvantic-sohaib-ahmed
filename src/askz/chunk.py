import json
import re
import sys
from pathlib import Path

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")

# Settings for the fixed-size strategy (counted in words).
CHUNK_WORDS = 200
OVERLAP_WORDS = 40


def split_by_heading(text):
    """Split Markdown text into (heading, body) sections."""
    sections = []
    heading, lines = "", []
    for line in text.splitlines():
        if re.match(r"^#{1,6}\s", line):
            if heading or lines:
                sections.append((heading, "\n".join(lines).strip()))
            heading, lines = line.lstrip("# ").strip(), []
        else:
            lines.append(line)
    sections.append((heading, "\n".join(lines).strip()))
    return sections


def chunk_by_heading(source, text):
    """Strategy 1: one chunk per heading section."""
    chunks = []
    for heading, body in split_by_heading(text):
        full = (heading + "\n" + body).strip()
        if len(full.split()) < 5:  # skip headings with almost no text
            continue
        chunks.append({
            "id": f"{Path(source).stem}-h{len(chunks) + 1}",
            "source": source,
            "service": heading,
            "text": full,
        })
    return chunks


def chunk_fixed(source, text, size=CHUNK_WORDS, overlap=OVERLAP_WORDS):
    """Strategy 2: fixed-size word windows that overlap a little."""
    title = split_by_heading(text)[0][0] or split_by_heading(text)[1][0]
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        piece = words[start:start + size]
        chunks.append({
            "id": f"{Path(source).stem}-f{len(chunks) + 1}",
            "source": source,
            "service": title,
            "text": " ".join(piece),
        })
        if start + size >= len(words):
            break
        start += size - overlap
    return chunks


def write_jsonl(path, chunks):
    with open(path, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")


def load_chunks(strategy, processed_dir=OUT_DIR):
    """Read a saved chunk file back. strategy is 'heading' or 'fixed'."""
    path = Path(processed_dir) / f"chunks_{strategy}.jsonl"
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    files = sorted(RAW_DIR.glob("*.md"))
    if not files:
        print("No .md files found in data/raw. Run this from the repository root.")
        return
    heading_chunks, fixed_chunks = [], []
    for file in files:
        text = file.read_text(encoding="utf-8")
        heading_chunks += chunk_by_heading(file.name, text)
        fixed_chunks += chunk_fixed(file.name, text)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUT_DIR / "chunks_heading.jsonl", heading_chunks)
    write_jsonl(OUT_DIR / "chunks_fixed.jsonl", fixed_chunks)

    for name, chunks in (("heading", heading_chunks), ("fixed", fixed_chunks)):
        sizes = [len(c["text"].split()) for c in chunks]
        print(f"{name}: {len(chunks)} chunks, "
              f"average {sum(sizes) // len(sizes)} words, "
              f"min {min(sizes)}, max {max(sizes)}")


if __name__ == "__main__":
    main()