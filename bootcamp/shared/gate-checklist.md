# Gate checklist (print this, tick it, pin it above your desk)

A week does not end until all four are true. Miss a gate → don't advance.

## Every week

- [ ] Weekly deliverable shipped (see `make gate WEEK=N` for exactly what that means)
- [ ] Graveyard updated (new deaths logged with a `cause of death` from the taxonomy)
- [ ] Journal entries written for each working day
- [ ] At least one concept "learned": you can code it, explain it in 2 sentences, and spot it wrong

## Every strategy (before it can be called tested)

- [ ] Runs on real data without errors
- [ ] Includes fees + slippage
- [ ] Has out-of-sample results
- [ ] Has a written verdict (edge / no edge / inconclusive)
- [ ] Has a graveyard entry if dead

## Every engine change (weeks 3+)

- [ ] Has a unit test
- [ ] Doesn't break existing strategies (`make test` green)
- [ ] Documented in `engine/README.md`

## The honesty checks nobody will run for you

- [ ] Every number in a report traces to a saved artifact with a fingerprint
- [ ] Every parameter was chosen before the OOS run, or the selection is disclosed
- [ ] Every "expected" number in a report was written before seeing the result
- [ ] Any live rule I changed mid-run is logged in the reconciliation file
