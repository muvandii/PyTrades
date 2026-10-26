"""Build Day 03 notebook. Instructor utility."""
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

# Day 03 — Visualisation, Normalisation & Creating Data

| | |
|---|---|
| **Video segment** | **23:00–44:40** — *Data visualization and graphs* · *Normalization* · *Making changes and creating new data* · *Deleting Data* ([watch](https://www.youtube.com/watch?v=GDMkkmkJigw&t=1380s)) |
| **Estimated study time** | **2–3 hours** (today's video is the longest so far — it is mostly keyboard time, pause often) |
| **Prerequisites** | Days 01–02 green: validated frames, CSV round-trips, `.loc` segregation of the Close panel |
| **Expected deliverable** | **P0.3:** normalised (=100) comparison of all 3 tickers — CSV + labelled chart + interpretation a stranger could audit |

## Learning objectives — by the end of today you will be able to

1. **Plot** a price panel with title/axis labels/legend via a reusable function that returns a `matplotlib` Axes (testable, not just pretty).
2. **Normalise** prices to a common base using each column's **first valid** value — and explain, with BANK as evidence, why the video's `iloc[0]` version breaks on late-listing tickers.
3. **Create derived columns** (e.g. daily `Range`, `RangePct`, `Body`) on a copy, and **drop** columns/rows without ever mutating the caller's frame.
4. **Explain** why a raw-price multi-ticker chart is analytically useless but a rebased chart is a fair *growth* comparison — and what even the rebased chart still hides (risk).
""")

md(r"""
---
## SECTION B — Video Learning · 23:00–44:40

**Pre-watch questions** (checked in Section H):
1. Three price lines start at 7.5, 28 and 100+ on one chart. Which stock "won"? Why is the chart unable to tell you?
2. He normalises with `close.div(close.iloc[0]).mul(100)`. What exactly does `iloc[0]` give him for a *panel* — and what happens if one ticker's first cell is NaN (our BANK)?
3. When he creates new data/columns, does the original frame change? How would you check?
4. `drop(...)` without assignment — has anything actually been deleted?

| Time | Chapter | Pay attention to |
|---|---|---|
| 23:00 | Data visualization and graphs | `close.plot(figsize=..., fontsize=...)`, `plt.legend`, `plt.show` — and the ugly truth that different start prices make lines incomparable |
| 26:00 | Normalization | `div(iloc[0])` then `mul(100)`; one ticker first, then the whole panel in one vectorised move |
| 30:00 | Making changes and creating new data | New columns from old ones; you are manufacturing features now, not just loading them |
| 42:00 | Deleting Data | `drop` semantics: returns a new object unless told otherwise |
| 44:40 | ⛔ STOP | Resampling is Day 04 |

Fallback: [23:00](https://www.youtube.com/watch?v=GDMkkmkJigw&t=1380s) · [26:00](https://www.youtube.com/watch?v=GDMkkmkJigw&t=1560s)
""")

code(r"""
# ▶️ SECTION B (code) - 23:00 to 44:40
from IPython.display import YouTubeVideo, display
display(YouTubeVideo("GDMkkmkJigw", start=1380, end=2680, width=800, height=450))
print("Fallback: https://www.youtube.com/watch?v=GDMkkmkJigw&t=1380s  (stop at 44:40)")
""")

md(r"""✍️ **My 3-bullet summary (edit me):** - · - · -""")

md(r"""
---
## SECTION C — Concept Notes

### C1. A chart is an argument — labels are its evidence
An unlabelled line could be anything. Minimum professional standard (already modelled on Day 01): **title saying what/when, y-label with the quantity, x is dates, legend naming every line.** Today that standard becomes a *function* so it can be tested and reused.

### C2. Normalisation = re-basing, not magic
`normalised = price / first_price × base`. Every series starts at `base` (100), so the chart now compares **growth**, not price level. Two professional upgrades on the video's version:
- Divide by the **first valid** (non-NaN) value per column — `iloc[0]` is NaN for BANK before April, and NaN poisons the whole column.
- Remember what rebasing *deletes*: volatility information. Two lines can end together while one was a rollercoaster. Day 04 puts the risk numbers back.

### C3. Creating columns: copy first, derive second
`out = df.copy(); out["Range"] = out["High"] - out["Low"]`. Assignment to a *slice* is the `SettingWithCopy` swamp from Day 02 — always be able to answer: "am I holding the original, a view, or a copy?" Derived quantities you'll meet today: `Range = High − Low` (intraday span), `RangePct = Range / Close` (span relative to price — level-free, like normalisation), `Body = Close − Open` (who won the day, and by how much).

### C4. `drop` returns; `inplace` mutates; silence does neither
`df.drop(columns=["X"])` **returns** a new frame — forget to assign it and nothing changed (a classic "my delete didn't work"). `inplace=True` mutates and returns `None` — this course bans it inside functions because callers deserve their data unmodified.
""")

code(SETUP_CODE)

md(r"""
---
## SECTION D — Guided Exploration

### D1 — The lying chart vs the fair chart
**Predict:** on the raw chart which line sits highest all year? After rebasing to 100 at each ticker's first valid value, which ends highest? Are those the same question?
""")
md(r"""✍️ **D1 prediction (edit me):** """)
code(r"""
# D1
ax = close_panel.plot(figsize=(10, 4), title="Raw Close prices (synthetic 2020) - a level comparison")
ax.set_ylabel("Close price"); plt.tight_layout(); plt.show()

rebased = close_panel.div(close_panel.apply(lambda s: s.loc[s.first_valid_index()])).mul(100)
ax = rebased.plot(figsize=(10, 4), title="Rebased to 100 at first valid value - a growth comparison")
ax.set_ylabel("Rebased value"); plt.tight_layout(); plt.show()
print("final rebased values:\n", rebased.apply(lambda s: s.loc[s.last_valid_index()]).round(2).to_dict())
# TODO(modify): rebase using div(close_panel.iloc[0]) exactly like the video. Which column dies, and why?
""")
md(r"""
✍️ **D1 observed (edit me):** raw chart's "winner" was really just the highest-_______ stock.
With `iloc[0]`, BANK became _______ because its first cell is _______. First-*valid* fixes it.

### D2 — `drop` did *what*?
**Predict:** `close_panel.drop(columns=["BANK"])` on its own line, then `close_panel.shape` next cell — has BANK gone?
""")
md(r"""✍️ **D2 prediction (edit me):** """)
code(r"""
# D2
close_panel.drop(columns=["BANK"])     # <- result goes nowhere
print("after unassigned drop:", close_panel.shape, list(close_panel.columns))
smaller = close_panel.drop(columns=["BANK"])
print("assigned result      :", smaller.shape, "| original still:", close_panel.shape)
# TODO(modify): what does close_panel.drop(columns=["NOPE"]) raise? When would errors="ignore" hide a real bug?
""")
md(r"""
✍️ **D2 observed (edit me):** `drop` _______ a new frame; without _______ nothing changes.
Banning `inplace=True` in functions protects _______.

### D3 — Derived columns carry a story
**Predict:** `RangePct` for ORNG (price ~25, volatile in our data) vs BANK (price ~250, calm): who has the bigger raw `Range`? Who has the bigger `RangePct`?
""")
md(r"""✍️ **D3 prediction (edit me):** """)
code(r"""
# D3
for t in ["ORNG", "BANK"]:
    ohlc = pd.DataFrame({f: multi.loc[:, (f, t)] for f in ["Open", "High", "Low", "Close"]})
    rp = ((ohlc["High"] - ohlc["Low"]) / ohlc["Close"]).mean()
    print(t, "| mean raw Range:", round(float((ohlc["High"] - ohlc["Low"]).mean()), 3),
          "| mean RangePct:", round(float(rp), 4))
# TODO(modify): compute mean RangePct for DEMO too and rank all three. Same lesson as Day 02's describe() std?
""")
md(r"""✍️ **D3 observed (edit me):** raw Range ranked _______; RangePct ranked _______. Dividing by _______ removes the price-level distortion — exactly why returns (Day 06) are ratios.""")

md(r"""
---
## SECTION E — Independent Practice

### Exercise 1 — Basic: `normalise` (the video's move, production-grade)
""")
code(r"""
def normalise(prices, base=100.0):
    '''Rebase a price Series OR DataFrame so each series starts at `base` at its
    FIRST VALID (non-NaN) value. NaNs before that value stay NaN.
    A column that is entirely NaN -> ValueError. Input must not be modified.
    Return the same type (Series in -> Series out; DataFrame in -> DataFrame out).'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>D1's guided code is the algorithm; your job is packaging it for both Series and DataFrame plus the all-NaN guard.</details>
<details><summary>Hint 2 — approach</summary>For a Series: `s.loc[s.first_valid_index()]` is the anchor (guard `first_valid_index() is None`). For a DataFrame, apply the Series logic per column — a comprehension or `.apply` over columns keeps one code path.</details>
<details><summary>Hint 3 — clue</summary>`isinstance(prices, pd.Series)` to branch. Tests hit: leading NaNs (BANK-shaped), base=1.0, and an all-NaN column that must raise rather than quietly produce NaNs.</details>

### Exercise 2 — Modification: manufacture features
""")
code(r"""
def add_range_columns(ohlcv):
    '''Return a COPY of a flat OHLCV frame with three new columns:
        Range    = High - Low
        RangePct = Range / Close
        Body     = Close - Open
    Any of Open/High/Low/Close missing -> ValueError. Input unmodified.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>C3's copy-then-derive pattern, three times. Order matters: RangePct consumes Range.</details>
<details><summary>Hint 2 — approach</summary>Validate the required set first (`set(...) - set(ohlcv.columns)`), copy, then assign. Tests compare against hand values on a 3-row frame.</details>
<details><summary>Hint 3 — clue</summary>If a test says the *input* gained columns, you forgot `.copy()` — assignment on the original object is visible to the caller.</details>

### Exercise 3 — Debugging: the normaliser that eats a ticker (and its neighbour)

Run the buggy cell. It has **two** defects: one kills BANK's column, the other silently damages the caller's panel. Diagnose both in the ✍️ cell, then implement the safe version.
""")
code(r"""
# --- BUGGY CODE (study; do not edit in place) ---
def select_and_normalise_buggy(panel, tickers):
    sub = panel[tickers]
    sub = sub.div(sub.iloc[0]).mul(100)      # defect A hides here
    panel.drop(columns=[c for c in panel.columns if c not in tickers], inplace=True)  # defect B hides here
    return sub

victim = close_panel.copy()
_cols_before = list(victim.columns)
out = select_and_normalise_buggy(victim, ["DEMO", "BANK"])
print("BANK column of result is all-NaN:", bool(out["BANK"].isna().all()))
print("caller's panel columns before:", _cols_before, "-> after:", list(victim.columns))
""")
md(r"""
✍️ **My diagnosis (edit me):** Defect A: … because … · Defect B: … because … (name *who* is harmed by B)
""")
code(r"""
def select_and_normalise(panel, tickers, base=100.0):
    '''Return normalise(panel[tickers]) in requested column order.
    Unknown ticker -> KeyError. The caller's panel must be byte-for-byte untouched.
    (Reusing your Exercise 1 is the intended design.)'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>A is D1's iloc[0]-vs-first-valid lesson. B is the function reaching *outside* its return value to mutate its argument — the caller never consented.</details>
<details><summary>Hint 2 — approach</summary>Validate tickers, slice a copy in requested order, hand it to `normalise`. No `inplace` anywhere, ever, in this course's functions.</details>

### Exercise 4 — Independent: plotting as a testable function
""")
code(r"""
def plot_prices(panel, title, ylabel="Price", ax=None):
    '''Plot every column of panel (Series -> one line) on one Axes.
    Must set: title=title, xlabel "Date", ylabel=ylabel, and a legend naming each line.
    Return the matplotlib Axes object. If ax is given, draw on it.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>`panel.plot(ax=ax)` does the drawing; your function adds the evidence (title/labels/legend) and *returns the Axes* so tests can interrogate it.</details>
<details><summary>Hint 2 — approach</summary>Convert a Series via `to_frame()` so one code path handles both. `ax = panel.plot(ax=ax)` returns an Axes when ax=None creates one.</details>
<details><summary>Hint 3 — clue</summary>Tests will read `ax.get_title()`, `ax.get_ylabel()`, count `ax.get_lines()` and read legend texts. If legend is missing, check you didn't pass `legend=False` anywhere.</details>

### Exercise 5 — Transfer: from picture to table
""")
code(r"""
def growth_table(prices, base=100.0):
    '''Summarise rebased growth per ticker of a price DataFrame. Return a DataFrame
    indexed by ticker, sorted by total growth DESCENDING, with columns:
        first_valid_date  Timestamp of first non-NaN price
        last_valid_date   Timestamp of last non-NaN price
        final_rebased     rebased value at last valid date (float)
        total_growth_pct  final_rebased/base - 1  (float, e.g. 0.25 = +25%)
    Use your normalise(); a ticker that is all-NaN -> ValueError (via normalise is fine).'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>The chart's endpoint ranking, made auditable. Everything comes from each column's first/last *valid* positions plus its rebased endpoint.</details>
<details><summary>Hint 2 — approach</summary>Normalise once, then per column gather `first_valid_index`/`last_valid_index` from the *original* prices and the rebased value at the last valid date; assemble rows, sort by growth.</details>

---
## SECTION F — Daily Mini-Project · P0.3 Normalised Comparison Report
""")
md(r"""
**Problem:** "Which of our three tickers actually grew most in 2020 — fairly compared?" Today you ship the artifact that answers it: a rebased panel file plus the chart and numbers that defend the answer.

### Specification — `build_normalised_report(panel, output_csv, base=100.0)`
- Normalise `panel` with your `normalise`; write it to `output_csv` (Date index header, parent folders created, re-runnable).
- Return your `growth_table` DataFrame for the same panel/base.
- No globals; input untouched; unseen tickers/windows must work.

**Then:** run it on `close_panel` → `data/processed/day03_normalised.csv`, plot the rebased panel with your `plot_prices`, and write the interpretation: (1) ranking by growth with numbers, (2) why the raw chart (D1) suggested a different story, (3) one thing rebasing hides that Day 04 must restore, (4) whether BANK's late start makes its "growth" comparable over the *same period* — and if not, what window restriction would fix it (you have the tool from Day 02 Ex. 5).

**Acceptance:** Section G project check green on unseen data · chart passes the C1 evidence standard · interpretation bullet 4 names a concrete common window.
""")
code(r"""
def build_normalised_report(panel, output_csv, base=100.0):
    '''See Section F. Returns the growth_table DataFrame; writes the normalised CSV.'''
    # TODO (compose Exercises 1 and 5; Path handling like Day 02)
    pass
""")
code(r"""
# SECTION F (apply) - None/table appears once implemented; the guided raw plot above already proved the contrast.
table = build_normalised_report(close_panel, PROCESSED / "day03_normalised.csv")
print(table)
if table is not None:
    ax = plot_prices(normalise(close_panel), "Synthetic tickers rebased to 100 at first valid value (2020)", ylabel="Rebased value")
    plt.tight_layout(); plt.show()
""")
md(r"""
✍️ **P0.3 interpretation (edit me):** 1) Growth ranking: … 2) Raw chart misled because … 3) Rebasing hides … 4) Common-window fix: compare over … because BANK …

---
## SECTION G — Automated Assessment (visible checks; review uses unseen variants)
""")
code(r"""
# SECTION G - harness + visible checks (self-contained; do not edit the harness)
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

_idx = pd.to_datetime(["2021-01-04", "2021-01-05", "2021-01-06", "2021-01-07"]); _idx.name = "Date"
P = pd.DataFrame({"AAA": [10.0, 11.0, 12.0, 13.0], "BBB": [np.nan, np.nan, 50.0, 75.0]}, index=_idx)
S = P["AAA"].copy()

check("Ex1 Series rebased to 100", lambda: np.allclose(normalise(S), [100, 110, 120, 130]))
check("Ex1 base=1 honoured", lambda: np.allclose(normalise(S, base=1.0), [1.0, 1.1, 1.2, 1.3]))
check("Ex1 leading NaNs preserved, first-valid anchor", lambda: (
    lambda r: bool(np.isnan(r["BBB"].iloc[0])) and np.allclose(r["BBB"].dropna(), [100, 150]))(normalise(P)))
check("Ex1 all-NaN column -> ValueError", lambda: raises(ValueError, lambda: normalise(P.assign(CCC=np.nan))))
check("Ex1 input untouched", lambda: P["AAA"].iloc[0] == 10.0)

_ohlc = pd.DataFrame({"Open": [10., 11], "High": [12., 13], "Low": [9., 10], "Close": [11., 12], "Volume": [5, 6]}, index=_idx[:2])
check("Ex2 Range/Body/RangePct values", lambda: (
    lambda r: list(r["Range"]) == [3.0, 3.0] and list(r["Body"]) == [1.0, 1.0]
    and np.allclose(r["RangePct"], [3/11, 3/12]) and "Range" not in _ohlc.columns)(add_range_columns(_ohlc)))
check("Ex2 missing column -> ValueError", lambda: raises(ValueError, lambda: add_range_columns(_ohlc.drop(columns=["Low"]))))

def _ex3():
    src = P.copy(); out = select_and_normalise(src, ["BBB", "AAA"])
    return (list(out.columns) == ["BBB", "AAA"] and np.allclose(out["BBB"].dropna(), [100, 150])
            and list(src.columns) == ["AAA", "BBB"] and src["AAA"].iloc[0] == 10.0)
check("Ex3 subset+normalise safe & ordered; caller untouched", _ex3)
check("Ex3 unknown ticker -> KeyError", lambda: raises(KeyError, lambda: select_and_normalise(P, ["ZZZ"])))

def _ex4():
    import matplotlib
    ax = plot_prices(P, "My Title", ylabel="Prices!")
    texts = [t.get_text() for t in ax.get_legend().get_texts()] if ax.get_legend() else []
    plt.close("all")
    return ax.get_title() == "My Title" and ax.get_ylabel() == "Prices!" and ax.get_xlabel() == "Date" and len(ax.get_lines()) == 2 and texts == ["AAA", "BBB"]
check("Ex4 Axes carries title/labels/legend/2 lines", _ex4)

def _ex5():
    r = growth_table(P)
    return (list(r.index) == ["BBB", "AAA"] and abs(r.loc["BBB", "total_growth_pct"] - 0.5) < 1e-12
            and r.loc["BBB", "first_valid_date"] == pd.Timestamp("2021-01-06")
            and abs(r.loc["AAA", "final_rebased"] - 130.0) < 1e-9)
check("Ex5 growth table sorted, correct anchors/values", _ex5)

def _proj():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "deep" / "norm.csv"
        r = build_normalised_report(P, out)
        back = pd.read_csv(out, parse_dates=["Date"], index_col="Date")
        return out.exists() and list(r.index) == ["BBB", "AAA"] and np.allclose(back["AAA"].dropna(), [100, 110, 120, 130])
check("F project: CSV + growth table consistent (nested path)", _proj)
print(f"\nSCORE: {sum(RESULTS)}/{len(RESULTS)} visible checks passing")
""")

md(r"""
---
## SECTION H — Knowledge Check

**H1 Predict:** `close_panel.div(close_panel.iloc[0]).mul(100)` — exactly which cells of BANK become NaN and why does NaN in *one* anchor cell destroy the *entire* column? ✍️

**H2 Explain:** rebasing makes growth comparable but deletes two kinds of information. Name both (one is price level — what is the other?). ✍️

**H3 Defend:** your `normalise` anchors on first-*valid*. A reviewer argues for anchoring on a fixed calendar date for all tickers instead. Give one strength of each choice with BANK as the example. ✍️

**H4 What-if:** a column's first valid value is `0.0` (bad tick). What does your function produce, and what *should* it ideally do? Connect to Day 01's `Close > 0` validation. ✍️

**H5 Critique:** "DEMO ended at rebased 130 and ORNG at 115, so DEMO was the better investment." Demolish this in two sentences using a word Day 04 will quantify. ✍️

**H6 Design:** Day 04 resamples daily→monthly. Predict: for a monthly *price* series, should each month keep its first, last, or mean daily close? Commit to an answer now. ✍️
""")

md(r"""
---
## SECTION I — Reflection & Retrieval Practice

### What I learned · What I can implement unaided · Still difficult
- ✍️ (three honest lists)

### Retrieval — Days 02 & 01 from memory
1. The three `read_csv` arguments that rebuild a multi-ticker download, and the corruption each prevents.
2. `multi.loc[:, "Close"]` returns what shape of object, with what as its columns?
3. Why did Day 01 insist `Close > 0`? Name a *today* operation that would silently explode without it.
4. Function vs method: classify `panel.plot`, `len(panel)`, `panel.drop`, `pd.MultiIndex.from_tuples`.
5. Your Day 02 `slice_date_range` rejects empty windows. State the two bounds you'd use to compare all 3 tickers over a *fair common* 2020 window, given BANK's April listing.

### Reimplementation challenge — Day 02's segregation, from memory
""")
code(r"""
def get_close_panel_from_memory(multi_df, tickers=None):
    '''Day 02 Ex4 contract: Close panel (all tickers in data order, or requested order),
    unknown ticker -> KeyError, independent copy. FROM MEMORY.'''
    # TODO
    pass

try:
    _p = get_close_panel_from_memory(multi, ["BANK", "DEMO"])
    _ok = list(_p.columns) == ["BANK", "DEMO"] and _p.shape == (len(multi), 2)
except Exception as exc:
    _ok = False; print("self-check raised:", type(exc).__name__, exc)
print("Day-02 reimplementation self-check:", "PASS" if _ok else "not yet - revisit Day 02 before Day 04")
""")
md(r"""
### ✅ Completion checklist
- [ ] Watched 23:00–44:40 with summary written · - [ ] D1–D3 predictions before running
- [ ] Ex 1–5 self-implemented, Ex 3 diagnosis names *who* defect B harms
- [ ] P0.3 shipped: CSV + evidenced chart + 4-point interpretation with a concrete common window
- [ ] Section G green after Restart & Run All · - [ ] H answered; retrieval honest

**Send back:** G score · H3 defence · still-difficult list. Day 04 (resampling & first risk numbers, Milestone 1) is next.
""")

nb = new_notebook(cells=CELLS)
nb.metadata.update({"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                    "language_info": {"name": "python", "version": "3.11"},
                    "title": "Day 03 - Visualisation, Normalisation and Creating Data",
                    "source_video": "https://www.youtube.com/watch?v=GDMkkmkJigw (23:00-44:40)"})
out = ROOT / "notebooks" / "Day_03_Visualisation_Normalisation_Creating_Data.ipynb"
nbformat.write(nb, out); print("wrote", out, "cells=", len(CELLS))
