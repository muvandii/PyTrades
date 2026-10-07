# Quality gates: the three checklists that decide whether work counts

Verbatim from the course spec. `make gate WEEK=N` checks the mechanical parts for you;
the manual parts are yours to confirm in the gate runner, out loud, in your journal.

## A strategy cannot ship unless

- [ ] It runs on real data without errors
- [ ] It includes fees + slippage
- [ ] It has out-of-sample results
- [ ] It has a written verdict (`edge` / `no edge` / `inconclusive`)
- [ ] It has a graveyard entry if dead

## An engine change cannot merge unless

- [ ] It has a unit test
- [ ] It does not break existing strategies (`make test` green)
- [ ] It is documented in `engine/README.md` (what changed, why, which numbers moved)

## A week cannot end unless

- [ ] The weekly deliverable shipped
- [ ] The graveyard is updated
- [ ] The journal has entries for each working day
- [ ] At least one concept is "learned": code it, explain it in two sentences, spot it wrong

## The one meta-rule

Miss a gate → do not advance. Fix it first. A skipped gate is not a shortcut; it is a
loan against Week 12, where it gets repaid with interest and a worse debugging session.
