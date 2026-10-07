# Phase 2 — Engine (Weeks 3-4)

**Milestone:** [M2 Backtest engine](milestones/M2-backtest-engine.md) — any idea, data to tearsheet + verdict, in under 30 minutes.

## What the teacher ships

| Piece | Where | Why |
| --- | --- | --- |
| Event-driven backtester spec | [spec/engine-spec.md](spec/engine-spec.md) | the contract surface + 8 numbered behaviours + 3 proofs |
| Cost model spec | [spec/cost-model.md](spec/cost-model.md) | turnover-based costs, reporting obligations, common mistakes |
| Walk-forward splitter spec | [spec/walkforward-splitter.md](spec/walkforward-splitter.md) | splits, embargo, pooled OOS, honesty rules |
| Look-ahead test suite | [lookahead/lookahead-test-suite.md](lookahead/lookahead-test-suite.md) | time travel, shift premium, contract suite, blind-data test |
| Reference implementation | `shared/repo-scaffold/kit/spine.py` | the plain 400-line version you replace |
| Contract tests | `kit/tests/test_spine_contract.py` | runs against kit OR your engine (`PYTRADES_ENGINE=`) |

## What the student ships

| Deliverable | Week | Artifact | One thing it teaches |
| --- | --- | --- | --- |
| [D05](deliverables/D05.md) | 3 | `engine/backtest.py` + tests | a backtest is an accounting system |
| [D06](deliverables/D06.md) | 3 | `engine/costs.py` + cost report | costs are a function of turnover |
| [D07](deliverables/D07.md) | 4 | walk-forward + tearsheets + look-ahead suite | OOS is a process, not a number |

## Concepts injected

| Concept | Triggered by |
| --- | --- |
| [C05 — Annualization](concepts/C05-annualization.md) | daily numbers, annual comparisons |
| [C06 — Volatility & Std Dev](concepts/C06-volatility-and-std-dev.md) | "is 1.2%/day a lot?" |
| [C07 — Sharpe Ratio](concepts/C07-sharpe-ratio.md) | two curves ending in the same place |
| [C08 — Max Drawdown & Recovery](concepts/C08-max-drawdown-and-recovery.md) | a 47% drawdown on your own tearsheet |
| [C09 — Calmar & Return-vs-Pain](concepts/C09-calmar-and-return-vs-pain.md) | equal Sharpe, unequal pain |
| [C10 — Transaction Costs & Slippage](concepts/C10-transaction-costs-and-slippage.md) | beautiful at 0 bps, dead at 10 |

## The phase in one paragraph

Week 3 is bookkeeping: bars in, targets in, fills out, cash and quantities tracked, costs charged
inside the loop. Week 4 is honesty: split the sample, report the pooled out-of-sample number,
auto-generate the tearsheet including the caveats, and prove with tests that the engine cannot
see the future. The deliverable is not a faster backtester - it is a *repeatable* one, because
Week 5 runs six strategies through it and Week 12 reconciles live trading against it.

## Gate

Week 3: [gates/week-03-gate.md](gates/week-03-gate.md) · Week 4: [gates/week-04-gate.md](gates/week-04-gate.md) ·
Self-grading: [rubric.md](rubric.md) · Solo students: [instructor/OPTIONAL-instructor-notes.md](instructor/OPTIONAL-instructor-notes.md).
