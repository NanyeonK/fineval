from __future__ import annotations

from pydantic import BaseModel


class ActionScoreRecord(BaseModel):
    ticker: str
    action_score: float
    bounded_score: float
    confidence_score: float
    quality_score: float
    reliability_score: float


class AuditPacket(BaseModel):
    as_of_date: str
    prompt_version: str
    decision_objects: list[dict]
    action_scores: list[dict]
    final_weights: list[dict]
    notes: dict
