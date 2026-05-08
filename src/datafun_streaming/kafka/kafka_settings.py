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
    "DEFAULT_GROUP_ID",
    "DEFAULT_TOPIC",
]

# === DECLARE DEFAULTS ===

DEFAULT_BOOTSTRAP_SERVERS = "localhost:9092"
DEFAULT_TOPIC = "product-sales-case"
DEFAULT_GROUP_ID = "streaming-consumer-group-A"
DEFAULT_AUTO_OFFSET_RESET = "earliest"


# == DECLARE A FROZEN (IMMUTABLE) DATA CLASS FOR KAFKA SETTINGS ===


@dataclass(frozen=True)
class KafkaSettings:
    """Kafka settings for producer and consumer examples."""

    bootstrap_servers: str
    topic: str
    group_id: str
    auto_offset_reset: str

    @classmethod
    def from_env(cls) -> Self:
        """Create Kafka settings from environment variables."""
        load_dotenv()

        return cls(
            bootstrap_servers=os.getenv(
                "KAFKA_BOOTSTRAP_SERVERS",
                DEFAULT_BOOTSTRAP_SERVERS,
            ),
            topic=os.getenv("KAFKA_TOPIC", DEFAULT_TOPIC),
            group_id=os.getenv("KAFKA_GROUP_ID", DEFAULT_GROUP_ID),
            auto_offset_reset=os.getenv(
                "KAFKA_AUTO_OFFSET_RESET",
                DEFAULT_AUTO_OFFSET_RESET,
            ),
        )

    def producer_config(self) -> dict[str, str]:
        """Return a confluent-kafka producer configuration."""
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "log_level": "3",
            "message.timeout.ms": "5000",
            "socket.timeout.ms": "5000",
            "request.timeout.ms": "5000",
        }

    def consumer_config(self) -> dict[str, str]:
        """Return a confluent-kafka consumer configuration."""
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "log_level": "3",
            "group.id": self.group_id,
            "auto.offset.reset": self.auto_offset_reset,
        }
