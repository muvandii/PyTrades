# Week 2 Authoring Guide — Days 08–13 (do not lower the Week-1 standard)

> **Status:** Week 1 (Days 01–07) is fully authored and verified. Week 2 is **specified
> here in full but not yet authored**, because compressing 11 complete notebooks into
> one batch would degrade exercises, tests and reference-validation. Author Week 2
> in the three batches named below. Total programme: **13 learning days ≤ 2 weeks**.
>
> Source remains the single video + its official chapters:
> https://www.youtube.com/watch?v=GDMkkmkJigw (see `COURSE_MAP.md`).

## 1. Non-negotiable design system (identical to Days 01–07)

Every Week-2 notebook MUST:
1. Follow **Sections A–I** in order; ~35–45 cells; learning objectives measurable
   (verb + artifact, never "understand X").
2. **Section B:** embed the exact segment with `YouTubeVideo(id, start, end)` (seconds
   below) + timestamped fallback links + 4 pre-watch questions whose answers are
   revisited in Section H. Verify segment content against the transcript *before*
   writing concept notes — never invent video micro-details; flag programme additions.
3. **Section D:** ≥3 predict→run→modify→record experiments, each with an ✍️ prediction
   cell *before* the code cell.
4. **Section E:** exactly 5 exercises in the fixed progression (Basic · Modification ·
   Debugging-with-written-diagnosis · Independent · Transfer), docstring contracts,
   pass-only stubs, 2–3 progressively specific hints each in `<details>` blocks,
   **no solutions in the repo**.
5. **Section F:** one mini-project function (spec table / acceptance criteria /
   artifacts under `data/processed/` or `pytrades/`) composed from that day's exercises.
6. **Section G:** self-contained visible-check harness (PASS/FAIL, never aborts,
   10–20 checks; see Days 03–07 builders for the pattern). Checks must be behavioural
   (values/types/dates/exceptions/round-trips), include unseen-data shapes, and be
   **reference-validated** ( §4 ).
7. **Section H:** 5–6 questions incl. predict-output, defend-your-implementation and
   what-if, plus a bridge question to the next day.
8. **Section I:** reflection + retrieval from days n−1, n−3, n−6 (approximation is fine,
   state the sources) + one from-memory reimplementation with a *gentle* self-check +
   completion checklist + explicit "send back" instructions.
9. Be **standalone** (own setup cell; embed the `_one`/`make_multi` fallback pattern
   from `tools/_day_setup.py`; no reliance on other notebooks' kernel state, and no
   grade depends on network or live APIs).
10. Ship **clean** (no outputs/execution counts) via a `tools/build_dayNN_notebook.py`.

## 2. Data changes required for Week 2 (build these first)

| Asset | Where | Why |
|---|---|---|
| **Long synthetic history (~10y, 2 520 business days)** `_long(seed, …)` in Day 08's builder + `data/sample/long_spy_like.csv` | Days 08–11, 13 | SMA50/100/200 crossovers (the video's SPY strategy) need years, not Week-1's 252 rows. Deterministic seed; plausible drift/vol regime; label synthetic everywhere. |
| **Unseen capstone ticker** (new seed, never used in any example) | Day 13 only | Prevents solution-recall; generate inside Day 13 setup with a seed not printed in earlier days. |
| **Mock API payloads** (JSON strings: success / rate-limit note / renamed columns / empty) | Day 12 setup cell | API skills must be testable with no key and no network (Week-1 rule). |
| `pytrades/` package skeleton | created *by the learner* Days 10–11 (author only its spec/tests) | The graduation from notebooks to importable code is the lesson. |

## 3. Per-day authoring specifications

