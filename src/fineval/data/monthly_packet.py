from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MonthlyTextPacket:
    ticker: str
    as_of_date: str
    packet_id: str
    sources: list[dict]


def load_packet_examples(path: str | Path) -> list[MonthlyTextPacket]:
    records = json.loads(Path(path).read_text())
    return [MonthlyTextPacket(**record) for record in records]


def filter_sources_point_in_time(sources: list[dict], as_of_date: str) -> list[dict]:
    return [source for source in sources if source["published_at"] <= as_of_date]
