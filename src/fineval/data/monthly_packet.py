from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class PacketSource:
    source_id: str
    source_type: str
    published_at: str
    text: str
    author: str | None = None
    provider: str | None = None
    title: str | None = None
    url: str | None = None
    as_of_date: str | None = None
    metadata: dict | None = None

    def __getitem__(self, key: str):
        return getattr(self, key)


@dataclass
class PacketProvenance:
    built_at: str
    builder: str
    source_count: int
    dataset_version: str | None = None
    notes: str | None = None


@dataclass
class MonthlyTextPacket:
    ticker: str
    as_of_date: str
    packet_id: str
    sources: list[PacketSource]
    provenance: PacketProvenance | None = None
    metadata: dict = field(default_factory=dict)


def packet_to_dict(packet: MonthlyTextPacket) -> dict:
    return asdict(packet)


def validate_packet_point_in_time(packet: MonthlyTextPacket) -> None:
    for source in packet.sources:
        if source.published_at > packet.as_of_date:
            raise ValueError(
                f'source {source.source_id} published after packet as_of_date: '
                f'{source.published_at} > {packet.as_of_date}'
            )


def validate_packet_source_count(packet: MonthlyTextPacket) -> None:
    if packet.provenance is None:
        return
    actual = len(packet.sources)
    expected = packet.provenance.source_count
    if actual != expected:
        raise ValueError(f'packet provenance source_count mismatch: expected {expected}, got {actual}')


def filter_sources_point_in_time(sources: list[PacketSource], as_of_date: str) -> list[PacketSource]:
    return [source for source in sources if source.published_at <= as_of_date]


def _parse_source(record: dict, idx: int) -> PacketSource:
    if 'source_id' not in record:
        record = {'source_id': f'source_{idx}', **record}
    return PacketSource(**record)


def load_packet_examples(path: str | Path) -> list[MonthlyTextPacket]:
    records = json.loads(Path(path).read_text())
    packets = []
    for record in records:
        parsed_sources = [_parse_source(source, idx) for idx, source in enumerate(record['sources'], start=1)]
        provenance = record.get('provenance')
        packet = MonthlyTextPacket(
            ticker=record['ticker'],
            as_of_date=record['as_of_date'],
            packet_id=record['packet_id'],
            sources=parsed_sources,
            provenance=PacketProvenance(**provenance) if provenance else None,
            metadata=record.get('metadata', {}),
        )
        validate_packet_point_in_time(packet)
        validate_packet_source_count(packet)
        packets.append(packet)
    return packets
