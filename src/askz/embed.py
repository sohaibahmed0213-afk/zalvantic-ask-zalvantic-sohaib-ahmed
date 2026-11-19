import sys
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chunk import load_chunks  # noqa: E402

MODELS = {
    "multilingual": "paraphrase-multilingual-MiniLM-L12-v2",
    "english": "all-MiniLM-L6-v2",
}


def build_index(chunks, model_name):
    model = SentenceTransformer(model_name)
    texts = [c["text"] for c in chunks]
    vectors = model.encode(texts, normalize_embeddings=True)
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors.astype("float32"))
    return model, index


def search(query, model, index, chunks, k=5):
    q = model.encode([query], normalize_embeddings=True)
    scores, ids = index.search(q.astype("float32"), k)
    return [(float(s), chunks[i]) for s, i in zip(scores[0], ids[0])]