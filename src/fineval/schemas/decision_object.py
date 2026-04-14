from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class Horizon(BaseModel):
    unit: Literal["day", "week", "month", "quarter"]
    value: int = Field(gt=0)


class EvidenceItem(BaseModel):
    type: Literal["macro_data", "market_data", "news", "filing", "transcript", "note", "user_context"]
    source_id: str
    source_summary: str
    relevance: str


class RelativeViewPayload(BaseModel):
    long_asset: str
    short_asset: str
    relation: Literal["outperform"] = "outperform"
    target_metric: Literal["excess_return", "relative_return"] = "relative_return"
    expected_spread: float
    direction_only: bool = False

    @field_validator("expected_spread")
    @classmethod
    def check_spread(cls, v: float) -> float:
        if abs(v) > 0.25:
            raise ValueError("expected_spread is implausibly large for prototype 0")
        return v


class ConfidenceObject(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    scale: Literal["0_to_1"] = "0_to_1"
    confidence_type: Literal["model_judgement", "stability_based", "agreement_based"] = "model_judgement"
    calibration_status: Literal["uncalibrated", "weakly_calibrated", "calibrated"] = "uncalibrated"
    reason: str
    uncertainty_notes: str


class AuditObject(BaseModel):
    schema_version: str = "v0.2"
    generated_from: str
    human_reviewed: bool = False
    integrity_status: Literal["unchecked", "pass", "fail_with_notes", "fail"] = "unchecked"
    rejection_reason: str | None = None


class FinancialDecisionObject(BaseModel):
    view_id: str
    timestamp: str
    model: str
    prompt_version: str
    view_type: Literal["relative", "absolute", "regime", "constraint"] = "relative"
    horizon: Horizon
    target_universe: list[str]
    statement: str
    evidence_bundle: list[EvidenceItem]
    view_payload: RelativeViewPayload
    confidence: ConfidenceObject
    audit: AuditObject

    @field_validator("evidence_bundle")
    @classmethod
    def check_evidence_nonempty(cls, v: list[EvidenceItem]) -> list[EvidenceItem]:
        if not v:
            raise ValueError("evidence_bundle must be non-empty")
        return v
