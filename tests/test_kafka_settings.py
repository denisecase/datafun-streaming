"""Tests for datafun_streaming.kafka.kafka_settings."""

import pytest

from datafun_streaming.kafka.kafka_settings import (
    DEFAULT_AUTO_OFFSET_RESET,
    DEFAULT_BOOTSTRAP_SERVERS,
    DEFAULT_BROKER_ADDRESS_FAMILY,
    DEFAULT_GROUP_ID,
    DEFAULT_TOPIC,
    KafkaSettings,
)

# === defaults ===


def test_defaults_are_defined() -> None:
    assert DEFAULT_BOOTSTRAP_SERVERS == "localhost:9092"
    assert isinstance(DEFAULT_TOPIC, str)
    assert isinstance(DEFAULT_GROUP_ID, str)
    assert DEFAULT_AUTO_OFFSET_RESET == "earliest"
    assert DEFAULT_BROKER_ADDRESS_FAMILY == "any"


# === from_env with defaults ===


def test_from_env_uses_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KAFKA_BOOTSTRAP_SERVERS", raising=False)
    monkeypatch.delenv("KAFKA_TOPIC", raising=False)
    monkeypatch.delenv("KAFKA_GROUP_ID", raising=False)
    monkeypatch.delenv("KAFKA_AUTO_OFFSET_RESET", raising=False)
    monkeypatch.delenv("KAFKA_BROKER_ADDRESS_FAMILY", raising=False)
    settings = KafkaSettings.from_env()
    assert settings.bootstrap_servers == DEFAULT_BOOTSTRAP_SERVERS
    assert settings.topic == DEFAULT_TOPIC
    assert settings.group_id == DEFAULT_GROUP_ID
    assert settings.auto_offset_reset == DEFAULT_AUTO_OFFSET_RESET
    assert settings.broker_address_family == DEFAULT_BROKER_ADDRESS_FAMILY


def test_from_env_reads_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KAFKA_BOOTSTRAP_SERVERS", "broker:9093")
    monkeypatch.setenv("KAFKA_TOPIC", "test-topic")
    monkeypatch.setenv("KAFKA_GROUP_ID", "test-group")
    monkeypatch.setenv("KAFKA_AUTO_OFFSET_RESET", "latest")
    monkeypatch.setenv("KAFKA_BROKER_ADDRESS_FAMILY", "v6")
    settings = KafkaSettings.from_env()
    assert settings.bootstrap_servers == "broker:9093"
    assert settings.topic == "test-topic"
    assert settings.group_id == "test-group"
    assert settings.auto_offset_reset == "latest"
    assert settings.broker_address_family == "v6"


# === config dicts ===


def test_producer_config_has_required_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KAFKA_BOOTSTRAP_SERVERS", raising=False)
    settings = KafkaSettings.from_env()
    config = settings.producer_config()
    assert "bootstrap.servers" in config
    assert config["bootstrap.servers"] == DEFAULT_BOOTSTRAP_SERVERS


def test_consumer_config_has_required_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KAFKA_BOOTSTRAP_SERVERS", raising=False)
    settings = KafkaSettings.from_env()
    config = settings.consumer_config()
    assert "bootstrap.servers" in config
    assert "group.id" in config
    assert "auto.offset.reset" in config


# === immutability ===


def test_settings_are_frozen(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KAFKA_BOOTSTRAP_SERVERS", raising=False)
    settings = KafkaSettings.from_env()
    with pytest.raises(AttributeError):
        settings.bootstrap_servers = "other:9092"  # type: ignore[misc]


# == broker address family propagation ===


def test_broker_address_family_v6_propagates_to_configs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("KAFKA_BROKER_ADDRESS_FAMILY", "v6")
    settings = KafkaSettings.from_env()
    assert settings.producer_config()["broker.address.family"] == "v6"
    assert settings.consumer_config()["broker.address.family"] == "v6"
