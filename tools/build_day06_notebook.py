"""Build Day 06 notebook. Instructor utility."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _day_setup import SETUP_CODE
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

ROOT = Path(__file__).resolve().parents[1]
CELLS = []
def md(t): CELLS.append(new_markdown_cell(t.strip("\n")))
def code(t): CELLS.append(new_code_cell(t.strip("\n")))

md(r"""
## SECTION A — Learning Mission

# Day 06 — Returns Done Properly & Moving Averages (+ Challenge 2)

| | |
|---|---|
| **Video segment** | **01:16:00–01:35:00** — *Simple and Log returns* · *Creating Moving averages data* · **Challenge 2** ([watch](https://www.youtube.com/watch?v=GDMkkmkJigw&t=4560s)) |
| **Estimated study time** | **2.5–3 hours** |
| **Prerequisites** | Day 05 returns matrix (operational); today we make returns *conceptual* and add trend indicators |
| **Expected deliverable** | **P1.2:** indicator frame (Close, SMAs, EMA, log returns) for a ticker + Challenge 2 charts with a **written, falsifiable signal idea — explicitly NOT a backtest yet** |

## Learning objectives
1. Compute **simple** and **log** returns, convert between them (`log = ln(1+simple)`, `simple = e^log − 1`), and explain the first-row NaN and why log returns *add* over time while simple returns *compound*.
2. Implement **SMA** via rolling windows with correct warm-up (`window-1` leading NaNs when `min_periods=window`) and state what `min_periods` trades away.
3. Implement **EMA** via `ewm(span=...)` and explain in one sentence how its weighting differs from SMA's.
4. Spot (and refuse) the two silent cheating devices in indicator code: `center=True` windows and `shift(-1)` "returns".
5. Complete Challenge 2's spirit: moving-average charts per ticker and a signal *hypothesis* stated precisely enough that Day 08 can test it.
""")

md(r"""
---
## SECTION B — Video Learning · 01:16:00–01:35:00

**Pre-watch:** 1) Price goes 100 → 110 → 100. Simple returns: +10%, then…? Do they sum to the total? Now log returns? 2) A 50-day SMA's first value appears on which row? 3) EMA vs SMA on a sudden spike: who reacts faster, and is "faster" always better? 4) Predict Challenge 2.

| Time | Chapter | Watch for |
|---|---|---|
| 01:16:00 | Simple and Log returns | `np.log(price / price.shift(1))` — the video's returns for strategy work are *log* returns |
| 01:23:00 | Creating Moving averages data | `rolling(window=...).mean()`, the NaN warm-up, `min_periods`, SMA50/SMA200 on SPY, then EMA via `ewm(span=...)` |
| 01:32:15 | **Challenge 2** | Your 5 Challenge-1 stocks: plot price with 50 & 200-day MAs and *look for a signal idea*. Our bundled history is ~1 year, so Section F adapts windows honestly (20/50 primary; 200 attempted & discussed) — window *lengths* adapt, the skill doesn't |
| 01:35:00 | ⛔ STOP | Reindexing is Day 07 |

