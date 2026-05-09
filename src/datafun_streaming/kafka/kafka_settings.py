"""src/datafun_streaming/kafka/kafka_settings.py.

Kafka settings for producer and consumer examples.
"""

# === IMPORTS ===

from dataclasses import dataclass
import os
from typing import Self

from dotenv import load_dotenv

# === EXPORTS ===

__all__ = [
    "KafkaSettings",
    "DEFAULT_AUTO_OFFSET_RESET",
    "DEFAULT_BOOTSTRAP_SERVERS",
    "DEFAULT_BROKER_ADDRESS_FAMILY",
    "DEFAULT_GROUP_ID",
    "DEFAULT_TOPIC",
]

# === DECLARE DEFAULTS ===

# The address of the Kafka broker.
# Local Kafka typically runs at localhost:9092.
DEFAULT_BOOTSTRAP_SERVERS = "localhost:9092"

# The address family rdkafka uses when resolving the broker hostname.
# "any"  — try both IPv4 and IPv6 (rdkafka default).
# "v4"   — force IPv4 only.
# "v6"   — force IPv6 only.
# WSL2 users on Windows may need "v6" if localhost resolves to ::1.
DEFAULT_BROKER_ADDRESS_FAMILY = "any"

# The Kafka topic this project exchanges messages on.
DEFAULT_TOPIC = "product-sales-case"

# Consumer group ID.
# Multiple consumers in the same group share the load of a topic.
DEFAULT_GROUP_ID = "streaming-consumer-group-A"

# Where the consumer begins reading when no prior offset exists.
# "earliest" — read from the beginning of the topic.
# "latest"   — read only new messages arriving after the consumer starts.
# "none"     — raise an error if no offset is found.
DEFAULT_AUTO_OFFSET_RESET = "earliest"


# === DECLARE A FROZEN (IMMUTABLE) DATA CLASS FOR KAFKA SETTINGS ===


@dataclass(frozen=True)
class KafkaSettings:
    """Kafka settings for producer and consumer examples.

    Frozen so settings cannot be accidentally mutated after creation.
    Always create instances via from_env() to load from the .env file.
    """

    bootstrap_servers: str = DEFAULT_BOOTSTRAP_SERVERS
    broker_address_family: str = DEFAULT_BROKER_ADDRESS_FAMILY
    topic: str = DEFAULT_TOPIC
    group_id: str = DEFAULT_GROUP_ID
    auto_offset_reset: str = DEFAULT_AUTO_OFFSET_RESET

    @classmethod
    def from_env(cls) -> Self:
        """Create Kafka settings from environment variables.

        Reads .env via python-dotenv, then falls back to DEFAULT_* constants
        for any variable not set in the environment.

        Returns:
            A fully populated KafkaSettings instance.
        """
        load_dotenv()

        return cls(
            bootstrap_servers=os.getenv(
                "KAFKA_BOOTSTRAP_SERVERS",
                DEFAULT_BOOTSTRAP_SERVERS,
            ),
            broker_address_family=os.getenv(
                "KAFKA_BROKER_ADDRESS_FAMILY",
                DEFAULT_BROKER_ADDRESS_FAMILY,
            ),
            topic=os.getenv("KAFKA_TOPIC", DEFAULT_TOPIC),
            group_id=os.getenv("KAFKA_GROUP_ID", DEFAULT_GROUP_ID),
            auto_offset_reset=os.getenv(
                "KAFKA_AUTO_OFFSET_RESET",
                DEFAULT_AUTO_OFFSET_RESET,
            ),
        )

    def producer_config(self) -> dict[str, str]:
        """Return a confluent-kafka producer configuration dict.

        Returns:
            Configuration passed directly to confluent_kafka.Producer().
        """
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "broker.address.family": self.broker_address_family,
            "log_level": "3",
            "message.timeout.ms": "5000",
            "socket.timeout.ms": "5000",
            "request.timeout.ms": "5000",
        }

    def consumer_config(self) -> dict[str, str]:
        """Return a confluent-kafka consumer configuration dict.

        Returns:
            Configuration passed directly to confluent_kafka.Consumer().
        """
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "broker.address.family": self.broker_address_family,
            "log_level": "3",
            "group.id": self.group_id,
            "auto.offset.reset": self.auto_offset_reset,
        }
