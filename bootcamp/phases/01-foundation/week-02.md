---
week: 2
phase: P1
title: Kill Three Viral Strategies
deliverables: [D03, D04]
concepts: [C03, C04]
milestone: M1
hours: 14-18
---

# Week 2 — Kill Three Viral Strategies

## Learning objective

Recompute three published or viral "profitable strategy" claims from raw prices, break them with execution, costs and sample size, and write a verdict and a graveyard entry for each - with the first one timed.

## Deliverable

- [D03 — Viral debunk #1 (timed, 30 minutes)](deliverables/D03.md) → `reports/debunks/debunk-01.md`
- [D04 — Viral debunks #2-3 + graveyard entries](deliverables/D04.md) → `reports/debunks/debunk-02.md`, `debunk-03.md`, three graveyard entries

This week ends at **milestone M1: reality check** - you can debunk a viral strategy, start to written verdict, in 30 minutes.

## Daily tasks

### Mon — Collect three claims, and write down what each one asserts

Find three claims of the form "X strategy returns Y%, win rate Z%". Sources: YouTube thumbnails, newsletter screenshots, X/Twitter threads, Medium posts, the strategy section of a broker blog. One of them should be a claim you privately believe.

For each: capture the URL, quote the claim verbatim, and write which of these it is really claiming:
- a **rule** (entry/exit logic you can code),
- a **result** (a number with a period and an instrument),
- or a **feeling** ("beats the market"), which you will translate into a rule and note the translation.

*Time: 2-3 h. Expect one claim to be uncodable - that is itself a finding: uncodable claims cannot be true or false.*

### Tue — Reconstruct claim #1 and reproduce its own numbers

Implement the smallest possible version of the rule. Recompute the claim's headline numbers (return, win rate) on real data from your Week 1 cache, over the claim's period if it has one.

Use `templates/debunk.md` - fill Step 1 and Step 3. Do not yet fix anything; your job today is to see whether the claim reproduces on its own terms.

*Time: 3-4 h. Expect: on its own terms it usually reproduces roughly, because the author did run something.*

### Wed — Break claim #1, timed (this is D03 and M1)

Set a timer. 30 minutes. In this order:

1. **Execution** (5 min): does the signal trade the bar it is computed on? Add `shift(1)` and re-measure. Record the delta.
2. **Costs** (10 min): `make costs S=<id>` or add fee+slippage. Find the breakeven bps.
3. **Sample** (10 min): count independent bets, not rows. Compute the win-rate confidence interval for that trade count.
4. **Write the verdict** (5 min): `debunked` / `survives (partially)` / `inconclusive`, plus the one mechanism that decided it.

Log the elapsed time in the report header. If you go over 30 minutes, log the actual number and note where the time went - the next two will be faster.

*Time: 1 h plus setup. This is the milestone; do it before reading further.*

### Thu — Debunk #2: a claim with a real edge in it

Pick the claim you believe most. This time, before running anything, write your prediction: which of the three killers gets it, and by how much.

Then run all three checks. If the claim survives all three, say so - `survives (partially)` is a legitimate verdict, and it is more informative than a comfortable debunk. Inject [C03 — Win Rate vs Edge](concepts/C03-win-rate-vs-edge.md) if the win rate is the headline.

*Time: 3-4 h. Expect: the claim survives costs but dies on sample size, or vice versa.*

### Fri — Debunk #3: the one with the tiny sample

Take the claim with the fewest trades (or the shortest period). Inject [C04 — Sample Size & Base Rates](concepts/C04-sample-size-and-base-rates.md).

Quantify it: how many independent bets? What win rate range does that sample support? What would the claim need to look like to be evidence?

*Time: 2-3 h.*

### Sat — Write the three debunks up (D03, D04)

Each file follows `templates/debunk.md` end to end. For each, the graveyard line must use a taxonomy cause. Then update `graveyard.md` with all three entries.

Also write the one-paragraph reflection for each: *would this claim have fooled me if I had not done the check?*

*Time: 3-4 h.*

### Sun — Timed fire drill, then the gate

1. Pick a fourth claim you have never looked at. Run the whole loop against the clock: reconstruct → data → measure → break → verdict. Target 30 minutes, cold.
2. Journal all week. Update the graveyard.
3. `make gate WEEK=2`. Fix failures.
4. Confidence check: in one sentence each, what is the difference between a win rate and an edge, and how many trades a claim needs before you take it seriously?

*Time: 2-3 h.*

## Gate

`make gate WEEK=2` must pass - see [gates/week-02-gate.md](gates/week-02-gate.md). The timed debunk (D03) is milestone **M1**: 30 minutes, start to written verdict, and the elapsed time is recorded in the report header.

## Graveyard prompt

Expect all three claims to die, and expect at least one to die of `insufficient sample` rather than dishonesty - the author may have tested it in good faith on 11 trades. Log the cause precisely: `no edge`, `cost death`, `look-ahead illusion`, `overfit`, `data problem`, `insufficient sample`. The precision is what makes Week 13's taxonomy possible.

## Concept injections this week

- [C03 — Win Rate vs Edge](concepts/C03-win-rate-vs-edge.md) — triggered by the "90% win rate" headline
- [C04 — Sample Size & Base Rates](concepts/C04-sample-size-and-base-rates.md) — triggered by a claim built on a handful of trades

## If you are ahead

Build `reports/debunks/debunk-intake.md`: a one-page intake checklist that turns any claim into the three checks in under 30 minutes. In Phase 5 you reuse it as the first triage step for your own ideas.
