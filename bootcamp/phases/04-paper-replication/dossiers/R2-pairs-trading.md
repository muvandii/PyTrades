# Dossier R2 — Pairs Trading

**Paper:** Gatev, E., Goetzmann, W.N., Rouwenhorst, K.G. (2006). *Pairs Trading: Performance of a
Relative-Value Arbitrage Rule*. Review of Financial Studies 19(3), 797-827.

**Why this paper:** it turns "buy the loser, sell the winner" into a testable relationship with a
testable failure mode, and it is the honest introduction to selection look-ahead - the trap in
which the pairs are chosen using data from the period they are traded in.

## The core claim

> Form pairs on normalised historical prices, trade divergence from the spread, and the spread
> reverts often enough to pay for costs.

## The specification, as precisely as the paper gives it

| Element | Paper | Your version |
| --- | --- | --- |
| Universe | all CRSP stocks, 1962-2002 | 20-40 candidate pairs from coherent sectors; document the economic link |
| Formation | 12-month formation period; pairs ranked by the sum of squared deviations of normalised prices (a distance metric) | first half of your sample, formation window as reported |
| Selection | top 5 pairs by distance from the formation-period ranking | top pairs by a *test*, not just distance (see below) |
| Trading | 6-month trading period; open at 2σ divergence, close on convergence (crossing of the spread mean), stop after the trading period ends | z-score rules: enter |z| ≥ 2, exit |z| ≤ 0.5, break stop at |z| ≥ 3.5, max holding period |
| Costs | the paper reports results gross and net of a range of commissions; the net version is what survives scrutiny | net of your assumed round trip on **both legs** |
| Reported numbers | excess return ≈ 11% per year before costs; net profitability that declines over time | expect a similar shape: strong pre-2000, weak after |

## The mechanism

1. **Common factors.** Two firms in the same business share most of their systematic risk; their
   relative price is driven by idiosyncratic flow (index changes, block trades, news sympathy).
2. **Liquidity provision.** The strategy is paid for supplying liquidity to whoever is dumping one
   leg and ripping the other - which is also why it pays four spreads per round trip.
3. **Time-varying relation.** The hedge ratio drifts and can break permanently: mergers, index
   membership changes, and business divergence all convert a "spread" into a trend.

## The test the course insists on (beyond the paper)

The paper's distance metric is a *heuristic* for a relationship. You will also test it:

| Test | Question it answers | Tool |
| --- | --- | --- |
| ADF on the spread | is the residual stationary-ish? | `statsmodels.tsa.stattools.adfuller` |
| Engle-Granger | do the log prices cointegrate? | `statsmodels.tsa.stattools.coint` |
| Half-life | how long does a deviation take to halve? | OLS of Δspread on lagged spread: `−ln(2)/λ` |

Selection must use the **formation window only**. Re-select and re-run on the trading window: that
is the walk-forward version of the paper, and it will produce a lower Sharpe than the naive one.
The difference is your selection look-ahead, and reporting it is part of the deliverable.

## Where it is vulnerable (your Thursday list)

| Attack | What to measure |
| --- | --- |
| Selection look-ahead | Sharpe with full-sample selection minus Sharpe with training-only selection |
| Relationship breaks | count of pairs whose spread never returned in the OOS window |
| Costs | four spreads per round trip plus the borrow assumption for the short leg |
| Crowding | the paper's own decay: performance is best in the earliest subsamples |
| Best-pair dependence | drop the best pair, then the best two: does anything remain? |
| Data quality | split-adjusted vs unadjusted prices change the formation ranking |

## What a replication owes the reader

1. The test output (ADF/cointegration p-values, half-lives) for the traded pairs.
2. The z-score rules stated numerically, plus how a "break stop" differs from a stop-loss.
3. Your Sharpe both with and without honest selection, and the gap named.
4. A count of relationships that broke - the strategy's true, non-diversifiable risk.

## Common failure modes in student replications

- Choosing pairs after looking at the trading period (the whole game is avoiding this).
- Trading convergence without a break stop, so one merger wipes out ten good trades.
- Ignoring the short leg's costs and borrow in the headline number.
- Reporting the "distance" ranking as evidence of cointegration, when distance is just
  standardised divergence over one window.
