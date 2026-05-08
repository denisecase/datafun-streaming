# datafun-streaming

Shared Python utilities for streaming data analytics projects.

Provides a consistent foundation so projects
can focus on streaming concepts rather than boilerplate.

## What's Included

| Subpackage                          | Purpose                                                   |
| ----------------------------------- | --------------------------------------------------------- |
| `datafun_streaming.kafka`           | Producer, consumer, admin, and connection utilities       |
| `datafun_streaming.storage`         | DuckDB persistence with schema inference                  |
| `datafun_streaming.data_validation` | Field-level validators, types, and reference data helpers |
| `datafun_streaming.io`              | CSV and JSON file I/O utilities                           |
| `datafun_streaming.stats`           | Incremental running statistics                            |
| `datafun_streaming.visualization`   | Plotly chart utilities for live data                      |
| `datafun_streaming.core`            | Shared type aliases used across subpackages               |

## Installation

```shell
uv add datafun-streaming
```

## Quick Start

```python
from datafun_streaming.kafka.kafka_settings import KafkaSettings
from datafun_streaming.storage.duckdb_utils import init_db, upsert_row
from datafun_streaming.stats.stats_utils import RunningStats

settings = KafkaSettings.from_env()
conn = init_db(Path("data/output/sales.duckdb"))
stats = RunningStats()
```

## Source

- GitHub: [github.com/denisecase/datafun-streaming](https://github.com/denisecase/datafun-streaming)
- PyPI: [pypi.org/project/datafun-streaming](https://pypi.org/project/datafun-streaming)
- License: MIT
