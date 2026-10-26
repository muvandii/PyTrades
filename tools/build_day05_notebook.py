"""Build Day 05 notebook. Instructor utility."""
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

# Day 05 — Loops, Correlation, Covariance & Heatmaps (+ Challenge 1)

| | |
|---|---|
| **Video segment** | **01:01:50–01:16:00** — *For loops* · *Correlation and Covariance* · *Heat map* · **Challenge 1** ([watch](https://www.youtube.com/watch?v=GDMkkmkJigw&t=3710s)) |
| **Estimated study time** | **2.5–3 hours** |
| **Prerequisites** | Milestone 1 gate passed; annualised volatility (Day 04) understood — today loops over it |
| **Data** | Bundled 3 tickers **plus 2 extra synthetic tickers (TECH, FOOD) generated in setup** = the video's "5 stocks" cast for Challenge 1, offline |
| **Expected deliverable** | **P1.1:** correlation report (matrix CSV + heatmap) ending in **one diversification claim you can defend with numbers** |

## Learning objectives
1. Compute per-ticker statistics with an **explicit `for` loop** and with **vectorised** pandas, and articulate when each wins.
2. Build a **returns matrix** (simple returns) — because correlation/covariance of *prices* is a trap you'll spring deliberately, then avoid forever.
3. Implement **correlation & covariance matrices** (optionally annualised covariance) and read a **heatmap** critically (diagonal, symmetry, NaN policy for BANK).
4. Execute the video's **Challenge 1** to a testable standard: for 5 stocks — annual risk per ticker + correlation & covariance matrices — then defend a diversification statement.
""")

md(r"""
---
## SECTION B — Video Learning · 01:01:50–01:16:00

**Pre-watch:** 1) Why loop over tickers if pandas can do all columns at once — what does the loop teach that vectorisation hides? 2) Two stocks both trend upward all year but zig-zag oppositely daily: price-correlation ≈? return-correlation ≈? 3) Covariance of returns is in what units? Why does correlation exist at all? 4) Guess Challenge 1's exact shopping list before he says it.

| Time | Chapter | Watch for |
|---|---|---|
| 01:01:50 | For loops | The pattern: `for ticker in tickers: ... collect result` — your Ex 1 hammers it into a function |
| 01:09:00 | Correlation and Covariance | Computed on **percentage-change returns**. If you miss that detail, Ex 3 diagnoses you |
| 01:10:20 | Heat map | Colour = correlation strength; annotate values or the picture is vibes |
| 01:15:00 | **Challenge 1** | Take 5 stocks: annual risk + correlation + covariance. Section F is this challenge, with acceptance tests the video never gave you |
| 01:16:00 | ⛔ STOP | Simple/log returns formalised on Day 06 |

