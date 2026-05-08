"""src/datafun_streaming/kafka/kafka_admin_utils.py.

Kafka topic management helpers for streaming examples.
"""

# === IMPORTS ===

import time

from confluent_kafka import Consumer, TopicPartition
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import KafkaException, NewTopic

from datafun_streaming.kafka.errors import kafka_admin_failed_message
from datafun_streaming.kafka.kafka_settings import KafkaSettings

# === EXPORTS

__all__ = [
    "create_admin_client",
    "create_topic",
    "delete_topic",
    "list_topics",
    "topic_exists",
    "get_topic_message_count",
]

# === DECLARE CONSTANTS ===

# rdkafka's internal broker handshake takes up to ~4 seconds on Windows
# before the AdminClient is ready to accept calls. These constants
# control how long we wait and how many times we retry.
ADMIN_READY_RETRIES: int = 5
ADMIN_READY_DELAY_SECONDS: float = 2.0


# === DEFINE ADMIN HELPER FUNCTIONS ===


def create_admin_client(settings: KafkaSettings) -> AdminClient:
    """Create a Kafka AdminClient."""
    return AdminClient({"bootstrap.servers": settings.bootstrap_servers})


def create_topic(
    admin: AdminClient,
    topic: str,
    *,
    num_partitions: int = 1,
    replication_factor: int = 1,
) -> None:
    """Create a Kafka topic if it does not already exist.

    Arguments:
        admin: An AdminClient instance.
        topic: The topic name to create.
        num_partitions: Number of partitions (default 1 for local dev).
        replication_factor: Replication factor (default 1 for local dev).

    Raises:
        RuntimeError: If topic creation fails.
    """
    if topic_exists(admin, topic):
        return

    new_topic = NewTopic(
        topic,
        num_partitions=num_partitions,
        replication_factor=replication_factor,
    )

    futures = admin.create_topics([new_topic])

    for topic_name, future in futures.items():
        try:
            future.result()
        except KafkaException as error:
            msg = (
                f"Failed to create topic {topic_name!r}.\n"
                f"Kafka reported: {error}\n\n"
                "Check that Kafka is running and that you have permission to create topics."
            )
            raise RuntimeError(msg) from error


def delete_topic(admin: AdminClient, topic: str) -> None:
    """Delete a Kafka topic if it exists.

    Deleting a topic removes all its messages. Run the producer again
    after deleting to repopulate the topic.

    Arguments:
        admin: An AdminClient instance.
        topic: The topic name to delete.

    Raises:
        RuntimeError: If topic deletion fails.
    """
    if not topic_exists(admin, topic):
        return

    futures = admin.delete_topics([topic])

    for topic_name, future in futures.items():
        try:
            future.result()
        except KafkaException as error:
            msg = (
                f"Failed to delete topic {topic_name!r}.\n"
                f"Kafka reported: {error}\n\n"
                "Check that Kafka is running and that you have permission to delete topics."
            )
            raise RuntimeError(msg) from error


def list_topics(admin: AdminClient) -> list[str]:
    """Return a sorted list of topic names currently in Kafka.

    Retries several times to allow rdkafka's broker handshake to complete.
    On Windows, the handshake can take up to ~4 seconds after the AdminClient
    is created, which causes an immediate call to fail with a transport error.

    Arguments:
        admin: An AdminClient instance.

    Returns:
        A sorted list of topic name strings.

    Raises:
        RuntimeError: If Kafka is unreachable after all retries.
    """
    last_error: Exception | None = None

    for attempt in range(1, ADMIN_READY_RETRIES + 1):
        try:
            metadata = admin.list_topics(timeout=5)
            return sorted(metadata.topics.keys())
        except KafkaException as error:
            last_error = error
            if attempt < ADMIN_READY_RETRIES:
                time.sleep(ADMIN_READY_DELAY_SECONDS)

    msg = kafka_admin_failed_message(
        operation="list_topics",
        topic="(all)",
        detail=(
            f"Kafka did not respond after {ADMIN_READY_RETRIES} attempts.\n"
            f"    Last error: {last_error}"
        ),
    )
    raise RuntimeError(msg) from last_error


def topic_exists(admin: AdminClient, topic: str) -> bool:
    """Return True if the topic already exists in Kafka."""
    return topic in list_topics(admin)


def get_topic_message_count(
    admin: AdminClient, topic: str, settings: KafkaSettings
) -> int:
    """Return the total number of messages available in a topic.

    Sums the high-water offset across all partitions.
    This reflects the total messages ever produced to the topic,
    not the number of unread messages for a specific consumer group.

    Arguments:
        admin: An AdminClient instance.
        topic: The topic name to inspect.
        settings: KafkaSettings instance containing configuration.

    Returns:
        Total message count across all partitions, or 0 if topic is empty.

    Raises:
        RuntimeError: If topic metadata cannot be retrieved.
    """
    try:
        metadata = admin.list_topics(topic=topic, timeout=5)
    except KafkaException as error:
        msg = kafka_admin_failed_message(
            operation="list_topics",
            topic=topic,
            detail=str(error),
        )
        raise RuntimeError(msg) from error

    topic_metadata = metadata.topics.get(topic)
    if topic_metadata is None:
        return 0

    bootstrap_servers = settings.bootstrap_servers
    temp_consumer = Consumer(
        {
            "bootstrap.servers": bootstrap_servers,
            "group.id": "_offset_inspector",
            "enable.auto.commit": "false",
        }
    )

    total = 0
    try:
        for partition_id in topic_metadata.partitions:
            tp = TopicPartition(topic, partition_id)
            low, high = temp_consumer.get_watermark_offsets(tp, timeout=5)
            total += max(0, high - low)
    finally:
        temp_consumer.close()

    return total
