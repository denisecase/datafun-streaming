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
    "DEFAULT_AUTO_OFFSET_RESET",
    "DEFAULT_BOOTSTRAP_SERVERS",
    "DEFAULT_BROKER_ADDRESS_FAMILY",
    "DEFAULT_CLEAR_TOPIC_ON_START",
    "DEFAULT_GROUP_ID",
    "DEFAULT_TOPIC",
    "KafkaSettings",
]

# === DECLARE DEFAULTS ===

DEFAULT_BOOTSTRAP_SERVERS = "localhost:9092"
DEFAULT_BROKER_ADDRESS_FAMILY = "any"
DEFAULT_TOPIC = "product-sales-case"
DEFAULT_GROUP_ID = "streaming-consumer-group-A"
DEFAULT_AUTO_OFFSET_RESET = "earliest"
DEFAULT_CLEAR_TOPIC_ON_START = False

# === DECLARE HELPERS ===


def _read_bool_env(name: str, default: bool) -> bool:
    """Read a boolean environment variable.

    Accepts true, 1, yes, y, and on as true.
    Accepts false, 0, no, n, and off as false.
    Raises ValueError for any other value.
    """
    value = os.getenv(name)

    if value is None:
        return default

    normalized = value.strip().lower()

    if normalized in {"true", "1", "yes", "y", "on"}:
        return True

    if normalized in {"false", "0", "no", "n", "off"}:
        return False

    msg = (
        f"Environment variable {name} must be a boolean value "
        f"(true/false, yes/no, 1/0, on/off). Got {value!r}."
    )
    raise ValueError(msg)


# === DECLARE A FROZEN SETTINGS CLASS ===


@dataclass(frozen=True)
class KafkaSettings:
    """Kafka settings for producer and consumer examples."""

    bootstrap_servers: str = DEFAULT_BOOTSTRAP_SERVERS
    broker_address_family: str = DEFAULT_BROKER_ADDRESS_FAMILY
    topic: str = DEFAULT_TOPIC
    group_id: str = DEFAULT_GROUP_ID
    auto_offset_reset: str = DEFAULT_AUTO_OFFSET_RESET
    clear_topic_on_start: bool = DEFAULT_CLEAR_TOPIC_ON_START

    @classmethod
    def from_env(cls) -> Self:
        """Create Kafka settings from environment variables."""
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
            clear_topic_on_start=_read_bool_env(
                "KAFKA_CLEAR_TOPIC_ON_START",
                DEFAULT_CLEAR_TOPIC_ON_START,
            ),
        )

    def producer_config(self) -> dict[str, str]:
        """Return a confluent-kafka producer configuration dict."""
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "broker.address.family": self.broker_address_family,
            "log_level": "3",
            "message.timeout.ms": "5000",
            "request.timeout.ms": "5000",
            "socket.timeout.ms": "5000",
        }

    def consumer_config(self) -> dict[str, str]:
        """Return a confluent-kafka consumer configuration dict."""
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "broker.address.family": self.broker_address_family,
            "group.id": self.group_id,
            "auto.offset.reset": self.auto_offset_reset,
            "log_level": "3",
        }
