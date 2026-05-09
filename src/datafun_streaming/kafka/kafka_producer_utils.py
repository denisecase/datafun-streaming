"""src/datafun_streaming/kafka/kafka_producer_utils.py.

Kafka producer helpers for streaming examples.
"""

# === IMPORTS ===

import logging
from typing import Any

from confluent_kafka import Producer

from datafun_streaming.io.io_utils import row_to_json
from datafun_streaming.kafka.errors import kafka_delivery_failed_message
from datafun_streaming.kafka.kafka_admin_utils import (
    create_admin_client,
    create_topic,
    delete_topic,
    topic_exists,
)
from datafun_streaming.kafka.kafka_settings import KafkaSettings

# === EXPORTS ===

__all__ = [
    "create_producer",
    "prepare_producer_topic",
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


def prepare_producer_topic(settings: KafkaSettings) -> None:
    """Prepare the Kafka topic before producing messages.

    If settings.clear_topic_on_start is true, delete and recreate the topic
    so the producer starts with an empty topic.

    If settings.clear_topic_on_start is false, keep an existing topic.

    If the topic does not exist, create it.
    """
    admin = create_admin_client(settings)

    if topic_exists(admin, settings.topic):
        if settings.clear_topic_on_start:
            delete_topic(admin, settings.topic)
        else:
            return

    if not topic_exists(admin, settings.topic):
        create_topic(admin, settings.topic)


def produce_kafka_message(
    *,
    producer: Producer,
    topic: str,
    key: str,
    message: dict[str, Any],
) -> None:
    """Produce one dictionary message to Kafka as JSON.

    This function sends one message and waits for delivery before returning.
    That makes producer examples reliable and easy to reason about.

    All arguments after the asterisk must be passed as keyword arguments.

    Arguments:
        producer: A confluent_kafka.Producer instance.
        topic: The Kafka topic to produce to.
        key: The Kafka message key.
        message: The message dictionary to produce.

    Raises:
        RuntimeError: If Kafka reports a delivery failure.
    """
    delivery_errors: list[str] = []

    def delivery_report(error: Any, _delivered_message: Any) -> None:
        """Record Kafka delivery failure details."""
        if error is not None:
            delivery_errors.append(str(error))

    producer.produce(
        topic=topic,
        key=key.encode("utf-8"),
        value=row_to_json(message).encode("utf-8"),
        callback=delivery_report,
    )

    remaining = producer.flush(timeout=10)

    if remaining > 0:
        detail = f"{remaining} Kafka message(s) were not delivered before timeout."
        msg = kafka_delivery_failed_message(detail=detail)
        raise RuntimeError(msg)

    if delivery_errors:
        detail = "; ".join(delivery_errors)
        msg = kafka_delivery_failed_message(detail=detail)
        raise RuntimeError(msg)
