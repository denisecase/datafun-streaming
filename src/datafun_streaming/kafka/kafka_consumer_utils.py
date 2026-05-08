"""src/datafun_streaming/kafka/kafka_consumer_utils.py.

Consumer helpers for Kafka messages.
"""

# === IMPORTS ===

import logging
from typing import Any

from confluent_kafka import Consumer

from datafun_streaming.io.io_utils import row_from_json
from datafun_streaming.kafka.errors import kafka_consume_failed_message
from datafun_streaming.kafka.kafka_settings import KafkaSettings

# === EXPORTS

__all__ = [
    "create_consumer",
    "consume_kafka_message",
]

# === DEFINE HELPER FUNCTIONS ===


def create_consumer(settings: KafkaSettings) -> Consumer:
    """Create a Kafka consumer."""
    return Consumer(
        settings.consumer_config(),
        logger=logging.getLogger("rdkafka.consumer"),
    )


def consume_kafka_message(
    *,
    consumer: Any,
    timeout_seconds: float,
) -> dict[str, Any] | None:
    """Consume one Kafka message and return it as a row dictionary."""
    message = consumer.poll(timeout_seconds)

    if message is None:
        return None

    if message.error():
        msg = kafka_consume_failed_message(detail=str(message.error()))
        raise RuntimeError(msg)

    raw_value = message.value()

    if raw_value is None:
        return None

    row = row_from_json(raw_value.decode("utf-8"))

    raw_key = message.key()
    row["_kafka_key"] = raw_key.decode("utf-8") if raw_key else ""
    row["_kafka_partition"] = message.partition()
    row["_kafka_offset"] = message.offset()

    return row
