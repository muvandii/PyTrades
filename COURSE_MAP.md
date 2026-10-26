# Course Map — Algorithmic Trading Python for Beginners (QuantProgram)

> **Source video (single source of truth for sequencing):**
> *Algorithmic Trading Python for Beginners - FULL TUTORIAL* — QuantProgram, 2022-01-14, **3:00:48**
> https://www.youtube.com/watch?v=GDMkkmkJigw
>
> All timestamps below are the video's **official chapters** from its description.
> Nothing has been reordered. Where this programme adds something the video does
> not cover (e.g. test discipline, modern `yfinance` column shapes, transaction
> costs in the capstone), it is labelled **[programme addition]**.

## Stated assumptions (tell your instructor if any of these are wrong)

| Assumption | Value used to size each day |
|---|---|
| Starting level | Beginner Python (can run a cell; variables/lists are new-ish) |
| Study time | ~2–3 hours per learning day (15–25 min watching, the rest implementing) |
| Python | 3.10+ (3.11/3.12 recommended) |
| Environment | Anaconda **as in the video**, or `venv` + `pip` [programme addition — either is acceptable] |
| Internet | Needed to watch/embed video and for *live* `yfinance` downloads only. All assessed work runs offline on bundled data. |
| Goal | Independent competence, not a profitable strategy. Nothing here is financial advice. |

## How the days were cut

One day ≠ one chapter. Days are cut at **concept boundaries** in the chapter list so
each day ends with a runnable deliverable. A long stretch of related pandas
operations (Days 3–4) is split across two days; a short-but-deep segment
(long-only bias, Day 9) gets a full day of application.

## The map