### Day 08 — First vectorised backtest: SMA crossover
- **Segment:** 01:57:00–02:11:40 (start 7020, end 7900). *Creating and Backtesting Strategies · Comparison to buy and hold.*
- **Objectives:** build signal→**position = signal.shift(1)**→strategy log returns; reconcile `exp(sum(log))` wealth; benchmark vs buy-&-hold on return, annualised vol, max drawdown (reuse Week-1 semantics).
- **Concepts to land:** signal vs position (Day 06 preview cashed in); why same-day execution on same-day close is look-ahead; warm-up/`dropna` discipline; equal-start-date benchmarking; "absolute performance of $1" panel from the video.
- **Exercises (spec exactly):**
  1. `strategy_log_returns(prices, fast, slow)` — log returns × shifted crossover position (long/short ±1 per video v1: `np.where(sma_f > sma_s, 1, -1)` then shift).
  2. `buy_and_hold_log_returns(prices)` aligned to the strategy's first tradable date.
  3. **Debug:** supplied backtest with **no shift** (and a `center=True` Easter egg) — written diagnosis (inflated results, why undetectable from equity curve alone), then fix into `positions_from_signal(signal)` (shift, first row 0, dtype int).
  4. `performance_summary(log_returns)` → dict {total_return via exp(sum)−1, annualised_vol √252, max_drawdown of implied wealth, n_days}.
  5. **Transfer:** `trade_count(positions)` (count |Δposition|>0 events; long→short flip counts how? — author must state & test).
- **Project P2.1:** `run_crossover_backtest(prices, fast=50, slow=100)` → (results DataFrame with price/SMAs/position/strategy+benchmark log returns/wealths, summary dict for both legs). Apply to long synthetic history; equity-curve plot vs buy-&-hold; 5-bullet verdict.
- **Known traps to test:** unshifted positions (compare position on crossover date), NaN-shift first row, performance recomputed from first tradable (not warm-up) date, flat-price series (no trades, zero returns, no crash).
- **Retrieval sources:** Days 07 (drawdown), 06 (signal-not-shifted), 04 (vol). **Reimplementation:** `performance_summary` core from memory.

