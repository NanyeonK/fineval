from __future__ import annotations


def hybrid_score(struct_score: float, adj_text_score: float, lam: float = 0.5) -> float:
    return lam * struct_score + (1 - lam) * adj_text_score
