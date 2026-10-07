---
week: 1
phase: P1
title: Raw Prices Are Not Data
deliverables: [D01, D02]
concepts: [C01, C02]
milestone: null
hours: 12-16
---

# Week 1 — Raw Prices Are Not Data

## Learning objective

Turn a downloaded price file into a validated dataset you can defend, and turn that dataset into an equity curve whose every number you can explain.

## Deliverable

- [D01 — Data pipeline + validation report](deliverables/D01.md): a working `kit/data_fetcher.py` workflow, 8-10 instruments cached with provenance, and `reports/data-validation.md`.
- [D02 — Measurement lab](deliverables/D02.md): `reports/measurement-lab.md` with equity curves, compounding arithmetic, and an expectancy table.

Both ship by Sunday. The gate is mechanical: `make gate WEEK=1`.

## Daily tasks

### Mon — Set up, then look at prices before you model anything

1. Clone the scaffold, `pip install -r requirements.txt`, `make doctor`. Fix whatever it complains about.
2. Run `make scaffold` and `make data SYMBOLS="SPY QQQ IWM TLT IEF GLD EEM EFA DBC UUP" START=2005-01-01`.
3. Open one CSV in a notebook. Plot close. Write down three things you notice (trends, gaps, vol clusters, a flat stretch).
4. `make journal` and fill it in. Yes, on day one. The habit is the deliverable.

*Time: 2-3 h. Failure you should expect: a provider returns nothing for a ticker, or a symbol needs an exchange suffix.*

### Tue — Fetch, cache, validate (D01 building)

1. `make validate` and read the output line by line. For every warning, decide: accept, investigate, or exclude the symbol. Write the decision down.
2. Open `data/SPY.meta.json`. Understand every field. The `sha256` is what makes your later verdicts provable.
3. Deliberately break something: hand-edit a close price to 10x in a copy of a CSV, run `make validate`, and confirm the validator catches it. Then revert with `make data ... --refresh`.
4. Start `reports/data-validation.md`: the coverage table plus one paragraph per symbol.

*Time: 2-4 h. This is the least glamorous day of the course and the one most likely to save you in Week 8.*

### Wed — Your first equity curve, and what compounding actually does

1. Buy-and-hold equity curve for SPY from `data/SPY.csv`. Plot it.
2. Compute total return two ways: `(1+r).prod() - 1` and `r.sum()`. Compare. On a 20-year SPY series, the difference is the whole lesson.
3. Same for a -50% year followed by a +50% year: you need +100% to recover. Write the arithmetic out longhand once, and never again forget it.
4. Inject [C01 — Returns & Compounding](concepts/C01-returns-and-compounding.md).

*Time: 2-3 h. The moment this clicks is the moment you stop drawing "straight line up" charts.*

### Thu — Build a strategy with a 90% win rate, on purpose

1. Take SPY. Rule: buy at the open, sell at the close, same day (or your market's equivalent). Measure the win rate.
2. Now compute expectancy per trade and profit factor. Compare win rate to expectancy - they will disagree.
3. Repeat with a rule that wins 9 out of 10 trades but loses 15x on the loser (widen the stop). Find a configuration where the win rate is over 90% and the equity curve goes down.
4. Inject [C02 — Expectancy & Profit Factor](concepts/C02-expectancy-and-profit-factor.md).

*Time: 2-4 h. You are pre-building the muscle for Week 2: almost every viral claim is this shape.*

### Fri — The measurement lab: three baselines

Build three reference lines every later strategy will be compared against:

1. **Buy and hold** on your universe (equal weight, rebalanced monthly).
2. **Random entries** with a fixed holding period (1 month), repeated 200 times - plot the distribution of outcomes.
3. **Always flat** (cash) - the zero line.

Compute total return, CAGR, and max drawdown for each. Save the numbers; save the plots.

*Time: 2-3 h. Expect: random entries produce a wide distribution - this is what "luck" looks like before you learn Sharpe.*

### Sat — Assemble the lab report (D02)

1. `reports/measurement-lab.md`:
   - the coverage note (one line: which symbols, which period, what was excluded and why)
   - equity curves for the three baselines, with the arithmetic shown for total return
   - the compounding exhibit (the -50%/+50% arithmetic, and the SPY sum-vs-product gap)
   - the expectancy table: rule, trades, win rate, avg win, avg loss, expectancy, profit factor
   - one paragraph: which number would you trust to compare two strategies, and why not the others?
2. Re-run everything from a clean shell (`make validate && make run ...`) and confirm it reproduces.

*Time: 3-4 h.*

### Sun — Verdict, graveyard, journal, gate

1. Write the week's first graveyard entries: the naive baselines ("random entries", "always flat") with `cause of death: no edge / thesis wrong`. Two lines each is fine; the taxonomy word matters.
2. Journal for each working day (5-6 entries).
3. Run `make gate WEEK=1`. Fix any failure.
4. Write down, in one sentence each: what compounding is, and what expectancy is. If you cannot, redo Wed and Thu.

*Time: 1-2 h.*

## Gate

`make gate WEEK=1` must pass. Full definition: [gates/week-01-gate.md](gates/week-01-gate.md).

Mechanical: 5+ cached CSVs, a data validation report, a measurement lab report containing an expectancy table, 5 journal entries, and the scaffold self-test. Manual: you can explain compounding and expectancy in two sentences each, and you can spot the wrong versions in `toolkit spot-it-wrong`.

## Graveyard prompt

Log the two baselines as your first deaths. `no edge` is a legitimate cause of death and will be the most common one in your graveyard: baselines exist to be beaten, and most strategies you test will not beat them. Writing that down in Week 1 makes Week 6 honest.

## Concept injections this week

- [C01 — Returns & Compounding](concepts/C01-returns-and-compounding.md) — triggered by your first equity curve
- [C02 — Expectancy & Profit Factor](concepts/C02-expectancy-and-profit-factor.md) — triggered by wanting to say "is this good?"

## If you are ahead

Write a `tools/describe_data.py` that prints, for every cached symbol: return distribution stats, annualised vol, max drawdown, and the three largest 1-day moves with dates. This is the "know your data" reflex; it pays off in Week 2 when a "90% win rate" claim is measured on a symbol with a 300% move in it.
