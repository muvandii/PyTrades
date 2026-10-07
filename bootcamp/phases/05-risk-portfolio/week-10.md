---
week: 10
phase: P5
title: Sizing, Correlation, Survival
deliverables: [D15]
concepts: [C20, C21, C22]
milestone: null
hours: 16-20
---

# Week 10 — Sizing, Correlation, Survival

## Learning objective

Turn a pile of signals into a portfolio that survives: position sizing rules that come from the edge and its variance, an allocation that accounts for correlation honestly, and a Monte Carlo answer to "how often does this blow up?"

## Deliverable

- [D15 — Risk policy + portfolio allocation + Monte Carlo + regime lab](deliverables/D15.md): `reports/risk-policy.md`, `reports/portfolio-allocation.md`, `reports/monte-carlo.md`, `reports/regime-lab.md`.

## Daily tasks

### Mon — Correlation and the portfolio that is worse than its parts (C20)

1. Take your surviving strategies (and the replications that survived Week 9). Compute the return correlation matrix on the overlap period - and check the overlap period first, it is usually shorter than you think.
2. Inject [C20 — Correlation & Portfolio Variance](concepts/C20-correlation-and-portfolio-variance.md).
3. Combine two strategies with Sharpe 1.4 and 1.2 at correlation 0.85, then at 0.25, then at −0.1. Write down the combined Sharpe in each case before you run it.

*Time: 3-4 h. Expect the high-correlation combination to disappoint you - that is the lesson.*

### Tue — Kelly, and why you will not use it (C21)

1. Inject [C21 — Kelly & Fractional Kelly](concepts/C21-kelly-and-fractional-kelly.md).
2. Compute the Kelly fraction for your best strategy: `f* = μ / σ²` (continuous) or the discrete version from win/loss odds. Then compute the growth-optimal fraction under *estimated* parameters.
3. Apply quarter-Kelly to your portfolio and compare with full-Kelly in a backtest. Note the drawdown difference - full Kelly's drawdowns are famously deeper than they look in a formula.

*Time: 4-5 h.*

### Wed — Risk of ruin, measured not assumed (C22)

1. Inject [C22 — Risk of Ruin](concepts/C22-risk-of-ruin.md).
2. Build `reports/monte-carlo.md`: block-bootstrap your portfolio's daily returns (2,000 paths, block length = holding period), apply your sizing rules *inside* each path (including any de-risking rules), and report: median terminal equity, 5th percentile, probability of a 50% drawdown, and probability of hitting a −80% "ruin" threshold.
3. The required sentence: "under my own rules, the probability of a 50% drawdown within one year is X%". If X > 20%, your sizing is wrong, not your strategy.

*Time: 4-5 h.*

### Thu — Position sizing implementation

1. Implement the sizing rules as code (`engine/sizing.py` or inside your portfolio module):
   - volatility targeting per position (reuse the C17 machinery, now applied portfolio-wide);
   - correlation-aware scaling: gross exposure reduced when the book's average pairwise correlation rises;
   - a de-risking rule with a threshold that you can state in one sentence and that would have triggered in your worst historical drawdown.
2. Backtest the sized portfolio vs equal-weight. Save the sizing-parameter sensitivity grid (3+ CSVs to `reports/sensitivity/`).

*Time: 4-5 h.*

### Fri — Regime lab

1. Split your sample into regimes by an observable rule (not hindsight): e.g. 200-day realised vol above/below its median, or price above/below its 200-day MA, or a simple 2-state HMM if you want the machinery.
2. Write `reports/regime-lab.md`: which strategies earn in which regimes, whether a regime filter would have helped *out of sample*, and - importantly - how many regime switches there were (a filter that trades twice a year is a different object than one that trades monthly).
3. Add the regime findings to the risk policy as a *contingency*, not as a signal: "if the portfolio's realised vol exceeds X for Y days, reduce gross to Z."

*Time: 4-5 h.*

### Sat — The one-page risk policy (D15 core)

`reports/risk-policy.md`, one page, containing:

| Section | Content |
| --- | --- |
| Mandate | what this portfolio is for, over what horizon, with what loss tolerance |
| Position sizing | the exact rule, the parameters, and the cap |
| Portfolio construction | which strategies, at what weights, rebalanced how often |
| Correlation policy | what happens when correlations rise; the threshold and the action |
| De-risking | the trigger, the action, and the resume condition (both observable) |
| Ruin definition | the drawdown level at which the portfolio is stopped and reviewed, and by what evidence it restarts |

Rules: no adjectives without numbers; every rule expressible as code; every rule testable in the
Monte Carlo you built Wednesday.

*Time: 4-5 h.*

### Sun — Journal, gate

1. `make gate WEEK=10`: the four reports exist, 3+ sensitivity CSVs, the ruin probability is computed.
2. Journal: what did the Monte Carlo change about your intended sizing? (If nothing, look again - the first run almost always shows a fatter tail than intuition predicted.)

*Time: 2-3 h.*

## Gate

`make gate WEEK=10` - see [gates/week-10-gate.md](gates/week-10-gate.md). **Checkpoint:** `risk-policy.md` states the sizing rules in one page; the portfolio allocation beats equal-weight on the same signals; Monte Carlo shows your ruin probability under your own rules.

## Graveyard prompt

Log the sizing rules that died: full Kelly on a fat-tailed strategy, correlation-blind diversification, a vol target set so high that your de-risking rule becomes structural. Each of these is a *rule* death, not a strategy death - and rule deaths are the most expensive kind, because they kill good strategies quietly.

## Concept injections this week

- [C20 — Correlation & Portfolio Variance](concepts/C20-correlation-and-portfolio-variance.md) — triggered by two Sharpe-1.4 strategies combining into something worse than either
- [C21 — Kelly & Fractional Kelly](concepts/C21-kelly-and-fractional-kelly.md) — triggered by having an edge and no idea what fraction it deserves
- [C22 — Risk of Ruin](concepts/C22-risk-of-ruin.md) — triggered by an "optimal" sizing whose drawdown path is intolerable
