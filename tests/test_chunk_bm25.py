import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src" / "askz"))

from bm25 import build_index, search, tokenize  # noqa: E402
from chunk import chunk_by_heading, chunk_fixed, split_by_heading  # noqa: E402
from evaluate import hit_at_k, is_hit  # noqa: E402

SAMPLE = """# Title

## Pricing

Zalvantic uses project based pricing with a clear proposal and no hidden fees for every client.

## Support

Zalvantic offers retainer packages for support, updates and monitoring after launch of the product.

## Team

The studio has engineers, designers and a founder who leads every project from the first call.

## Contact

Clients can send an email or a WhatsApp message and expect a reply within two working days.
"""


def test_split_by_heading_finds_all_sections():
    headings = [h for h, _body in split_by_heading(SAMPLE)]
    assert headings == ["Title", "Pricing", "Support", "Team", "Contact"]


def test_chunk_by_heading_skips_heading_without_text():
    chunks = chunk_by_heading("sample.md", SAMPLE)
    assert [c["id"] for c in chunks] == [
        "sample-h1", "sample-h2", "sample-h3", "sample-h4"]
    assert all(c["source"] == "sample.md" for c in chunks)
    assert chunks[0]["service"] == "Pricing"


def test_chunk_fixed_size_and_overlap():
    text = " ".join(f"w{i}" for i in range(50))
    chunks = chunk_fixed("a.md", text, size=20, overlap=5)
    assert len(chunks) == 3
    assert all(len(c["text"].split()) <= 20 for c in chunks)
    first = chunks[0]["text"].split()
    second = chunks[1]["text"].split()
    assert first[-5:] == second[:5]


def test_chunk_fixed_keeps_every_word():
    text = " ".join(f"w{i}" for i in range(50))
    chunks = chunk_fixed("a.md", text, size=20, overlap=5)
    words = set()
    for c in chunks:
        words.update(c["text"].split())
    assert words == set(text.split())


def test_tokenize_lowercases_and_drops_stopwords():
    assert tokenize("How long does a Project take?") == ["long", "project", "take"]


def test_bm25_returns_the_matching_chunk_first():
    chunks = chunk_by_heading("sample.md", SAMPLE)
    index = build_index(chunks)
    top = search("pricing and hidden fees", chunks, index, k=1)
    assert top[0][1]["service"] == "Pricing"
    top = search("retainer support", chunks, index, k=1)
    assert top[0][1]["service"] == "Support"


def test_hit_at_k_counts_a_correct_and_a_wrong_question():
    chunks = chunk_by_heading("sample.md", SAMPLE)
    index = build_index(chunks)
    questions = [
        {"question": "pricing and hidden fees", "lang": "en",
         "expected_source": "sample.md", "expected_section": "Pricing"},
        {"question": "pricing and hidden fees", "lang": "en",
         "expected_source": "other.md", "expected_section": "Pricing"},
    ]
    hits, results = hit_at_k(questions, chunks, index, k=3)
    assert hits == 1
    assert [hit for _q, hit in results] == [True, False]


def test_is_hit_needs_both_source_and_section():
    chunk = {"source": "faq.md", "text": "Pricing\nSome text"}
    good = {"expected_source": "faq.md", "expected_section": "Pricing"}
    wrong_file = {"expected_source": "home.md", "expected_section": "Pricing"}
    wrong_section = {"expected_source": "faq.md", "expected_section": "Team"}
    assert is_hit(chunk, good)
    assert not is_hit(chunk, wrong_file)
    assert not is_hit(chunk, wrong_section)