Fallback: [01:16:00](https://www.youtube.com/watch?v=GDMkkmkJigw&t=4560s) · [01:23:00](https://www.youtube.com/watch?v=GDMkkmkJigw&t=4980s) · [Challenge 2 ~01:32:15](https://www.youtube.com/watch?v=GDMkkmkJigw&t=5535s)
""")
code(r"""
# ▶️ SECTION B (code) - 01:16:00 to 01:35:00
from IPython.display import YouTubeVideo, display
display(YouTubeVideo("GDMkkmkJigw", start=4560, end=5700, width=800, height=450))
print("Fallback: https://www.youtube.com/watch?v=GDMkkmkJigw&t=4560s  (stop at 01:35:00)")
""")
md(r"""✍️ **3-bullet summary + Challenge 2 as assigned (edit me):** - · - · Challenge 2 = …""")

md(r"""
---
## SECTION C — Concept Notes

### C1. Two returns, two algebras
Simple: `P_t/P_{t-1} − 1` — what your wallet experiences per period; multi-period totals **compound**: `∏(1+r) − 1`. Log: `ln(P_t/P_{t-1})` — slightly smaller magnitude, symmetric (up 10% then down "10%" in log terms returns to start), and **additive over time**: sum of daily log returns = the whole period's log return. That's why quant code (video included) aggregates in log space, then converts back with `e^x − 1` for humans. First row has no predecessor → NaN, forever, deal with it explicitly.

### C2. SMA: a window with a memory cliff
`rolling(window=N).mean()`: each value is the mean of the last N closes including today. Until N observations exist you get NaN (that's `min_periods=N`, the honest default we'll require). `min_periods < N` starts early using partial windows — a *different statistic* wearing the same name. Every point in the window weighs equally; a price N+1 days old weighs zero. Cliff, not fade.

### C3. EMA: same job, fading memory
`ewm(span=N).mean()`: exponentially decaying weights — recent days matter more, nothing ever fully reaches zero. For a given N it hugs price closer (and whipsaws more) than SMA. pandas' `adjust=True` default normalises weights over the observed past; the video uses defaults, so do we — but say so.

### C4. The two cheating devices (memorise them)
`rolling(..., center=True)` puts *future* prices inside today's average. `pct_change` with `shift(-1)` computes tomorrow's return but labels it today. Both make backtests look clairvoyant; both are **look-ahead bias** — the original sin Day 08 will exorcise with `shift(+1)` *positions*. If code containing either appears in your work, tests and reviewers treat it as a failed day.

### C5. An indicator is not a strategy
"Price above its 50-day average" is a *measurement*. A strategy additionally specifies action, timing (when do you transact, at what price?), sizing and exit. Today ends at a precisely stated hypothesis; Day 08 adds the rest honestly.
""")

code(SETUP_CODE)

md(r"""
---
## SECTION D — Guided Exploration

### D1 — Additivity, demonstrated
**Predict:** sum of DEMO's daily log returns vs `ln(last/first)`: equal? And sum of simple returns vs `last/first − 1`?
""")
md(r"""✍️ **D1 prediction (edit me):** """)
code(r"""
# D1
p = df["Close"]
log_r = np.log(p / p.shift(1)); simple_r = p.pct_change()
print("sum(log)        :", round(float(log_r.sum()), 6), "| ln(last/first):", round(float(np.log(p.iloc[-1] / p.iloc[0])), 6))
print("sum(simple)     :", round(float(simple_r.sum()), 4), "| actual total  :", round(float(p.iloc[-1] / p.iloc[0] - 1), 4),
      "| compound check:", round(float((1 + simple_r).prod() - 1), 4))
# TODO(modify): verify exp(sum(log)) - 1 also gives the actual total. Three roads, one truth: which breaks if a NaN sneaks in?
""")
md(r"""
✍️ **D1 observed (edit me):** log returns _______ over time; simple returns _______.
The video sums log returns for strategy performance because _______.

### D2 — Warm-up rows are information
**Predict:** `rolling(20).mean()` on 252 closes: how many NaNs? With `min_periods=1`?
""")
md(r"""✍️ **D2 prediction (edit me):** """)
code(r"""
# D2
sma20 = p.rolling(window=20).mean()
sma20_eager = p.rolling(window=20, min_periods=1).mean()
print("NaNs default:", int(sma20.isna().sum()), "| NaNs min_periods=1:", int(sma20_eager.isna().sum()))
print("first eager value:", float(sma20_eager.iloc[0]), "= mean of just ___ observation(s) - same name, different statistic")
ax = p.plot(figsize=(10, 4), label="Close")
p.rolling(20).mean().plot(ax=ax, label="SMA20"); p.rolling(50).mean().plot(ax=ax, label="SMA50")
p.ewm(span=20, min_periods=20).mean().plot(ax=ax, label="EMA20")
ax.set_title("DEMO Close with SMA20/SMA50/EMA20"); ax.legend(); plt.tight_layout(); plt.show()
# TODO(modify): which line reacts first after sharp moves - SMA20 or EMA20? Point at a date as evidence.
""")
md(r"""
✍️ **D2 observed (edit me):** warm-up NaNs = _______ for window N. `min_periods=1` fabricates _______-observation "averages". EMA20 hugs price _______ than SMA20 because its weights _______.

### D3 — Spring the cheating devices on purpose
""")
code(r"""
# D3 - look-ahead, caught in the act on a tiny series
tiny = pd.Series([10., 10, 10, 100, 10], index=pd.bdate_range("2021-01-04", periods=5))
honest = tiny.rolling(3).mean(); centred = tiny.rolling(3, center=True).mean()
print(pd.DataFrame({"price": tiny, "rolling(3) honest": honest, "center=True (cheats)": centred}))
print("\nAt index 2021-01-06 the centred average already 'knows' about the 100 print on 2021-01-07.")
# TODO(modify): compute tiny.pct_change() vs tiny.pct_change().shift(-1) - which row claims the +900% return, and when could you have traded on it?
""")
md(r"""✍️ **D3 law (write it as your own rule):** an indicator stamped at date t may only use …""")

md(r"""
---
## SECTION E — Independent Practice

### Exercise 1 — Basic: both returns, exact contracts
""")
code(r"""
def simple_returns(prices):
    '''Simple returns of a Series or DataFrame (pct_change semantics).
    First row NaN; index/columns preserved; input unmodified.'''
    # TODO
    pass

def log_returns(prices):
    '''Log returns ln(P_t / P_{t-1}) of a Series or DataFrame. First row NaN.
    Any non-positive price anywhere -> ValueError (log of <=0 is not a return,
    it is a data crime - connect this to Day 01 in a comment).'''
    # TODO
    pass

def simple_to_log(r_simple):
    '''Element-wise ln(1 + r). Values <= -1 -> ValueError (total loss or worse has no log).'''
    # TODO
    pass

def log_to_simple(r_log):
    '''Element-wise exp(r) - 1 (the exact inverse of simple_to_log).'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>C1's four formulas. Guards first, maths second: check the *input domain* (prices > 0; simple returns > −1) before logarithms turn bad data into silent NaN/inf.</details>
<details><summary>Hint 3 — clue</summary>Domain checks that work for both Series and DataFrame: `(prices <= 0).any()` returns a Series for frames — use `.values.any()` or `np.any(...)`. Tests: round-trip log→simple recovers inputs; 100→110 values; zero price raises.</details>

### Exercise 2 — Modification: SMA with honest warm-up
""")
code(r"""
def sma(prices, window):
    '''Simple moving average of a Series or DataFrame. min_periods == window, always
    (no partial-window statistics). window must be an int >= 1 else ValueError.
    window=1 must return the input values unchanged.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>`rolling(window=window, min_periods=window).mean()` after validation. `isinstance(window, (int, np.integer))` — and remember `bool` is an int subclass (True is not a window; reject it if you're feeling rigorous).</details>

### Exercise 3 — Debugging: find both cheating devices
""")
code(r"""
# --- BUGGY/CHEATING CODE (study; do not edit) ---
def cheating_signal_frame(prices):
    out = prices.to_frame("Close")
    out["SMA10"] = prices.rolling(10, center=True).mean()          # device 1
    out["next_ret"] = prices.pct_change().shift(-1)                 # device 2 (innocently named!)
    out["signal"] = (out["Close"] > out["SMA10"]).astype(int)
    return out

_demo = cheating_signal_frame(df["Close"].head(30))
print(_demo.loc[_demo["next_ret"].abs().nlargest(3).index].round(4))
print("\nNote where the biggest 'next_ret' sits relative to its own date stamp.")
""")
md(r"""✍️ **Diagnosis (edit me):** Device 1 uses future … via … · Device 2 labels … as … · A backtest fed `signal * next_ret` would report … because …
""")
code(r"""
def ema(prices, span):
    '''Exponential moving average via ewm(span=span, min_periods=span) with pandas
    default adjust (state it in a comment - the video uses defaults).
    Series or DataFrame. span int >= 1 else ValueError.'''
    # TODO (your honest indicator, as penance)
    pass
""")

md(r"""
### Exercise 4 — Independent: crossover *signal* (still not a strategy)
""")
code(r"""
def crossover_signal(prices, fast=20, slow=50):
    '''Return a Series named "signal" of ints: 1 where sma(fast) > sma(slow), else 0.
    Rows where either SMA is NaN (warm-up) must be 0 - you cannot be "in" on an
    indicator that did not exist yet. fast < slow required, else ValueError.
    NOTE: this returns the SIGNAL on date t using data up to t. It must NOT shift -
    Day 08 is where positions get shifted for tradability; conflating them here fails tests.'''
    # TODO (compose your sma)
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Comparison of two alignments: NaN comparisons yield False in pandas boolean contexts *after* you handle dtype — be explicit: compute both SMAs, compare, fill warm-up with 0, cast int.</details>
<details><summary>Hint 3 — clue</summary>`(fast_sma > slow_sma).fillna(False).astype(int)` gets warm-up rows right. Resist adding `.shift(1)` — the docstring (and Day 08) explains why that would be a *different* function.</details>

### Exercise 5 — Transfer: rolling volatility (indicators compose)
""")
code(r"""
def rolling_volatility(prices, window=20, periods_per_year=252):
    '''Rolling annualised volatility of a price Series: rolling(window) sample std of
    LOG returns, times sqrt(periods_per_year). min_periods=window on the returns
    (so the first value lands `window` rows after the first return). Uses your
    log_returns - its ValueError on bad prices is desired behaviour here.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Day 04's volatility, windowed: returns first (252→251 values), then rolling std. Total NaN lead-in on the price index = window rows (1 return-NaN + window−1 more) — tests check exactly where the first number lands.</details>
""")

md(r"""
---
## SECTION F — Mini-Project · P1.2 Indicator Frame + Challenge 2 (adapted)

### Specification — `build_indicator_frame(prices, fast=20, slow=50)`
Return a DataFrame (input = price **Series**) with columns in order:
`Close`, `SMA{fast}` (e.g. `SMA20`), `SMA{slow}`, `EMA{fast}`, `log_returns`, `signal` —
composed *only* from today's functions.

**Then (Challenge 2, adapted):** for **DEMO and ORNG**: plot Close + SMA20 + SMA50 (labelled, Day-03 standard); *attempt* SMA200 for DEMO and for BANK and report what the data can/can't support (BANK has 188 valid closes — what does SMA200 owe you?); write your **signal hypothesis** in the cell below, e.g. "Being long only while SMA20>SMA50 would have avoided the worst drawdowns in … because …", with **two dated episodes** from your charts as evidence *for* and **one** whipsaw episode *against*.

**Acceptance:** G project check (column order/values vs recomputation) · hypothesis cites dates · the words "this is not yet a backtest because …" completed correctly (no positions/costs/timing yet).
""")
code(r"""
def build_indicator_frame(prices, fast=20, slow=50):
    '''See Section F. Column order: Close, SMA{fast}, SMA{slow}, EMA{fast}, log_returns, signal.'''
    # TODO
    pass
""")
code(r"""
# SECTION F (apply)
try:
    ind = build_indicator_frame(df["Close"])
    print(ind.dropna().head(3).round(4)); print("signal=1 days:", int(ind["signal"].sum()), "of", len(ind))
    ax = ind[["Close", "SMA20", "SMA50"]].plot(figsize=(10, 4), title="DEMO Close + SMA20/50 (synthetic 2020)")
    ax.set_ylabel("Price"); plt.tight_layout(); plt.show()
    _b = close_panel["BANK"]
    print("BANK valid closes:", int(_b.notna().sum()), "| SMA200 possible?", int(_b.notna().sum()) >= 200)
except Exception as exc:
    print("indicator frame not ready yet:", type(exc).__name__, exc)
""")
md(r"""✍️ **Signal hypothesis (edit me):** Hypothesis: … · Evidence for (2 dated episodes): … · Evidence against/whipsaw: … · This is not yet a backtest because …""")

md(r"""---\n## SECTION G — Automated Assessment""")
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

_idx = pd.bdate_range("2021-01-04", periods=5)
P = pd.Series([100., 110, 99, 102, 105], index=_idx, name="Close")
check("Ex1 simple returns values + first NaN", lambda: (
    bool(np.isnan(simple_returns(P).iloc[0])) and np.allclose(simple_returns(P).dropna(), [0.10, -0.10, 102/99-1, 105/102-1])))
check("Ex1 log returns additivity (sum == ln(last/first))", lambda: abs(float(log_returns(P).sum()) - np.log(105/100)) < 1e-12)
check("Ex1 conversions are exact inverses", lambda: np.allclose(
    log_to_simple(simple_to_log(simple_returns(P).dropna())), simple_returns(P).dropna()))
check("Ex1 non-positive price -> ValueError", lambda: raises(ValueError, lambda: log_returns(pd.Series([10., 0.0, 5.]))))
check("Ex1 simple<=-1 -> ValueError in simple_to_log", lambda: raises(ValueError, lambda: simple_to_log(pd.Series([-1.0]))))
check("Ex1 DataFrame support", lambda: np.allclose(log_returns(P.to_frame()).iloc[1, 0], np.log(1.1)))

check("Ex2 sma window=3 warm-up & values", lambda: (
    lambda r: bool(r.iloc[:2].isna().all()) and abs(r.iloc[2] - (100+110+99)/3) < 1e-12)(sma(P, 3)))
check("Ex2 sma window=1 is identity", lambda: np.allclose(sma(P, 1), P))
check("Ex2 window=0/-1/2.5 -> ValueError", lambda: all(raises(ValueError, lambda w=w: sma(P, w)) for w in (0, -1, 2.5)))

check("Ex3(ema) matches pandas ewm span=3 min_periods=3", lambda: np.allclose(
    ema(P, 3).dropna(), P.ewm(span=3, min_periods=3).mean().dropna()))
check("Ex3(ema) warm-up count = span-1", lambda: int(ema(P, 3).isna().sum()) == 2)

_up_down = pd.Series([100.]*10 + [110.]*10 + [90.]*10, index=pd.bdate_range("2021-01-04", periods=30))
def _ex4():
    s = crossover_signal(_up_down, fast=3, slow=5)
    return s.name == "signal" and set(s.unique()) <= {0, 1} and s.iloc[12] == 1 and s.iloc[18] == 0 and s.iloc[27] == 0 and int(s.iloc[:4].sum()) == 0
check("Ex4 signal: warm-up 0, in during up-transition, 0 when SMAs equal/low", _ex4)
check("Ex4 fast>=slow -> ValueError", lambda: raises(ValueError, lambda: crossover_signal(P, fast=50, slow=20)))
check("Ex4 signal is NOT shifted (uses t data at t)", lambda: (
    lambda s: s.iloc[12] == 1)(crossover_signal(_up_down, fast=3, slow=5)))

def _ex5():
    rv = rolling_volatility(P, window=2, periods_per_year=252)
    exp = log_returns(P).rolling(2, min_periods=2).std(ddof=1) * np.sqrt(252)
    return np.allclose(rv.dropna(), exp.dropna()) and rv.first_valid_index() == _idx[2]
check("Ex5 rolling vol values + first-valid lands at row window", _ex5)

def _proj():
    f = build_indicator_frame(_up_down, fast=3, slow=5)
    return (list(f.columns) == ["Close", "SMA3", "SMA5", "EMA3", "log_returns", "signal"]
            and np.allclose(f["SMA3"].dropna(), sma(_up_down, 3).dropna())
            and np.allclose(f["log_returns"].dropna(), log_returns(_up_down).dropna())
            and int(f["signal"].iloc[12]) == 1)
check("F project: indicator frame columns/order/values", _proj)
print(f"\nSCORE: {sum(RESULTS)}/{len(RESULTS)} visible checks passing")
""")

md(r"""
---
## SECTION H — Knowledge Check
**H1** Price: 100 → 110 → 100. Compute both simple returns, both log returns, and show exactly which algebra (sum vs compound) recovers the round trip for each. ✍️
**H2** Why is `min_periods=window` the honest default? Describe the statistic `min_periods=1` computes at row 2 of a "200-day" average. ✍️
**H3 Defend/refute:** "EMA20 is better than SMA20 because it reacts faster." Two sentences minimum; use the word *whipsaw*. ✍️
**H4** `center=True` in a *purely descriptive* chart (no trading) — cheating or legitimate? Draw the line precisely. ✍️
**H5** Your `crossover_signal` must not shift. Explain what Day 08 adds and why baking the shift in here would corrupt both today's tests and tomorrow's reasoning. ✍️
**H6 Design** BANK cannot have an SMA200 in our data. List three honest responses (data, window, exclusion) and pick one for the capstone with a reason. ✍️
""")

md(r"""
---
## SECTION I — Reflection & Retrieval Practice
### Learned · Can implement · Still difficult ✍️
### Retrieval — Days 05, 04, 02
1. Correlation belongs on _______ not _______; the spurious-price mechanism is shared _______.
2. Covariance annualises ×____, volatility ×____, correlation ×____. Justify via units.
3. Monthly Close aggregation = ____; the video-era "M" vs modern "ME" — concept same/different?
4. Day-02: the artifact standard (a saved CSV must reload to what three properties?)
5. Pairwise NaN policy in `corr`: BANK–DEMO correlation effectively covers which dates?
""")
code(r"""
def log_returns_from_memory(prices):
    '''ln(P_t/P_{t-1}), Series or DataFrame, first row NaN, non-positive -> ValueError. FROM MEMORY.'''
    # TODO
    pass

try:
    _p = pd.Series([100.0, 110.0, 99.0]); _r = log_returns_from_memory(_p)
    _ok = bool(np.isnan(_r.iloc[0])) and np.allclose(_r.dropna(), [np.log(1.1), np.log(0.9)])
except Exception as exc:
    _ok = False; print("self-check raised:", type(exc).__name__, exc)
print("log_returns reimplementation self-check:", "PASS" if _ok else "not yet")
""")
md(r"""
### ✅ Completion checklist
- [ ] Video, D1–D3 laws written in own words · - [ ] Ex 1–5 mine; both cheating devices named in Ex 3 diagnosis
- [ ] P1.2 + Challenge-2 charts; hypothesis has dated for/against evidence · - [ ] G green after Restart & Run All

**Send back:** G score · your hypothesis cell · H5. Day 07 (alignment, cumulative returns, drawdowns — Milestone 2) completes Week 1.
""")

nb = new_notebook(cells=CELLS)
nb.metadata.update({"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                    "language_info": {"name": "python", "version": "3.11"},
                    "title": "Day 06 - Returns and Moving Averages",
                    "source_video": "https://www.youtube.com/watch?v=GDMkkmkJigw (01:16:00-01:35:00)"})
out = ROOT / "notebooks" / "Day_06_Returns_and_Moving_Averages.ipynb"
nbformat.write(nb, out); print("wrote", out, "cells=", len(CELLS))
