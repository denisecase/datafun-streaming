"""src/datafun_streaming/kafka/kafka_consumer_utils.py.

Consumer helpers for Kafka messages.
"""

# === IMPORTS ===

import logging
from typing import Any

from confluent_kafka import Consumer
from confluent_kafka.cimpl import OFFSET_BEGINNING, TopicPartition

from datafun_streaming.io.io_utils import row_from_json
from datafun_streaming.kafka.errors import (
    kafka_consume_failed_message,
    kafka_topic_empty_message,
    kafka_topic_not_found_message,
)
from datafun_streaming.kafka.kafka_admin_utils import (
    create_admin_client,
    get_topic_message_count,
    topic_exists,
)
from datafun_streaming.kafka.kafka_settings import KafkaSettings

# === EXPORTS

__all__ = [
    "consume_kafka_message",
    "create_consumer",
    "create_consumer_from_beginning",
    "verify_consumer_topic_ready",
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
    """Consume one Kafka message and return it as a row dictionary.

    All arguments after the asterisk must be passed as keyword arguments.

    Arguments:
        consumer: A confluent_kafka.Consumer instance.
        timeout_seconds: How long to wait for a message before giving up.

    Returns:
        A dictionary representing the message, or None if no message was received.

    """
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


def verify_consumer_topic_ready(settings: KafkaSettings) -> None:
    """Verify the Kafka topic exists and has messages.

    Arguments:
        settings: KafkaSettings instance with the topic and consumer config.

    Returns:
        None

    Raises:
        RuntimeError: If the topic does not exist or has no messages.
    """
    admin = create_admin_client(settings)

    if not topic_exists(admin, settings.topic):
        msg = kafka_topic_not_found_message(
            topic=settings.topic,
            bootstrap_servers=settings.bootstrap_servers,
        )
        raise RuntimeError(msg)

    message_count = get_topic_message_count(admin, settings.topic, settings)

    if message_count == 0:
        msg = kafka_topic_empty_message(topic=settings.topic)
        raise RuntimeError(msg)


def create_consumer_from_beginning(settings: KafkaSettings) -> Any:
    """Create a Kafka consumer subscribed to the topic from the beginning.

    This is useful for learning examples where each run should read all
    available messages from the topic.

    Arguments:
        settings: KafkaSettings instance with the topic and consumer config.

    Returns:
        A confluent_kafka.Consumer instance subscribed to the topic from the beginning.
    """
    consumer = create_consumer(settings)

    consumer.subscribe(
        [settings.topic],
        on_assign=lambda c, partitions: c.assign(
            [
                TopicPartition(
                    partition.topic,
                    partition.partition,
                    OFFSET_BEGINNING,
                )
                for partition in partitions
            ]
        ),
    )

    return consumer
