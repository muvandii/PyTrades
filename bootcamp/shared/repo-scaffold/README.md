# pytrades-student (the repo you actually live in)

This is the repo you build during the 13-week bootcamp. Clone it, run one command,
and start Week 1. Everything else (weeks, concepts, gates, rubrics) lives in the
course package you were given; this is the workshop.

## Day 1, in four commands

```bash
git clone <your-fork-of-this-template> pytrades && cd pytrades
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
make doctor
```

`make doctor` checks Python version, dependencies, data directory, and prints what
to do next. If it is green, start Week 1.

## Layout

```
config/       one JSON spec per strategy (the schema is fixed, see config/README.md)
data/         cached OHLCV CSVs + .meta.json provenance sidecars (never hand-edit)
kit/          reference data fetcher, metrics and backtest spine (read-only)
engine/       YOUR backtester. Week 3-4 you fill this in. It replaces kit/spine.py.
strategies/   one folder per strategy: signal.py + notes
papers/       paper replications (Weeks 7-9)
live/         paper-trading bot, logs, reconciliation (Weeks 5, 11-12)
reports/      every generated artifact: tearsheets, debunks, cost studies, audits
journal/      one file per day, 90 entries by Week 13
tests/        YOUR tests, including the spine contract suite
tools/        helpers: gate checker, journal writer, concept checker, reporter
graveyard.md  every dead strategy, with cause of death
README.md     updated at Week 13 into your public front page
```

## Commands you will actually use

```bash
make data SYMBOLS="SPY QQQ" START=2010-01-01   # fetch real bars
make validate                                   # data quality report for every cached file
make list                                       # strategies defined in config/
make run S=S01_ma_cross NAME=baseline           # run the reference spine, save artifacts
make costs S=S01_ma_cross                       # cost sensitivity from 0 to 30 bps
make compare A=baseline B=with_costs            # side-by-side metrics
make test                                       # kit tests + your tests
make gate WEEK=1                                # the Week 1 gate, checked automatically
make journal                                    # create today's journal entry from the template
make report S=S01_ma_cross                      # markdown tearsheet for a saved backtest
```

`make run` uses `kit/spine.py` until Week 4. From Week 4 you switch it to your own
engine: `make run E=engine.backtest`. Your engine must pass
`tests/test_spine_contract.py` (copied from the course's look-ahead suite) before
the Week 4 gate will pass.

## No network? Work offline, honestly

Market endpoints are sometimes unreachable (firewalls, rate limits, a flight). The
course never blocks on that, but it also never lets you mistake synthetic bars for
evidence:

```bash
python -m kit.data_fetcher smoke                                  # offline smoke test, writes nothing
python -m kit.data_fetcher fetch SPY --provider synthetic         # explicit synthetic bars (flagged)
python -m kit.data_fetcher validate SPY                           # shows the SYNTHETIC tag
make validate                                                     # every cached file, with sources
```

Synthetic data is flagged in `data/<SYM>.meta.json`, `assert_not_synthetic()` refuses
it in a graded run, and the course's own laboratory series live in
`shared/sample-data/` (see the LAB_*.csv files: they exist to teach mechanics, and
`truth.json` is the answer key - read it only after writing your verdict).

## The four contracts (do not break these)

| Contract | Path | Producer |
| --- | --- | --- |
| Data | `data/<SYMBOL>.csv` + `.meta.json` | `kit/data_fetcher.py` |
| Spec | `config/<strategy_id>.json` | you, per `config/README.md` |
| Signal | `strategies/<id>/signal.py::generate(prices, params)` | you |
| Result | `reports/backtests/<name>/{equity,positions,trades}.csv`, `metrics.json`, `meta.json` | the engine |

Every week's work composes because these four never change shape. If you feel the
urge to change one, you are about to break your own history.

## House rules

1. **No hand-edited data.** If `data/*.csv` looks wrong, re-fetch it or write it
   down in `reports/data-validation.md` as an issue. Silent edits kill verdicts.
2. **Synthetic data never reaches a verdict.** `kit/data_fetcher.py` refuses to
   build it without an explicit flag, and `sample-data/` is a laboratory, not a market.
3. **Every run saves artifacts.** If it is not in `reports/`, it did not happen.
4. **Every strategy ends with a verdict**, even (especially) the dead ones.
5. **Costs and out-of-sample are always on** after Week 4. A result without both is
   a hypothesis, not a finding.
