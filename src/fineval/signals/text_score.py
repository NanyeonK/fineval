from __future__ import annotations


def text_score(call_comp: float, filing_comp: float, news_comp: float, weights: tuple[float, float, float] = (0.5, 0.25, 0.25)) -> float:
    return weights[0] * call_comp + weights[1] * filing_comp + weights[2] * news_comp


def adjusted_text_score(raw_text_score: float, dq: float, rl: float) -> float:
    return raw_text_score * dq * rl
