"""src/datafun_streaming/kafka/kafka_connection_utils.py.

Kafka connection helpers for streaming examples.
"""

# === IMPORTS ===

import socket

from datafun_streaming.kafka.errors import kafka_not_reachable_message
from datafun_streaming.kafka.kafka_settings import KafkaSettings

# === EXPORTS ===

__all__ = [
    "verify_kafka_connection",
]


def verify_kafka_connection(settings: KafkaSettings) -> None:
    """Verify that the Kafka bootstrap server is reachable."""
    bootstrap_server = settings.bootstrap_servers.split(",")[0].strip()

    if ":" not in bootstrap_server:
        msg = (
            "KAFKA_BOOTSTRAP_SERVERS must include host and port, "
            f"but got {bootstrap_server!r}."
        )
        raise ConnectionError(msg)

    host, port_text = bootstrap_server.rsplit(":", 1)

    try:
        port = int(port_text)
    except ValueError as error:
        msg = f"KAFKA_BOOTSTRAP_SERVERS has an invalid port. Got {bootstrap_server!r}."
        raise ConnectionError(msg) from error

    try:
        with socket.create_connection((host, port), timeout=5):
            return
    except OSError as error:
        msg = kafka_not_reachable_message(
            bootstrap_servers=settings.bootstrap_servers,
        )
        raise ConnectionError(msg) from error
