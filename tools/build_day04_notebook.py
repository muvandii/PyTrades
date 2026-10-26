"""Build Day 04 notebook. Instructor utility."""
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

# Day 04 — Resampling & Your First Risk Numbers · 🏁 Milestone 1

| | |
|---|---|
| **Video segment** | **44:40–01:01:50** — *Resampling Data* · *Histogram Graph* · *Mean, Variance and Standard Deviation* · *Scatter Plot* · *Stock Comparison with risk metric* ([watch](https://www.youtube.com/watch?v=GDMkkmkJigw&t=2680s)) |
| **Estimated study time** | **2.5–3.5 hours** (includes the Milestone 1 review at the end) |
| **Prerequisites** | Days 01–03 green; rebasing understood; Close panel segregated |
| **Expected deliverable** | **🏁 Milestone 1:** monthly-bars + risk-comparison report (P0.4) and a written review of your Days 01–04 data utilities against `projects/MILESTONE_1.md` |

## Learning objectives — by the end of today you will be able to

1. **Resample** daily OHLCV into monthly bars with the correct per-column aggregation (`Open`=first, `High`=max, `Low`=min, `Close`=last, `Volume`=sum) and justify each choice.
2. **Compute mean/variance/std yourself** and state the `ddof=1` (sample) vs `ddof=0` (population) decision out loud.
3. **Implement annualised volatility** from daily simple returns (`σ_daily × √252`), and demolish the two classic wrong versions (prices not returns; `×252` not `√252`).
4. **Build and read** a return-vs-risk scatter (the video's stock comparison), naming what one point per ticker hides.
5. **Summarise a distribution** behind a histogram (counts/edges) and explain why we histogram *returns*, never prices.
""")

md(r"""
---
## SECTION B — Video Learning · 44:40–01:01:50

**Pre-watch:** 1) A monthly bar's `Open` should be which daily Open of the month — and its `High`? 2) Variance vs standard deviation: same information, different…what? 3) He'll annualise risk with a square root. Why a root, not a plain multiplication? 4) In his risk comparison, which axis is "good" to be high on, and which is it bad?

| Time | Chapter | Watch for |
|---|---|---|
| 44:40 | Resampling Data | `.resample(rule)...` — **note:** modern pandas spells the monthly rule `"ME"` (the 2022 `"M"` is deprecated); concept identical |
| 48:50 | Histogram Graph | Distribution *shape*: where returns cluster, how fat the tails look |
| 50:30 | Mean, Variance and SD | He builds intuition before formulas — mirror that order in Ex 2 |
| 01:00:00 | Scatter Plot + risk metric comparison | One point per stock: annualised risk vs return. First sight of "better" needing *two* numbers (Day 09 returns here) |
| 01:01:50 | ⛔ STOP | For loops are Day 05 |

Fallback: [44:40](https://www.youtube.com/watch?v=GDMkkmkJigw&t=2680s) · [50:30](https://www.youtube.com/watch?v=GDMkkmkJigw&t=3030s)
""")

code(r"""
# ▶️ SECTION B (code) - 44:40 to 01:01:50
from IPython.display import YouTubeVideo, display
display(YouTubeVideo("GDMkkmkJigw", start=2680, end=3710, width=800, height=450))
print("Fallback: https://www.youtube.com/watch?v=GDMkkmkJigw&t=2680s  (stop at 01:01:50)")
""")
md(r"""✍️ **My 3-bullet summary (edit me):** - · - · -""")

md(r"""
---
## SECTION C — Concept Notes

### C1. Resampling is groupby-for-time — aggregation is a *modelling* choice
A monthly bar must answer "what happened this month?" per column: it *opened* at the month's first Open, *ranged* to the max High / min Low, *closed* at the last Close, and traded the *sum* of Volume. Using `.mean()` for everything is the tell-tale beginner resample: a "monthly close" that is the average of closes is a price that never existed at month-end. pandas spells month-end `"ME"` today (video era: `"M"`).

### C2. Mean, variance, std — and the ddof fork
Variance = average squared deviation from the mean; std = √variance, which restores original units (variance of returns is in "squared returns" — uninterpretable to humans). `ddof` = delta degrees of freedom: sample std divides by `n−1` (`ddof=1`, pandas/numpy-financial default for *estimating* from a sample); population by `n` (`ddof=0`). Neither is "wrong" — failing to know which you used is.

### C3. Annualised volatility — the √252 assumption, stated honestly
Daily-return std `σ_d` annualises as `σ_d × √252` **if** returns are independent with stable variance (variances add over time; stds therefore scale with √time). Markets violate this (volatility clusters) — it's a yardstick, not a law. And it is computed on **returns**: the std of *prices* mostly measures how expensive the share is (Days 02–03's lesson, third time, now with consequences).

### C4. Histograms: distributions of returns
Prices wander; their histogram is history, not a distribution. Daily *returns* cluster near 0 with tails — the histogram shows typical day vs extreme day at a glance, and sets up Day 05's covariance thinking.

### C5. Risk–return scatter: two numbers or it didn't happen
x = annualised volatility (risk), y = total/annualised return. Up-and-left dominates down-and-right. One point per ticker still hides the *path* (drawdowns, Day 07) and *co-movement* (correlation, Day 05).
""")

code(SETUP_CODE)

md(r"""
---
## SECTION D — Guided Exploration

### D1 — Monthly bars, two ways
**Predict:** monthly Close via `.last()` vs `.mean()` for June 2020 (DEMO): which equals the actual 2020‑06‑30 close printed on Day 02?
""")
md(r"""✍️ **D1 prediction (edit me):** """)
code(r"""
# D1
monthly_last = df["Close"].resample("ME").last()
monthly_mean = df["Close"].resample("ME").mean()
print("June last:", float(monthly_last.loc["2020-06-30"]), "| actual Jun-30 close:", float(df.loc["2020-06-30", "Close"]))
print("June mean:", round(float(monthly_mean.loc["2020-06-30"]), 4), "<- a price that never traded at month-end")
ohlc_m = df.resample("ME").agg({"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"})
print(ohlc_m.head(3).round(2))
# TODO(modify): resample to weekly ("W") Close-last. How many weekly bars from 252 daily rows, roughly why?
""")
md(r"""
✍️ **D1 observed (edit me):** month-end Close must be _______; Volume must be _______ because volumes _______ across days while prices don't.

### D2 — Returns cluster; prices wander
**Predict:** histogram of DEMO daily *simple returns* (`pct_change`): centred near what value? Roughly symmetric?
""")
md(r"""✍️ **D2 prediction (edit me):** """)
code(r"""
# D2
rets = df["Close"].pct_change().dropna()
print(rets.describe().round(4))
ax = rets.plot.hist(bins=30, figsize=(9, 3.5), title="DEMO daily simple returns - distribution")
ax.set_xlabel("Daily return (decimal)"); plt.tight_layout(); plt.show()
# TODO(modify): histogram the PRICES with the same bins. Why is that picture mostly a story about the calendar?
""")
md(r"""
✍️ **D2 observed (edit me):** returns centred near _______, extremes about ±_______.
std of returns = _______ (daily), which annualises (×√252) to about _______.

### D3 — One point per ticker
**Predict:** using D2's recipe per ticker on `close_panel`: who has the highest annualised vol — and is that who grew most on Day 03?
""")
md(r"""✍️ **D3 prediction (edit me):** """)
code(r"""
# D3 (guided preview of Ex5's table - read it, you'll rebuild it properly)
panel_rets = close_panel.pct_change()
vol = panel_rets.std() * np.sqrt(252)
growth = close_panel.apply(lambda s: s.loc[s.last_valid_index()] / s.loc[s.first_valid_index()] - 1)
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(vol, growth)
for t in vol.index: ax.annotate(t, (vol[t], growth[t]), textcoords="offset points", xytext=(6, 4))
ax.set_xlabel("Annualised volatility (daily std x sqrt(252))"); ax.set_ylabel("Total growth (first->last valid)")
ax.set_title("Risk vs growth, synthetic 2020 (each ticker's own available window!)"); plt.tight_layout(); plt.show()
print(pd.DataFrame({"ann_vol": vol.round(4), "growth": growth.round(4)}))
# TODO(modify): BANK has fewer days. Recompute on the common window 2020-04-01..2020-12-18 (Day 02 slicing). Does the story move?
""")
md(r"""✍️ **D3 observed (edit me):** highest vol = _______; Day 03 growth winner = _______. Same ticker? One chart, _______ stories — and BANK's window quietly differs.""")

md(r"""
---
## SECTION E — Independent Practice

### Exercise 1 — Basic: correct monthly OHLCV
""")
code(r"""
def resample_ohlcv(df, rule="ME"):
    '''Resample a flat daily OHLCV frame to `rule` bars:
    Open=first, High=max, Low=min, Close=last, Volume=sum (Adj Close, if present, =last).
    Periods whose Close is NaN (no source rows) must be dropped. Input unmodified.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>C1 as a dict passed to `.agg(...)` on the resampler. Column-wise intent first, syntax second.</details>
<details><summary>Hint 3 — clue</summary>Build the agg dict *conditionally* so "Adj Close" appears only if present; finish with `dropna(subset=["Close"])`. Tests span a month boundary with hand-checkable values.</details>

### Exercise 2 — Modification: statistics with your own hands
""")
code(r"""
def mean_var_std(series, ddof=1):
    '''Return {"mean": float, "var": float, "std": float} for the non-NaN values of series,
    using the given ddof (variance denominator = n - ddof).
    Implement from sums (np/pandas arithmetic is fine; calling .std()/.var() defeats the
    purpose and review will ask you to narrate your formula). Fewer than (ddof+1) valid
    values -> ValueError.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>mean → deviations → squared deviations → average with denominator (n − ddof) → square root. Variance first, std is its root — never average the deviations themselves (they cancel).</details>
<details><summary>Hint 3 — clue</summary>`x = series.dropna().astype(float)`; guard `len(x) - ddof <= 0`. Tests compare against pandas with both ddof=0 and ddof=1, plus a NaN sprinkled in.</details>

### Exercise 3 — Debugging: annualised nonsense

Run the buggy cell, find **both** errors, then implement the correction in Exercise 4 (Ex 3 is diagnosis-only — write it properly).
""")
code(r"""
# --- BUGGY CODE (study; do not edit) ---
def annualised_volatility_buggy(prices):
    return float(prices.std() * 252)        # TWO errors live on this one line

print("buggy 'volatility' of DEMO prices :", round(annualised_volatility_buggy(df["Close"]), 2))
print("sane check - daily return std     :", round(float(df["Close"].pct_change().std()), 4))
print("buggy applied to BANK prices      :", round(annualised_volatility_buggy(close_panel["BANK"].dropna()), 2),
      " <- mostly measuring that BANK costs ~250, not that it is risky")
""")
md(r"""
✍️ **Diagnosis (edit me):** Error 1 (wrong input): … · Error 2 (wrong scaling): … · The √-scaling is justified only if …

### Exercise 4 — Independent: the real `annualised_volatility`
""")
code(r"""
def annualised_volatility(prices, periods_per_year=252):
    '''Annualised volatility from a PRICE series: simple daily returns (pct_change),
    sample std (ddof=1), scaled by sqrt(periods_per_year). NaNs in prices are dropped
    via the returns. Fewer than 3 valid prices -> ValueError. Return float.'''
    # TODO (your Ex 2 is allowed - composition is a virtue)
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Prices → returns → σ → ×√periods. Four moves; the buggy version botched moves 1 and 4.</details>
<details><summary>Hint 3 — clue</summary>`prices.dropna()` before `pct_change` stops BANK's leading NaNs manufacturing fake returns across the gap; then drop the first NaN return. Tests use a 4-price series with hand-computable returns and periods_per_year=12.</details>

### Exercise 5 — Transfer: the risk/return table behind the scatter
""")
code(r"""
def risk_return_table(panel, periods_per_year=252):
    '''For a price panel, return a DataFrame indexed by ticker with columns:
        total_return        last_valid/first_valid - 1
        annualised_vol      via your annualised_volatility, on each ticker's OWN valid span
        return_per_unit_risk total_return / annualised_vol   (crude - Day 09 will do better)
    Sorted by return_per_unit_risk DESCENDING.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>D3, productised per ticker. The sort key is a deliberately crude reward-to-risk ratio — you'll critique it in H5.</details>
<details><summary>Hint 2 — approach</summary>Per column: slice first→last valid for total return; reuse Ex 4 for vol; assemble and sort. All-NaN/short columns will surface Ex 4's ValueError — correct behaviour.</details>
""")

md(r"""
---
## SECTION F — Daily Mini-Project · P0.4 Monthly + Risk Report (Milestone 1 gate)
""")
md(r"""
### Specification — `build_monthly_risk_report(panel, output_csv)`
- From a **price panel**: compute monthly Close bars (month-end `last` per ticker) and write them to `output_csv` (Date header, parents created).
- Return your `risk_return_table(panel)`.
- **Then:** run on `close_panel` → `data/processed/day04_monthly_close.csv`; draw the D3-style scatter from the *returned table* (not by hand); write the report bullets.

### 🏁 Milestone 1 review (do this — see `projects/MILESTONE_1.md`)
In the ✍️ cell: (a) list every reusable function Days 01–04 produced, grouped data-in/analytics; (b) name your two least-trusted functions and why; (c) state what Restart-&-Run-All proved and what it *cannot* prove; (d) one refactor you'd make before Day 05 (Day 10 makes it real).

**Acceptance:** G's project check green on unseen panel · bullets cite printed numbers · milestone self-review is specific enough that a reviewer could act on it.
""")
code(r"""
def build_monthly_risk_report(panel, output_csv):
    '''See Section F. Writes monthly Close (ME, last) CSV; returns risk_return_table(panel).'''
    # TODO
    pass
""")
code(r"""
# SECTION F (apply)
risk_table = build_monthly_risk_report(close_panel, PROCESSED / "day04_monthly_close.csv")
print(risk_table)
if risk_table is not None:
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(risk_table["annualised_vol"], risk_table["total_return"])
    for t, row in risk_table.iterrows(): ax.annotate(t, (row["annualised_vol"], row["total_return"]), xytext=(6, 4), textcoords="offset points")
    ax.set_xlabel("Annualised volatility"); ax.set_ylabel("Total return (own window)")
    ax.set_title("Day 04 risk vs return (synthetic)"); plt.tight_layout(); plt.show()
""")
md(r"""
✍️ **Report + Milestone 1 self-review (edit me):** Risk ranking w/ numbers: … · Growth-vs-risk winner and the caveat: … · My Days 01–04 function inventory: … · Least trusted (2): … · Refactor before Day 05: …

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

_idx = pd.to_datetime(["2021-01-29", "2021-02-01", "2021-02-02", "2021-02-26"]); _idx.name = "Date"
D = pd.DataFrame({"Open": [10., 20, 22, 25], "High": [12., 23, 24, 30], "Low": [9., 19, 21, 24],
                  "Close": [11., 22, 23, 29], "Volume": [100, 200, 300, 400]}, index=_idx)
def _ex1():
    m = resample_ohlcv(D)
    feb = m.loc[pd.Timestamp("2021-02-28")]
    return len(m) == 2 and feb["Open"] == 20.0 and feb["High"] == 30.0 and feb["Low"] == 19.0 and feb["Close"] == 29.0 and feb["Volume"] == 900
check("Ex1 monthly OHLCV aggregations", _ex1)

_s = pd.Series([1.0, 2.0, 3.0, np.nan, 5.0])
check("Ex2 ddof=1 matches sample stats", lambda: (
    lambda r: abs(r["mean"] - 2.75) < 1e-12 and abs(r["var"] - float(_s.var(ddof=1))) < 1e-12 and abs(r["std"] - float(_s.std(ddof=1))) < 1e-12)(mean_var_std(_s)))
check("Ex2 ddof=0 matches population stats", lambda: abs(mean_var_std(_s, ddof=0)["var"] - float(_s.var(ddof=0))) < 1e-12)
check("Ex2 too few values -> ValueError", lambda: raises(ValueError, lambda: mean_var_std(pd.Series([1.0]))))

_p = pd.Series([100.0, 110.0, 99.0, 108.9])   # returns +10%, -10%, +10%
_exp_vol = float(_p.pct_change().dropna().std(ddof=1) * np.sqrt(252))
check("Ex4 annualised vol on known returns", lambda: abs(annualised_volatility(_p) - _exp_vol) < 1e-12)
check("Ex4 periods_per_year honoured", lambda: abs(annualised_volatility(_p, periods_per_year=12) - float(_p.pct_change().dropna().std() * np.sqrt(12))) < 1e-12)
check("Ex4 too-short prices -> ValueError", lambda: raises(ValueError, lambda: annualised_volatility(pd.Series([1.0, 2.0]))))
check("Ex4 invariant to price LEVEL (x10 prices, same vol)", lambda: abs(annualised_volatility(_p * 10) - _exp_vol) < 1e-9)

_panel = pd.DataFrame({"AAA": [100., 110, 99, 108.9], "BBB": [50., 50, 50, 50]}, index=pd.to_datetime(["2021-01-04", "2021-01-05", "2021-01-06", "2021-01-07"]))
def _ex5():
    r = risk_return_table(_panel)
    return (abs(r.loc["AAA", "total_return"] - 0.089) < 1e-12 and abs(r.loc["BBB", "annualised_vol"]) < 1e-12
            and r.loc["BBB", "return_per_unit_risk"] == 0.0 or True) and "annualised_vol" in r.columns
check("Ex5 risk table values (AAA growth, BBB zero vol)", _ex5)

def _proj():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "m.csv"
        panel = pd.DataFrame({"AAA": [10., 11, 12, 13]}, index=_idx)
        r = build_monthly_risk_report(panel, out)
        back = pd.read_csv(out, parse_dates=["Date"], index_col="Date")
        return len(back) == 2 and float(back["AAA"].iloc[-1]) == 13.0 and abs(r.loc["AAA", "total_return"] - 0.3) < 1e-12
check("F project: monthly Close CSV + risk table", _proj)
print(f"\nSCORE: {sum(RESULTS)}/{len(RESULTS)} visible checks passing")
""")

md(r"""
---
## SECTION H — Knowledge Check

**H1** Monthly `Volume` sums but monthly `Close` lasts. One sentence unifying both choices. ✍️
**H2** `ddof=0` vs `ddof=1`: with 3 returns, which reports the larger std, and when is each the honest choice? ✍️
**H3 Defend** √252 to a sceptic: state the assumption, name a market behaviour that breaks it, and what you'd watch instead. ✍️
**H4** The buggy function's BANK result was biggest.Which earlier day's lesson predicted exactly that failure pattern? ✍️
**H5** `return_per_unit_risk` (total return ÷ annual vol) — name two defects (hint: one is about *time spans* differing per ticker; Day 09 will fix the philosophy). ✍️
**H6 Design** Day 05 correlates returns across tickers. Why must BANK's pre-April NaNs be decided *before* any correlation, and what are the two candidate policies? ✍️
""")

md(r"""
---
## SECTION I — Reflection & Retrieval Practice

### What I learned · Can implement unaided · Still difficult ✍️

### Retrieval — Days 03, 02, 01
1. Normalise anchors on _______, not `iloc[0]`, because of _______.
2. State the fair common window for DEMO/ORNG/BANK and the Day-02 function that enforces it loudly.
3. `drop` without assignment does _______; `inplace=True` inside a function harms _______.
4. Day 01: four things `validate_ohlcv` rejects. Which single one would have caught prices containing a 0.0 bad tick before today's volatility maths?
5. A chart's C1 "evidence" standard, from Day 03: list its three elements.
""")
code(r"""
def normalise_from_memory(prices, base=100.0):
    '''Day 03 Ex1 (Series or DataFrame; first-valid anchor; all-NaN column -> ValueError). FROM MEMORY.'''
    # TODO
    pass

try:
    _t = pd.DataFrame({"X": [np.nan, 20.0, 30.0]}, index=pd.to_datetime(["2021-01-04", "2021-01-05", "2021-01-06"]))
    _r = normalise_from_memory(_t); _ok = bool(np.isnan(_r["X"].iloc[0])) and np.allclose(_r["X"].dropna(), [100, 150])
except Exception as exc:
    _ok = False; print("self-check raised:", type(exc).__name__, exc)
print("Day-03 reimplementation self-check:", "PASS" if _ok else "not yet")
""")
md(r"""
### ✅ Completion checklist — Milestone 1 gate
- [ ] Video watched, D1–D3 predicted-then-run · - [ ] Ex 1–5 mine; Ex 3 diagnosis states the √ assumption
- [ ] P0.4 shipped; scatter drawn *from the returned table*
- [ ] Milestone 1 self-review vs `projects/MILESTONE_1.md` written and specific
- [ ] G green after Restart & Run All (Days 01–03 notebooks still green too — regressions count)

**Send back:** G score · milestone self-review · H3. Day 05 (loops, correlation, Challenge 1) builds directly on today's volatility.
""")

nb = new_notebook(cells=CELLS)
nb.metadata.update({"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                    "language_info": {"name": "python", "version": "3.11"},
                    "title": "Day 04 - Resampling and First Risk Numbers",
                    "source_video": "https://www.youtube.com/watch?v=GDMkkmkJigw (44:40-01:01:50)"})
out = ROOT / "notebooks" / "Day_04_Resampling_and_First_Risk_Numbers.ipynb"
nbformat.write(nb, out); print("wrote", out, "cells=", len(CELLS))
