"""src/datafun_streaming/kafka/kafka_producer_utils.py.

Kafka producer helpers for streaming examples.
"""

# === IMPORTS ===

import logging
from typing import Any

from confluent_kafka import Producer

from datafun_streaming.io.io_utils import row_to_json
from datafun_streaming.kafka.errors import (
    kafka_delivery_failed_message,
)
from datafun_streaming.kafka.kafka_settings import KafkaSettings

# === EXPORTS ===

__all__ = [
    "create_producer",
    "produce_kafka_message",
]

# === DEFINE HELPER FUNCTIONS ===


def create_producer(settings: KafkaSettings) -> Producer:
    """Create a Kafka producer.

    Arguments:
        settings: KafkaSettings object with producer configuration.

    Returns:
        A confluent_kafka.Producer instance.
    """
    return Producer(
        settings.producer_config(),
        logger=logging.getLogger("rdkafka.producer"),
    )


def produce_kafka_message(
    *,
    producer: Producer,
    topic: str,
    key: str,
    message: dict[str, Any],
) -> None:
    """Produce one dictionary message to Kafka as JSON.

    All arguments after the asterisk must be passed as keyword arguments.

    Arguments:
        producer: A confluent_kafka.Producer instance.
        topic: The Kafka topic to produce to.
        key: The Kafka message key.
        message: The message dictionary to produce.

    Returns:
        None

    Raises:
        RuntimeError: If Kafka reports a delivery failure.

    This function encodes the message as JSON and produces it to Kafka with the given key.
    It uses a delivery callback to check for delivery errors and raises a RuntimeError if any occur.

    """
    delivery_errors: list[str] = []

    def delivery_report(error: Any, delivered_message: Any) -> None:
        """Record Kafka delivery failure details."""
        if error is not None:
            delivery_errors.append(str(error))

    producer.produce(
        topic=topic,
        key=key.encode("utf-8"),
        value=row_to_json(message).encode("utf-8"),
        callback=delivery_report,
    )

    producer.poll(0)

    remaining = producer.flush(timeout=10)

    if remaining > 0:
        detail = f"{remaining} Kafka message(s) were not delivered before timeout."
        msg = kafka_delivery_failed_message(detail=detail)
        raise RuntimeError(msg)

    if delivery_errors:
        detail = "; ".join(delivery_errors)
        msg = kafka_delivery_failed_message(detail=detail)
        raise RuntimeError(msg)
