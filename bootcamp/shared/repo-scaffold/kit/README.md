# kit/ - the reference implementation (read it, then replace it)

`kit/` is deliberately small and deliberately boring. It is the thing you build
against in Weeks 1-2, the oracle you test against in Weeks 3-4, and the safety net
you fall back on when your engine is broken and a deadline is real.

| Module | What it is | You replace it in |
| --- | --- | --- |
| `data_fetcher.py` | keyless fetch (stooq → yahoo), cache + provenance sidecars, validation | never - it is infrastructure, not strategy |
| `metrics.py` | every number this course uses, unit-tested against hand computation | Week 3 → `engine/metrics.py`, validated against this |
| `spine.py` | the reference backtester, spec loader, artifact saver | Week 3-4 → `engine/backtest.py`, must pass the contract suite |

## Ground rules

1. **Never edit `kit/`.** Your engine will be compared to it; a modified oracle is
   no oracle. If you think a kit function is wrong, write a failing test in
   `tests/` that proves it, then journal about it.
2. **Read it before Week 3.** The cleanest way to learn what a backtester is:
   read 400 lines that do it plainly, then write your own.
3. **Keep it in `requirements`-free shape.** `kit/` uses pandas + numpy only.

## Run the kit's own tests

```bash
make test-kit        # 25 metric oracle tests
make test-contract   # 17 spine contract tests, against kit.spine or your engine
```
