# Phase 6 — Live Paper (Weeks 11-12)

**Milestone:** [M5 Live paper](milestones/M5-live-paper.md) — 30 days of live paper logs plus a reconciliation report; live vs backtest divergence explained.

## The shape of this phase

| Week | You build | You learn |
| --- | --- | --- |
| 11 | the scheduled harness, broker adapter, daily logs, dashboard | unattended operation; every operational failure mode |
| 12 | the shadow backtest, the reconciliation, the post-mortem | where live PnL actually goes, component by component |

## What ships

| Piece | Where | Why |
| --- | --- | --- |
| Signal generator spec | [spec/signal-generator-spec.md](spec/signal-generator-spec.md) | the daily cycle, the log schema, adapter interface, operational rules |
| Live bot + adapter | `live/bot.py`, `live/broker_paper.py` \| `live/broker_alpaca.py` | D16 |
| Daily logs | `live/log/YYYY-MM-DD.json` | every decision, including "do nothing" |
| Dashboard | `live/dashboard.html` | generated from logs, never hand-edited |
| Reconciliation | `live/reconciliation.md` | D17: the gap, decomposed and adding up |
| Post-mortem | `live/postmortem.md` | failures, interventions, expected-divergence budget |

## Deliverables and gate

[D16](deliverables/D16.md) · [D17](deliverables/D17.md) · [gates/week-11-gate.md](gates/week-11-gate.md) ·
[gates/week-12-gate.md](gates/week-12-gate.md) · [rubric.md](rubric.md)

## Concepts injected

| Concept | Trigger |
| --- | --- |
| [C23 — Slippage Modeling & Latency](concepts/C23-slippage-modeling-and-latency.md) | live fills systematically worse than the backtest's assumption |
| [C24 — Live vs Backtest Divergence](concepts/C24-live-vs-backtest-divergence.md) | live 40% below backtest, culprit unknown |
| [C25 — Regime Detection](concepts/C25-regime-detection.md) | the whole divergence is one volatile month |

## The 30-day clock (why the calendar is a deliverable)

`live/config.json` was created in **Week 5**. That is deliberate: a paper-trading window that
starts when the bot is finished (Week 11) has no chance to span more than one noise regime before
the capstone, and students who start late fail M5 for a reason that has nothing to do with skill.
The bot in Week 11 does not "start" the paper trade; it takes over a run that already has weeks of
history - which is also why the logs from Weeks 5-10 (if you kept them by hand or by script) are
acceptable evidence and should be committed.

## Honest failure is a pass here too

Not every student has API keys, a stable machine, or 30 quiet days. The course's requirements are
about *evidence*, not about perfect uptime: a run with six logged operational failures and an
honest reconciliation is a stronger artifact than one that claims a flawless month. What does not
pass: unlogged days presented as logged, manual interventions presented as unattended operation,
or a reconciliation whose remainder was relabelled.
