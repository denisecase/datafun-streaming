"""Tests for datafun_streaming.kafka.errors.

All message functions are pure string builders; no Kafka required.
Each test confirms the output is non-empty and contains key diagnostic terms.
"""

from datafun_streaming.kafka.errors import (
    kafka_admin_failed_message,
    kafka_consume_failed_message,
    kafka_delivery_failed_message,
    kafka_no_messages_message,
    kafka_not_reachable_message,
    kafka_topic_empty_message,
    kafka_topic_not_found_message,
)


def test_kafka_admin_failed_message() -> None:
    msg = kafka_admin_failed_message(
        operation="list_topics", topic="sales", detail="timeout"
    )
    assert "list_topics" in msg
    assert "sales" in msg
    assert "timeout" in msg


def test_kafka_consume_failed_message() -> None:
    msg = kafka_consume_failed_message(detail="broker unavailable")
    assert "broker unavailable" in msg
    assert len(msg) > 0


def test_kafka_delivery_failed_message() -> None:
    msg = kafka_delivery_failed_message(detail="timed out")
    assert "timed out" in msg
    assert len(msg) > 0


def test_kafka_no_messages_message() -> None:
    msg = kafka_no_messages_message()
    assert len(msg) > 0
    assert "timeout" in msg.lower() or "message" in msg.lower()


def test_kafka_not_reachable_message() -> None:
    msg = kafka_not_reachable_message(bootstrap_servers="localhost:9092")
    assert "localhost:9092" in msg


def test_kafka_topic_empty_message() -> None:
    msg = kafka_topic_empty_message(topic="sales-topic")
    assert "sales-topic" in msg


def test_kafka_topic_not_found_message() -> None:
    msg = kafka_topic_not_found_message(
        topic="sales-topic", bootstrap_servers="localhost:9092"
    )
    assert "sales-topic" in msg
    assert "localhost:9092" in msg
