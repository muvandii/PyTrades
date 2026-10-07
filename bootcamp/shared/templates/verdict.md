# Verdict: <STRATEGY_ID>

> Copy this to `strategies/<id>/verdict.md` and fill every field. A verdict with
> `inconclusive` in bold is a finished deliverable. A verdict with holes in it is not.
> Keep the annotated line at the bottom so the course can find this file's evidence:
> `produces=<deliverable id>` inside an "annotated" HTML comment, e.g. `produces=D05`.

**Date:** YYYY-MM-DD
**Spec fingerprint:** `<spec_fingerprint from meta.json>`
**Data fingerprint:** `<data_fingerprint from meta.json>`
**Backtest artifact:** `reports/backtests/<name>/`

## 1. The claim (one sentence)

What you expected to be true, in the form "if X, then Y, and it should pay because Z".

## 2. The test

| Item | Value |
| --- | --- |
| Universe | |
| Sample | <start> to <end>, <n> bars |
| Signal family | |
| Parameters | |
| In-sample | <start> to <end> |
| Out-of-sample | <start> to <end> |
| Costs | <fee> bps fee + <slip> bps slippage |
| Execution | next open / next close |
| Benchmark | |

## 3. Headline numbers (net of costs, out-of-sample)

| Metric | Strategy | Benchmark | Comment |
| --- | --- | --- | --- |
| CAGR | | | |
| Volatility | | | |
| Sharpe | | | |
| Sortino | | | |
| Max drawdown | | | |
| Calmar | | | |
| Turnover (annual) | | | |
| Trades | | | |
| Win rate | | | |
| Expectancy per trade | | | |
| Profit factor | | | |

## 4. Cost sensitivity

Breakeven cost (bps round-trip) where the edge disappears: **__ bps**

| Cost (bps) | CAGR | Sharpe | MaxDD |
| --- | --- | --- | --- |
| 0 | | | |
| 5 | | | |
| 10 | | | |
| 20 | | | |

## 5. Fragility checks

- [ ] Parameter neighbours are also positive (plateau, not spike) - see `reports/sensitivity/<id>.csv`
- [ ] Out-of-sample Sharpe sits inside a bootstrap CI that excludes zero
- [ ] Result survives vol-targeted sizing (not only fixed fraction)
- [ ] Result is not carried by 1-2 outlier trades: largest single trade = __% of total PnL
- [ ] Same result on a second, related universe (or a documented reason why not)

## 6. Verdict

**One of: `edge` / `no edge` / `inconclusive`.** State it plainly.

- **edge** means: positive net expectancy out-of-sample, plateau in parameters, survives 2x costs, and you can name the mechanism.
- **no edge** means: the mechanism failed a specific test. Say which test and how it failed.
- **inconclusive** means: you ran out of sample, data, or clarity. Say exactly what evidence would settle it.

## 7. Mechanism (why does this exist at all?)

In two sentences: who is on the other side of this trade, and why do they keep doing it?

## 8. Kill criteria

What would make you switch this off, in observable terms? (e.g. "20-day realised vol above 35%, or 90-day Sharpe below -0.5")

## 9. Graveyard line

`<id> — <date> — <cause of death in <8 words> — <link to this verdict>`

<!-- when you copy this file into your repo, add an "annotated" comment naming the deliverable (produces=D05) -->
