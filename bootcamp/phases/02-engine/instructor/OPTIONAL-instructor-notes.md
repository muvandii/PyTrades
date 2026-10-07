# OPTIONAL — instructor notes for Phase 2 (skip if you are solo)

Everything in this course is written to be completed solo. This file exists for the case where
someone is teaching it, or for a solo student who wants the "grader's eye" on their own work.
It is explicitly optional: none of it is required by any gate.

## The four things a first-time engine builder gets wrong

1. **Positions as weights.** They store target weights and call them positions. Consequences:
   buy-and-hold drifts, turnover is overstated, cash never exists. Detection: ask "how much
   cash do you hold on day 400?" A blank look means weights-only.
2. **The shift in the wrong place.** They shift the price instead of the signal, or shift inside
   the signal function, which then double-shifts or cancels. Detection: `grep -n "shift" engine/`
   and ask for the one sentence in `README.md` naming the single shift location.
3. **Costs after the fact.** Costs applied to the equity curve at the end rather than inside the
   loop; the run's `meta.json` then shows `total_cost_drag: 0.0` while the report shows costs.
   Detection: compare `meta.json.total_cost_drag` against the report's cost attribution.
4. **Silent NaN handling.** `fillna(0)` on the signal before validating it hides a broken warm-up
   window. Detection: check whether the first `max(lookback)` bars are flat by construction.

## Grading the buy-and-hold reproduction

"Within 1%" is deliberately loose, because adjusted vs unadjusted prices can move the number by
that much. What matters is the explanation of the residual: a student who says "0.6% gap, all of
it from dividend adjustment in the stooq series" understands the test; a student who says "close
enough" does not.

## What good looks like in M2

The timed run should be boring. A strong M2 has: a spec file created by copy-paste, a signal
function with no engine imports, one command to run, one command to render, and a verdict
written from the template in under six minutes. If any step needed the student to open
`backtest.py`, the engine is not finished.

## When to intervene

Only in three cases: (1) tests are being deleted instead of fixed; (2) a verdict quotes a number
that no saved artifact contains; (3) the student is about to run six strategies in Week 5 on an
engine whose contract suite fails. All three are integrity problems, not skill problems, and all
three are caught by asking for the artifact, not the answer.
