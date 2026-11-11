"""Build Day 08 notebook. Instructor utility."""
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

# Day 08 — Your First Vectorised Backtest: SMA Crossover vs Buy & Hold

| | |
|---|---|
| **Video segment** | **01:57:00–02:11:40** — *Creating and Backtesting Strategies* · *Comparison to buy and hold* ([watch](https://www.youtube.com/watch?v=GDMkkmkJigw&t=7020s)) |
| **Estimated study time** | **2.5–3 hours** |
| **Prerequisites** | Week 1 complete (Milestone 2 passed): log returns & SMA warm-up (Day 06), wealth & running-peak drawdowns (Day 07) |
| **Data** | `df_long` — **synthetic** ~10-year (2,520 business days) equity-index history (`data/sample/long_spy_like.csv`, deterministic seed 808) |
| **Expected deliverable** | **P2.1:** `run_crossover_backtest(prices, fast=50, slow=100)` + `$1` equity-curve chart vs buy-and-hold + 5-bullet backtest verdict |

## Learning objectives — by the end of today you will be able to

1. **Translate** a trailing SMA crossover rule into a causal **position** series via `position = signal.shift(1)` and prove on a single crossover bar why omitting `.shift(1)` trades on prices that have not happened yet.
2. **Compute** vectorised long/short (`±1`) strategy log returns and benchmark buy-and-hold log returns over the **exact same post-warm-up tradable window**.
3. **Reconcile** additive log returns with the video's *"absolute performance of $1"* curve (`exp(cumsum(r))`) and terminal return (`exp(sum(r)) − 1`).
4. **Diagnose** a look-ahead backtest containing an unshifted signal and a `center=True` window, explaining why a smooth equity curve cannot self-report leakage.
5. **Evaluate** a strategy against buy-and-hold across total return, annualised volatility (`√252`), max drawdown (anchored at `$1.00` starting capital), and trade count.

> ⚠️ **Research sketch, not a trading system.** Everything in Week 2 is an educational vectorised simulation on synthetic data — zero slippage, zero borrow fees today (costs arrive Day 09), and zero financial advice.
""")

md(r"""
---
## SECTION B — Video Learning · 01:57:00–02:11:40

**Pre-watch questions** (write your guesses before pressing play; revisit in Section H):
1. `SMA50` crosses above `SMA100` using **Monday's closing price**. What is the earliest return bar you could honestly earn in that new long position — Monday's return (`Fri→Mon`) or Tuesday's return (`Mon→Tue`)?
2. If your position on day `t` is `-1` (short) and the stock's log return on day `t` is `-0.03`, what is `-1 × (-0.03)` — and why does that product work cleanly in log space?
3. On a 2,520-day series with `SMA100`, why is it unfair to compare 2,420 days of strategy returns against all 2,519 days of buy-and-hold returns?
4. When the presenter plots *"absolute performance of $1"* using `.cumsum().apply(np.exp)`, what initial value does `$1` grow from, and why might a long/short `±1` strategy lag buy-and-hold on a rising index like SPY?

| Time | Chapter | Watch for |
|---|---|---|
| 01:57:00 | Creating and Backtesting Strategies | Computing `SMA_S` (50) and `SMA_L` (100/200) on SPY, `dropna()` on warm-up rows, `np.where(SMA_S > SMA_L, 1, -1)`, and the **1-day shift** before multiplying by log returns |
| 02:05:30 | Comparison to buy and hold | Summing log returns → `np.exp(...)`, plotting cumulative wealth of `$1` (`creturns` vs `cstrategy`), and noticing what shorting an upward-drifting index costs you |
| 02:11:40 | ⛔ STOP | *Long bias Strategy* & Challenge 3 are Day 09 |

Fallback: [01:57:00](https://www.youtube.com/watch?v=GDMkkmkJigw&t=7020s) · [02:05:30](https://www.youtube.com/watch?v=GDMkkmkJigw&t=7530s) · [stop at 02:11:40](https://www.youtube.com/watch?v=GDMkkmkJigw&t=7900s)
""")

code(r"""
# ▶️ SECTION B (code) - 01:57:00 to 02:11:40
from IPython.display import YouTubeVideo, display
display(YouTubeVideo("GDMkkmkJigw", start=7020, end=7900, width=800, height=450))
print("Fallback: https://www.youtube.com/watch?v=GDMkkmkJigw&t=7020s  (stop at 02:11:40)")
""")

md(r"""✍️ **My 3-bullet summary (edit me):** - · - · -""")

md(r"""
---
## SECTION C — Concept Notes

### C1. Signal at `t` → Position at `t+1`: the `.shift(1)` law
Day 06 drew a bright red line between a **measurement** (`signal_t`, computed after the market closes on day `t` using prices up to `Close_t`) and a **tradable holding** (`position_t`, what you actually held *during* day `t`, from `Close_{t-1}` to `Close_t`). Because `Close_t` is both the final ingredient of `SMA_t` *and* the numerator of `r_t = ln(Close_t / Close_{t-1})`, multiplying `signal_t * r_t` claims you knew `Close_t` at `Close_{t-1}` — **look-ahead bias**. Shifting by one bar fixes causality:
`position_t = signal_{t-1}` (`signal.shift(1)`), so today's return `r_t` is multiplied by *yesterday's* closing decision.

### C2. Video v1 long/short (`±1`) + plateau hygiene `[programme precision]`
In the video's first backtest, after warm-up rows are dropped, `SMA_fast > SMA_slow` maps to `+1` (long) and `<=` maps to `-1` (short) via `np.where(sma_f > sma_s, 1, -1)`. On continuous market prices `sma_f == sma_s` almost never occurs, **except** on flat/halted price plateaus (or synthetic edge-case tests). Declaring `-1` (short!) when a stock is completely flat at `100.0` manufactures a phantom short trade out of nothing. Our explicit three-state rule matches the video on every trending bar while staying sane on ties and warm-up:
- `sma_fast > sma_slow` → `+1` (long)
- `sma_fast < sma_slow` → `-1` (short)
- `sma_fast == sma_slow` or either SMA is `NaN` → `0` (flat / no edge)

### C3. Warm-up and the first tradable bar (`index[slow:]`)
With `min_periods=window` (Day 06), `SMA(slow)` is `NaN` on rows `0 .. slow−2` (`slow − 1` bars) and prints its **first valid value** at row `slow − 1` (the `slow`-th price). That close gives your first valid crossover decision `signal.iloc[slow - 1]`. After `.shift(1)`, the **first tradable return bar** is row `slow` (`prices.index[slow]`), leaving `len(prices) - slow` tradable days. Both the strategy AND passive buy-and-hold must be evaluated on `prices.index[slow:]` — starting `$1.00` together at `Close[slow - 1]`.

### C4. Log-return accounting & implied wealth (`peak >= 1.0`)
With position `p_t ∈ {-1, 0, +1}` and asset log return `r_t = ln(P_t / P_{t-1})`, the strategy's single-day log return is `s_t = p_t * r_t` (`[approximation note]`: exact for `p_t ∈ {0, +1}`; for `p_t = -1`, `-ln(P_t/P_{t-1})` mirrors the log move symmetrically, standard in vectorised research sketches like the video's). Cumulative wealth of `$1.00` is `W_t = exp(cumsum(s_t))` and terminal total return is `exp(sum(s_t)) - 1`. For max drawdown of implied wealth starting from `$1.00`, anchor the running peak at `1.0` (`peak = W.cummax().clip(lower=1.0)`): if day 1 loses `-20%` (`W_1 = 0.80`), your drawdown from starting capital is `-20%`, not `0%`.

### C5. Counting trades (`trade_count`)
Before the backtest begins, an investor holds **cash (`0`)**. Defining prior position as `prev = positions.shift(1, fill_value=0)`, a **trade event** occurs on every bar where `positions != prev` (`|Δposition| > 0`):
- Opening from cash (`0 → +1` or `0 → -1`): `|Δ| = 1` → **1 trade event**.
- Reversing long↔short on a crossover (`+1 → -1` or `-1 → +1`): `|Δ| = 2` on one bar → **1 rebalance event** in `trade_count` (Day 09 will charge `2×` unit transaction cost on `|Δ| = 2`).
- Holding steady (`+1 → +1`, `0 → 0`, `-1 → -1`): `|Δ| = 0` → **0 trades**.
""")

code(WEEK2_SETUP_CODE)

md(r"""
---
## SECTION D — Guided Exploration

### D1 — Catch the missing `.shift(1)` on an 8-day toy path
**Predict:** prices sit at `100` for 4 days, jump to `120` on day 5 (pushing `SMA2 > SMA4` *at day 5's close*), then stay at `120`. How much of day 5's `+20%` jump should an honest crossover strategy capture — all of it, half, or `0%`?
""")
md(r"""✍️ **D1 prediction (edit me):** """)
code(r"""
# D1 - single jump bar: shifted (causal) vs unshifted (clairvoyant)
toy = pd.Series([100., 100., 100., 100., 120., 120., 120., 120.],
                index=pd.bdate_range("2022-01-03", periods=8), name="Close")
f2, s4 = toy.rolling(2, min_periods=2).mean(), toy.rolling(4, min_periods=4).mean()
sig = pd.Series(np.where(f2 > s4, 1, np.where(f2 < s4, -1, 0)), index=toy.index)
lr = np.log(toy / toy.shift(1))
tbl = pd.DataFrame({
    "Close": toy, "SMA2": f2, "SMA4": s4, "signal_t": sig,
    "pos_t (shifted)": sig.shift(1, fill_value=0),
    "log_ret_t": lr.round(4),
    "honest_ret": (sig.shift(1, fill_value=0) * lr).round(4),
    "cheating_ret": (sig * lr).round(4),
})
print(tbl.iloc[3:])
# TODO(modify): append a crash bar 90.0 on day 9. Who magically dodges (or shorts!) the crash on the day it happens?
""")
md(r"""
✍️ **D1 observed (edit me):** on 2022-01-07 (the jump to 120), `signal_t` turned `1` *because* of the 120 close, while `pos_t` was still `___`. The unshifted column stole a `_____` log return that required knowing 120 before 120 printed.

### D2 — Why `df_long` exists, and why equal start dates matter
**Predict:** `df_long` has `2,520` rows and we run `SMA50` vs `SMA100`. On which 0-based row does `SMA100` first exist, on which row does the *first tradable strategy return* land, and how many tradable days remain?
""")
md(r"""✍️ **D2 prediction (edit me):** """)
code(r"""
# D2 - warm-up geometry on 10y synthetic index history
p_long = df_long["Close"]
sma50 = p_long.rolling(50, min_periods=50).mean()
sma100 = p_long.rolling(100, min_periods=100).mean()
first_sma_idx = p_long.index.get_loc(sma100.first_valid_index())
print("total bars:", len(p_long), "| first valid SMA100 row:", first_sma_idx,
      f"({sma100.first_valid_index().date()}) | first tradable row:", first_sma_idx + 1,
      f"({p_long.index[first_sma_idx + 1].date()}) | tradable days:", len(p_long) - 100)

lr_all = np.log(p_long / p_long.shift(1))
print("Buy&Hold total return (all 2,519 return bars) :", round(float(np.exp(lr_all.dropna().sum()) - 1), 4))
print("Buy&Hold total return (aligned 2,420 bars)    :", round(float(np.exp(lr_all.iloc[100:].sum()) - 1), 4))
# TODO(modify): repeat for slow=200 (Week 1's 252-row `df` would leave only 52 tradable bars!). How many bars on `df_long`?
""")
md(r"""
✍️ **D2 observed (edit me):** `SMA(slow)` needs `____` prices, so its first signal sits at index `____` and its first tradable return sits at index `____`. Comparing unaligned windows changes Buy&Hold's reported return by `____` without a single trade changing.

### D3 — The video's "$1 absolute performance" chart on `df_long`
**Predict:** `df_long` drifts upward overall (`180 → 416`, synthetic SPY-like). Will a strategy that goes **short (`-1`)** whenever `SMA50 < SMA100` beat or trail passive buy-and-hold over the full decade? Why?
""")
md(r"""✍️ **D3 prediction (edit me):** """)
code(r"""
# D3 - preview of the video's $1 wealth comparison (long/short +-1 vs buy & hold)
sig_ls = pd.Series(np.where(sma50 > sma100, 1, np.where(sma50 < sma100, -1, 0)), index=p_long.index)
pos_ls = sig_ls.shift(1, fill_value=0).iloc[100:]
bh_lr = lr_all.iloc[100:]
st_lr = pos_ls * bh_lr
wealth_df = pd.DataFrame({
    "Buy & Hold ($1)": np.exp(bh_lr.cumsum()),
    "SMA 50/100 Long/Short ($1)": np.exp(st_lr.cumsum()),
})
ax = wealth_df.plot(figsize=(10, 4), title="D3: Absolute performance of $1 on df_long (SYNTHETIC ~10y)")
ax.set_ylabel("Wealth ($)"); plt.tight_layout(); plt.show()
print("Terminal $1 ->", wealth_df.iloc[-1].round(3).to_dict())
# TODO(modify): inspect `pos_ls.value_counts()`. How many days was the strategy short (-1), and what was `bh_lr[pos_ls == -1].sum()`?
""")
md(r"""✍️ **D3 observed (edit me):** Buy & Hold turned `$1` into `$____`; Long/Short turned `$1` into `$____`. While `pos == -1`, the market's cumulative log return was `____`, so shorting during rebounds cost the strategy `____` (Day 09 tests going flat `0` instead).""")

md(r"""
---
## SECTION E — Independent Practice

### Exercise 1 — Basic: vectorised long/short crossover returns
""")
code(r"""
def strategy_log_returns(prices, fast=50, slow=100):
    '''Return a Series named "strategy_log_returns" of tradable daily log returns for
    the v1 long/short SMA crossover on `prices` (1D positive price Series):
      - SMA(fast) and SMA(slow) use min_periods=window (Day 06).
      - Signal at t: +1 if SMA(fast) > SMA(slow), -1 if SMA(fast) < SMA(slow),
        0 on ties (SMA(fast) == SMA(slow)) or warm-up NaNs.
      - Position at t = signal shifted by +1 bar (causal execution).
      - Slice result to the tradable window `prices.index[slow:]` (every bar has a
        valid prior-day SMA(slow) signal; length == len(prices) - slow).
    Validation: `prices` must be a Series with no NaNs and all values > 0; `fast` and
    `slow` ints with 1 <= fast < slow and len(prices) > slow; else raise ValueError.
    Caller's `prices` unmodified.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Validate inputs first (reject `bool` windows, `fast >= slow`, non-positive/NaN prices, or `len(prices) <= slow`). Then compute log returns, both trailing SMAs, the 3-state signal, shift by 1 bar, multiply, and slice `.iloc[slow:]`.</details>
<details><summary>Hint 2 — approach</summary>Check `isinstance(fast, (int, np.integer)) and not isinstance(fast, bool)` (same for `slow`). For the 3-state signal on valid bars: `np.where(sma_f > sma_s, 1, np.where(sma_f < sma_s, -1, 0))` masked to `0` where `sma_s.isna()`.</details>
<details><summary>Hint 3 — clue</summary>`pos = sig.shift(1, fill_value=0)`; `out = (pos * lr).iloc[slow:]`; `out.name = "strategy_log_returns"`. On a completely flat price series, `sma_f == sma_s` everywhere, so `out` is all `0.0`.</details>

### Exercise 2 — Modification: benchmark log returns on an identical window
""")
code(r"""
def buy_and_hold_log_returns(prices, align_to=None):
    '''Return a Series named "benchmark_log_returns" of ln(P_t / P_{t-1}) for `prices`.
      - If `align_to` is None: return all valid log returns (dropping row 0's NaN).
      - If `align_to` is a Series, DataFrame, or Index: align/slice the log returns
        to `align_to`'s exact index (raising ValueError if `align_to` is empty or
        requests dates missing/NaN in `prices`'s valid log returns).
    Validation: `prices` must be a 1D Series with no NaNs, all values > 0, and
    len(prices) >= 2; else ValueError.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>C3's equal-start-date rule packaged as a function: `bh = buy_and_hold_log_returns(prices, align_to=strat)` guarantees benchmark and strategy cover the exact same dates.</details>
<details><summary>Hint 2 — approach</summary>Compute `lr = np.log(prices / prices.shift(1)).dropna()`. Extract target index via `align_to.index if hasattr(align_to, "index") else pd.Index(align_to)` when `align_to is not None`.</details>
<details><summary>Hint 3 — clue</summary>Check `len(target_idx) > 0` and `target_idx.isin(lr.index).all()` before `lr.loc[target_idx]` so out-of-range or row-0 NaN dates raise `ValueError` loudly.</details>

### Exercise 3 — Debugging: unshifted backtest (+ a `center=True` poison pill)

Run the buggy cell, write a complete diagnosis of **both** look-ahead bugs and why the equity curve looks believable anyway, then implement `positions_from_signal(signal)`.
""")
code(r"""
# --- BUGGY / CHEATING BACKTEST (study; do not edit) ---
def backtest_mirage(prices, fast=10, slow=30):
    lr = np.log(prices / prices.shift(1))
    sma_f = prices.rolling(fast, center=True).mean()          # bug A
    sma_s = prices.rolling(slow).mean()
    sig = pd.Series(np.where(sma_f > sma_s, 1, -1), index=prices.index)
    strat = sig * lr                                          # bug B (no shift!)
    return np.exp(strat.dropna().cumsum())

_mirage = backtest_mirage(df["Close"])
print("Mirage terminal $1 wealth on 1y DEMO:", round(float(_mirage.iloc[-1]), 3),
      "| actual Buy&Hold:", round(float(df["Close"].iloc[-1] / df["Close"].iloc[0]), 3))
""")
md(r"""✍️ **Diagnosis (edit me):** Bug A (`center=True`): leaks `____` future bars into `sma_f` at date `t`. Bug B (`sig * lr`): multiplies date-`t` close signal by `____`. You CANNOT spot either bug just by glancing at the plotted equity curve because `____`.""")
code(r"""
def positions_from_signal(signal):
    '''Convert a 1D signal Series (entries in {-1, 0, 1}, NaNs treated as 0) into
    causal positions via a +1 bar shift:
      - Row 0 becomes 0 (no prior signal before the series begins).
      - Output has integer dtype (`int`), index preserved, name="position".
      - Empty Series or any non-NaN value outside {-1, 0, 1} -> ValueError.
      - Input unmodified.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Validate non-empty `pd.Series`, clean NaNs to `0`, verify every value sits in `{-1, 0, 1}` (reject floats like `0.5` or `2`), then `.shift(1, fill_value=0).astype(int)`.</details>
<details><summary>Hint 2 — clue</summary>`clean = signal.fillna(0)`; check `set(np.unique(clean)).issubset({-1, 0, 1})` (and reject boolean dtype so `True`/`False` masks aren't silently accepted if you want strictness — or ensure numeric values in `{-1, 0, 1}`). Set `.name = "position"`.</details>

### Exercise 4 — Independent: `performance_summary` from log returns
""")
code(r"""
def performance_summary(log_returns, periods_per_year=252):
    '''Summarise a 1D Series of daily log returns into a dict:
      - "total_return":   float, exp(sum(r)) - 1
      - "annualised_vol": float, sample std (ddof=1) of r * sqrt(periods_per_year)
      - "max_drawdown":   float (<= 0.0), min of (wealth / peak - 1) where
                          wealth = exp(cumsum(r)) and peak = wealth.cummax().clip(lower=1.0)
                          (anchored at $1.00 initial capital, C4)
      - "n_days":         int, count of valid (non-NaN) return observations
    Drop NaNs first; fewer than 2 valid observations or periods_per_year <= 0 -> ValueError.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Week 1's risk numbers adapted to log-return space: `exp(r.sum()) - 1` for total return, `r.std(ddof=1) * sqrt(periods_per_year)` for vol, and Day 07's running-peak drawdown with `$1.00` starting capital.</details>
<details><summary>Hint 2 — clue</summary>`r = log_returns.dropna().astype(float)`. Check `len(r) >= 2`. On a zero-return series (`[0.0, 0.0, 0.0]`), `total_return == 0.0`, `annualised_vol == 0.0`, `max_drawdown == 0.0` — make sure nothing divides by zero.</details>

### Exercise 5 — Transfer: `trade_count`
""")
code(r"""
def trade_count(positions):
    '''Count rebalance/trade events in a 1D integer-valued position Series:
    number of bars where position != previous bar's position, assuming cash (`0`)
    before bar 0 (`prev = positions.shift(1, fill_value=0)`).
      - Note (C5): a direct reversal (+1 -> -1 or -1 -> +1) on a single bar is
        counted as 1 trade event here (Day 09 weights it by |delta| = 2 for costs).
      - Empty Series or any NaN in `positions` -> ValueError. Return Python `int`.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Compare `positions` against `positions.shift(1, fill_value=0)`. Count how many bars have `|delta| > 0` and cast to `int`.</details>
<details><summary>Hint 2 — clue</summary>Check `isinstance(positions, pd.Series)`, `len(positions) > 0`, and `not positions.isna().any()`. Test mentally: `[0, 0, 0]` → `0`; `[1, 1, 1]` → `1` (initial entry from cash); `[0, 1, 1, -1, 0]` → `3`.</details>
""")

md(r"""
---
## SECTION F — Daily Mini-Project · P2.1 Crossover Backtest vs Buy & Hold

### Specification — `run_crossover_backtest(prices, fast=50, slow=100)`
Compose today's functions into a single research runner returning `(results, summary)`:
- **`results`** (`pd.DataFrame`, indexed by tradable dates `prices.index[slow:]`, zero NaNs), columns in exact order:
  `["Close", f"SMA{fast}", f"SMA{slow}", "signal", "position", "benchmark_log_returns", "strategy_log_returns", "benchmark_wealth", "strategy_wealth"]`
  where `signal` is the unshifted close signal on that date, `position` is the causal holding active *during* that date (`signal` from the previous close), and both `*_wealth` columns start from `$1.00` via `exp(cumsum(...))`.
- **`summary`** (`dict`) with keys `"strategy"` and `"benchmark"`, each holding `performance_summary(...)` augmented with `"trades": int` (`trade_count(results["position"])` for strategy; `1` for passive buy-and-hold's single entry).

**Then:** run on `df_long["Close"]` (`fast=50, slow=100`), save `results` to `data/processed/day08_sma_backtest.csv`, plot both `$1` wealth curves (labelled, Day-03 standard), and write your 5-bullet verdict below.
""")
code(r"""
def run_crossover_backtest(prices, fast=50, slow=100):
    '''See Section F specification. Returns (results_df, summary_dict).'''
    # TODO
    pass
""")
code(r"""
# SECTION F (apply)
try:
    bt_df, bt_sum = run_crossover_backtest(df_long["Close"], fast=50, slow=100)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    bt_df.to_csv(PROCESSED / "day08_sma_backtest.csv")
    print(pd.DataFrame(bt_sum).T.round(4))
    ax = bt_df[["benchmark_wealth", "strategy_wealth"]].plot(
        figsize=(10, 4), title="P2.1: SMA 50/100 Long/Short vs Buy & Hold ($1 wealth, synthetic ~10y)"
    )
    ax.set_ylabel("Wealth of $1"); plt.tight_layout(); plt.show()
except Exception as exc:
    print("backtest not ready yet:", type(exc).__name__, exc)
""")
md(r"""
✍️ **P2.1 5-bullet backtest verdict (edit me):**
- **Window & parameters:** …
- **Return comparison (`$1` terminal & %):** …
- **Volatility & max drawdown comparison:** …
- **Trade frequency & short-side behaviour:** …
- **Hypothesis for Day 09 (what happens if `-1` becomes `0`?):** …

---
## SECTION G — Automated Assessment
""")
code(r"""
# SECTION G - harness + visible checks (self-contained)
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

_idx8 = pd.bdate_range("2022-01-03", periods=8)
_jump = pd.Series([100., 100., 100., 100., 120., 120., 120., 120.], index=_idx8, name="Close")
_trend = pd.Series([100., 102., 105., 109., 114., 110., 104., 98., 93., 90.],
                   index=pd.bdate_range("2022-02-01", periods=10), name="Close")
_flat = pd.Series([50.0] * 12, index=pd.bdate_range("2022-03-01", periods=12), name="Close")

check("Ex1 trap: crossover jump bar earns 0 on jump day (position shifted!)", lambda: (
    lambda r: len(r) == 4 and r.index[0] == _idx8[4] and abs(float(r.iloc[0])) < 1e-12)(
        strategy_log_returns(_jump, fast=2, slow=4)))
check("Ex1 earns long return AFTER crossover, flips short after downturn", lambda: (
    lambda r: r.name == "strategy_log_returns" and len(r) == 6
    and abs(float(r.iloc[0]) - np.log(114.0 / 109.0)) < 1e-12
    and float(r.iloc[-1]) > 0)(strategy_log_returns(_trend, fast=2, slow=4)))
check("Ex1 flat-price series -> all 0.0 strategy returns, no crash", lambda: (
    lambda r: len(r) == 7 and np.allclose(r.values, 0.0))(strategy_log_returns(_flat, fast=2, slow=5)))
check("Ex1 validation: fast>=slow, non-positive, too-short -> ValueError", lambda: (
    raises(ValueError, lambda: strategy_log_returns(_trend, fast=4, slow=4))
    and raises(ValueError, lambda: strategy_log_returns(_trend, fast=5, slow=3))
    and raises(ValueError, lambda: strategy_log_returns(pd.Series([10., 0., 12., 14., 15.], index=_idx8[:5]), 2, 3))
    and raises(ValueError, lambda: strategy_log_returns(_trend.iloc[:4], fast=2, slow=4))))

check("Ex2 buy & hold aligns exactly to strategy's first tradable date", lambda: (
    lambda s: (lambda b: b.index.equals(s.index) and b.name == "benchmark_log_returns"
               and abs(float(np.exp(b.sum()) - 1) - (_trend.iloc[-1] / _trend.iloc[3] - 1)) < 1e-12)(
        buy_and_hold_log_returns(_trend, align_to=s)))(strategy_log_returns(_trend, fast=2, slow=4)))
check("Ex2 align_to=None returns full n-1 log returns; missing date -> ValueError", lambda: (
    len(buy_and_hold_log_returns(_trend)) == len(_trend) - 1
    and raises(ValueError, lambda: buy_and_hold_log_returns(_trend, align_to=pd.bdate_range("2019-01-01", periods=3)))))

check("Ex3 positions_from_signal shifts +1, row 0 is 0, int dtype, input intact", lambda: (
    lambda sig: (lambda p: list(p.values) == [0, 1, 1, -1] and p.dtype.kind in "iu"
                 and p.name == "position" and list(sig.values) == [1, 1, -1, 1])(
        positions_from_signal(sig)))(pd.Series([1, 1, -1, 1], index=_idx8[:4])))
check("Ex3 NaN in signal -> 0; out-of-range value -> ValueError", lambda: (
    list(positions_from_signal(pd.Series([np.nan, 1.0, -1.0], index=_idx8[:3])).values) == [0, 0, 1]
    and raises(ValueError, lambda: positions_from_signal(pd.Series([0, 2, -1])))
    and raises(ValueError, lambda: positions_from_signal(pd.Series([], dtype=float)))))

_known_lr = pd.Series([np.log(0.8), np.log(1.25), np.log(0.9)], index=_idx8[:3])  # wealth: 0.8 -> 1.0 -> 0.9
check("Ex4 performance_summary: total_return, vol, maxDD anchored at $1.00, n_days", lambda: (
    lambda d: abs(d["total_return"] - (-0.10)) < 1e-12
    and abs(d["max_drawdown"] - (-0.20)) < 1e-12
    and abs(d["annualised_vol"] - float(_known_lr.std(ddof=1) * np.sqrt(252))) < 1e-12
    and d["n_days"] == 3)(performance_summary(_known_lr)))
check("Ex4 flat 0.0 log returns -> 0 return, 0 vol, 0 maxDD; <2 obs -> ValueError", lambda: (
    lambda d: d["total_return"] == 0.0 and d["annualised_vol"] == 0.0 and d["max_drawdown"] == 0.0)(
        performance_summary(pd.Series([0.0, 0.0, 0.0, 0.0])))
    and raises(ValueError, lambda: performance_summary(pd.Series([0.01]))))

check("Ex5 trade_count: flat=0, buy&hold=1, reversal=1 event", lambda: (
    trade_count(pd.Series([0, 0, 0])) == 0
    and trade_count(pd.Series([1, 1, 1])) == 1
    and trade_count(pd.Series([0, 1, 1, -1, -1, 0])) == 3))
check("Ex5 trade_count rejects empty or NaN positions", lambda: (
    raises(ValueError, lambda: trade_count(pd.Series([], dtype=int)))
    and raises(ValueError, lambda: trade_count(pd.Series([0.0, np.nan, 1.0])))))

def _proj_ok():
    res, summ = run_crossover_backtest(_trend, fast=2, slow=4)
    exp_cols = ["Close", "SMA2", "SMA4", "signal", "position",
                "benchmark_log_returns", "strategy_log_returns",
                "benchmark_wealth", "strategy_wealth"]
    res_flat, summ_flat = run_crossover_backtest(_flat, fast=2, slow=5)
    return (list(res.columns) == exp_cols and len(res) == 6 and not res.isna().any().any()
            and abs(float(res["strategy_wealth"].iloc[-1]) - 1.0 - summ["strategy"]["total_return"]) < 1e-12
            and abs(float(res["benchmark_wealth"].iloc[-1]) - 1.0 - summ["benchmark"]["total_return"]) < 1e-12
            and summ["strategy"]["n_days"] == summ["benchmark"]["n_days"] == 6
            and summ["benchmark"]["trades"] == 1
            and summ_flat["strategy"]["trades"] == 0 and summ_flat["strategy"]["total_return"] == 0.0)
check("F project: columns, equal windows, wealth reconciliation & flat-series safety", _proj_ok)
print(f"\nSCORE: {sum(RESULTS)}/{len(RESULTS)} visible checks passing")
""")

md(r"""
---
## SECTION H — Knowledge Check

**H1 (Pre-watch #1 revisited)** Walk through a single date `t` where `Close_t` jumps +15% and causes `SMA50` to cross above `SMA100`. State `signal_t`, `position_t`, `position_{t+1}`, and explain in plain English what physical impossibility `signal_t * r_t` assumes. ✍️
**H2 (Pre-watch #3 revisited)** Suppose the first 100 warm-up bars of a sample contained a +25% rally. If you forgot to align `buy_and_hold_log_returns` to `prices.index[100:]`, which leg gets an unfair head start and by how much? ✍️
**H3 Defend** `peak = wealth.cummax().clip(lower=1.0)` inside `performance_summary`: construct a 3-day return vector where omitting `.clip(lower=1.0)` claims `max_drawdown == 0.0` despite losing money. ✍️
**H4 Predict output** `positions = pd.Series([1, 1, -1, 1])`. What does `trade_count(positions)` return, and how many *units* (`|Δposition|`) actually changed hands across all four bars? ✍️
**H5 What-if** Why did our tie rule map `sma_fast == sma_slow` to `0` rather than the video's `-1`? Name one real-world market situation (besides a synthetic constant test) where two SMAs can tie or prices repeat across bars. ✍️
**H6 Bridge to Day 09** On `df_long`, the `±1` crossover trailed buy-and-hold even though it avoided parts of major sell-offs. Using `L_in` (market log return when `pos == +1`) and `L_out` (market log return when `pos == -1`), write the exact algebraic relationship between Buy&Hold (`L_in + L_out`), Long-Only (`L_in`), and Long/Short (`L_in - L_out`). When does Long/Short lose to Long-Only? ✍️
""")

md(r"""
---
## SECTION I — Reflection & Retrieval Practice

### What I learned · Can implement unaided · Still difficult ✍️

### Retrieval — Days 07 (n−1), 06 (n−2), 04 (n−4)
1. **Day 07:** Why does `align_to_calendar` refuse `bfill`, and how is an unshifted backtest position the *same* temporal sin in a different costume?
2. **Day 07:** Running-peak drawdown formula vs the buggy global-max version in one line each.
3. **Day 06:** Convert a cumulative log return of `-0.22314` into a simple percentage return (`exp(x) - 1`). Why did we sum log returns first instead of summing simple returns?
4. **Day 06:** For `SMA(100)` with `min_periods=100`, how many leading `NaN` rows appear, and why does `first_tradable_row` equal `100` rather than `99`?
5. **Day 04:** State the statistical assumption behind multiplying daily return std by `√252` and one market stylized fact that violates it.
""")
code(r"""
def performance_summary_from_memory(log_returns, periods_per_year=252):
    '''Day 08 Ex4 core FROM MEMORY (close Section E above first!):
    return {"total_return", "annualised_vol", "max_drawdown", "n_days"} with $1 peak anchor.'''
    # TODO
    pass

try:
    _r_mem = pd.Series([np.log(0.9), np.log(1.1), 0.0])
    _d_mem = performance_summary_from_memory(_r_mem)
    _ok = (abs(_d_mem["total_return"] - (0.99 - 1.0)) < 1e-12
           and abs(_d_mem["max_drawdown"] - (-0.10)) < 1e-12 and _d_mem["n_days"] == 3)
except Exception as exc:
    _ok = False; print("self-check raised:", type(exc).__name__, exc)
print("performance_summary reimplementation self-check:", "PASS" if _ok else "not yet")
""")
md(r"""
### ✅ Completion checklist
- [ ] Video `01:57:00–02:11:40` watched; D1–D3 predictions written *before* running
- [ ] Ex 1–5 implemented unaided; Ex 3 diagnosis explains both `center=True` and missing `.shift(1)`
- [ ] P2.1 CSV + `$1` wealth chart generated on `df_long`; 5-bullet verdict cites printed numbers
- [ ] Section G 13/13 green after **Kernel → Restart & Run All**
- [ ] Section H6's `L_in / L_out` identity derived (you will use it immediately on Day 09)

**Send back:** Section G score · your H1 shift explanation · your P2.1 5-bullet verdict. Day 09 adds long-only bias, Challenge 3 drawdowns, and transaction costs for **🏁 Milestone 3**.
""")

nb = new_notebook(cells=CELLS)
nb.metadata.update({"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                    "language_info": {"name": "python", "version": "3.11"},
                    "title": "Day 08 - First Vectorised Backtest: SMA Crossover",
                    "source_video": "https://www.youtube.com/watch?v=GDMkkmkJigw (01:57:00-02:11:40)"})
out = ROOT / "notebooks" / "Day_08_First_Vectorised_Backtest_SMA_Crossover.ipynb"
nbformat.write(nb, out); print("wrote", out, "cells=", len(CELLS))