| Day | Topic | Video segment (official chapters) | Measurable learning objectives (you will be able to…) | Core exercise | Project deliverable |
|---|---|---|---|---|---|
| **01** | Environment, Jupyter & first market data | 00:00–13:00 · Intro, Anaconda, installing yfinance, Jupyter, numpy/pandas, downloading stock data | Set up & verify an environment in code; explain function vs method vs library; obtain OHLCV data for explicit dates; inspect shape/index/dtypes/missing values and *validate* a price frame (raising specific errors) | `validate_ohlcv`, `extract_close` (flat + MultiIndex columns), debug a broken price selector | **P0.1 Data intake report:** validated close-price CSV + chart + 5-bullet data-quality report |
| **02** | Working with data: read/write, select & segregate | 13:00–23:00 · Read and writing data, separating and segregating data | Round-trip CSV without destroying the index; select by label/position/date-range and predict the difference; prove a saved file equals the in-memory frame | Fix an index-losing CSV round-trip; implement date-range slicing that fails loudly on empty results | **P0.2** `load_prices()` + `slice_prices()` utilities with tests |
| **03** | Visualisation, normalisation & creating columns | 23:00–44:40 · Data visualisation, normalisation, making changes/creating new data, deleting data | Plot prices with labelled axes; normalise two series to a common base (=100) and explain why raw-price comparison misleads; add/drop columns without `SettingWithCopy` traps | Implement `normalise(prices, base=100)` handling a NaN first row | **P0.3** Normalised comparison chart of ≥3 tickers + written interpretation |
| **04** | Resampling & first risk numbers | 44:40–01:01:50 · Resampling, histogram, mean/variance/std, scatter plot, stock comparison with risk metric | Resample daily→monthly correctly (last vs mean — justify the choice); compute annualised volatility from daily returns and state the √252 assumption | Implement `annualised_volatility()`; explain a histogram of returns vs prices | **🏁 Milestone 1 — Data handler:** reviewed data utilities (Days 1–4), passing tests, README |
| **05** | Loops, correlation, covariance & heatmaps | 01:01:50–01:16:00 · For loops, correlation and covariance, heat map, **Challenge 1** | Build a multi-ticker returns matrix with a loop *and* vectorised code, and compare; read a correlation heatmap critically (correlation of *returns*, not prices) | Video's Challenge 1, re-specified with acceptance tests [programme addition: tests] | **P1.1** Correlation report for 5 tickers + one diversification claim you can defend |
| **06** | Returns & moving averages | 01:16:00–01:35:00 · Simple and log returns, creating moving averages, **Challenge 2** | Compute simple & log returns, convert between them, explain the first NaN; implement SMA & EMA and explain `min_periods`/warm-up rows | Video's Challenge 2 (SMA 50/200 plots for the 5 Challenge-1 stocks) with a written signal idea — no backtest yet | **P1.2** Indicator module: `sma()`, `ema()`, `log_returns()` with edge-case tests |
| **07** | Alignment, missing data, cumulative returns & drawdowns | 01:35:00–01:57:00 · Reindexing, forward/back fill, cumulative returns and drawdowns | Align two calendars with `reindex`; choose ffill vs bfill and name the bias each creates (**bfill = look-ahead**); implement running-peak drawdown from scratch | Debug a drawdown that silently uses future data | **🏁 Milestone 2 — Analytics:** cumulative-return & drawdown charts with a bias audit checklist |
| **08** | First vectorised backtest: SMA crossover | 01:57:00–02:11:40 · Creating and backtesting strategies, comparison to buy and hold | Translate "SMA50 > SMA100" into signal → **position (shifted 1 day)** → strategy returns; explain why the `.shift(1)` is the difference between a backtest and cheating | Rebuild the backtest from a spec without the video; find the look-ahead bug in supplied code | **P2.1** Backtest v1 vs buy-and-hold: total return, volatility, equity curve |
| **09** | Long-only bias & honest comparison | 02:11:40–02:16:30 · Long bias strategy, **Challenge 3** | Re-run long/short vs long-only vs buy-hold on identical data; argue from return **and** volatility **and** drawdown which is "better" and for whom | Video's Challenge 3 (drawdown comparison) + [programme addition] subtract a simple transaction cost per position change | **🏁 Milestone 3 — Backtest v1 review:** 1-page verdict with limitations section |
| **10** | Functions: a reusable strategy tester | 02:16:30–02:26:30 · Creating a function | Refactor notebook cells into `test_strategy(ticker, start, end, sma_pair)` with typed inputs, docstring, and no globals; explain parameter vs argument | De-globalise supplied code that only works when cells run in one order | **P2.2** `strategy.py` function library, importable outside the notebook |
| **11** | Classes: a strategy object you can import | 02:26:30–02:51:00 · Creating a class, importing and using a class, **Challenge 4** | Justify (or reject) a class over functions for strategy state; implement and import a strategy class from a fresh notebook | Video's Challenge 4 with an import-from-clean-kernel test | **P2.3** `pytrades/` package v0.1: data + indicators + strategy modules |
| **12** | APIs & data you don't control | 02:51:00–03:00:48 · API, working with API (Alpha Vantage) | Fetch data with an API key **kept out of code** [programme addition: `.env`]; handle rate-limit/malformed responses; explain why data quality/vendor choice changes backtest results | Failure-mode drill: bad key, empty payload, renamed columns | **P2.4** API data adapter returning the same validated frame as Day 01 (mocked tests, no live key required) |
| **13** | **Capstone** (no new video) | Re-watch: 01:57:00–02:16:30 only | Design, backtest and *critique* a strategy **not shown in the video** (e.g. close vs SMA200 filter, or EMA crossover) on a ticker you have not used before | Full spec in the Day 13 notebook | **🏁 Capstone:** reproducible notebook + `pytrades/` code + 1-page report (method, results, biases, costs, what would break it live) |

## Project progression (each day builds the same codebase)

```
P0 Data intake (Days 1–4)  →  P1 Analytics (Days 5–7)  →  P2 Backtester (Days 8–12)  →  Capstone (Day 13)
 load · validate · plot        returns · risk · drawdown     signals · positions · review     unseen strategy + unseen ticker
```

## Cumulative assessment plan

- **Every day:** Section G automated checks (visible) + unseen variants with different
  dates/tickers/values (hard-coding cannot pass) + Section H explain-in-your-own-words.
- **Retrieval practice:** closing questions revisit earlier days at widening intervals
  (Day *n* tests Days *n−1*, *n−3*, *n−6* where possible).
- **Milestones (Days 4, 7, 9):** code-quality, tests and documentation review before moving on.
- **Definition of a finished day:** the checklist at the end of the notebook — watching the video is item 1 of 7, not the finish line.

## Honest limitations of the source video (addressed, not hidden)

1. **2022 code vs today's `yfinance`:** recent `yfinance` versions can return
   MultiIndex columns and handle `Adj Close`/`auto_adjust` differently. Day 01
   teaches you to *inspect and adapt* instead of copy-pasting.
2. **No transaction costs, slippage or survivorship discussion** in the video's
   backtest. Introduced as labelled programme additions on Days 9 and 13.
3. **API keys shown on screen** in the video. Day 12 teaches the opposite habit.
4. A vectorised SMA backtest is a *research sketch*, not a trading system.
   The capstone report must say what it ignores.
