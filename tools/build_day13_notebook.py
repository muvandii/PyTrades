"""Build Day 13 Capstone notebook. Instructor utility."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _day_setup import WEEK2_SETUP_CODE
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

ROOT = Path(__file__).resolve().parents[1]
CELLS = []
def md(t): CELLS.append(new_markdown_cell(t.strip("\n")))
def code(t): CELLS.append(new_code_cell(t.strip("\n")))

md(r"""
## SECTION A — Learning Mission

# Day 13 — 🏁 Capstone: Unseen Strategy, Unseen Ticker & Honest Research Critique

| | |
|---|---|
| **Video segment** | **Re-watch `01:57:00–02:16:30` only** — *Creating and Backtesting Strategies · Long bias · Challenge 3* ([watch](https://www.youtube.com/watch?v=GDMkkmkJigw&t=7020s)) |
| **Estimated study time** | **3–4 hours** (independent design, backtest, robustness checks & 1-page critique) |
| **Prerequisites** | Days 01–12 green; `pytrades` v0.3 (`data`, `indicators`, `strategy`) complete; capstone family pre-committed in Day 12 H6 |
| **Data** | `unseen_df` — **unseen synthetic ~10-year ticker (`UNSEEN`)** generated in setup with a fresh seed never used in Days 01–12 |
| **Expected deliverable** | **🏁 Capstone (`projects/CAPSTONE.md`):** reproducible notebook + `pytrades/` imports + results & robustness CSVs + equity/drawdown chart + 1-page critical report |

> ### 📜 Golden Rule of This Capstone
> **A money-losing capstone with honest analysis passes; a "profitable" one with leakage fails.**

## Learning objectives — by the end of today you will be able to

1. **Design and implement** a causal trend/breakout strategy **not shown as the main video strategy** (`Price > SMA200` filter, `EMA crossover`, or `Donchian breakout`) with strict warm-up and `.shift(1)` execution discipline.
2. **Compose** your `pytrades/` package (`data`, `indicators`, `strategy`) on an unseen 10-year price history without duplicating Week 1–2 formulas or introducing notebook globals.
3. **Audit code mechanically** for look-ahead leakage (`shift(-...)`, `.bfill(`, `method="bfill"`, `center=True`) and prove causal timing on synthetic jump/flat probes.
4. **Evaluate** net-of-cost performance (`cost_rate > 0`) against an equal-window Buy & Hold benchmark across return, annualised vol, max drawdown, trade count, time in market, and friction sensitivity.
5. **Author a 1-page research critique** defending methodology, disclosing any parameter tuning, naming ≥4 concrete biases/limitations, and explaining what would break the strategy in live trading.
""")

md(r"""
---
## SECTION B — Video Review · Re-watch 01:57:00–02:16:30 Only

There is **no new video material** today — you finished the entire 3-hour tutorial yesterday.
Re-watch the 19.5-minute backtesting core (`01:57:00–02:16:30`) once with a **reviewer's eye**, checking four questions:

1. Where in the presenter's workflow are `SMA_S` and `SMA_L` chosen (`50` and `100`/`200`), and does he ever test them on an unseen ticker without re-picking?
2. Which real-world frictions are `0.0` in his code that your capstone **must** include or critique?
3. When he switches `-1 → 0` (*Long bias*), how does `time_in_market` change, and why must your report print `time_in_market` alongside `total_return` and `max_drawdown`?
4. If your pre-committed strategy loses `-5%` on `UNSEEN` while Buy & Hold loses `-23%` with twice the drawdown, is that a failed capstone or an instructive result?

Fallback: [01:57:00](https://www.youtube.com/watch?v=GDMkkmkJigw&t=7020s) · [02:11:40 Long bias](https://www.youtube.com/watch?v=GDMkkmkJigw&t=7900s) · [stop at 02:16:30](https://www.youtube.com/watch?v=GDMkkmkJigw&t=8190s)
""")

code(r"""
# LINT-EXEMPT: instructor video embed cell
# ▶️ SECTION B (code) - re-watch 01:57:00 to 02:16:30 only
from IPython.display import YouTubeVideo, display
display(YouTubeVideo("GDMkkmkJigw", start=7020, end=8190, width=800, height=450))
print("Fallback: https://www.youtube.com/watch?v=GDMkkmkJigw&t=7020s  (stop at 02:16:30)")
""")

md(r"""✍️ **My pre-registered capstone plan (copy from Day 12 H6 BEFORE inspecting `unseen_df`):** Strategy family = `____` · Parameters = `____` · Baseline `cost_rate` = `0.001` (10 bps)""")

md(r"""
---
## SECTION C — Capstone Specification & Rubric Notes

### C1. Approved strategy menu (pick ONE — full spec in `projects/CAPSTONE.md`)
1. **Option A — Price-vs-SMA(200) Trend Filter (long-only):** `signal_t = 1` when `Close_t > sma(Close, window)_t`, else `0` (`0` on warm-up rows `0..window-2` and ties `Close == SMA`). Tradable window starts at `index[window]`.
2. **Option B — Dual EMA Crossover (long-only, e.g. `fast=30, slow=120`):** `signal_t = 1` when `ema(Close, fast)_t > ema(Close, slow)_t`, else `0` (`0` on warm-up `0..slow-2` and ties). Tradable window starts at `index[slow]`.
3. **Option C — Donchian Channel Breakout (long-only, e.g. `entry_window=50, exit_window=20`):** compare `Close_t` to trailing prior-bar channel `upper_t = Close.shift(1).rolling(entry_window, min_periods=entry_window).max()` and `lower_t = Close.shift(1).rolling(exit_window, min_periods=exit_window).min()` (`1` above upper, `0` below lower, else hold `signal_{t-1}`; `0` during warm-up `0..max(entry,exit)`).

In **every** option, `signal_t` uses data up to `Close_t` only, and `position_t = long_only_positions(signal)_t` (`.shift(1)`) executes over `t → t+1`.

### C2. Why `UNSEEN` uses a brand-new seed
Days 08–11 reused `df_long` (`seed=808`), so by Day 11 you already knew `df_long` rose `+118%` and favoured `80/200` in 2020–2024. `unseen_df` below is generated with a fresh multi-regime process (`UNSEEN`) you have never seen. Resist editing your pre-committed parameters after seeing the chart — if you compare a second parameter set as a sensitivity check, **label it post-hoc** in your report!

### C3. Upfront disclosure: how Section G marks Day 13
Section G grades **research integrity and mechanical contracts**, never profitability:
1. `pytrades` v0.3 imports cleanly (`validate_ohlcv`, `fetch_daily`, `sma`, `ema`, `log_returns`, `long_only_positions`, `apply_transaction_costs`, `performance_summary`, `trade_count`, `SMACrossoverStrategy`, `EMACrossoverStrategy`).
2. **Static anti-leakage lint:** your learner functions and non-exempt notebook code cells are scanned for forbidden look-ahead constructs (`shift(-`, `.bfill(`, `method="bfill"`, `method='bfill'`, `center=True`).
3. **Behavioural causality:** step-jump probe earns `0.0` on the jump bar; flat series yields `0` trades; `cost_rate <= 0` is rejected; strategy and Buy & Hold share identical `n_days`; **a money-losing path passes 100% of checks**.
""")

code(WEEK2_SETUP_CODE + r"""
# LINT-EXEMPT: instructor setup cell generating unseen capstone ticker
import importlib, inspect, re
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

def _make_unseen_capstone_ohlcv(seed=202613, start_price=64.0, n=2520):
    '''Deterministic unseen ~10-year synthetic single-stock OHLCV for Day 13 Capstone.'''
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2015-01-02", periods=n, freq="B")
    regimes = [
        (500,  0.00060, 0.0120),
        (420, -0.00055, 0.0165),
        (520,  0.00075, 0.0110),
        (360, -0.00095, 0.0190),
        (720,  0.00055, 0.0125),
    ]
    lr = (np.concatenate([rng.normal(mu, sig, k) for k, mu, sig in regimes])
          if sum(k for k, _, _ in regimes) == n else rng.normal(0.0, 0.014, size=n))
    lr[0] = 0.0
    close = start_price * np.exp(np.cumsum(lr))
    open_ = np.empty(n); open_[0] = start_price
    open_[1:] = close[:-1] * np.exp(rng.normal(0, 0.0022, size=n - 1))
    intraday = np.abs(rng.normal(0, 0.0055, size=n))
    out = pd.DataFrame({
        "Open": np.round(open_, 4),
        "High": np.round(np.maximum(open_, close) * (1 + intraday), 4),
        "Low": np.round(np.minimum(open_, close) * (1 - intraday), 4),
        "Close": np.round(close, 4),
        "Adj Close": np.round(close, 4),
        "Volume": rng.integers(900_000, 5_500_000, size=n),
    }, index=dates)
    out.index.name = "Date"
    return out

unseen_df = _make_unseen_capstone_ohlcv()
print("UNSEEN capstone ticker ready:", unseen_df.shape,
      f"{unseen_df.index.min().date()}..{unseen_df.index.max().date()}")
""")

md(r"""
---
## SECTION D — Guided Exploration (Data Audit & Toy Signal Mechanics)

### D1 — Audit `unseen_df` & understand the Buy & Hold baseline
**Predict:** every single-stock path is riskier than a diversified index (`df_long` had `~18%` vol and `-38%` maxDD). Before plotting `unseen_df["Close"]`, predict whether a single cyclical stock with `1.1%–1.9%` daily vol regimes can suffer a deeper drawdown than `-50%`.
""")
md(r"""✍️ **D1 prediction (edit me):** """)
code(r"""
# LINT-EXEMPT: instructor guided exploration D1
p_u = unseen_df["Close"]
lr_u = np.log(p_u / p_u.shift(1)).dropna()
w_u = np.exp(lr_u.cumsum())
dd_u = (w_u / w_u.cummax().clip(lower=1.0) - 1.0)
print("UNSEEN start->end Close:", float(p_u.iloc[0]), "->", float(p_u.iloc[-1]))
print("Full-span Buy&Hold | total_return:", round(float(w_u.iloc[-1] - 1), 4),
      "| ann_vol:", round(float(lr_u.std() * np.sqrt(252)), 4),
      "| maxDD:", round(float(dd_u.min()), 4))
ax = p_u.plot(figsize=(10, 3.5), title="UNSEEN Synthetic Close (2015-2024) - Do NOT re-pick parameters from this plot!")
ax.set_ylabel("Close ($)"); plt.tight_layout(); plt.show()
# TODO(modify): locate the peak date and trough date of `dd_u.min()` (Day 07 skill). How long did UNSEEN spend underwater?
""")
md(r"""
✍️ **D1 observed (edit me):** passive Buy & Hold on `UNSEEN` returned `____%` with a brutal `____%` max drawdown! Even a strategy finishing near `0%` net return here protects massive capital relative to passive holding — **provided** it did so without look-ahead.

### D2 — Compare the 3 candidate rules on a **toy** wave (no `unseen_df` peeking!)
**Predict:** on a 20-day toy wave (`100` → `130` → `95`), which triggers more transitions when daily closes oscillate around a trend line: `Close > SMA(window)` (raw price crossing one smooth line) or `EMA(fast) > EMA(slow)` (two smoothed lines)?
""")
md(r"""✍️ **D2 prediction (edit me):** """)
code(r"""
# LINT-EXEMPT: instructor guided exploration D2 on toy wave
toy_wave = pd.Series(
    [100, 102, 101, 105, 103, 108, 106, 112, 109, 115, 111, 107, 109, 103, 105, 99, 101, 96, 95, 94],
    index=pd.bdate_range("2023-01-02", periods=20), dtype=float
)
sma6 = toy_wave.rolling(6, min_periods=6).mean()
sig_filter = pd.Series(np.where(toy_wave > sma6, 1, 0), index=toy_wave.index).where(sma6.notna(), 0)
e3, e6 = toy_wave.ewm(span=3, min_periods=3).mean(), toy_wave.ewm(span=6, min_periods=6).mean()
sig_ema = pd.Series(np.where(e3 > e6, 1, 0), index=toy_wave.index).where(e6.notna(), 0)
print("Price > SMA6 changes:", int((sig_filter.diff().fillna(0).abs() > 0).sum()), "| signal:", list(sig_filter.iloc[5:].values))
print("EMA3 > EMA6  changes:", int((sig_ema.diff().fillna(0).abs() > 0).sum()), "| signal:", list(sig_ema.iloc[5:].values))
# TODO(modify): compute `hi6 = toy_wave.shift(1).rolling(6, min_periods=6).max()`. Why did we `.shift(1)` BEFORE `.rolling(6).max()`?
""")
md(r"""
✍️ **D2 observed (edit me):** `Close > SMA` flipped `___` times vs `EMA3 > EMA6` `___` times because raw `Close` is noisier than a smoothed fast average (whipsaw risk when `Close` hugs `SMA200`!).

### D3 — Preview the static look-ahead linter
**Predict:** should a linter flag `# never use shift(-1)` inside a Python `# comment`, or only inside executable code?
""")
md(r"""✍️ **D3 prediction (edit me):** """)
code(r"""
# LINT-EXEMPT: instructor guided exploration D3 demonstrating comment stripping
sample_clean = '''
def ok_fn(s):
    # Note: we never use shift(-1) or center=True!
    return s.shift(1, fill_value=0)
'''
sample_dirty = '''
def bad_fn(s):
    x = s.rolling(10, center=True).mean()
    return x.bfill().shift(-1)
'''
def _strip_comments(src):
    return "\n".join(line.split("#", 1)[0] for line in src.splitlines())

print("Clean after comment strip:", repr(_strip_comments(sample_clean).strip()))
print("Dirty contains 'center=True'?:", "center=True" in _strip_comments(sample_dirty))
# TODO(modify): check `fillna(method='bfill')` as well as `.bfill(` — both spell backfill!
""")
md(r"""✍️ **D3 observed (edit me):** stripping `# ...` comments first avoids false alarms on documentation while catching `shift(-`, `.bfill(`, `method="bfill"`, and `center=True` in executable lines.""")

md(r"""
---
## SECTION E — Capstone Implementation Scaffolding

### Exercise 1 — Basic: `capstone_signal` + `capstone_warmup_bars` (your chosen non-video rule)
""")
code(r"""
# Set CAPSTONE_WARMUP to your chosen strategy's warm-up bar count so `prices.index[CAPSTONE_WARMUP:]`
# is the exact first tradable return bar (e.g. 200 for SMA200 filter, 120 for EMA 30/120, 51 for Donchian 50/20).
CAPSTONE_WARMUP = 200   # edit to match your pre-committed strategy if needed (>= 5)

def capstone_signal(prices, **params):
    '''Compute your chosen NON-VIDEO causal long-only signal Series in {0, 1} on `prices`:
      - Must work when called with 1 positional argument `capstone_signal(prices)`
        (using sensible default window(s) small enough to run on >= `min_len` bars when
        overridden via `params`, OR adaptive/configurable `window` — accept an optional
        `window=None` / `fast=None, slow=None` override in `**params` so Section G can
        test short 20-bar probes via `capstone_signal(probe, window=5)`!).
      - Specifically: if `window` is passed in `params` (an int >= 2), scale/use `window`
        as the slow/lookback horizon (e.g. `SMA(window)`, `EMA(max(1, window//2), window)`,
        or `Donchian(window, max(1, window//2))`) so short synthetic unit tests can
        probe causality! When `params` is empty, use your full capstone defaults.
      - Rows during warm-up and ties on flat-price series MUST be `0`.
      - Returns int Series in {0, 1} with `index == prices.index`, `name="signal"`,
        unshifted (`.shift(1)` happens in `long_only_positions`!).
      - Empty/NaN/non-positive `prices` -> ValueError. Input unmodified.'''
    # TODO (compose pytrades.indicators functions!)
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Import `sma` / `ema` from `pytrades.indicators`. Supporting an optional `window` keyword in `**params` (defaulting to `CAPSTONE_WARMUP`, e.g. `w = params.get("window", CAPSTONE_WARMUP)`) lets Section G test your exact signal logic on 12-row jump/flat probes while Section F runs your full 200-bar (or 120-bar) capstone on `unseen_df`!</details>
<details><summary>Hint 2 — clue</summary>Example structure for Option A (`Price > SMA`): `w = int(params.get("window", CAPSTONE_WARMUP))`; compute `ma = sma(prices, w)`; `sig = pd.Series(np.where(prices > ma, 1, 0), index=prices.index).where(ma.notna(), 0).astype(int)`; `sig.name = "signal"`. Notice on flat `[100., 100., ...]`, `prices > ma` is `False` everywhere → all `0`s!</details>

### Exercise 2 — Modification: `capstone_metrics` (`pytrades` summary + `time_in_market`)
""")
code(r"""
def capstone_metrics(net_log_returns, positions, periods_per_year=252):
    '''Compose `pytrades.strategy.performance_summary` and `pytrades.strategy.trade_count`
    to return a dict with exact keys:
      {"total_return": float, "annualised_vol": float, "max_drawdown": float,
       "trades": int, "time_in_market": float, "n_days": int}
    where `time_in_market` is the fraction (`0.0 .. 1.0`) of bars with `positions != 0`.
    Mismatched indices, NaNs in `positions`, or `< 2` valid returns -> ValueError.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — clue</summary>Validate `isinstance(net_log_returns, pd.Series)` and `isinstance(positions, pd.Series)` with `positions.index.equals(net_log_returns.index)` and `not positions.isna().any()`; call `ps = performance_summary(net_log_returns, periods_per_year)` and `tc = trade_count(positions)`; add `"time_in_market": float((positions != 0).mean())`.</details>

### Exercise 3 — Debugging: diagnose a leaky breakout & implement `lint_for_lookahead`

Study `leaky_donchian_backtest`, diagnose all three bugs in prose, then implement the static linter `lint_for_lookahead(source_code)` used by Section G.
""")
code(r"""
# LINT-EXEMPT: instructor buggy anti-example (study; do not edit)
def leaky_donchian_backtest(prices, window=20):
    upper = prices.rolling(window, center=True).max()             # bug 1
    sig = (prices >= upper).astype(int).replace(0, np.nan).bfill().fillna(0)  # bug 2
    ret = sig * np.log(prices / prices.shift(-1))                 # bug 3
    return ret
""")
md(r"""✍️ **Diagnosis (edit me):** Bug 1 (`center=True`): `____`. Bug 2 (`.bfill()`): pulls future `1`s backward into `____`. Bug 3 (`prices.shift(-1)` + unshifted `sig`): `____`.""")
code(r"""
# LINT-EXEMPT: linter definition cell (docstring & regexes name the forbidden tokens)
def lint_for_lookahead(source_code):
    '''Static look-ahead linter for Python source strings (ignores `#` comments):
    Strip `# ...` comments per line, then return a sorted list of distinct violation
    tags present in executable code from:
      - "negative_shift"   if `shift(-` (ignoring whitespace like `shift( -`) appears
      - "bfill"            if `.bfill(` or `method="bfill"` or `method='bfill'` appears
      - "centered_window"  if `center=True` (ignoring whitespace around `=`) appears
    Clean code returns `[]`. Non-str `source_code` -> ValueError.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Strip `#` comments line-by-line (`line.split("#", 1)[0]`), join back, and test three small regexes (`r"shift\s*\(\s*-"`, `r"(\.bfill\s*\(|method\s*=\s*['\"]bfill['\"])"`, `r"center\s*=\s*True"`).</details>
<details><summary>Hint 2 — clue</summary>Return `sorted(found_set)` so output order is deterministic regardless of check order.</details>

### Exercise 4 — Independent: `run_capstone` (using `pytrades/`, costs mandatory!)
""")
code(r"""
def run_capstone(prices, cost_rate=0.001, window=None):
    '''Execute your capstone backtest on 1D positive `prices` Series using `pytrades/`:
      - `cost_rate` MUST be strictly positive (`> 0`, non-bool) -> else raise ValueError
        (zero-cost backtests are disallowed in the capstone!).
      - Determine lookback `w = CAPSTONE_WARMUP if window is None else int(window)`
        (`1 <= w < len(prices) - 1`, else ValueError).
      - Compute `sig = capstone_signal(prices)` (if `window is None`) else
        `capstone_signal(prices, window=w)`; convert to causal positions via
        `pytrades.strategy.long_only_positions(sig)`; slice tradable window
        `idx = prices.index[w:]` (`len(idx) >= 2`).
      - Apply `pytrades.strategy.apply_transaction_costs(..., cost_rate=cost_rate)`
        symmetrically to BOTH `capstone_strategy` (`pos * lr`) and `buy_and_hold`
        (`pos_bh = pd.Series(1, index=idx)`).
      - Return `(results_df, summary_df)`:
        * `results_df` (indexed by `idx`, zero NaNs) has exact columns:
          ["Close", "signal", "position", "benchmark_log_returns",
           "strategy_log_returns", "benchmark_wealth", "strategy_wealth"]
        * `summary_df` (indexed by ["buy_and_hold", "capstone_strategy"]) has exact columns:
          ["total_return", "annualised_vol", "max_drawdown", "trades", "time_in_market", "n_days"].'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Every piece already exists in `pytrades.indicators`, `pytrades.strategy`, and Ex 1–2! Notice `cost_rate <= 0` raises `ValueError`: capstone rules forbid frictionless fantasy runs.</details>
<details><summary>Hint 2 — clue</summary>Verify `summary_df.loc["buy_and_hold", "n_days"] == summary_df.loc["capstone_strategy", "n_days"] == len(results_df)` and `abs(results_df["strategy_wealth"].iloc[-1] - 1.0 - summary_df.loc["capstone_strategy", "total_return"]) < 1e-12`.</details>

### Exercise 5 — Transfer: `capstone_robustness_check` (cost-grid stress test)
""")
code(r"""
def capstone_robustness_check(prices, cost_rates=(0.0005, 0.001, 0.0025, 0.005), window=None):
    '''Run `run_capstone(prices, cost_rate=c, window=window)` across strictly positive
    `cost_rates` (sorted ascending) and return a DataFrame (RangeIndex) with exact columns:
      ["cost_rate", "strategy_return", "benchmark_return", "excess_return", "max_drawdown", "trades"]
    Empty `cost_rates` or any rate `<= 0` / bool -> ValueError.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — clue</summary>Validate non-empty `cost_rates` with every rate non-bool `> 0`, sort ascending, call `_, summ = run_capstone(prices, cost_rate=c, window=window)`, and extract the 6 fields per rate.</details>
""")

md(r"""
---
## SECTION F — Capstone Deliverable: Execution, Charts & 1-Page Report
""")
code(r"""
# SECTION F (apply) - run capstone on UNSEEN, save CSV artifacts & render 2-panel chart
print('REMINDER: A money-losing capstone with honest analysis passes; a "profitable" one with leakage fails.')
try:
    cap_res, cap_sum = run_capstone(unseen_df["Close"], cost_rate=0.001)
    cap_rob = capstone_robustness_check(unseen_df["Close"], cost_rates=(0.0005, 0.001, 0.0025, 0.005))
    PROCESSED.mkdir(parents=True, exist_ok=True)
    cap_res.to_csv(PROCESSED / "day13_capstone_results.csv")
    cap_sum.to_csv(PROCESSED / "day13_capstone_summary.csv")
    print("\n=== Capstone Summary on UNSEEN (net of 10 bps) ===")
    print(cap_sum.round(4))
    print("\n=== Transaction-Cost Robustness Grid ===")
    print(cap_rob.round(4).to_string(index=False))

    w_plot = cap_res[["benchmark_wealth", "strategy_wealth"]].rename(
        columns={"benchmark_wealth": "Buy & Hold (net $1)", "strategy_wealth": "Capstone Strategy (net $1)"}
    )
    dd_plot = (w_plot.div(w_plot.cummax().clip(lower=1.0)) - 1.0) * 100.0
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    w_plot.plot(ax=axes[0], title="Day 13 Capstone on UNSEEN: Net $1 Wealth (10 bps cost, synthetic ~10y)")
    axes[0].set_ylabel("Wealth ($)")
    dd_plot.plot(ax=axes[1], title="Underwater Drawdown (%) - $1.00 Initial Capital Anchor")
    axes[1].set_ylabel("Drawdown (%)"); plt.tight_layout(); plt.show()
except Exception as exc:
    print("Capstone pipeline not ready yet:", type(exc).__name__, exc)
""")
md(r"""
✍️ **🏁 1-Page Capstone Research Report (edit all 5 sections; rubric in `projects/CAPSTONE.md`):**

### 1. Strategy Method & Causal Timing Rule
- **Exact mathematical formula for `signal_t` and `position_t`:** …
- **Warm-up bars dropped & exact tradable date span (`n_days`):** …

### 2. Parameters & Selection Honesty
- **Parameters tested:** …
- **Pre-commitment audit:** Did these match Day 12 H6 before plotting `UNSEEN`? *(If you ran any extra parameter experiments, disclose them here — honesty earns full credit; hidden tuning fails review.)* …

### 3. Empirical Results & Cost Sensitivity on `UNSEEN`
- **Return, annualised volatility, max drawdown, trades, and `time_in_market` vs Buy & Hold (`10 bps`):** …
- **Friction sensitivity (`5 bps` → `50 bps` from `cap_rob`):** …

### 4. Named Limitations & Biases (minimum 4 concrete items)
1. **Single-asset / synthetic regime dependence:** …
2. **Transaction-cost & execution simplification:** …
3. **Zero cash return while flat (`1 - time_in_market`):** …
4. **Parameter / horizon sensitivity:** …

### 5. "What Would Break This Live" (operational & market reality)
*(Write one substantive paragraph covering overnight gaps across earnings/macro news, spread widening during panics when signals flip, whipsaw bleed in trendless markets, and corporate-action / feed-delay hazards from Day 12.)*
…

---
## SECTION G — Automated Assessment (Mechanical Integrity & Anti-Leakage Gate)
""")
code(r"""
# LINT-EXEMPT: Section G mechanical harness (checks integrity & causality, NEVER profitability!)
print('A money-losing capstone with honest analysis passes; a "profitable" one with leakage fails.\n')
RESULTS = []
def check(name, fn):
    try: ok = bool(fn()); msg = ""
    except Exception as exc: ok = False; msg = f"{type(exc).__name__}: {exc}"
    RESULTS.append(ok); print(("PASS" if ok else "FAIL"), "-", name, (("| " + msg) if msg else ""))
def raises(t, fn):
    try: fn()
    except t: return True
    except Exception: return False
    return False

def _pkg_v03_ok():
    import pytrades, pytrades.data as d, pytrades.indicators as ind, pytrades.strategy as st
    importlib.reload(d); importlib.reload(ind); importlib.reload(st); importlib.reload(pytrades)
    return all(hasattr(d, k) for k in ("validate_ohlcv", "fetch_daily", "parse_av_daily")) and \
           all(hasattr(ind, k) for k in ("sma", "ema", "log_returns")) and \
           all(hasattr(st, k) for k in ("long_only_positions", "apply_transaction_costs",
                                        "performance_summary", "trade_count",
                                        "SMACrossoverStrategy", "EMACrossoverStrategy"))
check("G1 pytrades v0.3 exports complete data, indicators & strategy surface", _pkg_v03_ok)

check("G2 lint_for_lookahead catches shift(-1), .bfill(), method='bfill' & center=True", lambda: (
    lint_for_lookahead("x = s.shift(1)  # never shift(-1) or center=True") == []
    and lint_for_lookahead("a = s.shift(-1)\nb = s.bfill()\nc = s.rolling(5, center=True).mean()")
        == ["bfill", "centered_window", "negative_shift"]
    and lint_for_lookahead("s.fillna(method='bfill')") == ["bfill"]))

def _self_lint_ok():
    if not callable(lint_for_lookahead): return False
    # 1) Inspect in-memory learner functions
    for fn in (capstone_signal, capstone_metrics, run_capstone, capstone_robustness_check):
        if not callable(fn): return False
        if lint_for_lookahead(inspect.getsource(fn)) != []:
            return False
    # 2) Scan non-exempt code cells of Day 13 notebook on disk (if present)
    nb_file = BASE / "notebooks" / "Day_13_Capstone_Unseen_Strategy_and_Critique.ipynb"
    if nb_file.exists():
        import json as _json
        nb_raw = _json.loads(nb_file.read_text())
        for cell in nb_raw.get("cells", []):
            if cell.get("cell_type") == "code":
                txt = "".join(cell.get("source", []))
                if "# LINT-EXEMPT" not in txt and lint_for_lookahead(txt) != []:
                    return False
    return True
check("G3 learner capstone functions & notebook cells pass static anti-leakage lint", _self_lint_ok)

_jump12 = pd.Series([100.] * 6 + [130.] * 6, index=pd.bdate_range("2023-02-01", periods=12), name="Close")
_flat12 = pd.Series([80.] * 12, index=pd.bdate_range("2023-03-01", periods=12), name="Close")
_lose16 = pd.Series([100., 102., 105., 108., 112., 116., 95., 95., 98., 101., 85., 85., 88., 91., 78., 78.],
                    index=pd.bdate_range("2023-04-03", periods=16), name="Close")

def _sig_ok():
    snap = _jump12.copy()
    s = capstone_signal(_jump12, window=4)
    sf = capstone_signal(_flat12, window=4)
    return (isinstance(s, pd.Series) and s.index.equals(_jump12.index) and s.name == "signal"
            and set(s.unique()) <= {0, 1} and int(s.iloc[:3].sum()) == 0
            and int(sf.sum()) == 0 and _jump12.equals(snap)
            and raises(ValueError, lambda: capstone_signal(pd.Series([10., 0., 12.]), window=2)))
check("G4 capstone_signal: {0,1} values, warm-up 0, flat-series 0, caller unmodified", _sig_ok)

def _metrics_ok():
    idx = pd.bdate_range("2023-01-02", periods=4)
    r = pd.Series([0.01, 0.0, -0.02, 0.0], index=idx)
    pos = pd.Series([1, 0, 1, 0], index=idx)
    m = capstone_metrics(r, pos)
    return (set(m.keys()) == {"total_return", "annualised_vol", "max_drawdown", "trades", "time_in_market", "n_days"}
            and abs(m["time_in_market"] - 0.5) < 1e-12 and m["trades"] == 4 and m["n_days"] == 4)
check("G5 capstone_metrics computes accurate time_in_market, trades & summary fields", _metrics_ok)

def _causal_jump_ok():
    # Jump happens at index 6 (100 -> 130). With window=4, tradable slice starts at index 4:
    # index 4 (100), index 5 (100), index 6 (130 jump!). Before index 6 prices were flat 100,
    # so causal position ON index 6 MUST be 0 (cannot capture the surprise jump on jump day!).
    res, _ = run_capstone(_jump12, cost_rate=0.001, window=4)
    jump_dt = _jump12.index[6]
    return int(res.loc[jump_dt, "position"]) == 0 and abs(float(res.loc[jump_dt, "strategy_log_returns"])) < 1e-12
check("G6 causal timing proof: surprise jump bar has position == 0 on jump day", _causal_jump_ok)

check("G7 run_capstone enforces strictly positive cost_rate (> 0)", lambda: (
    raises(ValueError, lambda: run_capstone(_jump12, cost_rate=0.0, window=4))
    and raises(ValueError, lambda: run_capstone(_jump12, cost_rate=-0.001, window=4))
    and raises(ValueError, lambda: run_capstone(_jump12, cost_rate=True, window=4))))

def _equal_window_ok():
    res, summ = run_capstone(_jump12, cost_rate=0.001, window=4)
    exp_cols = ["Close", "signal", "position", "benchmark_log_returns",
                "strategy_log_returns", "benchmark_wealth", "strategy_wealth"]
    sum_cols = ["total_return", "annualised_vol", "max_drawdown", "trades", "time_in_market", "n_days"]
    return (list(res.columns) == exp_cols and not res.isna().any().any()
            and list(summ.index) == ["buy_and_hold", "capstone_strategy"]
            and list(summ.columns) == sum_cols
            and int(summ.loc["buy_and_hold", "n_days"]) == int(summ.loc["capstone_strategy", "n_days"]) == len(res)
            and abs(float(res["strategy_wealth"].iloc[-1]) - 1.0 - float(summ.loc["capstone_strategy", "total_return"])) < 1e-12)
check("G8 run_capstone schema, equal benchmark window & terminal wealth reconciliation", _equal_window_ok)

def _losing_passes_ok():
    # Whipsaw sawtooth path designed to lose money honestly under trend/breakout rules + costs
    res, summ = run_capstone(_lose16, cost_rate=0.005, window=4)
    return float(summ.loc["capstone_strategy", "total_return"]) < 0.0 and len(res) == 12
check("G9 money-losing whipsaw path passes cleanly (honesty graded, NEVER profitability)", _losing_passes_ok)

check("G10 flat-price series -> 0 capstone trades & 0.0 strategy return", lambda: (
    lambda summ: int(summ.loc["capstone_strategy", "trades"]) == 0
    and abs(float(summ.loc["capstone_strategy", "total_return"])) < 1e-12)(
        run_capstone(_flat12, cost_rate=0.001, window=4)[1]))

def _rob_ok():
    rob = capstone_robustness_check(_lose16, cost_rates=[0.01, 0.001, 0.005], window=4)
    cols = ["cost_rate", "strategy_return", "benchmark_return", "excess_return", "max_drawdown", "trades"]
    return (list(rob.columns) == cols and list(rob["cost_rate"]) == [0.001, 0.005, 0.01]
            and np.allclose(rob["excess_return"], rob["strategy_return"] - rob["benchmark_return"])
            and raises(ValueError, lambda: capstone_robustness_check(_lose16, cost_rates=[0.0, 0.001], window=4)))
check("G11 capstone_robustness_check sorts positive cost grid & computes excess_return", _rob_ok)

def _unseen_full_ok():
    res, summ = run_capstone(unseen_df["Close"], cost_rate=0.001)
    return len(res) > 2000 and int(summ.loc["buy_and_hold", "n_days"]) == len(res)
check("G12 full UNSEEN 10-year capstone run completes cleanly with >2,000 tradable bars", _unseen_full_ok)

print(f"\nSCORE: {sum(RESULTS)}/{len(RESULTS)} visible mechanical checks passing")
print('A money-losing capstone with honest analysis passes; a "profitable" one with leakage fails.')
""")

md(r"""
---
## SECTION H — Capstone Defence Questions

**H1 (Causal proof)** Walk a sceptical reviewer through **one exact date** in `cap_res` where `signal` flipped `0 → 1`: show `signal` and `position` on day `t` and day `t+1`, confirming your code waited until `t+1` to earn the position's return. ✍️
**H2 (Benchmark fairness)** Why does `cap_sum` have fewer than `2,519` `n_days`, and what bias would appear if you compared your `cap_sum.loc["capstone_strategy", "total_return"]` against D1's full-span Buy & Hold number (`2,519` days)? ✍️
**H3 (Whipsaw & cost physics)** Compare `cap_sum`'s `trades` and `time_in_market` against `cap_rob` at `50 bps` (`0.005`). How many basis points of round-trip friction can your chosen rule survive before trailing Buy & Hold — or if it already trails, what drives the drag? ✍️
**H4 (Static vs behavioural testing)** Give an example of a subtle look-ahead bug that **evades** `lint_for_lookahead`'s regex checks (e.g. computing a threshold using `prices.mean()` over the full 10-year sample!) and explain how you ensured your capstone avoided full-sample statistics. ✍️
**H5 (Live reality check)** Suppose you turned this research script on tomorrow with `$10,000` using market-on-close orders triggered at `15:59:55 ET`. Name two concrete reasons your live fills over the next year would diverge from `cap_res["strategy_wealth"]`. ✍️
""")

md(r"""
---
## SECTION I — Programme Reflection & Final Retrieval

### Across Days 01–13: Biggest mindset shift · Proudest module in `pytrades/` · Next skill to build ✍️

### Final Retrieval — Days 12 (n−1), 10 (n−3), 07 (n−6), 01 (Day 1)
1. **Day 12:** Why can an HTTP `200 OK` JSON response still represent a failed API request, and where must API keys live instead of source code?
2. **Day 10–11:** Why did `SMACrossoverStrategy` delegate to `pytrades` functions instead of re-implementing rolling means and drawdown formulas inside the class?
3. **Day 07:** State the difference between volatility and maximum drawdown in terms of investor behaviour.
4. **Day 01:** Why was `"the code ran without throwing an exception"` never accepted as proof of correctness on any single day of this programme?
""")
code(r"""
# Final closed-book synthesis check: given a 1D wealth Series (>= $0), return
# (total_return, max_drawdown_anchored_at_1) in 4 lines FROM MEMORY.
def wealth_audit_from_memory(wealth):
    '''Given `wealth` starting from $1.00 capital (`wealth = exp(cumsum(r))`),
    return `(total_return_float, max_drawdown_float)` anchored at peak >= 1.0.'''
    # TODO
    pass

try:
    _w_m = pd.Series([0.85, 1.10, 0.88, 1.05])
    _tr_m, _dd_m = wealth_audit_from_memory(_w_m)
    _ok = abs(_tr_m - 0.05) < 1e-12 and abs(_dd_m - (-0.20)) < 1e-12
except Exception as exc:
    _ok = False; print("self-check raised:", type(exc).__name__, exc)
print("Final programme synthesis self-check:", "PASS" if _ok else "not yet")
""")
md(r"""
### ✅ Final Capstone & Programme Completion Checklist
- [ ] **All 13 daily notebooks (`Days 01–13`)** pass **Kernel → Restart & Run All** with zero cell errors
- [ ] **`pytrades/` v0.3** committed cleanly (`__init__.py`, `data.py`, `indicators.py`, `strategy.py` — zero secrets, zero notebook globals)
- [ ] **Section G (`12/12`)** green, including static look-ahead lint (`G3`), causal jump test (`G6`), and money-losing whipsaw pass check (`G9`)
- [ ] **Artifacts generated:** `day13_capstone_results.csv`, `day13_capstone_summary.csv`, and 2-panel wealth + underwater drawdown chart
- [ ] **1-page Capstone Report & H1–H5 defence** completed with ≥4 named limitations and live-failure analysis

**Send back for final review:** your Day 13 Section G score (`12/12`), `day13_capstone_summary.csv` table, and your complete 1-page Capstone Report. Congratulations on finishing the 13-day PyTrades engineering programme!
""")

nb = new_notebook(cells=CELLS)
nb.metadata.update({"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                    "language_info": {"name": "python", "version": "3.11"},
                    "title": "Day 13 - Capstone: Unseen Strategy and Honest Critique",
                    "source_video": "https://www.youtube.com/watch?v=GDMkkmkJigw (review 01:57:00-02:16:30)"})
out = ROOT / "notebooks" / "Day_13_Capstone_Unseen_Strategy_and_Critique.ipynb"
nbformat.write(nb, out); print("wrote", out, "cells=", len(CELLS))