Fallback: [01:01:50](https://www.youtube.com/watch?v=GDMkkmkJigw&t=3710s) · [01:15:00](https://www.youtube.com/watch?v=GDMkkmkJigw&t=4500s)
""")
code(r"""
# ▶️ SECTION B (code) - 01:01:50 to 01:16:00
from IPython.display import YouTubeVideo, display
display(YouTubeVideo("GDMkkmkJigw", start=3710, end=4560, width=800, height=450))
print("Fallback: https://www.youtube.com/watch?v=GDMkkmkJigw&t=3710s  (stop at 01:16:00)")
""")
md(r"""✍️ **My 3-bullet summary + Challenge 1 as I heard it (edit me):** - · - · Challenge 1 = …""")

md(r"""
---
## SECTION C — Concept Notes

### C1. Loop vs vectorised — both are tools, neither is a personality
A loop makes the per-ticker steps explicit and handles per-column quirks (BANK's shorter history) transparently; vectorised pandas is shorter and faster and lets the library handle alignment. Professional habit: **prototype with whichever is clearer; prove both agree** (today's tests force agreement).

### C2. The returns matrix is the unit of cross-asset work
Daily simple returns per ticker, dates in rows. From it flows: per-ticker σ (Day 04), correlation, covariance. NaN policy is a decision, not a detail: pairwise-complete (pandas default in `corr`) uses overlapping dates per pair — BANK pairs use Apr-onward only. State it every time.

### C3. Correlation vs covariance
Covariance measures joint movement in squared-return units — magnitude depends on each series' own volatility, hence hard to eyeball. Correlation rescales it to [−1, +1]: `corr = cov / (σ_x · σ_y)`. Diagonal is always 1.0 (a series vs itself); matrix is symmetric. **Prices** of two upward-trending stocks correlate ≈ +1 even if their daily returns are unrelated or opposite — trend is shared calendar, not co-movement. Returns strip the trend out.

### C4. Heatmaps communicate; matrices *decide*
Heatmap for human scanning (annotate numbers), matrix values for claims. "These two diversify each other" must cite their return-correlation over a stated window — colour adjectives don't count.

### C5. Annualising covariance [video-adjacent, flagged]
Daily-return covariance annualises ×252 (variance-like quantities scale with time, Day 04's √ logic squared). Correlation is unitless and is *not* annualised.
""")

code(SETUP_CODE + r"""

# Day 05 extension: grow the bundled 3 tickers to the video's 5-stock cast (synthetic, offline).
panel5 = close_panel.copy()
panel5["TECH"] = _one(999, 80.0, 0.0012, 0.022)["Close"]    # hot & volatile
panel5["FOOD"] = _one(555, 40.0, 0.0002, 0.006)["Close"]    # sleepy staple
print(panel5.shape, list(panel5.columns))
panel5.head(2)
""")

md(r"""
---
## SECTION D — Guided Exploration

### D1 — Spring the prices trap
**Predict:** `panel5.corr()` (prices!) DEMO–TECH vs their *returns* correlation: which is bigger, and which one means anything?
""")
md(r"""✍️ **D1 prediction (edit me):** """)
code(r"""
# D1
price_corr = panel5.corr(numeric_only=True)
rets5 = panel5.pct_change()
ret_corr = rets5.corr()
print("DEMO-TECH  price corr:", round(float(price_corr.loc["DEMO", "TECH"]), 3),
      "| return corr:", round(float(ret_corr.loc["DEMO", "TECH"]), 3))
print("mean off-diagonal |corr|  prices:", round(float(price_corr.where(~np.eye(5, dtype=bool)).abs().mean().mean()), 3),
      "| returns:", round(float(ret_corr.where(~np.eye(5, dtype=bool)).abs().mean().mean()), 3))
# TODO(modify): check ORNG-FOOD both ways. Write the one-sentence moral below.
""")
md(r"""
✍️ **D1 observed (edit me):** price correlations inflate towards _______ because both series share a _______.
Co-movement that matters for portfolios lives in _______.

### D2 — Loop it, then vectorise it. Same answer or it didn't happen.
**Predict:** annualised vol per ticker via your Day-04 formula in a loop vs `rets.std()*sqrt(252)` vectorised — identical? What if BANK's NaNs are handled differently in each?
""")
md(r"""✍️ **D2 prediction (edit me):** """)
code(r"""
# D2
loop_vol = {}
for t in panel5.columns:                                   # the video's loop shape, made explicit
    r = panel5[t].dropna().pct_change().dropna()
    loop_vol[t] = float(r.std(ddof=1) * np.sqrt(252))
vec_vol = (panel5.pct_change().std() * np.sqrt(252)).to_dict()
for t in panel5.columns:
    print(t, "loop:", round(loop_vol[t], 4), "| vectorised:", round(float(vec_vol[t]), 4))
# TODO(modify): add mean daily return to BOTH implementations. Which one was easier to extend? Say why in D2 observed.
""")
md(r"""
✍️ **D2 observed (edit me):** agreed to ___ decimal places. Loop cost me _______ lines; vectorised cost _______.
The loop's real advantage showed when _______ (think BANK).

### D3 — Read the heatmap like a sceptic
Run, then answer underneath: (a) most-correlated pair? (b) least? (c) why is the diagonal boring-but-useful as a sanity check?
""")
code(r"""
# D3 - seaborn if installed (video's tool), matplotlib fallback keeps today runnable anywhere
try:
    import seaborn as sns
    fig, ax = plt.subplots(figsize=(7, 5.5))
    sns.heatmap(ret_corr, annot=True, fmt=".2f", vmin=-1, vmax=1, cmap="coolwarm", ax=ax)
    ax.set_title("Return correlation, 5 synthetic tickers (pairwise, own overlaps)")
except ImportError:
    fig, ax = plt.subplots(figsize=(7, 5.5))
    im = ax.imshow(ret_corr.values, vmin=-1, vmax=1, cmap="coolwarm")
    ax.set_xticks(range(len(ret_corr.columns)), ret_corr.columns); ax.set_yticks(range(len(ret_corr.columns)), ret_corr.columns)
    for i in range(len(ret_corr.columns)):
        for j in range(len(ret_corr.columns)):
            ax.text(j, i, f"{ret_corr.values[i, j]:.2f}", ha="center", va="center")
    fig.colorbar(im); ax.set_title("Return correlation (matplotlib fallback; pip install seaborn for the video's version)")
plt.tight_layout(); plt.show()
print(ret_corr.round(3))
""")
md(r"""✍️ **D3 answers (edit me):** (a) … (b) … (c) diagonal: … Also: BANK's correlations used only dates from _______ (pairwise policy, C2).""")

md(r"""
---
## SECTION E — Independent Practice

### Exercise 1 — Basic: the loop, productised
""")
code(r"""
def loop_annualised_vols(panel, periods_per_year=252):
    '''Return {ticker: annualised_vol_float} computing per-ticker daily simple-return
    std (ddof=1) * sqrt(periods_per_year), iterating tickers with an explicit loop
    (the video's pattern). Use each ticker's own non-NaN span. A ticker with <3 valid
    prices -> ValueError.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>D2's guided loop, verbatim logic, new signature. Dict out, not prints.</details>
<details><summary>Hint 3 — clue</summary>Drop NaNs *before* pct_change per ticker (BANK gap!), then drop the first NaN return. Tests compare against the vectorised result on a panel with a late-start column — mismatch almost always means NaN handling diverged.</details>

### Exercise 2 — Modification: one returns function to feed them all
""")
code(r"""
def returns_matrix(panel, method="simple"):
    '''Daily returns matrix of a price panel. method="simple": pct_change.
    method="log": log(price / previous price). Any other method -> ValueError.
    Shape/index/columns preserved (first row NaN). Prices are NOT pre-cleaned:
    NaN propagation is pandas' - document that choice in one comment.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Day 06 goes deep on these; today you need them operational. Log returns = `np.log(panel / panel.shift(1))`.</details>
<details><summary>Hint 3 — clue</summary>Validate `method` *first* so typos fail fast. Tests check 100→110: simple = 0.10, log = ln(1.1) ≈ 0.09531 — and that the two are NOT equal.</details>

### Exercise 3 — Debugging: correlation that lies with a straight face

Diagnose the buggy function (one conceptual error, huge consequences), then implement the honest version.
""")
code(r"""
# --- BUGGY CODE (study; do not edit) ---
def correlation_matrix_buggy(panel):
    return panel.corr()                      # <-- spot it?

_up = pd.DataFrame({
    "UP1": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19.0],
    "UP2": [20, 22, 21, 24, 23, 26, 25, 28, 27, 30.0]},   # also trends up; daily moves ANTI-sync with UP1's steps
    index=pd.bdate_range("2021-01-04", periods=10))
print("buggy (prices) corr:", round(float(correlation_matrix_buggy(_up).loc["UP1", "UP2"]), 3),
      "| returns corr:", round(float(_up.pct_change().corr().loc["UP1", "UP2"]), 3))
""")
md(r"""✍️ **Diagnosis (edit me):** the bug is _______; shared _______ masquerades as _______; a portfolio built on it would believe … while daily reality is …""")
code(r"""
def correlation_of_returns(panel, method="simple"):
    '''Correlation matrix of the panel's daily RETURNS (via your returns_matrix).
    pandas pairwise-complete behaviour is the documented NaN policy - keep it,
    and say so in a comment.'''
    # TODO
    pass

def covariance_of_returns(panel, method="simple", annualise=False, periods_per_year=252):
    '''Covariance matrix of daily returns (via returns_matrix). If annualise=True,
    multiply by periods_per_year (C5). Correlation must NOT be annualised - there is
    deliberately no such switch on correlation_of_returns.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Both are one-liners once returns exist: the intellectual content is *which* matrix gets fed in, and the annualisation asymmetry between cov and corr.</details>

### Exercise 4 — Independent: find the diversifier
""")
code(r"""
def most_diversifying_pair(panel, method="simple"):
    '''Return (ticker_a, ticker_b, corr_float) for the pair with the LOWEST return
    correlation (most negative / closest to -1), ticker_a < ticker_b alphabetically.
    Ties: alphabetically first pair. Fewer than 2 tickers -> ValueError.
    Pairs whose correlation is NaN (no overlap) are ignored; if ALL pairs are NaN -> ValueError.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Only the strict upper triangle of the correlation matrix contains candidate pairs; diagonal is self-love, lower triangle is duplicates.</details>
<details><summary>Hint 2 — approach</summary>Loop `i<j` over columns (today's loop theme pays off), track the minimum, skip NaNs. Sorting tickers first makes ties deterministic.</details>
<details><summary>Hint 3 — clue</summary>np.isnan guard per pair. Tests use a 3-ticker frame where the answer is NOT the pair a price-correlation would pick.</details>

### Exercise 5 — Transfer: Challenge 1's risk column, generalised
""")
code(r"""
def annual_risk_table(panel, periods_per_year=252):
    '''DataFrame indexed by ticker with columns:
        mean_daily_return, daily_vol, annualised_vol
    (simple returns, own valid span per ticker, ddof=1). Sorted by annualised_vol
    DESCENDING. This is Challenge 1's "annual risk" deliverable as a reusable table.'''
    # TODO (loop or vectorised - but be able to say which you chose and why, H2)
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Ex 1 plus means, assembled as a table. If your loop and vectorised drafts disagree on BANK-shaped columns, your NaN policy drifted — reconcile before coding further.</details>
""")

md(r"""
---
## SECTION F — Mini-Project · P1.1 Challenge 1, To A Professional Standard

**The video's Challenge 1 (01:15:00), re-specified:** for our 5-stock panel, produce (i) annual risk per ticker, (ii) the return-correlation matrix, (iii) the covariance matrix — then defend **one** diversification claim.

### Specification — `build_correlation_report(panel, output_csv, method="simple")`
- Write the **correlation** matrix (of returns) to `output_csv` with ticker index header (round-trip readable like Day 02's artifacts; parents created).
- Return `{"most_diversifying": (a, b, corr), "most_correlated": (a, b, corr), "tickers": [...]}` where most_correlated = highest *off-diagonal* pair (same tie/NaN rules as Ex 4 — reuse logic, don't fork it).

**Then:** run on `panel5` → `data/processed/day05_correlation.csv`; heatmap it (D3 cell is your template); write the claim cell: "Pair (X,Y) diversifies best (corr=…, window=…, NaN policy=…), meaning …; the pair a naive price-correlation would have chosen is … and would mislead because …. What this does NOT prove: …"

**Acceptance:** G project check on unseen panel · claim cites a number, a window and a policy · "does NOT prove" sentence is present and true.
""")
code(r"""
def build_correlation_report(panel, output_csv, method="simple"):
    '''See Section F.'''
    # TODO
    pass
""")
code(r"""
# SECTION F (apply)
report = build_correlation_report(panel5, PROCESSED / "day05_correlation.csv")
print(report)
risk5 = None
try:
    risk5 = annual_risk_table(panel5); print(risk5.round(4))
except Exception as exc:
    print("annual_risk_table not ready yet:", type(exc).__name__)
""")
md(r"""✍️ **My defended diversification claim (edit me):** Pair … corr=… over … (policy: …). Meaning: … · Naive price-corr choice: … misleading because … · This does NOT prove: …""")

md(r"""---\n## SECTION G — Automated Assessment""")
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

_idx = pd.bdate_range("2021-01-04", periods=6)
PANEL = pd.DataFrame({
    "AAA": [100., 102, 101, 105, 103, 108],
    "BBB": [np.nan, np.nan, 50., 51, 49, 52],
    "CCC": [200., 198, 202, 197, 205, 200]}, index=_idx)

def _vec_vol(panel):
    return {t: float(panel[t].dropna().pct_change().dropna().std(ddof=1) * np.sqrt(252)) for t in panel.columns}
check("Ex1 loop vols match vectorised (incl. late-start BBB)", lambda: (
    lambda r, e: all(abs(r[k] - e[k]) < 1e-12 for k in e))(loop_annualised_vols(PANEL), _vec_vol(PANEL)))
check("Ex2 simple vs log first return (100->110)", lambda: (
    abs(float(returns_matrix(pd.DataFrame({"A": [100., 110.]}), "simple")["A"].iloc[1]) - 0.10) < 1e-12
    and abs(float(returns_matrix(pd.DataFrame({"A": [100., 110.]}), "log")["A"].iloc[1]) - np.log(1.1)) < 1e-12))
check("Ex2 bad method -> ValueError", lambda: raises(ValueError, lambda: returns_matrix(PANEL, "wat")))
check("Ex2 first row NaN, shape preserved", lambda: returns_matrix(PANEL).shape == PANEL.shape and bool(returns_matrix(PANEL).iloc[0].isna().all()))

_anti = pd.DataFrame({"UP1": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19.0],
                      "UP2": [20, 22, 21, 24, 23, 26, 25, 28, 27, 30.0]}, index=pd.bdate_range("2021-01-04", periods=10))
check("Ex3 corr is of RETURNS (anti-sync steps score < price corr)", lambda: (
    float(correlation_of_returns(_anti).loc["UP1", "UP2"]) < float(_anti.corr().loc["UP1", "UP2"]) - 0.3))
check("Ex3 cov annualise = daily x252; corr has no annualise", lambda: np.allclose(
    covariance_of_returns(_anti, annualise=True).values, covariance_of_returns(_anti).values * 252))
check("Ex3 diagonal == 1 and symmetric", lambda: (
    lambda c: np.allclose(np.diag(c), 1) and np.allclose(c.values, c.values.T, equal_nan=True))(correlation_of_returns(PANEL)))

check("Ex4 picks genuinely least-correlated pair", lambda: (
    lambda r: r[0] < r[1] and (r[0], r[1]) == min(
        [("AAA", "BBB"), ("AAA", "CCC"), ("BBB", "CCC")],
        key=lambda ab: (float(correlation_of_returns(PANEL).loc[ab[0], ab[1]]), ab)))(most_diversifying_pair(PANEL)))
check("Ex4 <2 tickers -> ValueError", lambda: raises(ValueError, lambda: most_diversifying_pair(PANEL[["AAA"]])))
check("Ex5 risk table sorted desc, values sane", lambda: (
    lambda r: list(r.columns) == ["mean_daily_return", "daily_vol", "annualised_vol"]
    and bool((r["annualised_vol"].diff().dropna() <= 1e-15).all())
    and abs(r.loc["AAA", "annualised_vol"] - _vec_vol(PANEL)["AAA"]) < 1e-12)(annual_risk_table(PANEL)))

def _proj():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "x" / "corr.csv"
        rep = build_correlation_report(PANEL, out)
        back = pd.read_csv(out, index_col=0)
        exp = correlation_of_returns(PANEL)
        return (rep["most_diversifying"][:2] == most_diversifying_pair(PANEL)[:2]
                and rep["most_correlated"][2] >= rep["most_diversifying"][2]
                and np.allclose(back.values, exp.values, equal_nan=True))
check("F project: corr CSV round-trips; extremes consistent with Ex4", _proj)
print(f"\nSCORE: {sum(RESULTS)}/{len(RESULTS)} visible checks passing")
""")

md(r"""
---
## SECTION H — Knowledge Check
**H1** Price-corr 0.98, return-corr 0.05 for a pair. In one paragraph: what happened, and which number belongs in a risk report? ✍️
**H2** Loop vs vectorised: give a concrete moment *today* where the loop version was easier to reason about, and one where vectorised was. ✍️
**H3 Defend** pairwise-complete correlation for BANK pairs — then attack it: what does mixing different windows per pair do to "the" matrix as a single object? ✍️
**H4** Why is there an annualise switch on covariance but never on correlation? Answer via units. ✍️
**H5** Your diversification claim's "does NOT prove" sentence: expand it — correlation is backward-looking how, and what regime change breaks it? ✍️
**H6 Design** Day 06 formalises log returns. Predict one algebraic property log returns have over multi-day horizons that simple returns lack (think: adding vs compounding). ✍️
""")

md(r"""
---
## SECTION I — Reflection & Retrieval Practice
### Learned · Can implement · Still difficult ✍️
### Retrieval — Days 04, 03, 01
1. Annualised vol formula, the √ assumption, and the input it must *never* receive raw.
2. Monthly bar: Open=__, High=__, Low=__, Close=__, Volume=__. The odd one out and why.
3. Normalising to first-valid vs `iloc[0]` — the BANK failure in one line.
4. `validate_ohlcv`'s monotonic + duplicates checks: which resample/returns disasters do they pre-empt?
5. A function that prints results instead of returning them fails which Milestone-1 criterion, and why do tests care?
""")
code(r"""
def annualised_volatility_from_memory(prices, periods_per_year=252):
    '''Day 04 Ex4 contract, FROM MEMORY: simple returns, ddof=1, x sqrt(periods).
    <3 valid prices -> ValueError.'''
    # TODO
    pass

try:
    _p = pd.Series([100.0, 110.0, 99.0, 108.9]); _exp = float(_p.pct_change().dropna().std() * np.sqrt(252))
    _ok = abs(annualised_volatility_from_memory(_p) - _exp) < 1e-12
except Exception as exc:
    _ok = False; print("self-check raised:", type(exc).__name__, exc)
print("Day-04 reimplementation self-check:", "PASS" if _ok else "not yet")
""")
md(r"""
### ✅ Completion checklist
- [ ] Video + Challenge 1 noted in own words · - [ ] D1 trap sprung and explained
- [ ] Ex 1–5 mine (loop actually loops) · - [ ] P1.1: CSV + heatmap + defended claim with window+policy
- [ ] G green after Restart & Run All · - [ ] Retrieval done unaided

**Send back:** G score · your diversification claim · H3 attack. Day 06 turns returns+indicators into the raw material of strategies.
""")

nb = new_notebook(cells=CELLS)
nb.metadata.update({"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                    "language_info": {"name": "python", "version": "3.11"},
                    "title": "Day 05 - Loops, Correlation, Covariance, Challenge 1",
                    "source_video": "https://www.youtube.com/watch?v=GDMkkmkJigw (01:01:50-01:16:00)"})
out = ROOT / "notebooks" / "Day_05_Loops_Correlation_Covariance_Challenge1.ipynb"
nbformat.write(nb, out); print("wrote", out, "cells=", len(CELLS))
