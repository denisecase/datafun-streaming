"""src/datafun_streaming/kafka/errors.py.

Error messages for Kafka.
"""

# === EXPORTS

__all__ = [
    "kafka_admin_failed_message",
    "kafka_consume_failed_message",
    "kafka_delivery_failed_message",
    "kafka_no_messages_message",
    "kafka_not_reachable_message",
    "kafka_topic_empty_message",
    "kafka_topic_not_found_message",
]

# === DEFINE HELPER FUNCTIONS ===


def kafka_admin_failed_message(*, operation: str, topic: str, detail: str) -> str:
    """Return help text for a failed Kafka admin operation."""
    return f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
A Kafka admin operation failed.
Operation: {operation}
Topic:     {topic}
Details:
    {detail}

CHECK:
1. Confirm Kafka is running. Follow ref_START_KAFKA.md.
2. Confirm you have permission to {operation} topics.
3. Try the operation manually from the CLI:
   cd ~/kafka
   bin/kafka-topics.sh --list --bootstrap-server localhost:9092
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""".strip()


def kafka_consume_failed_message(*, detail: str) -> str:
    """Return help text for a Kafka consume failure."""
    return f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
The consumer ran, but Kafka did not return a usable message.
Kafka reported an error while consuming a message.
Details:
    {detail}

CHECK:
1. Confirm Kafka is running.
2. Confirm the topic exists. Follow MANAGE_TOPIC.md.
3. Run the producer again if the topic has no messages.
4. If you already consumed these messages,
   set a different KAFKA_GROUP_ID in .env.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""".strip()


def kafka_delivery_failed_message(*, detail: str) -> str:
    """Return help text for a Kafka delivery failure."""
    return f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
The message was generated, but Kafka did not accept it.
Kafka did not confirm message delivery.
Details:
    {detail}

CHECK:
1. Confirm Kafka is running.
2. Confirm the topic exists.
3. Confirm the broker is reachable at localhost:9092.
4. Try MANAGE_TOPIC.md to verify Kafka independently of Python.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""".strip()


def kafka_no_messages_message() -> str:
    """Return help text when no Kafka messages are consumed."""
    return """
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Kafka may be reachable, but no unread messages
were available for this consumer.
No message received before timeout.

CHECK:
1. Confirm Kafka is running.
2. Confirm the topic exists. Follow MANAGE_TOPIC.md.
3. Run the producer in another project terminal.
4. If this consumer group already read the messages,
   set a different KAFKA_GROUP_ID in .env.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""".strip()


def kafka_not_reachable_message(*, bootstrap_servers: str) -> str:
    """Return help text for a Kafka connection failure."""
    return f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Python code is running,
but Kafka is not available.
Kafka is not reachable.
The program tried to connect to:
    KAFKA_BOOTSTRAP_SERVERS = {bootstrap_servers}

CHECK:
1. Start Kafka first. Follow START_KAFKA.md.
2. Verify Kafka is running. In a terminal, run:
   cd ~/kafka
   bin/kafka-topics.sh --list --bootstrap-server localhost:9092
3. Verify the topic exists. Follow MANAGE_TOPIC.md.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""".strip()


def kafka_topic_empty_message(*, topic: str) -> str:
    """Return help text when a Kafka topic exists but has no messages."""
    return f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
The topic exists but contains no messages.
Topic is empty:
    KAFKA_TOPIC = {topic}

CHECK:
1. Run the producer first to send messages to this topic.
2. If you already ran the producer, confirm it completed successfully.
3. If messages were consumed by another consumer group,
   run the producer again to repopulate the topic.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""".strip()


def kafka_topic_not_found_message(*, topic: str, bootstrap_servers: str) -> str:
    """Return help text when a required Kafka topic does not exist."""
    return f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
The topic does not exist in Kafka.
Topic not found:
    KAFKA_TOPIC = {topic}
    KAFKA_BOOTSTRAP_SERVERS = {bootstrap_servers}

CHECK:
1. Create the topic first. Follow ref_MANAGE_TOPIC.md.
   cd ~/kafka
   bin/kafka-topics.sh --create --topic {topic} --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
2. Confirm the topic was created:
   bin/kafka-topics.sh --list --bootstrap-server localhost:9092
3. Confirm KAFKA_TOPIC in .env matches the topic you created.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""".strip()
