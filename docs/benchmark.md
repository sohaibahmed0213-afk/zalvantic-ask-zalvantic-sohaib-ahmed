# Week 3 benchmark

Questions: 45 (33 English, 12 Roman Urdu). Each system returns its top 5 chunks.

- recall@5: share of questions where a correct chunk is in the top 5.
- MRR: average of 1/rank of the first correct chunk (0 if it is not in the top 5).

| System | Chunking | recall@5 All | MRR All | recall@5 English | MRR English | recall@5 Roman Urdu | MRR Roman Urdu |
|---|---|---|---|---|---|---|---|
| BM25 | heading (51 chunks) | 0.84 | 0.72 | 0.85 | 0.72 | 0.83 | 0.74 |
| Embeddings: multilingual | heading (51 chunks) | 0.82 | 0.63 | 0.88 | 0.70 | 0.67 | 0.44 |
| Embeddings: english | heading (51 chunks) | 0.69 | 0.56 | 0.79 | 0.64 | 0.42 | 0.33 |
| BM25 | fixed (15 chunks) | 0.89 | 0.74 | 0.88 | 0.73 | 0.92 | 0.78 |
| Embeddings: multilingual | fixed (15 chunks) | 0.60 | 0.47 | 0.64 | 0.52 | 0.50 | 0.32 |
| Embeddings: english | fixed (15 chunks) | 0.69 | 0.55 | 0.82 | 0.68 | 0.33 | 0.22 |


## Notes

Results below are for heading chunks (51 chunks), recall@5.

| System | All | English | Roman Urdu |
|---|---|---|---|
| BM25 | 0.84 | 0.85 | 0.83 |
| Embeddings: multilingual | 0.82 | 0.88 | 0.67 |
| Embeddings: english | 0.69 | 0.79 | 0.42 |

**What I see**

1. BM25 is the best system overall and clearly the best on Roman Urdu. The multilingual embedding model comes close overall (0.82 vs 0.84) and is slightly better on English at recall@5 (0.88 vs 0.85), but its MRR is lower (0.70 vs 0.72), so the correct chunk is ranked lower.
2. On Roman Urdu, the multilingual model (0.67) is much better than the English-only model (0.42), so a multilingual model helps. It is still behind BM25 (0.83). A possible reason, not tested: our Roman Urdu questions contain English words such as "project" or "support", which BM25 matches exactly, while the embedding models were mostly trained on Urdu script, not Roman Urdu.
3. Chunking matters. Fixed-size chunks (15 large chunks) give BM25 higher scores (0.89), partly because with only 15 chunks it is easier to hit the right one. They hurt the multilingual model (0.60). A possible reason, not tested: embedding models only read the first part of a long text, and fixed chunks are 200 words.
4. There are only 45 questions (12 in Roman Urdu). One question is worth 0.02 overall and 0.08 on Roman Urdu, so small differences, such as 0.84 vs 0.82, may be noise.

**Decision for Week 4:** keep heading chunks and combine BM25 with the multilingual embedding model (hybrid search). BM25 is strong on exact words and the embeddings add matches by meaning. The English-only model stays as a baseline only.