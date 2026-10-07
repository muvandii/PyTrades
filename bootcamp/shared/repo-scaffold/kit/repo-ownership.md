# What you own vs what you rent

| Path | Owner | Rule |
| --- | --- | --- |
| `data/` | the fetcher | never hand-edit; re-fetch or document |
| `kit/` | the course | read-only; it is the oracle |
| `engine/` | **you** | your backtester, metrics, walk-forward, tearsheets |
| `config/` | you | one spec per experiment |
| `strategies/` | you | `signal.py` + `verdict.md` + notes |
| `papers/` | you | replication code and comparison notes |
| `live/` | you | bot, logs, dashboard, reconciliation |
| `reports/` | generated | never edit a generated artifact; regenerate it |
| `journal/`, `graveyard.md` | you | the two things nobody can generate for you |

Rent when it is infrastructure (data plumbing, cost defaults, contracts).
Own when it is the thing the course is teaching (engine, metrics, strategy logic,
risk rules, verdicts).