### Day 09 — Long-only bias & honest comparison · 🏁 Milestone 3
- **Segment:** 02:11:40–02:16:30 (7900–8190). *Long bias Strategy · Challenge 3.* (Short video, long thought — size the day to 2.5–3 h of analysis.)
- **Objectives:** derive long-only (1/0) from long/short (±1); re-run the 3-way comparison on identical windows; execute Challenge 3 (drawdowns across the variants); argue "better, for whom" from return ∧ vol ∧ drawdown ∧ trade count.
- **Programme addition (label it):** flat **transaction cost per position change** (e.g. `cost_rate × |Δposition|` subtracted on change days, in log-return space as an approximation — say it's an approximation). The video omits costs; Week-2 honesty requires them.
- **Exercises:** 1. `long_only_positions(signal)` mapping −1→0 (shift discipline retained). 2. `apply_transaction_costs(strategy_log_returns, positions, cost_rate)`. 3. **Debug:** costs applied *every day held* instead of on changes, plus a version charging on the pre-shift signal — diagnose both. 4. `compare_strategies(prices, fast, slow, cost_rate=0.0)` → summary table [buy&hold, long/short, long-only] × Day-08 metrics + trades. 5. **Transfer:** `cost_breakeven_scan(...)` — over a grid of cost_rates find where long-only's total return crosses buy-&-hold's (return frame of totals; no plotting required in the function).
- **Project / 🏁 Milestone 3:** 1-page verdict (in-notebook markdown + `projects/MILESTONE_3.md` to be authored alongside, mirroring M1/M2 style): recommendation, evidence table, costs sensitivity, explicit limitations (single asset, one window, no slippage model beyond flat cost, parameter cherry-picking risk 50/100, survivorship only-n/a-synthetic).
- **Traps to test:** cost only on change bars (flat position ⇒ zero cost), flip ±1 costs 2× unit or stated alternative, identical comparison windows across legs.
- **Retrieval:** Days 08, 06, 03. **Reimplementation:** `positions_from_signal` from memory.

### Day 10 — Functions: a reusable strategy tester
- **Segment:** 02:16:30–02:26:30 (8190–8790). *Creating a function* (his `test_strategy(stock, start, end, SMA pair)`).
- **Objectives:** parameterise (ticker-agnostic: prices in, results out — our offline adaptation of his download-inside design, discuss the trade-off explicitly); docstring + input validation; zero globals; harvest Week-1/2 functions into **`pytrades/`** `strategy.py` + `indicators.py` + `data.py` created by the learner from their own notebook implementations.
- **Exercises:** 1. Refactor brief → `test_strategy(prices, fast, slow, long_only=True, cost_rate=0.0)` returning Day-09 summary row. 2. **Modification:** add `initial_capital` scaling of wealth output. 3. **Debug:** function secretly reading a global `data` frame (works in notebook, dies on import) — diagnose via a *fresh-kernel import test*. 4. Write the three `pytrades/` modules (author supplies `tests/` spec in Section G: subprocess-free import + smoke calls). 5. **Transfer:** parameter sweep `sweep_sma_pairs(prices, pairs)` returning ranked summaries + a written overfitting warning.
- **Project P2.2:** `pytrades/` v0.1 committed; notebook *imports* from it for its Section F rerun (proof of extraction). Author `projects/` note updating the Milestone-2 function inventory into package layout.
- **Traps to test:** mutation of caller's prices, import-from-clean-kernel (nbconvert run covers this), sweep must not select "best" silently (function returns table only).
- **Retrieval:** Days 09, 07, 04. **Reimplementation:** `sma` + `log_returns` signatures from memory inside the package (closed notebooks).

### Day 11 — Classes: a strategy object you can import (+ Challenge 4)
- **Segment:** 02:26:30–02:51:00 (8790–10260). *Creating a class · Importing and Using a Class · Challenge 4.*
- **Objectives:** state where a class earns its keep (parameters + cached results + lifecycle: load→compute→summarise→plot) vs plain functions; implement `SMACrossoverStrategy` with `__init__(prices, fast, slow, long_only, cost_rate)`, `.run()`, `.summary()`, `.plot()` (returns Axes, Day-03 standard); import it from `pytrades.strategy` in a *separate fresh notebook cell run*.
- **Exercises:** 1. Minimal class skeleton with validated `__init__` (fast<slow etc.). 2. Add `.run()` caching (second call reuses; changing `.fast` invalidates — author decides & tests the invalidation contract). 3. **Debug:** mutable-default + shared-state class (results leak between instances) — diagnose & repair. 4. Full class delegating maths to Day-10 functions (no duplicated formulas — test that class summary == function summary on same inputs). 5. **Transfer / Challenge 4:** subclass or parameterise for an **EMA-crossover** variant reusing the base machinery; written justification of inheritance vs composition choice.
- **Project P2.3:** `pytrades` v0.2 with class; demonstration notebook section importing *only* from the package; CHANGELOG-style note.
- **Traps to test:** two instances independence, `summary()` before `run()` raises a *clear* error (or auto-runs — one contract, stated), equality with function pipeline.
- **Retrieval:** Days 10, 08, 05. **Reimplementation:** sketch class API from memory (signatures only) + justify one method in prose.

### Day 12 — APIs & data you don't control
- **Segment:** 02:51:00–03:00:48 (10260–10848). *API · Working with API (Alpha Vantage).* Transcript-verified beats: `pip install alpha_vantage`, `TimeSeries(key=..., output_format="pandas")`, `get_daily(...)`, columns arriving vendor-named (`4. close` style), vendor/price-quality remarks (Polygon, Norgate).
- **Hard rules for authoring this day:** **no live key is ever required or graded**; do NOT reproduce the video's on-screen key anywhere; keys are read from environment/`.env` [programme addition]; all Section G tests run on **canned payloads** (§2).
- **Objectives:** parse a vendor daily-bars payload into exactly the Day-01 validated frame contract; map vendor column names; handle (a) rate-limit/info payload, (b) empty series, (c) missing field — each with a distinct, loud exception; explain why vendor choice changes backtest results (adjustments, survivorship, granularity).
- **Exercises:** 1. `parse_av_daily(payload: dict)` → clean OHLCV frame (renames, dtypes, DatetimeIndex sorted; reuse Day-01-style validation inline). 2. `normalise_vendor_columns(df, mapping)` generic renamer (unknown extra columns dropped *loudly* via return-report? author decides: choose raise-on-missing-required, ignore-extras, and test both). 3. **Debug:** key hard-coded in source + silent `except: pass` returning empty frame — diagnose (security + silent-failure), repair pattern. 4. `fetch_daily(symbol, api_key=None, _get=None)` with injectable transport for tests (dependency-injection lite). 5. **Transfer:** adapter for a *second* canned vendor shape (list-of-rows JSON) proving the internal contract is vendor-indep.
- **Project P2.4:** `pytrades/data.py` gains the adapter; Section F runs the *full Day-08 backtest* through API-sourced (canned) data end-to-end.
- **Traps to test:** rate-limit dict must not become an empty "successful" frame; string numbers parsed to floats; descending vendor order sorted ascending.
- **Retrieval:** Days 01 (validation contract!), 08, 06. **Reimplementation:** Day-01 validation checks list from memory.

### Day 13 — Capstone (no new video)
- **Segment:** re-watch 01:57:00–02:16:30 (7020–8190) only, embedded as one cell.
- **Task (author the full spec + rubric in the notebook and in `projects/CAPSTONE.md`):**
  design & test a strategy **not in the video** — choose one: price-vs-SMA200 filter (long-only),
  EMA crossover, or Donchian-style breakout (rolling max/min from Day 06 rolling skills) —
  on the **unseen synthetic ticker**, using only `pytrades/` code, with transaction costs on,
  benchmarked vs buy-&-hold on an identical window.
- **Deliverables:** runnable capstone notebook (Restart-&-Run-All), results table
  (return ∧ vol ∧ maxDD ∧ trades ∧ time-in-market), equity + drawdown charts to Day-03/07
  standards, and a 1-page report: method, parameters & how chosen (honest about any tuning),
  results, at least 4 named limitations/biases, "what would break this live" paragraph.
- **Assessment is rubric-based** (correctness of position timing; cost handling; no look-ahead;
  window discipline; quality of critique; reproducibility). Section G of Day 13 checks only
  *mechanical* contracts (functions exist in `pytrades/`, no `shift(-`/`.bfill(`/`center=True`
  strings in learner code cells — a lint the author may implement, clearly disclosed to the
  learner upfront), not profitability. **A money-losing capstone with honest analysis passes;
  a "profitable" one with leakage fails.** Print that sentence in the notebook.

## 4. Mandatory validation protocol per notebook (the Week-1 gauntlet)

1. `nbformat.validate` passes; cell census shows Sections A–I + ≥5 Hint blocks.
2. Execute a **copy** top-to-bottom (`nbconvert --execute --allow-errors`, pytrades kernel):
   **zero cell errors**; Section G prints a score (low with stubs, never crashes).
3. Write a **throwaway reference implementation in /tmp** (never in the repo), exec the
   notebook's *actual* Section G cell against it ⇒ **100% of visible checks pass**.
   Fix notebook/tests — never "adjust" by weakening a check to match a bug (Weeks 1
   precedents: Day-04 partial-string `.loc` fix; Day-06 plateau-equality fix).
4. Learner copy has **no outputs / execution counts**; generated artifacts during
   validation are removed; `git status` shows only intended files.
5. Update `README.md` progress table + `COURSE_MAP.md` if any scope shifted.
6. Commit per batch with the verification numbers in the message, push the session branch.

## 5. Batching & sequencing

| Batch | Author | Then ask learner for |
|---|---|---|
| **W2-A** | Day 08 + Day 09 (+ long-history data + `projects/MILESTONE_3.md`) | Day-08 shift explanation (H) · Day-09 verdict draft |
| **W2-B** | Day 10 + Day 11 (package specs/tests) | clean-kernel import proof · class-vs-function justification |
| **W2-C** | Day 12 + Day 13 (+ `projects/CAPSTONE.md`, canned payloads) | capstone topic choice before they start Day 13 |

Say **"produce the next"** to trigger W2-A. If the learner's returned work changes any
assumption (pace, sticking points), adapt exercise volume — never the validation gauntlet.

## 6. Explicitly out of scope (do not sneak in)
Live trading/APIs that place orders · real-money advice · leverage/options ·
ML-based signals · performance promises. Everything Week 2 backtests stays a
vectorised *research sketch*; Day 11's class is for research organisation, not execution.
