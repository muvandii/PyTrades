"""Build Day 11 notebook. Instructor utility."""
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

# Day 11 — Strategy Classes, `pytrades` v0.2 & Challenge 4

| | |
|---|---|
| **Video segment** | **02:26:30–02:51:00** — *Creating a class* · *Importing and Using a Class* · **Challenge 4** ([watch](https://www.youtube.com/watch?v=GDMkkmkJigw&t=8790s)) |
| **Estimated study time** | **2.5–3.5 hours** |
| **Prerequisites** | Day 10 green: `pytrades/` v0.1 (`data`, `indicators`, `strategy`) importable from a fresh kernel |
| **Expected deliverable** | **P2.3:** `pytrades` v0.2 exporting `SMACrossoverStrategy` & `EMACrossoverStrategy` (Challenge 4) + package-only comparison report & CHANGELOG note |

## Learning objectives — by the end of today you will be able to

1. **Decide and defend** when a Python class earns its complexity (bundling validated data, parameters, cached backtest state, and `.run()`/`.summary()`/`.plot()` lifecycle) vs when a Day-10 pure function is cleaner.
2. **Implement** validated strategy state (`__init__`, defensive `.prices` copy, `@property` setters and `.set_parameters(...)` that automatically invalidate stale cached results).
3. **Diagnose and repair** mutable-default and class-attribute bugs that leak state across separate strategy instances.
4. **Build** `SMACrossoverStrategy` delegating its indicator and performance maths to your Day-10 functions (**zero duplicated formulas**, proven by `strat.summary() == test_strategy(...)`) with a Day-03-standard `.plot()` returning `Axes`.
5. **Complete Challenge 4** by implementing `EMACrossoverStrategy` on top of your base crossover lifecycle and critiquing inheritance vs composition in prose.
""")

md(r"""
---
## SECTION B — Video Learning · 02:26:30–02:51:00

**Pre-watch questions** (write guesses first; checked in Section H):
1. In `class SMABacktester: def __init__(self, ...):`, what actually *is* `self` when you create two objects `a = SMABacktester(...)` and `b = SMABacktester(...)`?
2. Suppose `a.run()` computes a backtest and stores `a._results`. Then you change `a.fast = 20` and call `a.summary()` *without* clearing or re-running `a._results`. Whose numbers did `a.summary()` just report?
3. Why is duplicating the SMA and drawdown formulas inside both `test_strategy(...)` *and* `SMACrossoverStrategy.run(...)` a maintenance time bomb?
4. Predict **Challenge 4** (~02:49:30): once an SMA backtester class exists in a `.py` file, what kind of indicator/strategy extension does the presenter challenge you to build on your own?

| Time | Chapter | Watch for |
|---|---|---|
| 02:26:30 | Creating a class | `__init__`, instance attributes (`self.symbol`, `self.SMA_S`, `self.SMA_L`, `self.results`), `get_data`, `test_results`, `plot_results`, and a parameter-updating method |
| 02:45:00 | Importing and Using a Class | Saving the class into a `.py` module, importing it into a clean notebook, instantiating, running, plotting |
| 02:49:30 | **Challenge 4** | Build/modify your own strategy class variant (our offline-testable specification: **`EMACrossoverStrategy`** reusing the base machinery) |
| 02:51:00 | ⛔ STOP | *API / Alpha Vantage* is Day 12 |

Fallback: [02:26:30](https://www.youtube.com/watch?v=GDMkkmkJigw&t=8790s) · [02:45:00](https://www.youtube.com/watch?v=GDMkkmkJigw&t=9900s) · [Challenge 4 ~02:49:30](https://www.youtube.com/watch?v=GDMkkmkJigw&t=10170s) · [stop at 02:51:00](https://www.youtube.com/watch?v=GDMkkmkJigw&t=10260s)
""")

code(r"""
# ▶️ SECTION B (code) - 02:26:30 to 02:51:00
from IPython.display import YouTubeVideo, display
display(YouTubeVideo("GDMkkmkJigw", start=8790, end=10260, width=800, height=450))
print("Fallback: https://www.youtube.com/watch?v=GDMkkmkJigw&t=8790s  (stop at 02:51:00)")
""")

md(r"""✍️ **My 3-bullet summary + Challenge 4 in one sentence (edit me):** - · - · Challenge 4 = …""")

md(r"""
---
## SECTION C — Concept Notes

### C1. When does a class beat a plain function?
Day 10's `test_strategy(prices, fast, slow, long_only, cost_rate)` is unbeatable for a stateless one-liner or grid sweep. A **class** earns its keep only when several operations share **validated state + cached intermediate artifacts** across a workflow:
`strat = SMACrossoverStrategy(prices, 50, 100, cost_rate=0.001)` → `strat.run()` (computes & caches the full tradable DataFrame once) → `strat.summary()` (reads cached series) → `strat.plot()` (plots cached wealth curves). Remember: this is **research organisation**, not a live order-execution engine.

### C2. Explicit lifecycle & cache-invalidation contract
Caching creates a classic bug: stale results after parameter edits. We state one unambiguous contract and test every edge of it:
1. Before `.run()` has been called (or right after any parameter change), `self._results` is `None`. Calling `.summary()` or `.plot()` while `self._results is None` **raises `RuntimeError`** (loud, explicit — never silently returns `None` or stale numbers).
2. Calling `.run()` when `self._results is not None` returns a copy/view of the cached frame **without** recomputing (`self._run_count` stays unchanged).
3. Updating `.fast`, `.slow`, `.long_only`, or `.cost_rate` (via `@property` setters or `.set_parameters(...)`) validates the new configuration first and immediately sets `self._results = None`.

### C3. Instance attributes (`self.x`) vs Class attributes (`cls.x`)
Writing `log = []` directly under `class Foo:` creates **one list shared by every instance of `Foo`**. Writing `def __init__(self, cfg={}):` creates **one default dict shared across calls**. Mutable state belongs inside `__init__` on `self` (`self.log = []`, `self.prices = prices.copy()`).

### C4. Single source of truth: classes delegate to functions
Never copy-paste formulas between functions and classes. `SMACrossoverStrategy` calls `sma`, `log_returns`, `positions_from_signal` / `long_only_positions`, `apply_transaction_costs`, `performance_summary`, and `trade_count` from your `pytrades` modules. Consequence: `strat.run(); strat.summary()` is **guaranteed** to agree with `test_strategy(...)` to floating-point precision.

### C5. Challenge 4 — Inheritance vs Composition
To add `EMACrossoverStrategy`, only the two moving-average series change (`ema` instead of `sma`); causal `.shift(1)`, warm-up slicing (`index[slow:]`), turnover costs, summary dict, and plotting are 100% identical.
- **Template-method inheritance:** `BaseCrossoverStrategy` defines `_moving_averages(self)` hook; `SMACrossoverStrategy` overrides it with `sma`, `EMACrossoverStrategy` with `ema` (~8 lines, zero duplicated backtest logic).
- **Composition / parameterisation:** pass an indicator callable `ma_fn=sma` or `kind="ema"` into a single `MovingAverageCrossoverStrategy`. Often simpler when variants only swap one plug-in function! You will implement the subclass for Challenge 4 and weigh both designs in Section E5 / H5.
""")

code(WEEK2_SETUP_CODE + r"""
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))
""")

md(r"""
---
## SECTION D — Guided Exploration

### D1 — Class attribute vs instance attribute (`self`) caught in the act
**Predict:** ` SharedTrap` defines `trades = []` on the class body. If we create `a = SharedTrap()` and `b = SharedTrap()`, and append `"BUY DEMO"` to `a.trades`, what is `b.trades`?
""")
md(r"""✍️ **D1 prediction (edit me):** """)
code(r"""
# D1 - shared class-attribute mutation vs isolated `self` attribute
class _SharedTrap:
    trades = []
class _SafeInstance:
    def __init__(self):
        self.trades = []

a1, b1 = _SharedTrap(), _SharedTrap()
a1.trades.append("BUY DEMO")
a2, b2 = _SafeInstance(), _SafeInstance()
a2.trades.append("BUY DEMO")
print("_SharedTrap   -> b1.trades:", b1.trades, "| same list object?:", a1.trades is b1.trades)
print("_SafeInstance -> b2.trades:", b2.trades, "| same list object?:", a2.trades is b2.trades)
# TODO(modify): test `def __init__(self, tags=[]): self.tags = tags` on two instances. Same trap?
""")
md(r"""
✍️ **D1 observed (edit me):** `a1.trades is b1.trades` was `____` because class-body lists are created **once** when the `class` statement executes, whereas `self.trades = []` inside `__init__` creates a fresh list per instance.

### D2 — `@property` setters & cache invalidation in miniature
**Predict:** in `_TinyCache` below, we call `c.compute()`, `c.compute()`, then set `c.window = 10`, then `c.compute()`. What will `c._run_count` equal after each of the three `.compute()` calls?
""")
md(r"""✍️ **D2 prediction (edit me):** after call 1: ___ · after call 2: ___ · after `window=10` + call 3: ___""")
code(r"""
# D2 - property setter invalidating a cached computation
class _TinyCache:
    def __init__(self, s, window=5):
        self._s = s.copy(); self._window = window; self._cache = None; self._run_count = 0
    @property
    def window(self): return self._window
    @window.setter
    def window(self, val):
        if val < 1: raise ValueError("window >= 1")
        self._window = val; self._cache = None   # <-- invalidates stale cache!
    def compute(self):
        if self._cache is None:
            self._cache = self._s.rolling(self._window, min_periods=self._window).mean()
            self._run_count += 1
        return self._cache

tc = _TinyCache(df["Close"].iloc[:20], window=5)
tc.compute(); print("after call 1, _run_count =", tc._run_count)
tc.compute(); print("after call 2 (cached!), _run_count =", tc._run_count)
tc.window = 10; print("right after tc.window=10, _cache is None?:", tc._cache is None)
tc.compute(); print("after call 3 (recomputed!), _run_count =", tc._run_count)
# TODO(modify): comment out `self._cache = None` in the setter and see what wrong window `tc.compute()` returns!
""")
md(r"""
✍️ **D2 observed (edit me):** `_run_count` progressed `___ → ___ → ___`. Without invalidating `_cache = None` in the setter, `tc.window` would say `10` while `tc.compute()` silently returned the old `5`-day series.

### D3 — SMA 50/100 vs EMA 50/100 on `df_long` (Challenge 4 preview)
**Predict:** EMA weights recent prices more heavily than SMA (Day 06). On `df_long["Close"]` (`50/100`, long-only, `10 bps` cost), which variant will generate **more trades** — `SMA` or `EMA` — and will extra responsiveness automatically produce higher net return?
""")
md(r"""✍️ **D3 prediction (edit me):** more trades: ___ · higher net return: ___""")
code(r"""
# D3 - compare SMA vs EMA crossover turnover & net wealth on df_long
p = df_long["Close"]; lr = np.log(p / p.shift(1)).iloc[100:]
for label, f_ma, s_ma in [
    ("SMA 50/100", p.rolling(50, min_periods=50).mean(), p.rolling(100, min_periods=100).mean()),
    ("EMA 50/100", p.ewm(span=50, min_periods=50).mean(), p.ewm(span=100, min_periods=100).mean()),
]:
    sig = pd.Series(np.where(f_ma > s_ma, 1, 0), index=p.index).where(s_ma.notna(), 0)
    pos = sig.shift(1, fill_value=0).iloc[100:]
    turn = (pos - pos.shift(1, fill_value=0)).abs()
    net = pos * lr - 0.001 * turn
    print(f"{label} | trades={int((turn > 0).sum()):2d} | net total_return={np.exp(net.sum())-1:+.4f}")
# TODO(modify): re-run at `cost_rate = 0.004` (40 bps). Which indicator suffers faster as trading friction rises?
""")
md(r"""✍️ **D3 observed (edit me):** `SMA 50/100` traded `___` times (`net = ____`), `EMA 50/100` traded `___` times (`net = ____`). Faster reaction is a trade-off between earlier trend entry and extra whipsaw/cost.""" )

md(r"""
---
## SECTION E — Independent Practice

### Exercise 1 — Basic: `StrategyState` (validated `__init__` + invalidating setters)
""")
code(r"""
class StrategyState:
    '''Validated parameter & price holder for a 2-window crossover strategy:
      - `__init__(self, prices, fast=50, slow=100, long_only=True, cost_rate=0.0)`:
        validates `prices` (non-empty positive NaN-free 1D Series), non-bool ints
        `1 <= fast < slow < len(prices)`, `isinstance(long_only, bool)`, and non-bool
        real `cost_rate >= 0`; else raises ValueError.
      - Stores a defensive copy `self.prices = prices.copy()`, initialises
        `self._results = None` and `self._run_count = 0`.
      - Exposes `@property` + setter for `fast`, `slow`, `long_only`, `cost_rate` AND
        `set_parameters(self, fast=None, slow=None, long_only=None, cost_rate=None)`:
        any valid change updates the attribute(s) and resets `self._results = None`;
        any invalid update raises ValueError WITHOUT corrupting existing attributes.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Write one internal validator `set_parameters(fast=..., slow=..., long_only=..., cost_rate=...)` that validates the *complete* proposed configuration `(new_fast, new_slow, new_lo, new_cost)` atomically before mutating `self._fast`, `self._slow`, etc. Then `__init__` and every `@property` setter simply delegate to `set_parameters`!</details>
<details><summary>Hint 2 — clue</summary>Atomic validation means if `s = StrategyState(p, 20, 50)` and someone calls `s.fast = 80` (`>= 50`), `ValueError` is raised and `s.fast` is STILL `20`! Also explain why `s.set_parameters(fast=60, slow=120)` succeeds in one step when `s.fast = 60` alone would fail against the old `slow=50`.</details>

### Exercise 2 — Modification: `BaseCrossoverStrategy` (`.run()` cache & `.summary()` guard)
""")
code(r"""
class BaseCrossoverStrategy(StrategyState):
    '''Lifecycle base class extending `StrategyState`:
      - `_moving_averages(self)`: abstract hook returning `(fast_ma, slow_ma)` Series;
        raises `NotImplementedError` on `BaseCrossoverStrategy` itself.
      - `run(self)`: if `self._results is None`, calls `self._moving_averages()`,
        computes Day 08-10 causal crossover backtest on `self.prices.index[self.slow:]`,
        increments `self._run_count += 1`, caches `self._results` (DataFrame with exact
        columns ["Close", "fast_ma", "slow_ma", "signal", "position",
        "benchmark_log_returns", "strategy_log_returns", "benchmark_wealth", "strategy_wealth"],
        where both `*_log_returns` and `*_wealth` are NET of `self.cost_rate`!),
        and returns a `.copy()` of `self._results`. Subsequent `run()` calls without
        parameter changes reuse cache (`_run_count` unchanged).
      - `summary(self)`: if `self._results is None`, raises `RuntimeError` with a clear
        message ("Call .run() before .summary()"); otherwise returns the exact 9-key
        dict contract of Day 10's `test_strategy`.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Template Method pattern: `BaseCrossoverStrategy` owns 100% of the causal shift, warm-up trim (`iloc[self.slow:]`), transaction-cost deduction, wealth curves, caching, and `.summary()`, leaving *only* `_moving_averages(self)` to subclasses.</details>
<details><summary>Hint 2 — approach</summary>Return `self._results.copy()` from `.run()` so an external caller mutating the returned DataFrame cannot corrupt `self._results` inside your instance!</details>
<details><summary>Hint 3 — clue</summary>In `.summary()`, compute `performance_summary` on `self._results["strategy_log_returns"]` and `trade_count` on `self._results["position"]` so `summary()` matches Day 10's `test_strategy` key-for-key: `{"fast", "slow", "long_only", "cost_rate", "total_return", "annualised_vol", "max_drawdown", "trades", "n_days"}`.</details>

### Exercise 3 — Debugging: leaky class attributes & mutable defaults

Diagnose **both** shared-state bugs in `LeakyStrategyLog`, then implement `IsolatedStrategyLog`.
""")
code(r"""
# --- BUGGY CLASS (study; do not edit) ---
class LeakyStrategyLog:
    notes = []                                                  # bug 1
    def __init__(self, name, params={"fast": 20, "slow": 50}):  # bug 2
        self.name = name
        self.params = params
    def record(self, note, new_fast=None):
        self.notes.append(f"{self.name}: {note}")
        if new_fast is not None:
            self.params["fast"] = new_fast

_a = LeakyStrategyLog("SPY_test"); _b = LeakyStrategyLog("QQQ_test")
_a.record("ran v1", new_fast=10)
print("_b.notes :", _b.notes, " <-- QQQ never ran anything!")
print("_b.params:", _b.params, " <-- QQQ's fast window silently mutated to 10!")
""")
md(r"""✍️ **Diagnosis (edit me):** Bug 1 (`notes = []` on class): `____`. Bug 2 (`params={...}` in `def __init__`): Python evaluates default argument dicts **once** at `def` time, so `_a.params is _b.params` unless we default to `____` and copy inside `__init__`.""")
code(r"""
class IsolatedStrategyLog:
    '''Repaired version of LeakyStrategyLog:
      - `params=None` defaults to a fresh `{"fast": 20, "slow": 50}` dict per instance;
        if a dict is passed in, store a shallow `.copy()` so caller mutations don't leak.
      - `self.notes` is an instance list (`[]` per object).
      - `record(self, note, new_fast=None)` appends `f"{self.name}: {note}"` to `self.notes`
        and updates `self.params["fast"] = new_fast` when `new_fast is not None`.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — clue</summary>`self.notes = []` and `self.params = {"fast": 20, "slow": 50} if params is None else dict(params)` inside `__init__`.</details>

### Exercise 4 — Independent: `SMACrossoverStrategy` + `.plot()` + `pytrades` v0.2
""")
code(r"""
class SMACrossoverStrategy(BaseCrossoverStrategy):
    '''Concrete SMA crossover strategy delegating indicator maths to `sma`:
      - `_moving_averages(self)`: returns `(sma(self.prices, self.fast), sma(self.prices, self.slow))`
        using `min_periods=window` (from `pytrades.indicators.sma`).
      - `plot(self, ax=None, title=None)`: raises `RuntimeError` if `self._results is None`;
        otherwise plots `benchmark_wealth` and `strategy_wealth` on `ax` (creating
        `fig, ax = plt.subplots(...)` if `ax is None`), sets a non-empty title,
        y-axis label, and legend, and returns `ax` (Day-03 testable Axes standard).'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Because `BaseCrossoverStrategy` already handles validation, caching, causal shifting, costs, and `.summary()`, `SMACrossoverStrategy` only needs `_moving_averages` (~3 lines) and `plot` (~8 lines)! Add `SMACrossoverStrategy` to `pytrades/strategy.py` and bump `pytrades/__init__.py` to `__version__ = "0.2.0"`.</details>
<details><summary>Hint 2 — clue</summary>In `plot`: check `if self._results is None: raise RuntimeError("Call .run() before .plot()")`; plot `self._results[["benchmark_wealth", "strategy_wealth"]].plot(ax=ax)`, call `ax.set_title(...)`, `ax.set_ylabel("Wealth ($1)")`, `ax.legend()`, and `return ax`.</details>

### Exercise 5 — Transfer (Challenge 4): `EMACrossoverStrategy` + design critique
""")
code(r"""
class EMACrossoverStrategy(SMACrossoverStrategy):
    '''Challenge 4: Exponential Moving Average crossover strategy (`ewm(span=..., min_periods=...)`)
    reusing 100% of `BaseCrossoverStrategy` / `SMACrossoverStrategy` lifecycle & plotting.
    Exported alongside `SMACrossoverStrategy` in `pytrades/strategy.py`.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Override `_moving_averages(self)` to return `(ema(self.prices, self.fast), ema(self.prices, self.slow))` (delegating to `pytrades.indicators.ema`), plus adjust the default plot title if none was supplied so charts self-identify as EMA vs SMA.</details>
<details><summary>Hint 2 — clue</summary>Test on a constant flat series: `ema(flat, fast) == ema(flat, slow) == flat`, so our 3-state tie rule yields `0` trades and `0.0` return automatically!</details>
""")
md(r"""✍️ **Challenge 4 Design Justification — Inheritance vs Composition (edit me):** Here subclassing `_moving_averages` worked cleanly because `____`. However, if we next wanted Bollinger-band, RSI, and 3-MA strategies with *different* parameter sets (not `fast`/`slow`), deep inheritance would break down because `____`, and composition (`____`) would be better.""")

md(r"""
---
## SECTION F — Mini-Project · P2.3 Package-Only SMA vs EMA Report (`pytrades` v0.2)

### Specification — `compare_crossover_classes(prices, fast=50, slow=100, cost_rate=0.001, output_csv=None)`
- Import `SMACrossoverStrategy`, `EMACrossoverStrategy`, and `test_strategy` **directly from `pytrades.strategy`** (`importlib.reload` allowed so fresh edits pick up).
- Instantiate and `.run()` both classes on `prices` with `(fast, slow, long_only=True, cost_rate=cost_rate)`.
- Assert parity `SMACrossoverStrategy.summary() == test_strategy(...)`.
- Return a 2-row DataFrame indexed by `["SMA", "EMA"]` containing the 9 summary columns; write to `output_csv` if provided (parents created).
""")
code(r"""
import importlib

def compare_crossover_classes(prices, fast=50, slow=100, cost_rate=0.001, output_csv=None):
    '''See Section F specification. Must import classes from `pytrades.strategy`.'''
    # TODO
    pass
""")
code(r"""
# SECTION F (apply) - imports ONLY from pytrades!
try:
    import pytrades, pytrades.strategy
    importlib.reload(pytrades.strategy); importlib.reload(pytrades)
    cls_tbl = compare_crossover_classes(
        df_long["Close"], fast=50, slow=100, cost_rate=0.001,
        output_csv=PROCESSED / "day11_sma_vs_ema.csv"
    )
    print("pytrades version:", getattr(pytrades, "__version__", "unknown"))
    print(cls_tbl.round(4))
    sma_obj = pytrades.strategy.SMACrossoverStrategy(df_long["Close"], 50, 100, True, 0.001)
    ema_obj = pytrades.strategy.EMACrossoverStrategy(df_long["Close"], 50, 100, True, 0.001)
    sma_obj.run(); ema_obj.run()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
    sma_obj.plot(ax=axes[0], title="SMA 50/100 ($1 net wealth)")
    ema_obj.plot(ax=axes[1], title="EMA 50/100 ($1 net wealth)")
    plt.tight_layout(); plt.show()
except Exception as exc:
    print("pytrades v0.2 classes not ready yet:", type(exc).__name__, exc)
""")
md(r"""
✍️ **P2.3 `pytrades` v0.2 CHANGELOG & Findings (edit me):**
- **`v0.2.0` additions (`pytrades/strategy.py`):** …
- **SMA 50/100 vs EMA 50/100 (`10 bps` net) comparison:** …
- **Where caching helped during plotting & summarising:** …

---
## SECTION G — Automated Assessment
""")
code(r"""
# SECTION G - harness + visible checks (self-contained)
import tempfile
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

_p16 = pd.Series(
    [100., 103., 107., 112., 118., 112., 102., 90., 80., 72., 73., 76., 81., 87., 92., 96.],
    index=pd.bdate_range("2022-04-01", periods=16), name="Close"
)

def _ex1_init():
    src = _p16.copy()
    st = StrategyState(src, fast=2, slow=4, long_only=True, cost_rate=0.001)
    src.iloc[0] = 9999.0
    return (float(st.prices.iloc[0]) == 100.0 and st.fast == 2 and st.slow == 4
            and st._results is None and st._run_count == 0
            and raises(ValueError, lambda: StrategyState(_p16, fast=4, slow=2))
            and raises(ValueError, lambda: StrategyState(_p16, fast=2, slow=4, long_only=1))
            and raises(ValueError, lambda: StrategyState(_p16, fast=2, slow=4, cost_rate=-0.1)))
check("Ex1 StrategyState validates __init__ & makes defensive copy of prices", _ex1_init)

def _ex1_setters():
    st = StrategyState(_p16, fast=2, slow=5)
    st._results = "sentinel"
    st.fast = 3
    ok1 = (st.fast == 3 and st._results is None)
    st._results = "sentinel"
    bad = raises(ValueError, lambda: setattr(st, "fast", 6)) and st.fast == 3
    st._results = "sentinel"
    st.set_parameters(fast=6, slow=10, cost_rate=0.002)
    return ok1 and bad and st.fast == 6 and st.slow == 10 and st.cost_rate == 0.002 and st._results is None
check("Ex1 setters & set_parameters validate atomically and invalidate _results", _ex1_setters)

check("Ex2 summary() and plot() BEFORE run() raise RuntimeError", lambda: (
    raises(RuntimeError, lambda: SMACrossoverStrategy(_p16, 2, 4).summary())
    and raises(RuntimeError, lambda: SMACrossoverStrategy(_p16, 2, 4).plot())))

def _ex2_cache():
    s = SMACrossoverStrategy(_p16, fast=2, slow=4, long_only=True, cost_rate=0.001)
    r1 = s.run(); c1 = s._run_count
    r2 = s.run(); c2 = s._run_count
    r1.iloc[0, 0] = -999.0  # mutating returned copy must not corrupt internal cache!
    s.cost_rate = 0.005; c_mid = s._results
    r3 = s.run(); c3 = s._run_count
    return (c1 == 1 and c2 == 1 and c_mid is None and c3 == 2
            and float(s.run().iloc[0, 0]) > 0 and r3["strategy_wealth"].iloc[-1] < r2["strategy_wealth"].iloc[-1])
check("Ex2 .run() caches results, protects internal copy & recomputes after mutation", _ex2_cache)

def _ex3_iso():
    x = IsolatedStrategyLog("A"); y = IsolatedStrategyLog("B")
    x.record("hello", new_fast=7)
    return x.notes == ["A: hello"] and y.notes == [] and x.params["fast"] == 7 and y.params["fast"] == 20
check("Ex3 IsolatedStrategyLog eliminates class-attribute & mutable-default leaks", _ex3_iso)

def _ex4_two_instances():
    a = SMACrossoverStrategy(_p16, fast=2, slow=4, long_only=True, cost_rate=0.0)
    b = SMACrossoverStrategy(_p16, fast=3, slow=6, long_only=False, cost_rate=0.002)
    a.run(); b.run()
    return a.summary()["n_days"] == 12 and b.summary()["n_days"] == 10 and a.summary()["total_return"] != b.summary()["total_return"]
check("Ex4 two SMACrossoverStrategy instances stay completely independent", _ex4_two_instances)

def _ex4_parity():
    import pytrades.strategy as ps
    importlib.reload(ps)
    s = SMACrossoverStrategy(_p16, fast=2, slow=5, long_only=True, cost_rate=0.0015)
    s.run(); d_cls = s.summary()
    d_fn = ps.test_strategy(_p16, fast=2, slow=5, long_only=True, cost_rate=0.0015)
    return d_cls.keys() == d_fn.keys() and all(
        (d_cls[k] == d_fn[k] if isinstance(d_fn[k], (bool, int)) else abs(d_cls[k] - d_fn[k]) < 1e-12)
        for k in d_fn
    )
check("Ex4 single-source-of-truth: SMACrossoverStrategy.summary() == test_strategy()", _ex4_parity)

def _ex4_plot():
    s = SMACrossoverStrategy(_p16, 2, 4); s.run()
    fig, ax = plt.subplots()
    out_ax = s.plot(ax=ax, title="Test Equity")
    ok = (out_ax is ax and len(ax.get_lines()) >= 2 and bool(ax.get_title()) and bool(ax.get_ylabel()))
    plt.close(fig)
    return ok
check("Ex4 .plot() returns matplotlib Axes with >=2 wealth lines, title & ylabel", _ex4_plot)

def _ex5_ema():
    sma_s = SMACrossoverStrategy(_p16, 2, 5, long_only=True, cost_rate=0.001)
    ema_s = EMACrossoverStrategy(_p16, 2, 5, long_only=True, cost_rate=0.001)
    r_sma = sma_s.run(); r_ema = ema_s.run()
    flat = pd.Series([100.] * 10, index=pd.bdate_range("2022-06-01", periods=10))
    ema_flat = EMACrossoverStrategy(flat, 2, 4); ema_flat.run()
    return (not np.allclose(r_sma["fast_ma"].values, r_ema["fast_ma"].values)
            and np.allclose(r_ema["fast_ma"].values, _p16.ewm(span=2, min_periods=2).mean().iloc[5:].values)
            and ema_flat.summary()["trades"] == 0 and ema_flat.summary()["total_return"] == 0.0)
check("Ex5 Challenge 4: EMACrossoverStrategy uses ewm & handles flat series cleanly", _ex5_ema)

def _ex5_pkg_v02():
    import pytrades, pytrades.strategy as ps
    importlib.reload(ps); importlib.reload(pytrades)
    s1 = ps.SMACrossoverStrategy(_p16, 2, 4); s1.run()
    s2 = ps.EMACrossoverStrategy(_p16, 2, 4); s2.run()
    return s1.summary()["n_days"] == 12 and s2.summary()["n_days"] == 12
check("Ex4/5 pytrades.strategy exports working SMACrossoverStrategy & EMACrossoverStrategy", _ex5_pkg_v02)

def _proj_ok():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "p23" / "cmp.csv"
        tbl = compare_crossover_classes(_p16, fast=2, slow=5, cost_rate=0.001, output_csv=out)
        back = pd.read_csv(out, index_col=0)
        return list(tbl.index) == ["SMA", "EMA"] and len(back) == 2 and "total_return" in tbl.columns
check("F project: compare_crossover_classes imports from pytrades & writes CSV", _proj_ok)
print(f"\nSCORE: {sum(RESULTS)}/{len(RESULTS)} visible checks passing")
""")

md(r"""
---
## SECTION H — Knowledge Check

**H1 (Pre-watch #1 & #2 revisited)** Trace what goes wrong if `s = SMACrossoverStrategy(df_long["Close"], 50, 100); s.run(); s._fast = 20; s.summary()` bypasses your `@fast.setter` by mutating the private attribute `s._fast` directly. Why does Python convention prefix `_fast` and `_results` with a leading underscore? ✍️
**H2 Defend or reject** raising `RuntimeError` in `.summary()` before `.run()` vs having `.summary()` implicitly auto-call `.run()`. State one advantage of each contract and why explicit failure is safer while learning. ✍️
**H3 Single source of truth** Suppose Day 12 discovers a subtle bug in `performance_summary` (say `ddof=0` was used by mistake). Compare fixing that bug in **one place** (`pytrades/strategy.py`) vs fixing it across 7 copy-pasted notebooks and 2 classes. ✍️
**H4 Predict output** `s = SMACrossoverStrategy(p, 20, 50); df_out = s.run(); df_out["strategy_wealth"] = 999.0`. If `run()` forgot `.copy()` when returning `self._results`, what would a second call to `s.plot()` draw? ✍️
**H5 Challenge 4 reflection** Compare two ways to add a 3rd variant (`WMACrossoverStrategy`): (a) subclassing `BaseCrossoverStrategy` again vs (b) `CrossoverStrategy(prices, fast, slow, ma_fn=wma)`. Which scales cleaner to 10 indicator functions, and when would subclassing still win? ✍️
**H6 Bridge to Day 12** Up to today, `prices` arrived clean from bundled CSVs. Tomorrow `prices` arrives from an external JSON API (`Alpha Vantage` shape) with string numbers (`"182.5000"`), vendor column names (`"4. close"`), descending dates, and occasional `"Note": "Thank you for using Alpha Vantage! Our standard API call frequency is..."` rate-limit dictionaries. Which layer of `pytrades/` (`data.py`, `indicators.py`, or `strategy.py`) should absorb 100% of that mess so `SMACrossoverStrategy` never changes a single line? ✍️
""")

md(r"""
---
## SECTION I — Reflection & Retrieval Practice

### What I learned · Can implement unaided · Still difficult ✍️

### Retrieval — Days 10 (n−1), 08 (n−3), 05 (n−6)
1. **Day 10:** Why did our `test_strategy` take `prices` instead of calling `yf.download` inside, and how did `types.FunctionType` catch hidden notebook globals?
2. **Day 10:** Why does `sweep_sma_pairs` return the full table instead of returning only the "best" `(fast, slow)` tuple?
3. **Day 08:** On a `2,520`-row series, why does `SMACrossoverStrategy(prices, 50, 100).run()` have `2,420` rows rather than `2,421`?
4. **Day 05:** Why must correlation and covariance be computed on *returns* rather than *prices*, and how does covariance annualise vs correlation?
""")
code(r"""
# Closed-notebook retrieval: sketch a clean strategy class API FROM MEMORY
# (signatures + __init__ + run/summary guard contract) and justify ONE method in a docstring.
class MinimalCrossoverSketch:
    '''Sketch the public API (`__init__`, `run`, `summary`) from memory:
    `summary()` before `run()` must raise RuntimeError; `run()` caches on `self._results`.'''
    # TODO
    pass

try:
    _sk = MinimalCrossoverSketch(pd.Series([100., 105., 110., 115., 120.],
                                            index=pd.bdate_range("2022-01-03", periods=5)), 1, 2)
    _pre_raises = False
    try: _sk.summary()
    except RuntimeError: _pre_raises = True
    _sk.run()
    _ok = _pre_raises and isinstance(_sk.summary(), dict)
except Exception as exc:
    _ok = False; print("self-check raised:", type(exc).__name__, exc)
print("class lifecycle sketch self-check:", "PASS" if _ok else "not yet")
""")
md(r"""
### ✅ Completion checklist
- [ ] Video `02:26:30–02:51:00` watched; Challenge 4 implemented as `EMACrossoverStrategy`
- [ ] Ex 1–5 green (`11/11` checks in Section G), including `SMACrossoverStrategy.summary() == test_strategy()`
- [ ] `pytrades` v0.2 (`__version__ = "0.2.0"`) exports `SMACrossoverStrategy` & `EMACrossoverStrategy`
- [ ] **Fresh-kernel proof:** Restart & Run All executes Section F importing *only* from `pytrades`
- [ ] Inheritance-vs-composition trade-off justified in own words

**Send back:** Section G score · clean-kernel import output (`pytrades` v0.2) · your inheritance-vs-composition paragraph (E5/H5). Day 12 hardens `pytrades/data.py` against external vendor APIs.
""")

nb = new_notebook(cells=CELLS)
nb.metadata.update({"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                    "language_info": {"name": "python", "version": "3.11"},
                    "title": "Day 11 - Classes: Strategy Object & Challenge 4 (pytrades v0.2)",
                    "source_video": "https://www.youtube.com/watch?v=GDMkkmkJigw (02:26:30-02:51:00)"})
out = ROOT / "notebooks" / "Day_11_Classes_Importable_Strategy_Object.ipynb"
nbformat.write(nb, out); print("wrote", out, "cells=", len(CELLS))
