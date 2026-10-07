# Syllabus — AI Trading Strategy Bootcamp

A 13-week, self-paced, project-driven course. You do not read about trading strategies; you build
them, break them, bury the ones that fail, and take one to live paper trading in public.

**The promise:** by Week 13 you have a public repository containing a backtester you wrote, 15+
strategy verdicts net of costs, 6+ graveyard autopsies, 2-3 paper replications, 30+ days of live
paper logs with a reconciliation, and a writeup a stranger can follow.

**The success metric, stated as a skill:** can you debunk a viral strategy in 30 minutes, and take
a new idea from data to verdict in under an hour? If yes by Week 13, the course worked - and the
evidence is not your word for it: the artifacts are in the repo.

---

## How the course works

**Build first, theory second.** Every concept is injected *when a failure makes it necessary* -
never front-loaded. If you have not yet felt the problem a concept solves, you are not ready for
that concept, and the course will not hand it to you early.

**The daily rhythm (Mon-Sun, each week repeats it):**

| Day | What happens |
| --- | --- |
| Mon | Thesis: what do I believe, and what would prove me wrong? |
| Tue | Build v0: the smallest version that runs |
| Wed | Backtest: measure it honestly, with costs |
| Thu | Break it: costs, out-of-sample, walk-forward, perturbation |
| Fri | Diagnose: what died, and which concept explains why? (concept injection) |
| Sat | Rebuild: apply the concept, run again |
| Sun | Verdict + journal + graveyard + gate |

**Failure is graded.** The graveyard is a required artifact, not an embarrassment. A quarter with
four dead strategies and one survivor is a successful quarter; a quarter with six survivors
usually means the tests were too kind.

**Ship-or-don't-advance.** Each week ends with a gate (`make gate WEEK=n`) that checks artifacts,
not intentions. Each phase ends with a milestone that has a pass condition you either meet or
fail - and failing is fine, as long as it is documented and remediated.

**Non-negotiable in every strategy verdict:** costs, out-of-sample evidence, and a verdict word
(edge / no edge / inconclusive).

---

## The 13 weeks

<!-- BEGIN:GENERATED weeks -->
| Wk | Phase | Title | Ships | Concepts injected | Milestone | Hours |
| --: | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | P1 | [Raw Prices Are Not Data](phases/01-foundation/week-01.md) | D01, D02 | C01, C02 | — | 12-16 |
| 2 | P1 | [Kill Three Viral Strategies](phases/01-foundation/week-02.md) | D03, D04 | C03, C04 | M1 | 14-18 |
| 3 | P2 | [Build the Accounting Machine](phases/02-engine/week-03.md) | D05, D06 | C05, C06, C07 | — | 16-20 |
| 4 | P2 | [Costs, OOS, Tearsheets](phases/02-engine/week-04.md) | D07 | C08, C09, C10 | M2 | 16-20 |
| 5 | P3 | [The Factory Floor](phases/03-strategy-factory/week-05.md) | D08, D09 | C11, C12, C13 | — | 16-20 |
| 6 | P3 | [Six Strategies and an Honest Mirror](phases/03-strategy-factory/week-06.md) | D10, D11 | C14, C15 | M3 | 18-22 |
| 7 | P4 | [Replicate a Paper: Time-Series Momentum](phases/04-paper-replication/week-07.md) | D12 | C16, C17 | — | 18-22 |
| 8 | P4 | [Replicate a Paper: Pairs Trading](phases/04-paper-replication/week-08.md) | D13 | C18 | — | 18-22 |
| 9 | P4 | [Replicate a Paper: Vol-Managed Portfolios](phases/04-paper-replication/week-09.md) | D14 | C19 | M4 | 16-20 |
| 10 | P5 | [Sizing, Correlation, Survival](phases/05-risk-portfolio/week-10.md) | D15 | C20, C21, C22 | — | 16-20 |
| 11 | P6 | [Go Live (Paper)](phases/06-live-paper/week-11.md) | D16 | C23 | — | 14-18 |
| 12 | P6 | [Reconcile Reality](phases/06-live-paper/week-12.md) | D17 | C24, C25 | M5 | 14-18 |
| 13 | P7 | [Ship It in Public](phases/07-synthesis/week-13.md) | D18 | — | M6 | 14-20 |
<!-- END:GENERATED weeks -->

