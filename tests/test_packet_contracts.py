import pytest

from fineval.data.monthly_packet import (
    MonthlyTextPacket,
    PacketProvenance,
    PacketSource,
    validate_packet_point_in_time,
    validate_packet_source_count,
)


def make_valid_packet() -> MonthlyTextPacket:
    return MonthlyTextPacket(
        ticker='NVDA',
        as_of_date='2024-01-31',
        packet_id='nvda_2024_01',
        sources=[
            PacketSource(
                source_id='src1',
                source_type='earnings_call',
                published_at='2024-01-20',
                text='AI demand remains strong.',
                provider='toy',
            ),
            PacketSource(
                source_id='src2',
                source_type='news',
                published_at='2024-01-28',
                text='Capex outlook revised upward.',
                provider='toy',
            ),
        ],
        provenance=PacketProvenance(
            built_at='2024-01-31T18:00:00Z',
            builder='toy-builder',
            source_count=2,
            dataset_version='toy-v1',
        ),
    )


def test_packet_point_in_time_validation_passes_for_valid_packet():
    packet = make_valid_packet()
    validate_packet_point_in_time(packet)
    validate_packet_source_count(packet)


def test_packet_point_in_time_validation_rejects_future_source():
    packet = make_valid_packet()
    packet.sources[1].published_at = '2024-02-01'
    with pytest.raises(ValueError):
        validate_packet_point_in_time(packet)


def test_packet_source_count_validation_rejects_mismatch():
    packet = make_valid_packet()
    packet.provenance.source_count = 1
    with pytest.raises(ValueError):
        validate_packet_source_count(packet)


def test_packet_source_requires_required_fields():
    with pytest.raises(TypeError):
        PacketSource(
            source_type='news',
            published_at='2024-01-20',
            text='missing source id',
        )
