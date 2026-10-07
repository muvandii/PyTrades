# Look-ahead test suite (Week 3-4)

Four tests. The first two you write yourself; the last two ship with the course. All four must
pass before the Week 4 gate.

## 1. Time-travel test (write it)

```python
def test_positions_are_identical_when_the_future_is_removed():
    full = run_backtest(spec, prices=PRICES)
    cut = run_backtest(spec, prices={k: v.loc[:CUT_DATE] for k, v in PRICES.items()})
    assert cut.positions.loc[:CUT_DATE].equals(full.positions.loc[:CUT_DATE])
    assert (cut.equity.loc[:CUT_DATE] - full.equity.loc[:CUT_DATE]).abs().max() < 1e-6
```

If this fails, some part of your pipeline - usually a normalisation, a fill, or a warm-up window -
is reading bars that had not happened yet at the truncation date.

## 2. Signal-shift premium (write it)

Run any momentum rule with `signal_shift=0` and `signal_shift=1`. The premium must be positive
on a trending series (cheating helps) and is usually 0.05-0.5 Sharpe. Record the number for your
strategy; if it is exactly zero, your signal is probably constant.

## 3. Contract suite (ships: `kit/tests/test_spine_contract.py`)

```bash
PYTRADES_ENGINE=engine.backtest python -m pytest kit/tests/test_spine_contract.py -q
```

Covers execution lag, buy-and-hold identity under next_close, cost monotonicity, turnover
accounting, rejected inputs, trade extraction, persistence and provenance.

## 4. Blind-data test (your judgment, not code)

Run the same spec on a symbol you have never looked at, with parameters unchanged. Then answer:

- Did the character of the result change (trade frequency, holding period, tail behaviour)?
- If yes: something in the specification was tuned to the instrument you originally used.

No assertion - this one is a written paragraph in `reports/lookahead-audit.md`, because the
failure mode is not a bug, it is a habit.

## Checklist for the Week 4 gate

- [ ] `tests/test_lookahead.py` contains tests 1 and 2, both passing
- [ ] `make test-contract E=engine.backtest` passes (test 3)
- [ ] `reports/lookahead-audit.md` contains the blind-data paragraph (test 4) and the measured
      shift premium from test 2
- [ ] One sentence in `engine/README.md`: "the only place the signal timeline is shifted is
      `<file>:<line>`" - grep your own repo for `.shift(` and confirm each occurrence is justified
