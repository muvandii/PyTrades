# PORTFOLIO.md — portfolio and risk document template

This is the document you would hand to someone who asked "okay, so what would you actually trade?"
It is not a pitch: it is a claim about your own work, with evidence per line and criteria for
removing each one.

---

# Portfolio

**As of:** `<date>` · **Account size (paper):** `<value>` · **Live window:** `<N>` days, status `<live / in progress>`

## The lines

| Line | Strategy | Weight | Sizing rule | Evidence | Remove if |
| --- | --- | --- | --- | --- | --- |
| 1 | `<strategy id>` | `<%>` | `<vol target / fractional Kelly fraction>` | [`<verdict path>`](<link>) | `<observable criterion>` |
| 2 | | | | | |
| 3 | | | | | |

Rules: every line links a verdict; every weight is justified by the same sizing arithmetic; every
line has a removal criterion you could check on a Tuesday.

## Risk policy in one paragraph

> `<Target portfolio vol, max gross exposure, correlation policy (threshold + action), de-risking trigger + action + resume condition, ruin definition. Half a page maximum; the full policy lives in reports/risk-policy.md.>`

## The evidence for each line

| Line | Sharpe (net, OOS) | Max DD | Turnover/yr | Breakeven bps | Live vs backtest (bps/month) |
| --- | --- | --- | --- | --- | --- |
| 1 | | | | | |
| 2 | | | | | |

## Portfolio-level numbers

| Metric | Value | Artifact |
| --- | --- | --- |
| Target vol / realised vol | `<x%>` / `<y%>` | `reports/portfolio-allocation.md` |
| Correlation (median pairwise, and crisis) | `<x>` / `<y>` | same |
| P(50% drawdown within a year) | `<x%>` | `reports/monte-carlo.md` |
| Expected annual cost drag | `<x%>` | `reports/risk-policy.md` |
| Regime exposure (share of days high-vol) | `<x%>` | `reports/regime-lab.md` |

## What would change this portfolio

1. **Correlation regime**: if median pairwise correlation rises above `<x>`, reduce gross by `<y%>`.
2. **Strategy decay**: if a line's rolling 12-month net Sharpe is below `<z>` for two consecutive quarters, remove it and log a graveyard entry.
3. **Live divergence**: if unexplained divergence exceeds `<x>` bps/month for two months, halt and audit the harness before trading.
4. **A better line**: a new candidate must beat the *weakest incumbent* on OOS Sharpe with a CI excluding zero, and bring pairwise correlation below `<x>`.

## The graveyard clause

> `<One sentence: what fraction of everything you tested is dead, and why you would expect the next idea to join it.>`
