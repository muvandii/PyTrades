"""Build Day 10 notebook. Instructor utility."""
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

# Day 10 — Reusable Strategy Functions & Your `pytrades/` Package (v0.1)

| | |
|---|---|
| **Video segment** | **02:16:30–02:26:30** — *Creating a function* (`test_strategy`) ([watch](https://www.youtube.com/watch?v=GDMkkmkJigw&t=8190s)) |
| **Estimated study time** | **2.5–3.5 hours** (includes extracting Week 1–2 code into `pytrades/` v0.1) |
| **Prerequisites** | Milestone 3 gate passed; function inventory from Milestones 1–2 ready to harvest |
| **Expected deliverable** | **P2.2:** committed `pytrades/` v0.1 package (`data.py`, `indicators.py`, `strategy.py`) + in-sample/out-of-sample SMA sweep report imported from your package |

## Learning objectives — by the end of today you will be able to

1. **Contrast** an IO-coupled function (`test_strategy(ticker, start, end, sma)` that downloads data inside) against a pure **data-in, results-out** function (`test_strategy(prices, fast, slow, ...)`), defending the offline/testability trade-off.
2. **Implement** `test_strategy` and `test_strategy_wealth` (`initial_capital` scaling) with complete docstrings, input validation, and **zero caller mutation**.
3. **Diagnose and eliminate** hidden notebook globals using an isolated-namespace (`clean-import`) test.
4. **Extract** your Week 1–2 functions into an importable **`pytrades/`** package (`__init__.py`, `data.py`, `indicators.py`, `strategy.py`) matching `projects/PACKAGE_SPEC.md`.
5. **Run** a multi-pair `sweep_sma_pairs` study and document why ranking historical parameter grids creates **multiple-testing / overfitting bias**.
""")

md(r"""
---
## SECTION B — Video Learning · 02:16:30–02:26:30

**Pre-watch questions** (write guesses first; checked in Section H):
1. What is the exact difference between a **parameter** (`def f(fast, slow):`) and an **argument** (`f(50, 100)`)?
2. In the video, `test_strategy(stock, start, end, SMA)` calls `yf.download(...)` *inside* the function body. What happens when you call that function 50 times in a parameter sweep — or when Yahoo Finance is offline?
3. A function works on cell `In [42]` of your notebook, you copy-paste it verbatim into `strategy.py`, and `from pytrades.strategy import test_strategy` crashes on the first call with `NameError: name 'data' is not defined`. How did that happen?
4. If you test 30 `(fast, slow)` pairs on one 10-year chart and pick the `#1` row, should you expect that same pair to rank `#1` on the *next* 5 years?

| Time | Chapter | Watch for |
|---|---|---|
| 02:16:30 | Creating a function | Wrapping the notebook's SMA crossover steps into `def test_strategy(stock, start, end, SMA):`, returning terminal performance & outperformance |
| 02:23:00 | Calling with different inputs | Switching tickers and `(fast, slow)` pairs in one line instead of editing 8 cells — and notice the repeated network downloads |
| 02:26:30 | ⛔ STOP | *Creating a class* begins Day 11 |

Fallback: [02:16:30](https://www.youtube.com/watch?v=GDMkkmkJigw&t=8190s) · [02:23:00](https://www.youtube.com/watch?v=GDMkkmkJigw&t=8580s) · [stop at 02:26:30](https://www.youtube.com/watch?v=GDMkkmkJigw&t=8790s)
""")

code(r"""
# ▶️ SECTION B (code) - 02:16:30 to 02:26:30
from IPython.display import YouTubeVideo, display
display(YouTubeVideo("GDMkkmkJigw", start=8190, end=8790, width=800, height=450))
print("Fallback: https://www.youtube.com/watch?v=GDMkkmkJigw&t=8190s  (stop at 02:26:30)")
""")

md(r"""✍️ **My 3-bullet summary (edit me):** - · - · -""")

md(r"""
---
## SECTION C — Concept Notes

### C1. Our offline architectural upgrade: separate IO from maths **[programme adaptation]**
The video bundles **data acquisition** (`yf.download`) and **backtest maths** inside one function `test_strategy(stock, start, end, SMA)`. Convenient for a 10-minute demo; painful in real engineering:
- Testing 25 SMA pairs re-downloads the exact same ticker 25 times (slow, rate-limited).
- Unit tests fail whenever the internet drops or a vendor renames a column (Day 12).
- You cannot feed synthetic edge cases (flat prices, step jumps) into a ticker string.

Our contract separates the two layers cleanly: `pytrades.data` loads/slices prices **once**; `pytrades.strategy.test_strategy(prices, fast, slow, ...)` is a **pure function** (prices in, summary dict out, zero network calls, zero globals, zero side effects).

### C2. The Hidden-Global Trap (why notebook code dies on `import`)
Inside Jupyter, if `def f(fast): return df["Close"].rolling(fast).mean()` omits `prices` from its signature, Python resolves `df` in the notebook's `globals()`. It *appears* to work — until you restart the kernel out of order or move `f` into `pytrades/strategy.py`, where `df` does not exist (`NameError`). Worse: if `df` *does* exist globally in a notebook, calling `f(my_other_stock_fast)` silently ignores your other stock and computes on `df`! Rule: **every value a function reads must arrive through its parameters or explicit module imports.**

### C3. Caller ownership: never mutate inputs
If a caller passes `s = df_long["Close"]` (or a DataFrame) into your function and you attach columns or sort/modify it in place, you corrupt the caller's workspace. Read from Series inputs or `.copy()` before adding columns.

### C4. Graduating to `pytrades/` (`sys.path` & `importlib.reload`)
A Python **package** is a directory (`BASE / "pytrades"`) containing `__init__.py` plus module files (`data.py`, `indicators.py`, `strategy.py`). Two practical Jupyter facts:
1. When Jupyter starts inside `notebooks/`, `Path.cwd()` is `notebooks/`, so add the repo root `str(BASE)` to `sys.path` (setup cell below does this automatically) so `import pytrades` resolves `PyTrades/pytrades/`.
2. Python caches imported modules in `sys.modules`: after editing `pytrades/strategy.py` on disk, call `importlib.reload(pytrades.strategy)` (or Restart Kernel) so the notebook sees your new file rather than the stale cached copy.

### C5. Parameter sweeps: measurement, not magic
`sweep_sma_pairs` automates testing `[(10, 30), (20, 50), (50, 100), (50, 200), ...]`. Notice what our specification **forbids**: the function returns the *entire table* and never silently crowns or trades the top row. Searching `M` parameter pairs on finite noisy history inflates the best in-sample return by pure luck (**multiple-testing / data-snooping bias**).
""")

code(WEEK2_SETUP_CODE + r"""
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))
print("Repo root on sys.path:", str(BASE) in sys.path)
""")

md(r"""
---
## SECTION D — Guided Exploration

### D1 — Pure inputs, keyword clarity, and non-mutation proof
**Predict:** if a function computes `out = prices.copy(); out.iloc[0] = 999999.0` vs `prices.iloc[0] = 999999.0`, what happens to `df_long["Close"].iloc[0]` outside the function in each case?
""")
md(r"""✍️ **D1 prediction (edit me):** """)
code(r"""
# D1 - proving caller non-mutation in 4 lines (the exact pattern Section G uses)
def _polite_scale(prices, capital=10_000.0):
    lr = np.log(prices / prices.shift(1)).fillna(0.0)
    return capital * np.exp(lr.cumsum())

probe = df_long["Close"].iloc[:10].copy()
snapshot = probe.copy()
scaled = _polite_scale(probe, capital=5_000.0)
print("probe unchanged?:", probe.equals(snapshot), "| start wealth:", float(scaled.iloc[0]), "| end:", round(float(scaled.iloc[-1]), 2))
# TODO(modify): call _polite_scale using keyword arguments in reversed order `(capital=2500, prices=probe)`. Same result?
""")
md(r"""
✍️ **D1 observed (edit me):** `probe.equals(snapshot)` is `____`. Keyword arguments bind by `____` rather than position, making `long_only=True, cost_rate=0.001` self-documenting at call sites.

### D2 — Simulate a clean-kernel import without leaving Python
**Predict:** `_bad_sma` below runs fine in this notebook because `df` exists in `globals()`. What exact exception will Python raise when we transplant `_bad_sma`'s bytecode into a clean module namespace containing only `np` and `pd`?
""")
md(r"""✍️ **D2 prediction (edit me):** """)
code(r"""
# D2 - catch a hidden notebook global red-handed
import types

def _bad_sma(window):
    return df["Close"].rolling(window, min_periods=window).mean()   # <-- secretly reads global `df`!

print("In dirty notebook globals, _bad_sma(5).iloc[-1] =", round(float(_bad_sma(5).iloc[-1]), 4))
clean_ns = {"np": np, "pd": pd, "__builtins__": __builtins__}
isolated_fn = types.FunctionType(_bad_sma.__code__, clean_ns, "_bad_sma")
try:
    isolated_fn(5)
except Exception as exc:
    print("In clean module namespace ->", type(exc).__name__, ":", exc)
# TODO(modify): rewrite `_good_sma(prices, window)` so `types.FunctionType(_good_sma.__code__, clean_ns, ...)(df["Close"], 5)` succeeds!
""")
md(r"""
✍️ **D2 observed (edit me):** in the clean namespace `_bad_sma` raised `________` because `df` lived in `________`, not in the function's parameters.

### D3 — In-sample winners vs out-of-sample reality on `df_long`
**Predict:** split `df_long` into `2015–2019` (in-sample) and `2020–2024` (out-of-sample) across 5 SMA pairs `[(15, 40), (20, 60), (50, 100), (50, 150), (80, 200)]`. Will the `#1` pair in `2015–2019` stay `#1` in `2020–2024`?
""")
md(r"""✍️ **D3 prediction (edit me):** """)
code(r"""
# D3 - quick preview of rank instability across halves of the decade
def _quick_lo_ret(p, f, s, cost=0.001):
    lr = np.log(p / p.shift(1)).iloc[s:]
    sf, ss = p.rolling(f, min_periods=f).mean(), p.rolling(s, min_periods=s).mean()
    sig = pd.Series(np.where(sf > ss, 1, 0), index=p.index).where(ss.notna(), 0)
    pos = sig.shift(1, fill_value=0).iloc[s:]
    turn = (pos - pos.shift(1, fill_value=0)).abs()
    return float(np.exp((pos * lr - cost * turn).sum()) - 1)

pairs_demo = [(15, 40), (20, 60), (50, 100), (50, 150), (80, 200)]
p_is = df_long["Close"].loc[:"2019-12-31"]
p_oos = df_long["Close"].loc["2020-01-01":]
cmp = pd.DataFrame([
    {"pair": f"{f}/{s}", "IS_2015_19": _quick_lo_ret(p_is, f, s), "OOS_2020_24": _quick_lo_ret(p_oos, f, s)}
    for f, s in pairs_demo
]).sort_values("IS_2015_19", ascending=False)
cmp["IS_rank"] = range(1, len(cmp) + 1)
cmp["OOS_rank"] = cmp["OOS_2020_24"].rank(ascending=False).astype(int)
print(cmp.to_string(index=False))
# TODO(modify): add `(10, 25)` and `(100, 220)`. Does widening the search grid make the top IS number look better, and does OOS agree?
""")
md(r"""✍️ **D3 observed (edit me):** the `2015–2019` `#1` pair (`____`) ranked `#____` out-of-sample (`2020–2024`). Picking parameters *after* peeking at the whole sample inflates apparent skill because `____`.""")

md(r"""
---
## SECTION E — Independent Practice

### Exercise 1 — Basic: `test_strategy` (pure data-in, dict-out)
""")
code(r"""
def test_strategy(prices, fast=50, slow=100, long_only=True, cost_rate=0.0):
    '''Pure, ticker-agnostic SMA crossover evaluator on 1D positive `prices` Series:
      - Uses Day 08-09 semantics: min_periods=window SMAs; 3-state signal
        (+1 if fast>slow, -1 if fast<slow, 0 on tie/warm-up); causal +1 shift;
        if `long_only=True` clip -1 -> 0; slice tradable window `prices.index[slow:]`;
        subtract `cost_rate * |delta_position|` (initial cash = 0 before `index[slow]`);
        $1.00 peak anchor for max_drawdown.
      - Return dict with exact keys:
        {"fast": int, "slow": int, "long_only": bool, "cost_rate": float,
         "total_return": float, "annualised_vol": float, "max_drawdown": float,
         "trades": int, "n_days": int}.
      - Validation: `prices` non-empty NaN-free positive Series; `fast`, `slow` non-bool
        ints with `1 <= fast < slow < len(prices)`; `long_only` must be a `bool`;
        `cost_rate` non-bool real `>= 0`; else raise ValueError.
      - Caller's `prices` must not be modified.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>One self-contained function unifying Day 08 (`long_only=False`) and Day 09 (`long_only=True` + `cost_rate`). Validate every parameter type up front before touching rolling windows.</details>
<details><summary>Hint 2 — approach</summary>Guard `isinstance(long_only, bool)` explicitly; slice `pos_tradable = pos.iloc[slow:]` and `lr_tradable = lr.iloc[slow:]`; compute turnover on `pos_tradable` relative to `pos_tradable.shift(1, fill_value=0)` so Day 09 `compare_strategies` and `test_strategy` agree to 12 decimal places.</details>
<details><summary>Hint 3 — clue</summary>Cross-check: on `df_long["Close"]` with `fast=50, slow=100, long_only=True, cost_rate=0.001`, `total_return` must match Day 09's `long_only` row (`~0.8010`) and `n_days == 2420`.</details>

### Exercise 2 — Modification: `test_strategy_wealth` (`initial_capital` scaling)
""")
code(r"""
def test_strategy_wealth(prices, fast=50, slow=100, long_only=True,
                         cost_rate=0.0, initial_capital=10_000.0):
    '''Run `test_strategy` AND return `(wealth_df, summary)` scaled to `initial_capital`:
      - `wealth_df`: DataFrame on `prices.index[slow:]` with exact columns
        ["strategy_wealth", "benchmark_wealth"], where each curve equals
        `initial_capital * exp(cumsum(net_log_returns))` (benchmark holds position 1
        on `prices.index[slow:]` and pays day-0 entry `cost_rate` symmetrically).
      - `summary`: dict containing all `test_strategy(...)` keys PLUS:
        "initial_capital": float, "ending_capital": float, "benchmark_ending_capital": float.
      - `initial_capital` must be a non-bool real `> 0`, else ValueError.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Wealth scales linearly with starting capital (`W_t = C_0 * exp(cumsum(r_t))`), while percentage metrics (`total_return`, `annualised_vol`, `max_drawdown`) are scale-invariant!</details>
<details><summary>Hint 2 — clue</summary>Verify `abs(summary["ending_capital"] - initial_capital * (1 + summary["total_return"])) < 1e-9` — a built-in accounting identity check.</details>

### Exercise 3 — Debugging: exorcise hidden globals and in-place mutation

Diagnose all three defects in `secret_global_tester`, then write `standalone_sma_tester(prices, fast=20, slow=50)` so it runs cleanly inside an isolated namespace containing **only** `np`, `pd`, and `__builtins__`.
""")
code(r"""
# --- BUGGY NOTEBOOK FUNCTION (study; do not edit) ---
RUN_HISTORY = []
def secret_global_tester(fast, slow):
    df_long["SMA_f"] = df_long["Close"].rolling(fast).mean()     # defect 1 + defect 2!
    df_long["SMA_s"] = df_long["Close"].rolling(slow).mean()
    sig = np.where(df_long["SMA_f"] > df_long["SMA_s"], 1, 0)
    ret = float(np.exp((pd.Series(sig, index=df_long.index).shift(1) * np.log(df_long["Close"] / df_long["Close"].shift(1))).iloc[slow:].sum()) - 1)
    RUN_HISTORY.append((fast, slow, ret))                        # defect 3!
    return ret

print("Columns of df_long BEFORE calling buggy function:", list(df_long.columns))
""")
md(r"""✍️ **Diagnosis (edit me):** Defect 1 (import killer): reads global `____` instead of a parameter, raising `____` on clean module import. Defect 2 (caller corruption): mutates `df_long` in place by inserting columns `____`. Defect 3 (stateful side-effect): appends to global `____`, so repeated calls leak memory/state across runs.""")
code(r"""
def standalone_sma_tester(prices, fast=20, slow=50):
    '''Self-contained long-only zero-cost SMA crossover total return (float) on
    `prices.index[slow:]`, written using ONLY `prices`, `fast`, `slow`, `np`, and `pd`
    (no calls to outer notebook helpers, no globals, no mutation of `prices`).
    Invalid inputs (`1 <= fast < slow < len(prices)`, positive NaN-free Series) -> ValueError.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Section G transplants `standalone_sma_tester.__code__` into `{"np": np, "pd": pd, "__builtins__": __builtins__}` (just like D2!) and calls it. Even calling another notebook function would fail that ultra-strict isolation check unless it were imported inside a module — so keep all ~10 lines self-contained here.</details>
<details><summary>Hint 2 — clue</summary>Validate `prices`, `fast`, `slow`; compute `lr = np.log(prices / prices.shift(1))`, `sf = prices.rolling(fast, min_periods=fast).mean()`, `ss = prices.rolling(slow, min_periods=slow).mean()`, `sig = pd.Series(np.where(sf > ss, 1, 0), index=prices.index).where(ss.notna(), 0)`, `pos = sig.shift(1, fill_value=0)`, and `float(np.exp((pos * lr).iloc[slow:].sum()) - 1.0)`.</details>

### Exercise 4 — Independent: extract `pytrades/` v0.1 (`data`, `indicators`, `strategy`)

Create the directory `PyTrades/pytrades/` at the repository root following **`projects/PACKAGE_SPEC.md` (v0.1)**:
- `pytrades/__init__.py` (`__version__ = "0.1.0"`)
- `pytrades/data.py` (`validate_ohlcv`, `load_prices`, `slice_prices`)
- `pytrades/indicators.py` (`simple_returns`, `log_returns`, `sma`, `ema`)
- `pytrades/strategy.py` (`positions_from_signal`, `long_only_positions`, `apply_transaction_costs`, `performance_summary`, `trade_count`, `test_strategy`)

Then implement `import_pytrades_v01()` below to import (and `importlib.reload`) your package cleanly.
""")
code(r"""
import importlib

def import_pytrades_v01():
    '''Ensure `str(BASE)` is on `sys.path`, import and `importlib.reload`
    `pytrades`, `pytrades.data`, `pytrades.indicators`, and `pytrades.strategy`,
    and return `{"root": pytrades, "data": data_mod, "indicators": ind_mod, "strategy": strat_mod}`.'''
    # TODO (create pytrades/*.py files at repo root first, then implement this loader)
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Write clean `.py` files under `BASE / "pytrades"` in your editor (harvesting your tested code from Days 01, 02, 06, 08, 09, and today's Ex 1). Make sure every `.py` file starts with `import numpy as np` / `import pandas as pd` and zero notebook globals!</details>
<details><summary>Hint 2 — clue</summary>Inside `import_pytrades_v01()`: check `if str(BASE) not in sys.path: sys.path.insert(0, str(BASE))`, `import pytrades, pytrades.data, pytrades.indicators, pytrades.strategy`, call `importlib.reload(...)` on each in dependency order (`data`, `indicators`, `strategy`, `pytrades`), and return the 4-key dict.</details>

### Exercise 5 — Transfer: `sweep_sma_pairs` + overfitting warning
""")
code(r"""
def sweep_sma_pairs(prices, pairs, long_only=True, cost_rate=0.001):
    '''Evaluate `test_strategy(prices, fast=f, slow=s, long_only=long_only, cost_rate=cost_rate)`
    for every `(f, s)` tuple in `pairs` and return a DataFrame (RangeIndex) with exact columns:
      ["fast", "slow", "total_return", "annualised_vol", "max_drawdown", "trades", "n_days"]
    sorted by `total_return` DESCENDING (ties broken by `fast` ascending, then `slow` ascending).
    Must NOT print or auto-select a single "best" pair. Empty `pairs` or any invalid pair -> ValueError.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Materialise `pairs = list(pairs)`, reject empty list, call your `test_strategy` for each `(f, s)` (which validates `1 <= f < s < len(prices)` automatically!), build the DataFrame, and sort with `ascending=[False, True, True]` on `["total_return", "fast", "slow"]` then `.reset_index(drop=True)`.</details>
<details><summary>Hint 2 — clue</summary>Notice `n_days` will differ across rows with different `slow` windows (e.g. `slow=50` vs `slow=200`)! Mention that subtle apples-to-oranges trap in your overfitting warning below.</details>
""")
md(r"""✍️ **Mandatory Overfitting & Window-Span Warning (edit me):** Ranking `N` `(fast, slow)` pairs on one historical series overstates future performance because (1) multiple-testing luck: `____`; and (2) rows with different `slow` lengths don't even share the same `n_days` (`____`).""")

md(r"""
---
## SECTION F — Mini-Project · P2.2 Package-Backed In-Sample vs Out-of-Sample Sweep

### Specification — `build_oos_sweep_report(prices, split_date, pairs, output_csv, cost_rate=0.001)`
- Import `test_strategy` from **`pytrades.strategy`** (proving your `pytrades/` v0.1 extraction works!).
- Split `prices` into two non-overlapping segments around `split_date`:
  - `in_sample = prices.loc[:split_date]`
  - `out_of_sample = prices.loc[prices.index > pd.Timestamp(split_date)]`
  (either segment too short for `max(slow)` → `ValueError`).
- Evaluate every `(fast, slow)` in `pairs` (long-only, `cost_rate`) on both segments and return a DataFrame (sorted by `is_return` descending, `RangeIndex`) with exact columns:
  `["fast", "slow", "is_return", "is_rank", "oos_return", "oos_rank"]`
  (`is_rank` and `oos_rank` are 1-based `int` ranks, `1` = highest return, `method="min"`).
- Save to `output_csv` (parents created).
""")
code(r"""
def build_oos_sweep_report(prices, split_date, pairs, output_csv, cost_rate=0.001):
    '''See Section F specification. Must import `test_strategy` from `pytrades.strategy`.'''
    # TODO
    pass
""")
code(r"""
# SECTION F (apply) - imports from your pytrades/ v0.1 package!
try:
    mods = import_pytrades_v01()
    grid = [(15, 40), (20, 60), (30, 90), (50, 100), (50, 150), (80, 200)]
    oos_df = build_oos_sweep_report(
        df_long["Close"], "2019-12-31", grid, PROCESSED / "day10_oos_sweep.csv", cost_rate=0.001
    )
    print("Loaded pytrades version:", getattr(mods["root"], "__version__", "unknown"))
    print(oos_df.to_string(index=False))
except Exception as exc:
    print("P2.2 package / sweep report not ready yet:", type(exc).__name__, exc)
""")
md(r"""
✍️ **P2.2 Extraction & IS/OOS Audit Note (edit me):**
- **Modules created in `pytrades/` v0.1:** …
- **Did the 2015–2019 `#1` SMA pair stay `#1` in 2020–2024? Cite numbers:** …
- **Why separating `pytrades.data` from `pytrades.strategy` paid off during this 12-backtest grid:** …

---
## SECTION G — Automated Assessment
""")
code(r"""
# SECTION G - harness + visible checks (self-contained)
import tempfile, types
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

_p15 = pd.Series(
    [100., 103., 107., 112., 118., 112., 102., 90., 80., 72., 72., 72., 75., 80., 86.],
    index=pd.bdate_range("2022-04-01", periods=15), name="Close"
)
_snap = _p15.copy()

check("Ex1 test_strategy keys, values & non-mutation of caller prices", lambda: (
    lambda r: set(r.keys()) == {"fast", "slow", "long_only", "cost_rate", "total_return",
                                "annualised_vol", "max_drawdown", "trades", "n_days"}
    and r["n_days"] == 11 and r["long_only"] is True and _p15.equals(_snap))(
        test_strategy(_p15, fast=2, slow=4, long_only=True, cost_rate=0.0)))
check("Ex1 transaction cost reduces total_return monotonically", lambda: (
    test_strategy(_p15, 2, 4, True, 0.0)["total_return"] > test_strategy(_p15, 2, 4, True, 0.01)["total_return"]))
check("Ex1 long_only=False differs from long_only=True on downturn path", lambda: (
    test_strategy(_p15, 2, 4, long_only=False, cost_rate=0.0)["total_return"]
    != test_strategy(_p15, 2, 4, long_only=True, cost_rate=0.0)["total_return"]))
check("Ex1 validation rejects bad windows, non-bool long_only, negative cost_rate", lambda: (
    raises(ValueError, lambda: test_strategy(_p15, 4, 2))
    and raises(ValueError, lambda: test_strategy(_p15, True, 4))
    and raises(ValueError, lambda: test_strategy(_p15, 2, 4, long_only="yes"))
    and raises(ValueError, lambda: test_strategy(_p15, 2, 4, cost_rate=-0.01))))

def _ex2_ok():
    wdf, summ = test_strategy_wealth(_p15, fast=2, slow=4, long_only=True, cost_rate=0.002, initial_capital=25_000.0)
    return (list(wdf.columns) == ["strategy_wealth", "benchmark_wealth"] and len(wdf) == 11
            and abs(summ["ending_capital"] - 25_000.0 * (1.0 + summ["total_return"])) < 1e-8
            and abs(float(wdf["strategy_wealth"].iloc[-1]) - summ["ending_capital"]) < 1e-8)
check("Ex2 test_strategy_wealth scales capital & reconciles ending_capital", _ex2_ok)
check("Ex2 initial_capital <= 0 or bool -> ValueError", lambda: (
    raises(ValueError, lambda: test_strategy_wealth(_p15, 2, 4, initial_capital=0.0))
    and raises(ValueError, lambda: test_strategy_wealth(_p15, 2, 4, initial_capital=-100.0))
    and raises(ValueError, lambda: test_strategy_wealth(_p15, 2, 4, initial_capital=True))))

def _ex3_zero_globals():
    if not callable(standalone_sma_tester): return False
    clean_env = {"np": np, "pd": pd, "__builtins__": __builtins__}
    pure = types.FunctionType(standalone_sma_tester.__code__, clean_env, "pure",
                              standalone_sma_tester.__defaults__)
    r_pure = pure(_p15.copy(), 2, 4)
    r_ref = test_strategy(_p15, 2, 4, long_only=True, cost_rate=0.0)["total_return"]
    return isinstance(r_pure, float) and abs(r_pure - r_ref) < 1e-12 and raises(ValueError, lambda: pure(_p15, 5, 2))
check("Ex3 standalone_sma_tester runs in a ZERO-global isolated namespace", _ex3_zero_globals)

check("Ex4 import_pytrades_v01 returns root/data/indicators/strategy modules", lambda: (
    lambda m: isinstance(m, dict) and set(m.keys()) == {"root", "data", "indicators", "strategy"})(import_pytrades_v01()))

def _ex4_pkg_smoke():
    mods = import_pytrades_v01()
    d_mod, i_mod, s_mod = mods["data"], mods["indicators"], mods["strategy"]
    ohlcv = df.iloc[:12].copy()
    ok_val = d_mod.validate_ohlcv(ohlcv) is True
    sl = d_mod.slice_prices(ohlcv, str(ohlcv.index[2].date()), str(ohlcv.index[6].date()))
    sm = i_mod.sma(_p15, 3); em = i_mod.ema(_p15, 3); lr = i_mod.log_returns(_p15)
    pos = s_mod.long_only_positions(pd.Series([1, -1, 1], index=_p15.index[:3]))
    ts = s_mod.test_strategy(_p15, fast=2, slow=4, long_only=True, cost_rate=0.001)
    return (ok_val and len(sl) == 5 and int(sm.isna().sum()) == 2 and int(em.isna().sum()) == 2
            and bool(np.isnan(lr.iloc[0])) and list(pos.values) == [0, 1, 0]
            and abs(ts["total_return"] - test_strategy(_p15, 2, 4, True, 0.001)["total_return"]) < 1e-12)
check("Ex4 pytrades v0.1 passes data/indicators/strategy behavioural smoke tests", _ex4_pkg_smoke)

def _ex5_sweep():
    sw = sweep_sma_pairs(_p15, [(3, 6), (2, 4), (2, 5)], long_only=True, cost_rate=0.001)
    cols = ["fast", "slow", "total_return", "annualised_vol", "max_drawdown", "trades", "n_days"]
    return (list(sw.columns) == cols and len(sw) == 3
            and bool((sw["total_return"].diff().dropna() <= 1e-15).all()))
check("Ex5 sweep_sma_pairs returns full table sorted by total_return desc", _ex5_sweep)
check("Ex5 sweep_sma_pairs rejects empty or invalid pairs", lambda: (
    raises(ValueError, lambda: sweep_sma_pairs(_p15, []))
    and raises(ValueError, lambda: sweep_sma_pairs(_p15, [(5, 3)]))))

def _proj_ok():
    p_two = df_long["Close"].iloc[:400]
    split = str(p_two.index[199].date())
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "p22" / "oos.csv"
        rep = build_oos_sweep_report(p_two, split, [(10, 30), (20, 50), (15, 45)], out, cost_rate=0.001)
        back = pd.read_csv(out)
        return (list(rep.columns) == ["fast", "slow", "is_return", "is_rank", "oos_return", "oos_rank"]
                and list(rep["is_rank"]) == [1, 2, 3] and set(rep["oos_rank"]) <= {1, 2, 3}
                and len(back) == 3)
check("F project: IS/OOS sweep report uses pytrades & writes round-trip CSV", _proj_ok)
print(f"\nSCORE: {sum(RESULTS)}/{len(RESULTS)} visible checks passing")
""")

md(r"""
---
## SECTION H — Knowledge Check

**H1 (Pre-watch #1 & #2 revisited)** State two concrete engineering bugs or bottlenecks caused by calling `yf.download(...)` *inside* `test_strategy(stock, start, end, SMA)` instead of passing `prices` in. ✍️
**H2 (Pre-watch #3 revisited)** Explain step-by-step how Python's LEGB scope rule lets a broken notebook function pass every interactive cell test yet crash with `NameError` the moment it moves into `pytrades/strategy.py`. ✍️
**H3 Defend** `importlib.reload` during package development: what sits in `sys.modules` if you edit `pytrades/strategy.py` on disk and re-run `from pytrades.strategy import test_strategy` *without* reloading or restarting the kernel? ✍️
**H4 Predict output** In `sweep_sma_pairs(df_long["Close"], [(20, 50), (50, 200)])`, what are the two `n_days` values? Describe a market scenario (e.g. a huge rally during bars `50..199`) where comparing their `total_return` columns directly is misleading, and state how you would align them if fair comparison were required. ✍️
**H5 What-if (multiple testing)** Suppose 20 completely random coin-flip strategies (`50/50` long/flat) each have a `5%` chance of beating Buy & Hold by `+15%` over a sample. Roughly what is the probability (`1 - 0.95^20`) that *at least one* coin-flipper beats Buy & Hold by `+15%`? Connect that number to `sweep_sma_pairs`. ✍️
**H6 Bridge to Day 11** Look at `test_strategy`, `test_strategy_wealth`, and a plotting helper: all three take `(prices, fast, slow, long_only, cost_rate)` and recompute the exact same rolling averages from scratch. When does bundling `(data + parameters + cached results + methods)` into a **class** earn its complexity over plain functions? ✍️
""")

md(r"""
---
## SECTION I — Reflection & Retrieval Practice

### What I learned · Can implement unaided · Still difficult ✍️

### Retrieval — Days 09 (n−1), 07 (n−3), 04 (n−6)
1. **Day 09:** Write the `L_in / L_out` log-return expressions for Buy & Hold, Long-Only, and Long/Short, and state the condition under which `Long-Only > Long/Short`.
2. **Day 09:** Why does `apply_transaction_costs` compute turnover against `positions.shift(1, fill_value=0)` rather than `positions.diff().fillna(0)`?
3. **Day 07:** Why must `max_drawdown` divide by `cummax` (anchored at `1.0` for `$1` wealth) rather than `.max()`?
4. **Day 04:** Does scaling `initial_capital` from `$10,000` to `$1,000,000` change `total_return`, `annualised_vol`, or `max_drawdown`? Why or why not?
""")
code(r"""
# Closed-notebook retrieval: write Day-06 `sma` and `log_returns` signatures + bodies FROM MEMORY
# (the exact two building blocks inside pytrades/indicators.py!)
def sma_from_memory(prices, window):
    '''Trailing SMA with min_periods=window; non-bool int window >= 1 else ValueError.'''
    # TODO
    pass

def log_returns_from_memory(prices):
    '''ln(P_t / P_{t-1}); first row NaN; any price <= 0 -> ValueError.'''
    # TODO
    pass

try:
    _p_m = pd.Series([100.0, 110.0, 99.0, 108.9])
    _s_m = sma_from_memory(_p_m, 2); _l_m = log_returns_from_memory(_p_m)
    _ok = (bool(np.isnan(_s_m.iloc[0])) and abs(float(_s_m.iloc[1]) - 105.0) < 1e-12
           and bool(np.isnan(_l_m.iloc[0])) and abs(float(_l_m.sum()) - np.log(108.9 / 100.0)) < 1e-12)
except Exception as exc:
    _ok = False; print("self-check raised:", type(exc).__name__, exc)
print("indicators from-memory self-check:", "PASS" if _ok else "not yet")
""")
md(r"""
### ✅ Completion checklist
- [ ] Video `02:16:30–02:26:30` watched; IO-vs-pure trade-off articulated in own words
- [ ] Ex 1–5 implemented; `standalone_sma_tester` passes the isolated zero-global check
- [ ] `pytrades/` v0.1 (`__init__.py`, `data.py`, `indicators.py`, `strategy.py`) created at repo root per `projects/PACKAGE_SPEC.md`
- [ ] **Fresh-kernel proof:** Kernel → Restart & Run All passes 12/12 checks in Section G with Section F importing directly from `pytrades`
- [ ] Overfitting warning + IS/OOS rank comparison completed honestly

**Send back:** Section G score · clean-kernel import confirmation (`pytrades.__version__`) · your IS/OOS rank table & H5 calculation. Day 11 wraps your `pytrades/` engine in a clean, stateful strategy class (+ Challenge 4).
""")

nb = new_notebook(cells=CELLS)
nb.metadata.update({"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                    "language_info": {"name": "python", "version": "3.11"},
                    "title": "Day 10 - Functions: Reusable Strategy Tester & pytrades v0.1",
                    "source_video": "https://www.youtube.com/watch?v=GDMkkmkJigw (02:16:30-02:26:30)"})
out = ROOT / "notebooks" / "Day_10_Functions_Reusable_Strategy_Tester.ipynb"
nbformat.write(nb, out); print("wrote", out, "cells=", len(CELLS))