## Gates and milestones

Every week's gate runs from the student repo: `make gate WEEK=n`. Gates check files, tables,
journal counts, and manual confirmations you make with `python tools/check_gate.py`.

<!-- BEGIN:GENERATED gates -->
| Wk | Gate: you do not advance until | Verified by | Milestone |
| --: | :-- | :-- | :-- |
| 1 | `make data && make validate` runs clean from a fresh clone; reports/measurement-lab.md contains an equity curve and an expectancy… | 6 auto + 1 manual | — |
| 2 | Milestone M1: a timed, unassisted 30-minute debunk, start to written verdict, with the timer log kept in the report. | 4 auto + 1 manual | M1 |
| 3 | Your engine passes the 8 engine unit tests and the time-travel test (positions up to T are identical whether or not future data e… | 6 auto + 1 manual | — |
| 4 | Milestone M2: hand yourself a fresh idea you have never tested and go from raw data to tearsheet + verdict in under 30 minutes, t… | 6 auto + 1 manual | M2 |
| 5 | Three strategies with tearsheets, three verdicts, a populated strategies/index.md, and at least two graveyard entries; also start… | 5 auto + 1 manual | — |
| 6 | Milestone M3: 6 strategies tested, 3+ in the graveyard, at least one survivor whose OOS Sharpe sits inside a bootstrap CI that ex… | 6 auto + 1 manual | M3 |
| 7 | papers/R1_tsmom/comparison.md shows your Sharpe and the paper's Sharpe side by side, with every gap traced to a named deviation (… | 4 auto + 1 manual | — |
| 8 | papers/R2_pairs/comparison.md includes the cointegration test output, the chosen pair(s), spread z-score rules, and a walk-forwar… | 4 auto + 1 manual | — |
| 9 | Milestone M4: 2-3 replications shipped, each with comparison.md + deviations.md, plus papers/synthesis.md answering 'what replica… | 5 auto + 1 manual | M4 |
| 10 | reports/risk-policy.md states sizing rules in one page; the portfolio allocation beats equal-weight on the same signals, and Mont… | 6 auto + 1 manual | — |
| 11 | The bot runs unattended for 7 consecutive days: signals generated, orders submitted or explicitly skipped, every day logged, dash… | 4 auto + 1 manual | — |
| 12 | Milestone M5: 30+ days of live logs, a reconciliation report that attributes divergence to fees/slippage/timing/missed fills/regi… | 5 auto + 1 manual | M5 |
| 13 | Milestone M6: the stranger-clone test - a fresh clone plus a documented 15 minutes gets someone from README.md to a reproduced te… | 6 auto + 1 manual | M6 |
<!-- END:GENERATED gates -->

<!-- BEGIN:GENERATED milestones -->
| ID | Wk | Milestone | Pass condition (hard gate) |
| :-- | --: | :-- | :-- |
| M1 | 2 | [Reality check](phases/01-foundation/milestones/M1-reality-check.md) | Debunk a viral strategy, start to written verdict, in 30 minutes (timed and logged). |
| M2 | 4 | [Backtest engine](phases/02-engine/milestones/M2-backtest-engine.md) | Take a fresh idea from data to tearsheet + verdict end-to-end in under 30 minutes. |
| M3 | 6 | [Strategy factory](phases/03-strategy-factory/milestones/M3-strategy-factory.md) | 6 strategies tested, 3+ in the graveyard, at least 1 survivor with out-of-sample evidence. |
| M4 | 9 | [Paper replication](phases/04-paper-replication/milestones/M4-paper-replication.md) | 2-3 papers implemented end-to-end and compared against the paper's claims with a deviation log. |
| M5 | 12 | [Live paper](phases/06-live-paper/milestones/M5-live-paper.md) | 30 days of live paper logs plus a reconciliation report; live vs backtest divergence explained. |
| M6 | 13 | [Capstone](phases/07-synthesis/milestones/M6-capstone.md) | Public writeup + portfolio + repo shipped; a stranger can clone the repo and understand everything. |
<!-- END:GENERATED milestones -->

## Concept injections

Twenty-five concepts, each triggered by a specific failure you will hit. The format is always the
same: why now, the formula (one line), runnable code (3-5 lines), an example applied to your
current strategy, a time box (10-20 minutes), and a done-when that requires you to code it,
explain it, and spot a wrong version.

<!-- BEGIN:GENERATED concepts -->
| Tier | Wk | ID | Concept | Demanded by | Triggering failure |
| :-- | --: | :-- | :-- | :-- | :-- |
| T1 | 1 | [C01](phases/01-foundation/concepts/C01-returns-and-compounding.md) | Returns & Compounding | [D02](phases/01-foundation/deliverables/D02.md) | Your first equity curve looks like a straight line going up - until you compute what a 50% loss… |
| T1 | 1 | [C02](phases/01-foundation/concepts/C02-expectancy-and-profit-factor.md) | Expectancy & Profit Factor | [D02](phases/01-foundation/deliverables/D02.md) | You cannot say whether a strategy is good; you can only say it made money. |
| T1 | 2 | [C03](phases/01-foundation/concepts/C03-win-rate-vs-edge.md) | Win Rate vs Edge | [D03](phases/01-foundation/deliverables/D03.md) | The '90% win rate' strategy you are debunking has a 90% win rate - and still loses. |
| T1 | 2 | [C04](phases/01-foundation/concepts/C04-sample-size-and-base-rates.md) | Sample Size & Base Rates | [D04](phases/01-foundation/deliverables/D04.md) | Debunk #2 has 11 trades and you want to call it an edge (or a fraud) either way. |
| T2 | 3 | [C05](phases/02-engine/concepts/C05-annualization.md) | Annualization | [D05](phases/02-engine/deliverables/D05.md) | Your engine prints daily numbers and every sane comparison is annual. |
| T2 | 3 | [C06](phases/02-engine/concepts/C06-volatility-and-std-dev.md) | Volatility & Standard Deviation | [D05](phases/02-engine/deliverables/D05.md) | You want to compare a 1.2%/day strategy to a 0.4%/day strategy and know if that is a lot. |
| T2 | 3 | [C07](phases/02-engine/concepts/C07-sharpe-ratio.md) | Sharpe Ratio | [D05](phases/02-engine/deliverables/D05.md) | Two equity curves end at the same place and you cannot tell which one was luckier. |
| T2 | 4 | [C08](phases/02-engine/concepts/C08-max-drawdown-and-recovery.md) | Max Drawdown & Recovery | [D07](phases/02-engine/deliverables/D07.md) | Your first engine tearsheet prints a 47% drawdown and you nearly delete the strategy. |
| T2 | 4 | [C09](phases/02-engine/concepts/C09-calmar-and-return-vs-pain.md) | Calmar & Return-vs-Pain | [D07](phases/02-engine/deliverables/D07.md) | Two strategies with similar returns, radically different drawdowns: Sharpe says tie. |
| T2 | 4 | [C10](phases/02-engine/concepts/C10-transaction-costs-and-slippage.md) | Transaction Costs & Slippage | [D06](phases/02-engine/deliverables/D06.md) | Your strategy is beautiful with zero costs and dead at 10 bps round-trip. |
| T2 | 5 | [C11](phases/03-strategy-factory/concepts/C11-sortino-and-downside-deviation.md) | Sortino & Downside Deviation | [D08](phases/03-strategy-factory/deliverables/D08.md) | Strategy A has a better Sharpe, Strategy B never hurt you: both have the same upside. |
| T3 | 5 | [C12](phases/03-strategy-factory/concepts/C12-bootstrap-and-confidence-intervals.md) | Bootstrap & Confidence Intervals | [D10](phases/03-strategy-factory/deliverables/D10.md) | Your best strategy's Sharpe is 1.4, your worst is 1.1, and you are about to rank them. |
| T3 | 5 | [C13](phases/03-strategy-factory/concepts/C13-parameter-sensitivity-and-plateaus.md) | Parameter Sensitivity & Plateaus | [D11](phases/03-strategy-factory/deliverables/D11.md) | You found (14, 3.5) and every neighbouring value loses money. |
| T3 | 6 | [C14](phases/03-strategy-factory/concepts/C14-t-test-intuition.md) | t-test Intuition | [D10](phases/03-strategy-factory/deliverables/D10.md) | You need a decision rule for 'is this mean return distinguishable from zero'. |
| T3 | 6 | [C15](phases/03-strategy-factory/concepts/C15-overfitting-and-walkforward.md) | Overfitting & Walk-Forward Honesty | [D11](phases/03-strategy-factory/deliverables/D11.md) | Your in-sample Sharpe is 2.1 and your out-of-sample Sharpe is -0.2. |
| T3 | 7 | [C16](phases/04-paper-replication/concepts/C16-time-series-vs-cross-sectional.md) | Time-Series vs Cross-Sectional | [D12](phases/04-paper-replication/deliverables/D12.md) | The TSMOM paper's returns come from a mechanism your single-instrument backtests cannot express. |
| T3 | 7 | [C17](phases/04-paper-replication/concepts/C17-volatility-targeting.md) | Volatility Targeting | [D12](phases/04-paper-replication/deliverables/D12.md) | Same signal, wildly different risk across regimes; fixed size makes your Sharpe regime-dependen… |
| T3 | 8 | [C18](phases/04-paper-replication/concepts/C18-cointegration-and-spreads.md) | Cointegration & Spreads | [D13](phases/04-paper-replication/deliverables/D13.md) | Two assets drift apart forever and your 'mean reversion' trade becomes a trend trade - against… |
| T3 | 9 | [C19](phases/04-paper-replication/concepts/C19-replication-deviations.md) | Replication Deviations: Statistical vs Economic Significance | [D14](phases/04-paper-replication/deliverables/D14.md) | Your replication of the paper returns 60% of the paper's Sharpe and you must decide if it repli… |
| T4 | 10 | [C20](phases/05-risk-portfolio/concepts/C20-correlation-and-portfolio-variance.md) | Correlation & Portfolio Variance | [D15](phases/05-risk-portfolio/deliverables/D15.md) | Two strategies with Sharpe 1.4 and 1.2 combine into something worse than either. |
| T4 | 10 | [C21](phases/05-risk-portfolio/concepts/C21-kelly-and-fractional-kelly.md) | Kelly & Fractional Kelly | [D15](phases/05-risk-portfolio/deliverables/D15.md) | You have an edge and no idea what fraction of your capital it deserves. |
| T4 | 10 | [C22](phases/05-risk-portfolio/concepts/C22-risk-of-ruin.md) | Risk of Ruin | [D15](phases/05-risk-portfolio/deliverables/D15.md) | Your optimal-f sizing has a 30% chance of halving the account before it compounds. |
| T5 | 11 | [C23](phases/06-live-paper/concepts/C23-slippage-modeling-and-latency.md) | Slippage Modeling & Latency | [D16](phases/06-live-paper/deliverables/D16.md) | Live fills are systematically worse than the close your backtest assumed. |
| T5 | 12 | [C24](phases/06-live-paper/concepts/C24-live-vs-backtest-divergence.md) | Live vs Backtest Divergence | [D17](phases/06-live-paper/deliverables/D17.md) | Live PnL is 40% below backtest PnL and you cannot tell which component ate it. |
| T5 | 12 | [C25](phases/06-live-paper/concepts/C25-regime-detection.md) | Regime Detection | [D17](phases/06-live-paper/deliverables/D17.md) | Your whole live divergence is one volatile month, not a bug. |
<!-- END:GENERATED concepts -->

## Deliverables

<!-- BEGIN:GENERATED deliverables -->
| ID | Wk | Deliverable | Milestone | Teaches exactly one thing |
| :-- | --: | :-- | :-- | :-- |
| D01 | 1 | [Data pipeline + validation report](phases/01-foundation/deliverables/D01.md) | M1 | Raw prices are not data yet: fetch, cache, validate, then trust. |
| D02 | 1 | [Measurement lab: first equity curves + expectancy table](phases/01-foundation/deliverables/D02.md) | M1 | An equity curve is the only honest scoreboard; expectancy is its atom. |
| D03 | 2 | [Viral debunk #1 (timed, 30 minutes)](phases/01-foundation/deliverables/D03.md) | M1 | A published win rate is a marketing number until you recompute it from prices. |
| D04 | 2 | [Viral debunks #2-3 + graveyard entries](phases/01-foundation/deliverables/D04.md) | M1 | Most 'edges' are a definition problem, a cost problem, or a sample-size problem. |
| D05 | 3 | [Backtester v1: event loop, next-bar fills, cash, positions](phases/02-engine/deliverables/D05.md) | M2 | A backtest is an accounting system that happens to touch markets. |
| D06 | 3 | [Cost model + cost sensitivity report](phases/02-engine/deliverables/D06.md) | M2 | Costs are a function of turnover: what looks like an edge is often a liquidity donation. |
| D07 | 4 | [Walk-forward/OOS runner + tearsheets + look-ahead suite green](phases/02-engine/deliverables/D07.md) | M2 | Out-of-sample is a process, not a number you compute once. |
| D08 | 5 | [Strategies S01-S03: MA cross, RSI reversion, Bollinger](phases/03-strategy-factory/deliverables/D08.md) | M3 | Signal families fail in family-specific ways; naming the family predicts the autopsy. |
| D09 | 5 | [Strategy registry + graveyard v1](phases/03-strategy-factory/deliverables/D09.md) | M3 | A registry turns 'I tested a bunch of stuff' into a track record. |
| D10 | 6 | [Strategies S04-S06: Donchian, momentum, pairs + bootstrap CIs](phases/03-strategy-factory/deliverables/D10.md) | M3 | Every backtest number is a sample from a distribution you have not seen. |
| D11 | 6 | [Overfitting audit + parameter sensitivity heatmaps](phases/03-strategy-factory/deliverables/D11.md) | M3 | If the edge only exists at one parameter value, the edge is in your search, not the marke… |
| D12 | 7 | [Replication R1: Time-Series Momentum](phases/04-paper-replication/deliverables/D12.md) | M4 | Reading a paper is an implementation task; the paper's numbers are an input, not an answe… |
| D13 | 8 | [Replication R2: Pairs Trading](phases/04-paper-replication/deliverables/D13.md) | M4 | Cointegration is a relationship between two series, not a property of either one. |
| D14 | 9 | [Replication R3: Vol-Managed Portfolios + cross-paper synthesis](phases/04-paper-replication/deliverables/D14.md) | M4 | Replication fidelity is a spectrum; the deviation IS the result. |
| D15 | 10 | [Risk policy: sizing rules + portfolio allocation + Monte Carlo + regime lab](phases/05-risk-portfolio/deliverables/D15.md) | M5 | Signals decide what to trade; sizing decides whether you survive to trade it. |
| D16 | 11 | [Live harness running: broker adapter, daily signal job, dashboard](phases/06-live-paper/deliverables/D16.md) | M5 | A live bot is a boring scheduling problem wearing a finance costume. |
| D17 | 12 | [30-day live log + reconciliation report + divergence post-mortem](phases/06-live-paper/deliverables/D17.md) | M5 | Live PnL diverges from backtest PnL in explainable, budgetable ways. |
| D18 | 13 | [Capstone: public repo + writeup + portfolio doc + roadmap](phases/07-synthesis/deliverables/D18.md) | M6 | Research you cannot explain to a stranger is research you do not understand. |
<!-- END:GENERATED deliverables -->

## Grading

The course is graded on artifacts. There is no exam; the weights below are the exam.

<!-- BEGIN:GENERATED grading -->
| Artifact | Weight | Passing bar |
| :-- | --: | :-- |
| Strategy verdicts | 30% | 15+ strategies shipped, each with a written verdict |
| Backtester quality | 15% | Custom, unit-tested, documented in engine/README.md |
| Paper replications | 20% | 2-3 replications with deviation notes |
| Live paper log | 20% | 30 days of logs + reconciliation report |
| Journal + graveyard | 15% | 90 daily entries, every dead strategy autopsied |
| **Total** | **100%** | 60% = pass, 80% = good, 90%+ = publication-worthy |
<!-- END:GENERATED grading -->

## Every deliverable has an annotated evidence file

The files below carry annotation markers of the form `annotated: produces=<deliverable id>`, which is how the course proves
that each deliverable has a home in the package rather than existing only in a plan.

<!-- BEGIN:GENERATED annotations -->
| File | Evidences deliverable(s) | Teaches |
| :-- | :-- | :-- |
| [phases/01-foundation/deliverables/D01.md](phases/01-foundation/deliverables/D01.md) | D01 | — |
| [phases/01-foundation/deliverables/D02.md](phases/01-foundation/deliverables/D02.md) | D02 | — |
| [phases/01-foundation/deliverables/D03.md](phases/01-foundation/deliverables/D03.md) | D03 | — |
| [phases/01-foundation/deliverables/D04.md](phases/01-foundation/deliverables/D04.md) | D04 | — |
| [phases/02-engine/deliverables/D05.md](phases/02-engine/deliverables/D05.md) | D05 | — |
| [phases/02-engine/deliverables/D06.md](phases/02-engine/deliverables/D06.md) | D06 | — |
| [phases/02-engine/deliverables/D07.md](phases/02-engine/deliverables/D07.md) | D07 | — |
| [phases/03-strategy-factory/deliverables/D08.md](phases/03-strategy-factory/deliverables/D08.md) | D08 | — |
| [phases/03-strategy-factory/deliverables/D09.md](phases/03-strategy-factory/deliverables/D09.md) | D09 | — |
| [phases/03-strategy-factory/deliverables/D10.md](phases/03-strategy-factory/deliverables/D10.md) | D10 | — |
| [phases/03-strategy-factory/deliverables/D11.md](phases/03-strategy-factory/deliverables/D11.md) | D11 | — |
| [phases/04-paper-replication/deliverables/D12.md](phases/04-paper-replication/deliverables/D12.md) | D12 | — |
| [phases/04-paper-replication/deliverables/D13.md](phases/04-paper-replication/deliverables/D13.md) | D13 | — |
| [phases/04-paper-replication/deliverables/D14.md](phases/04-paper-replication/deliverables/D14.md) | D14 | — |
| [phases/05-risk-portfolio/deliverables/D15.md](phases/05-risk-portfolio/deliverables/D15.md) | D15 | — |
| [phases/06-live-paper/deliverables/D16.md](phases/06-live-paper/deliverables/D16.md) | D16 | — |
| [phases/06-live-paper/deliverables/D17.md](phases/06-live-paper/deliverables/D17.md) | D17 | — |
| [phases/07-synthesis/deliverables/D18.md](phases/07-synthesis/deliverables/D18.md) | D18 | — |
<!-- END:GENERATED annotations -->

## The package tree

The course ships as the tree below; the student repo it scaffolds lives under `shared/`.

<!-- BEGIN:GENERATED tree -->
```text
bootcamp/
├── capstone/
│   ├── portfolio-template.md
│   ├── recall-test.md
│   ├── rubric.md
│   └── writeup-template.md
├── phases/
│   ├── 01-foundation/
│   │   ├── concepts/
│   │   │   ├── C01-returns-and-compounding.md
│   │   │   ├── C02-expectancy-and-profit-factor.md
│   │   │   ├── C03-win-rate-vs-edge.md
│   │   │   └── C04-sample-size-and-base-rates.md
│   │   ├── deliverables/
│   │   │   ├── D01.md
│   │   │   ├── D02.md
│   │   │   ├── D03.md
│   │   │   └── D04.md
│   │   ├── gates/
│   │   │   ├── week-01-gate.md
│   │   │   └── week-02-gate.md
│   │   ├── milestones/
│   │   │   └── M1-reality-check.md
│   │   ├── templates/
│   │   │   └── viral-debunk-sheet.md
│   │   ├── README.md
│   │   ├── rubric.md
│   │   ├── week-01.md
│   │   └── week-02.md
│   ├── 02-engine/
│   │   ├── concepts/
│   │   │   ├── C05-annualization.md
│   │   │   ├── C06-volatility-and-std-dev.md
│   │   │   ├── C07-sharpe-ratio.md
│   │   │   ├── C08-max-drawdown-and-recovery.md
│   │   │   ├── C09-calmar-and-return-vs-pain.md
│   │   │   └── C10-transaction-costs-and-slippage.md
│   │   ├── deliverables/
│   │   │   ├── D05.md
│   │   │   ├── D06.md
│   │   │   └── D07.md
│   │   ├── gates/
│   │   │   ├── week-03-gate.md
│   │   │   └── week-04-gate.md
│   │   ├── instructor/
│   │   │   └── OPTIONAL-instructor-notes.md
│   │   ├── lookahead/
│   │   │   └── lookahead-test-suite.md
│   │   ├── milestones/
│   │   │   └── M2-backtest-engine.md
│   │   ├── spec/
│   │   │   ├── cost-model.md
│   │   │   ├── engine-spec.md
│   │   │   └── walkforward-splitter.md
│   │   ├── README.md
│   │   ├── rubric.md
│   │   ├── week-03.md
│   │   └── week-04.md
│   ├── 03-strategy-factory/
│   │   ├── concepts/
│   │   │   ├── C11-sortino-and-downside-deviation.md
│   │   │   ├── C12-bootstrap-and-confidence-intervals.md
│   │   │   ├── C13-parameter-sensitivity-and-plateaus.md
│   │   │   ├── C14-t-test-intuition.md
│   │   │   └── C15-overfitting-and-walkforward.md
│   │   ├── deliverables/
│   │   │   ├── D08.md
│   │   │   ├── D09.md
│   │   │   ├── D10.md
│   │   │   └── D11.md
│   │   ├── gates/
│   │   │   ├── week-05-gate.md
│   │   │   └── week-06-gate.md
│   │   ├── milestones/
│   │   │   └── M3-strategy-factory.md
│   │   ├── spec/
│   │   │   └── strategy-config-schema.md
│   │   ├── templates/
│   │   │   ├── configs/
│   │   │   │   ├── S01_ma_cross.json
│   │   │   │   ├── S02_rsi_reversion.json
│   │   │   │   ├── S03_bollinger.json
│   │   │   │   ├── S04_donchian.json
│   │   │   │   ├── S05_momentum.json
│   │   │   │   └── S06_pairs.json
│   │   │   ├── signal_S01_ma_cross.py
│   │   │   ├── signal_S02_rsi_reversion.py
│   │   │   ├── signal_S03_bollinger.py
│   │   │   ├── signal_S04_donchian.py
│   │   │   ├── signal_S05_momentum.py
│   │   │   ├── signal_S06_pairs.py
│   │   │   └── strategy-templates.md
│   │   ├── worked-example/
│   │   │   ├── README.md
│   │   │   ├── config.json
│   │   │   ├── graveyard-entry.md
│   │   │   ├── signal.py
│   │   │   ├── tearsheet.md
│   │   │   └── verdict.md
│   │   ├── README.md
│   │   ├── rubric.md
│   │   ├── week-05.md
│   │   └── week-06.md
│   ├── 04-paper-replication/
│   │   ├── concepts/
│   │   │   ├── C16-time-series-vs-cross-sectional.md
│   │   │   ├── C17-volatility-targeting.md
│   │   │   ├── C18-cointegration-and-spreads.md
│   │   │   └── C19-replication-deviations.md
│   │   ├── deliverables/
│   │   │   ├── D12.md
│   │   │   ├── D13.md
│   │   │   └── D14.md
│   │   ├── dossiers/
│   │   │   ├── R1-time-series-momentum.md
│   │   │   ├── R2-pairs-trading.md
│   │   │   └── R3-vol-managed-portfolios.md
│   │   ├── gates/
│   │   │   ├── week-07-gate.md
│   │   │   ├── week-08-gate.md
│   │   │   └── week-09-gate.md
│   │   ├── milestones/
│   │   │   └── M4-paper-replication.md
│   │   ├── README.md
│   │   ├── rubric.md
│   │   ├── week-07.md
│   │   ├── week-08.md
│   │   └── week-09.md
│   ├── 05-risk-portfolio/
│   │   ├── concepts/
│   │   │   ├── C20-correlation-and-portfolio-variance.md
│   │   │   ├── C21-kelly-and-fractional-kelly.md
│   │   │   └── C22-risk-of-ruin.md
│   │   ├── deliverables/
│   │   │   └── D15.md
│   │   ├── gates/
│   │   │   └── week-10-gate.md
│   │   ├── README.md
│   │   ├── rubric.md
│   │   └── week-10.md
│   ├── 06-live-paper/
│   │   ├── concepts/
│   │   │   ├── C23-slippage-modeling-and-latency.md
│   │   │   ├── C24-live-vs-backtest-divergence.md
│   │   │   └── C25-regime-detection.md
│   │   ├── deliverables/
│   │   │   ├── D16.md
│   │   │   └── D17.md
│   │   ├── gates/
│   │   │   ├── week-11-gate.md
│   │   │   └── week-12-gate.md
│   │   ├── milestones/
│   │   │   └── M5-live-paper.md
│   │   ├── spec/
│   │   │   └── signal-generator-spec.md
│   │   ├── README.md
│   │   ├── rubric.md
│   │   ├── week-11.md
│   │   └── week-12.md
│   └── 07-synthesis/
│       ├── concepts/
│       ├── deliverables/
│       │   └── D18.md
│       ├── gates/
│       │   └── week-13-gate.md
│       ├── milestones/
│       │   └── M6-capstone.md
│       ├── README.md
│       ├── rubric.md
│       └── week-13.md
├── shared/
│   ├── data-fetcher/
│   │   ├── kit/
│   │   │   ├── __init__.py
│   │   │   └── data_fetcher.py
│   │   └── README.md
│   ├── metrics-module/
│   │   ├── kit/
│   │   │   ├── __init__.py
│   │   │   └── metrics.py
│   │   └── README.md
│   ├── repo-scaffold/
│   │   ├── .pytest_cache/
│   │   │   ├── v/
│   │   │   │   └── cache/
│   │   │   │       ├── lastfailed
│   │   │   │       └── nodeids
│   │   │   ├── .gitignore
│   │   │   ├── CACHEDIR.TAG
│   │   │   └── README.md
│   │   ├── config/
│   │   ├── data/
│   │   ├── engine/
│   │   ├── journal/
│   │   ├── kit/
│   │   │   ├── tests/
│   │   │   │   ├── test_data_fetcher.py
│   │   │   │   ├── test_metrics.py
│   │   │   │   ├── test_spine_cli.py
│   │   │   │   └── test_spine_contract.py
│   │   │   ├── README.md
│   │   │   ├── __init__.py
│   │   │   ├── contracts.md
│   │   │   ├── data_fetcher.py
│   │   │   ├── lookahead-patterns.md
│   │   │   ├── metrics.py
│   │   │   ├── pinned-env.md
│   │   │   ├── repo-ownership.md
│   │   │   └── spine.py
│   │   ├── live/
│   │   ├── papers/
│   │   ├── reports/
│   │   ├── strategies/
│   │   ├── tests/
│   │   ├── tools/
│   │   │   ├── check_gate.py
│   │   │   ├── doctor.py
│   │   │   ├── journal.py
│   │   │   ├── report.py
│   │   │   ├── spot_it_wrong.py
│   │   │   └── validate_all.py
│   │   ├── .gitignore
│   │   ├── Makefile
│   │   ├── README.md
│   │   ├── gates.json
│   │   └── requirements.txt
│   ├── sample-data/
│   │   ├── LAB_MR.csv
│   │   ├── LAB_PAIR_A.csv
│   │   ├── LAB_PAIR_B.csv
│   │   ├── LAB_RANDOM.csv
│   │   ├── LAB_TREND.csv
│   │   ├── LAB_VOL.csv
│   │   ├── README.md
│   │   └── truth.json
│   ├── templates/
│   │   ├── debunk.md
│   │   ├── deviation-log.md
│   │   ├── graveyard-entry.md
│   │   ├── reconciliation.md
│   │   ├── strategy-config-schema.md
│   │   ├── strategy-config.schema.json
│   │   ├── tearsheet.md
│   │   ├── thesis.md
│   │   └── verdict.md
│   ├── costs-model.md
│   ├── gate-checklist.md
│   ├── journal-template.md
│   ├── quality-gates.md
│   ├── retro-template.md
│   └── testing-guide.md
├── tests/
├── tools/
│   ├── build_syllabus.py
│   ├── coursekit.py
│   ├── make_sample_data.py
│   ├── sync_gates.py
│   ├── test_the_course.py
│   └── verify_course.py
├── README.md
├── registry.json
└── syllabus.md
```
<!-- END:GENERATED tree -->

## What is deliberately out of scope

Options and derivatives pricing, stochastic calculus, HFT and microstructure, reinforcement
learning for trading, production infrastructure, and anything requiring a PhD to read. If you
finish the course and want those, you will now have the return series, the engine, and the cost
model that make them learnable - which is the point of not starting there.

## How to start

1. Read [`shared/repo-scaffold/README.md`](shared/repo-scaffold/README.md) and run the quickstart.
2. Open [`phases/01-foundation/week-01.md`](phases/01-foundation/week-01.md) and do Monday's task.
3. Keep a journal from day one: `shared/journal-template.md`, one entry per day, 80+ by Week 13.
