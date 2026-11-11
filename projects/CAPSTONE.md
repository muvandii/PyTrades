# 🏁 Day 13 Capstone — Unseen Strategy, Unseen Ticker & Honest Critique

> **"A money-losing capstone with honest analysis passes; a 'profitable' one with leakage fails."**

## 1. The Task

Design, implement, backtest, and critically evaluate **one** trend/momentum rule **not
built as the main video strategy**, applied to Day 13's **unseen synthetic ticker**
(`unseen_df`, 2,520 business days, deterministic seed never used in Days 01–12),
using your **`pytrades/`** package (`v0.3`), with **non-zero transaction costs** enabled
and benchmarked against **passive Buy & Hold on the exact same tradable window**.

### Approved non-video strategy families (choose ONE, pre-committed in Day 12 H6)

1. **Price-vs-SMA(200) Trend Filter (long-only):**
   - `signal_t = 1` where `Close_t > sma(Close, window=200)_t`, else `0` (`0` on ties and warm-up rows `0..198`).
   - Causal execution: `position_t = long_only_positions(signal)_t`; tradable window starts at `index[200]`.
2. **Dual EMA Crossover (long-only, e.g. `fast=30, slow=120`):**
   - `signal_t = 1` where `ema(Close, fast)_t > ema(Close, slow)_t`, else `0` (`0` on ties and warm-up rows `0..slow-2`).
   - Reuses or composes `pytrades.strategy.EMACrossoverStrategy` / `pytrades.indicators.ema`; tradable window starts at `index[slow]`.
3. **Donchian Channel Breakout (long-only, e.g. `entry_window=50, exit_window=20`):**
   - Trailing channel bounds from *prior* closes (`hi_t = Close.rolling(entry_window).max().shift(1)` or evaluated at `t` on `Close.shift(1)`): enter `1` when `Close_t > upper_t`, exit to `0` when `Close_t < lower_t`, otherwise hold `signal_{t-1}`; then apply `.shift(1)` from `signal_t` to `position_t`!

## 2. Required Deliverables

1. **Reproducible Capstone Notebook** (`notebooks/Day_13_Capstone_Unseen_Strategy_and_Critique.ipynb`):
   executes cleanly top-to-bottom after **Kernel → Restart & Run All** with zero network calls.
2. **Working `pytrades/` Package (`v0.3`)** imported by the capstone notebook (no copy-pasted duplicate indicator/summary/cost formulas).
3. **Artifacts in `data/processed/`:**
   - `day13_capstone_results.csv` (daily tradable series: Close, signal, position, net log returns, net `$1` wealths)
   - `day13_capstone_summary.csv` (`buy_and_hold` vs `capstone_strategy` across `total_return`, `annualised_vol`, `max_drawdown`, `trades`, `time_in_market`, `n_days`)
4. **Two-Panel Chart (Day-03/07 standard):**
   - Top panel: net `$1` wealth (`capstone_strategy` vs `buy_and_hold`, identical start date, titled & labelled with legend).
   - Bottom panel: underwater drawdown `%` (`$1.00` high-water-mark anchor) for both legs.
5. **1-Page Written Capstone Report** (in Day 13 Section F) covering all five sections:
   - **Method & exact mathematical rule** (signal timestamp vs execution timestamp).
   - **Parameters & selection honesty** (did you keep your Day-12 pre-committed parameters, or tune after seeing `unseen_df`? Disclose honestly!).
   - **Results & cost sensitivity** (citing `day13_capstone_summary.csv` and `capstone_robustness_check` across `5–50 bps`).
   - **At least 4 named limitations / biases** (e.g. single synthetic asset, flat log-space turnover cost model, zero cash yield while flat, close-on-close execution impossibility, parameter/window sensitivity).
   - **"What would break this live"** paragraph ( concrete market & operational mechanisms: gap risk across overnight news, bid-ask spread expansion during crashes, whipsaw bleed in sideways regimes, data feed delays/unadjusted corporate actions).

## 3. Rubric (How Day 13 Is Assessed)

| Dimension | Pass standard | Automatic fail trigger |
|---|---|---|
| **Causal timing (no look-ahead)** | `position = signal.shift(1)` verified; static leakage lint clean (no `shift(-`, `.bfill(`, `center=True`) | Unshifted signal×return, negative shift, backfill, or centred rolling window |
| **Window & cost fairness** | `cost_rate > 0` applied symmetrically; `n_days` identical between strategy & Buy & Hold | Zero costs, charging daily hold fees by mistake, or comparing unequal date spans |
| **Package engineering** | Imports & composes `pytrades` (`data`, `indicators`, `strategy`); zero hidden globals | Duplicating Week-1/2 maths inline while ignoring `pytrades/` |
| **Analytical honesty** | Nuanced trade-off discussion; tuning disclosed; ≥4 concrete limitations + live-failure analysis | Claiming a backtest proves guaranteed live profits, or hiding parameter sweeps |
| **Reproducibility** | Restart & Run All passes 12/12 mechanical checks in Section G | Out-of-order cell state or network/API-key dependency |
