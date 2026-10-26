"""Build Day 02 notebook + data/sample/multi_ticker_ohlcv.csv. Instructor utility."""
from pathlib import Path
import numpy as np
import pandas as pd
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

ROOT = Path(__file__).resolve().parents[1]

# ---- deterministic multi-ticker sample (identical code is embedded as fallback in the notebook)
def _one(seed, start_price, mu, sigma, n=252):
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2020-01-02", periods=n, freq="B")
    lr = rng.normal(loc=mu, scale=sigma, size=n)
    close = start_price * np.exp(np.cumsum(lr))
    open_ = np.empty(n); open_[0] = start_price
    open_[1:] = close[:-1] * np.exp(rng.normal(0, 0.002, size=n - 1))
    intraday = np.abs(rng.normal(0, 0.004, size=n))
    f = pd.DataFrame({
        "Open": np.round(open_, 4),
        "High": np.round(np.maximum(open_, close) * (1 + intraday), 4),
        "Low": np.round(np.minimum(open_, close) * (1 - intraday), 4),
        "Close": np.round(close, 4), "Adj Close": np.round(close, 4),
        "Volume": rng.integers(800_000, 3_000_000, size=n)}, index=dates)
    f.index.name = "Date"
    return f

def make_multi():
    parts = {"DEMO": _one(42, 100.0, 0.0004, 0.011),
             "ORNG": _one(7, 25.0, 0.0008, 0.018),
             "BANK": _one(123, 250.0, 0.0001, 0.008).loc["2020-04-01":]}  # listed later -> leading NaNs
    m = pd.concat(parts, axis=1)                       # level0=ticker, level1=field
    m = m.swaplevel(0, 1, axis=1)                      # level0=field (yfinance layout)
    fields = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    m = m.reindex(columns=pd.MultiIndex.from_product([fields, ["DEMO", "ORNG", "BANK"]]))
    m.index.name = "Date"
    return m

out_csv = ROOT / "data" / "sample" / "multi_ticker_ohlcv.csv"
make_multi().to_csv(out_csv)
print("wrote", out_csv)

CELLS = []
def md(t): CELLS.append(new_markdown_cell(t.strip("\n")))
def code(t): CELLS.append(new_code_cell(t.strip("\n")))

md(r"""
## SECTION A — Learning Mission

# Day 02 — Working With Data: Save It, Reload It, Segregate It

| | |
|---|---|
| **Video segment** | **13:00–23:00** — *Read and writing Data* · *Separating and Segregating Data* ([watch](https://www.youtube.com/watch?v=GDMkkmkJigw&t=780s)) |
| **Estimated study time** | **2–3 hours** (≈10 min watching · ≈30 min guided · ≈80 min independent · ≈30 min project) |
| **Prerequisites** | Day 01 complete (validated OHLCV frame, function vs method, `.loc` vs `.iloc`). If Day 01's checklist isn't green, finish it first — today assumes it. |
| **Data** | `data/sample/multi_ticker_ohlcv.csv` — 3 synthetic tickers (DEMO, ORNG, BANK×) in `yfinance` multi-download format. BANK "lists" on 2020‑04‑01, so its early rows are empty *on purpose*. |
| **Expected deliverable** | **P0.2:** a Q2‑2020 close-price panel CSV built by your own `build_close_panel_file`, plus a written interpretation of `.describe()` |

## Learning objectives — by the end of today you will be able to

1. **Round-trip** a DataFrame through CSV (`to_csv` → `read_csv`) and *prove* the reloaded frame equals the original in values, columns and index type.
2. **Load a two-header-row CSV** (`header=[0,1], index_col=0, parse_dates`) into a MultiIndex-column DataFrame, and convert its columns **MultiIndex ⇄ flat index of tuples** without losing information.
3. **Segregate** the Close panel for several tickers with `.loc[:, "Close"]`, return an independent copy, and explain why the video calls `.copy()`.
4. **Read `.describe()` critically** — especially why `count` can differ per ticker and why comparing raw-price `std` across tickers misleads.
5. **Slice an inclusive date range** that fails loudly (`ValueError`) on an empty selection instead of silently returning nothing.
6. **Diagnose and repair** a frame that was loaded *without* date parsing — the single most common beginner data bug in this field.

> 📏 **Programme length check:** this is Day 02 of **13 learning days** — inside the two-week (14-day) maximum for the full course.
""")

md(r"""
---
## SECTION B — Video Learning · 13:00–23:00

**Answer from instinct first** (checked in Section H):

1. You `to_csv` a DataFrame and read it back with a bare `pd.read_csv(path)`. What has happened to your dates?
2. Why would a multi-ticker download need **two** header rows — what lives in each?
3. `stocks.loc[:, "Close"]` on that download: how many columns come back, and what are they named?
4. The presenter adds `.copy()` after segregating the Close data. What future pain is he avoiding?

| Time | Chapter | Pay attention to |
|---|---|---|
| 13:00 | Read and writing Data | `to_csv`, then `read_csv` with **`header=[0,1]`, `index_col=0`, `parse_dates=[0]`** added one at a time — watch what each fixes |
| ~17:00 | (within chapter) | `stocks.columns`, MultiIndex ⇄ flat tuples: `to_flat_index()` / `pd.MultiIndex.from_tuples(...)` |
| 21:35 | Separating and Segregating Data | `.describe()`, then `.loc[:, "Close"]` + `.copy()` to isolate the panel every later step uses |
| 23:00 | ⛔ STOP | Data visualisation is Day 03 |

Fallback: [13:00](https://www.youtube.com/watch?v=GDMkkmkJigw&t=780s) · [21:35](https://www.youtube.com/watch?v=GDMkkmkJigw&t=1295s) · Embedding needs internet + an iframe-friendly frontend.
""")

code(r"""
# ▶️ SECTION B (code) — today's segment only: 13:00 - 23:00
from IPython.display import YouTubeVideo, display
display(YouTubeVideo("GDMkkmkJigw", start=780, end=1380, width=800, height=450))
print("Fallback: https://www.youtube.com/watch?v=GDMkkmkJigw&t=780s  (stop at 23:00)")
""")

md(r"""
✍️ **My 3-bullet summary of 13:00–23:00, in my own words (edit me):**

-
-
-
""")

md(r"""
---
## SECTION C — Concept Notes

### C1. A CSV is just text — *everything* else is your instructions
`to_csv` writes characters. It does **not** remember that column 0 was a `DatetimeIndex` or that `Volume` was an integer. On reload, *you* re-supply that knowledge:

| `read_csv` argument | What it restores | Symptom when you forget it |
|---|---|---|
| `index_col=0` (or `"Date"`) | First column becomes the index | A mystery `Unnamed: 0` / `Date` *data* column + a useless `RangeIndex` |
| `parse_dates=[...]` / `parse_dates=True` with `index_col` | Strings → timestamps | Dates sort alphabetically, `.loc["2020-06-01":...]` breaks, time maths impossible |
| `header=[0,1]` | Two header rows → MultiIndex columns | Ticker row becomes a *data* row full of strings; numeric columns turn to `object` dtype |

**Round-trip rule for this course:** after any save/load, `assert` equality of shape, columns, index type and a numeric spot-check. "It loaded" proves nothing.

### C2. MultiIndex columns anatomy
A multi-ticker `yfinance` frame has column **levels**: level 0 = field (`Open…Close…Volume`), level 1 = ticker. `df.columns.to_flat_index()` gives an index of tuples like `("Close", "DEMO")`; `pd.MultiIndex.from_tuples(...)` rebuilds the levels. Same information, different ergonomics — the video converts both ways so you recognise both in other people's code.

### C3. Segregation with `.loc` — rows × columns, by label
`multi.loc[:, "Close"]` reads: *all rows (`:`), the level-0 label `Close`* → a panel whose columns are tickers. This **Close panel** (dates × tickers) becomes the canonical object for Days 03–07. The video stores `.loc[:, "Close"].copy()` — a *segregated, independently owned* frame, so later edits can never mutate (or warn about) the original download. Treat `.copy()` after slicing as a professional reflex whenever you will modify the result.

### C4. `.describe()` — read it like an auditor, not a tourist
`count` is *non-NaN* count per column: BANK lists in April, so its count is lower — that one row of `.describe()` just told you the tickers have different histories (Day 07's alignment problem, arriving early). And `std` of raw prices scales with price level: a 250-unit stock is not "10× riskier" than a 25-unit one because its `std` is 10× bigger. Risk is computed on **returns** (Day 04/06) — today, learn to *distrust* the easy number.

### C5. Inclusive slicing & silent emptiness
Label slicing `df.loc[start:end]` includes **both** endpoints (unlike Python list slicing) and tolerates non-trading-day bounds (Saturday start → Monday's row first). Its failure mode is silence: a typo'd year returns 0 rows and downstream code happily averages nothing. Today's Exercise 5 makes that loud.
""")

code(r"""
# SECTION C/D setup — run first. Loads the bundled multi-ticker file, or regenerates identical data.
import sys, io
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
PROCESSED = BASE / "data" / "processed"

def _one(seed, start_price, mu, sigma, n=252):
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2020-01-02", periods=n, freq="B")
    lr = rng.normal(loc=mu, scale=sigma, size=n)
    close = start_price * np.exp(np.cumsum(lr))
    open_ = np.empty(n); open_[0] = start_price
    open_[1:] = close[:-1] * np.exp(rng.normal(0, 0.002, size=n - 1))
    intraday = np.abs(rng.normal(0, 0.004, size=n))
    f = pd.DataFrame({"Open": np.round(open_, 4),
        "High": np.round(np.maximum(open_, close) * (1 + intraday), 4),
        "Low": np.round(np.minimum(open_, close) * (1 - intraday), 4),
        "Close": np.round(close, 4), "Adj Close": np.round(close, 4),
        "Volume": rng.integers(800_000, 3_000_000, size=n)}, index=dates)
    f.index.name = "Date"; return f

def make_multi():
    parts = {"DEMO": _one(42, 100.0, 0.0004, 0.011), "ORNG": _one(7, 25.0, 0.0008, 0.018),
             "BANK": _one(123, 250.0, 0.0001, 0.008).loc["2020-04-01":]}
    m = pd.concat(parts, axis=1).swaplevel(0, 1, axis=1)
    fields = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    m = m.reindex(columns=pd.MultiIndex.from_product([fields, ["DEMO", "ORNG", "BANK"]]))
    m.index.name = "Date"; return m

def _find(name):
    for base in [Path.cwd(), *Path.cwd().parents]:
        for cand in (base / "data" / "sample" / name, base.parent / "data" / "sample" / name):
            if cand.exists(): return cand
    return None

multi_path = _find("multi_ticker_ohlcv.csv") or _find("demo_ohlcv.csv")  # placeholder overwritten below if needed
multi_path = _find("multi_ticker_ohlcv.csv")
if multi_path is not None:
    multi = pd.read_csv(multi_path, header=[0, 1], index_col=0, parse_dates=True)
    print("loaded bundled multi-ticker file:", multi_path)
else:
    multi = make_multi()
    multi_path = Path.cwd() / "multi_ticker_ohlcv_fallback.csv"
    multi.to_csv(multi_path)
    print("bundled file not found - regenerated identical data and wrote:", multi_path)

demo_path = _find("demo_ohlcv.csv")
df = (pd.read_csv(demo_path, parse_dates=["Date"], index_col="Date")
      if demo_path is not None else _one(42, 100.0, 0.0004, 0.011))

print("multi shape:", multi.shape, "| index:", type(multi.index).__name__)
print("multi columns (first 6):", list(multi.columns)[:6])
multi.head(3)
""")

md(r"""
---
## SECTION D — Guided Exploration (predict → run → modify → record)

### D1 — What a bare `read_csv` really gives you
**Predict:** `df` (flat, one ticker) saved to text and read back *with no arguments*: what type is the index, and what happens to the `Date`?
""")
md(r"""✍️ **D1 prediction (edit me):** """)
code(r"""
# D1
buf = io.StringIO(); df.head(4).to_csv(buf)
print("--- the actual file contents ---\n", buf.getvalue())
bare = pd.read_csv(io.StringIO(buf.getvalue()))
print("bare load -> index:", type(bare.index).__name__, "| columns:", list(bare.columns), "| Date dtype:", bare["Date"].dtype)
proper = pd.read_csv(io.StringIO(buf.getvalue()), parse_dates=["Date"], index_col="Date")
print("proper load -> index:", type(proper.index).__name__, "| columns:", list(proper.columns))
# TODO(modify): try bare.loc["2020-01-03"] vs proper.loc["2020-01-03"]. Which raises, and what is the error telling you?
""")
md(r"""
✍️ **D1 observed (edit me):** without instructions, dates came back as _______ with a _______ index.
A CSV stores _______; the `DatetimeIndex` exists only because I _______.

### D2 — `.describe()` as an audit
**Predict:** before running — which ticker has the smallest `count` in the Close panel, and which has the largest `std`? Are those the same story?
""")
md(r"""✍️ **D2 prediction (edit me):** """)
code(r"""
# D2
close_panel = multi.loc[:, "Close"].copy()
print(close_panel.describe().round(2))
print("\nfirst valid date per ticker:")
print(close_panel.apply(lambda s: s.first_valid_index()))
# TODO(modify): divide each column by its own mean (close_panel / close_panel.mean()) and describe again.
# What happened to the std ranking? That is C4's point, in numbers.
""")
md(r"""
✍️ **D2 observed (edit me):** BANK's `count` is lower because _______. Raw `std` ranked _______,
but that mostly reflects _______, not risk. Risk needs _______ (Days 04/06).

### D3 — Segregate, then slice
**Predict:** `multi.loc["2020-06-01":"2020-06-30", "Close"]` — how many rows? June 2020 has 30 days…
""")
md(r"""✍️ **D3 prediction (edit me):** """)
code(r"""
# D3
june_close = multi.loc["2020-06-01":"2020-06-30", "Close"]
print("rows:", len(june_close), "|", june_close.index.min().date(), "->", june_close.index.max().date())
one = multi.loc[:, ("Close", "DEMO")]
print("single cell-block type:", type(one).__name__, "| name:", one.name)
# TODO(modify): segregate the HIGH panel for June the same way. Then slice with start="2020-06-06" (a Saturday)
# and record the first date returned. Inclusive label slicing + non-trading bounds = ?
""")
md(r"""
✍️ **D3 observed (edit me):** June returned ___ rows because only _______ days appear.
A Saturday start returned _______ first — label slicing is _______ of bounds that exist in the index range.
""")

md(r"""
---
## SECTION E — Independent Practice (from the docstrings; docs allowed, video closed)
""")

md(r"""### Exercise 1 — Basic application: a CSV round-trip you can *prove*""")
code(r"""
def save_prices(df, path):
    '''Write df to CSV at path (str or Path), creating parent folders if needed.
    The DatetimeIndex must be written as a 'Date' column. Return Path(path).'''
    # TODO
    pass


def load_prices(path):
    '''Load a CSV written by save_prices. Index must come back as a sorted
    DatetimeIndex named 'Date' (not a string column). Return the DataFrame.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>C1's table is the whole exercise: writing is one method on df; reading needs the two arguments that rebuild the index.</details>
<details><summary>Hint 2 — approach</summary>`Path(path).parent.mkdir(parents=True, exist_ok=True)` before writing. On reading, `parse_dates` + `index_col` on the same "Date", then `sort_index()`.</details>
<details><summary>Hint 3 — clue</summary>If your reloaded frame has a column literally called `Unnamed: 0`, you saved the index but didn't claim it on load. That column is the receipt of the mistake.</details>

### Exercise 2 — Modification: MultiIndex ⇄ flat tuples (the video's column gymnastics, as functions)
""")
code(r"""
def flatten_columns(multi_df):
    '''Return a COPY of multi_df whose MultiIndex columns are replaced by a flat
    Index of tuples, e.g. ("Close", "DEMO"). Do not modify the input.'''
    # TODO
    pass


def unflatten_columns(flat_df):
    '''Inverse of flatten_columns: return a COPY whose tuple columns are rebuilt
    into a pd.MultiIndex. flatten -> unflatten must restore the original columns exactly.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>The video names both tools: one is a method *on the columns Index* producing a flat index; the other is a `pd.MultiIndex` class method rebuilding levels from tuples.</details>
<details><summary>Hint 2 — approach</summary>Work on `out = df.copy()` then reassign `out.columns = ...`. Tests compare the *input* afterwards to catch in-place edits.</details>
<details><summary>Hint 3 — clue</summary>`df.columns.to_flat_index()` one way; `pd.MultiIndex.from_tuples(df.columns)` back. If round-trip equality fails, print both column objects — level *names* are usually innocent; order is not.</details>

### Exercise 3 — Debugging: the frame that forgot it was a time series

Run the cell below. A classmate loaded a price CSV with a bare `read_csv` and now
"date slicing doesn't work and sorting looks wrong". **Write three distinct defects**
in the ✍️ cell, then implement the repair function.
""")
code(r"""
# --- BUGGY WORKFLOW (study; do not edit) ---
CSV_TEXT = '''Date,Open,High,Low,Close,Volume
2021-01-06,12,13,11,12.5,300
2021-01-04,10,11,9,10.5,100
2021-01-05,11,12,10,11.5,200
'''
raw = pd.read_csv(io.StringIO(CSV_TEXT))          # <-- the bare load
print("index:", type(raw.index).__name__, "| Date dtype:", raw["Date"].dtype)
try:
    print(raw.loc["2021-01-05"])
except Exception as exc:
    print("date .loc raised:", type(exc).__name__, "-", exc)
print("Close dtype:", raw["Close"].dtype, "| row order preserved from file (unsorted dates!)")
""")
md(r"""
✍️ **My diagnosis (edit me — graded):**
1. Defect: … because …
2. Defect: … because …
3. Defect: … because …
""")
code(r"""
def repair_loaded_frame(raw):
    '''Repair a DataFrame produced by a bare read_csv of a price file like CSV_TEXT.

    Requirements:
      - require a 'Date' column, else raise ValueError
      - convert it to datetimes and make it the index (named 'Date'); drop the column
      - sort ascending by date; duplicate dates -> ValueError
      - convert remaining columns to numeric dtypes
      - do not modify the input; return the repaired copy
    '''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>You are re-supplying, after the fact, everything `parse_dates`/`index_col` would have done at load time — plus the sort the file itself failed to provide.</details>
<details><summary>Hint 2 — approach</summary>`pd.to_datetime(out["Date"])` → `set_index` → `sort_index` → check `index.has_duplicates` → `apply(pd.to_numeric)` or per-column conversion.</details>
<details><summary>Hint 3 — clue</summary>Copy first (`raw.copy()`); tests mutate-check the original. Invalid date strings should surface as an exception — letting `to_datetime` raise is honest behaviour.</details>

### Exercise 4 — Independent implementation: `get_close_panel`
""")
code(r"""
def get_close_panel(multi_df, tickers=None):
    '''Segregate the Close panel from a MultiIndex-column OHLCV frame (level0=field, level1=ticker).

    - tickers=None  -> all tickers, in the order they appear in the data
    - tickers=[...] -> exactly those columns, in the REQUESTED order
    - unknown ticker -> KeyError
    - return an independent copy (mutating the result must never affect multi_df)
    '''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>C3: `.loc[:, "Close"]` gives the whole panel in one move. Subsetting/reordering columns of *that* is then ordinary column selection.</details>
<details><summary>Hint 2 — approach</summary>Validate requested tickers against the panel's columns *yourself* so the failure is a clean KeyError naming the ticker, then select in requested order.</details>
<details><summary>Hint 3 — clue</summary>`panel = multi_df.loc[:, "Close"]`; guard `missing = [t for t in tickers if t not in panel.columns]`; finish with `.copy()` — the video's reflex, now yours.</details>

### Exercise 5 — Transfer: date slicing that refuses to fail silently (not in the video)
""")
code(r"""
def slice_date_range(df, start, end):
    '''Return rows of df with start <= index <= end (BOTH inclusive), sorted by date.

    - start/end may be strings ('2020-06-01') or Timestamps
    - works even if df arrives unsorted (do not modify df)
    - start > end -> ValueError
    - empty result -> ValueError (a silent empty frame is a bug, not an answer)
    '''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>D3 showed label slicing needs a sorted index and tolerates weekend bounds. Your job is the guard rails pandas doesn't provide.</details>
<details><summary>Hint 2 — approach</summary>Normalise bounds with `pd.Timestamp(start)`, compare, sort a copy, slice with `.loc[...]`, then check `empty`.</details>
<details><summary>Hint 3 — clue</summary>Think about which check must come first so `start > end` on a weekend-only range reports the *right* error. Tests use a Saturday start and an out-of-range year separately.</details>
""")

md(r"""
---
## SECTION F — Daily Mini-Project · P0.2 Q2‑2020 Close Panel, Built Properly

**Problem:** downstream days need *one* clean artifact: daily Close for every ticker over a stated window, in a plain CSV anyone can load. The raw vendor file (two header rows, leading NaNs, full year) is not that artifact. Build the transformer once, correctly.

### Specification — `build_close_panel_file(multi_csv_path, start, end, output_csv)`

| | Requirement |
|---|---|
| **Load** | `read_csv` with the two-header-row settings from C1 (you choose the exact arguments — defend them in H3) |
| **Transform** | Segregate Close via your `get_close_panel`; restrict via your `slice_date_range` |
| **Save** | Flat CSV: header `Date,DEMO,ORNG,BANK` (ticker order = data order), creating parent folders; re-runnable |
| **Return** | `{"n_rows": int, "start": Timestamp, "end": Timestamp, "tickers": list[str], "missing_by_ticker": {ticker: int}}` (missing counted **within the sliced window**) |
| **Constraints** | Compose Exercises 4–5 (no duplicated logic); no globals; unseen windows/tickers must work |

**Then:** run it for **2020‑04‑01 → 2020‑06‑30** into `data/processed/day02_close_panel.csv` and complete the `.describe()` interpretation below (note: *within Q2*, BANK exists from day one — has its `count` caught up? Check, don't assume).

### Acceptance criteria
- [ ] Section G project check passes on an unseen multi-ticker file in a temp folder
- [ ] Reloading your output with `load_prices` (Ex. 1) gives a `DatetimeIndex` frame — the artifact obeys your own standard
- [ ] Each interpretation bullet cites a number from `.describe()` output *you printed*
""")
code(r"""
# SECTION F - implement, composing Exercises 4 and 5
def build_close_panel_file(multi_csv_path, start, end, output_csv):
    '''See Section F specification.'''
    # TODO
    pass
""")
code(r"""
# SECTION F (apply) - prints None until implemented; the describe() below it works either way.
summary = build_close_panel_file(multi_path, "2020-04-01", "2020-06-30", PROCESSED / "day02_close_panel.csv")
print("summary:", summary)

q2 = multi.loc["2020-04-01":"2020-06-30", "Close"]
print(q2.describe().round(2))
""")
md(r"""
✍️ **`.describe()` interpretation — Q2 2020 (edit me, every bullet needs a number):**
1. `count` per ticker in Q2 vs the full year (D2): …
2. Highest `std` is …; that does / does not mean riskiest because …
3. `min`→`max` range that surprises me most, and why: …
4. One thing `.describe()` on *prices* can never tell me (preview of Day 06): …
""")

md(r"""
---
## SECTION G — Automated Assessment (visible checks; review re-tests on unseen variants)

Same contract as Day 01: PASS/FAIL per behaviour, never stops early, FAILs before
Section E are the expected starting state. Hard-coding fails review by construction.
""")
code(r"""
# SECTION G - harness + visible checks (do not edit the harness)
import tempfile
RESULTS = []
def check(name, fn):
    try: ok = bool(fn()); msg = ""
    except Exception as exc: ok = False; msg = f"{type(exc).__name__}: {exc}"
    RESULTS.append(ok); print(("PASS" if ok else "FAIL"), "-", name, (("| " + msg) if msg else ""))

def raises(exc_type, fn):
    try: fn()
    except exc_type: return True
    except Exception: return False
    return False

def _flat():
    idx = pd.to_datetime(["2021-01-04", "2021-01-05", "2021-01-06"]); idx.name = "Date"
    return pd.DataFrame({"Open": [10., 11, 12], "High": [11., 12, 13], "Low": [9., 10, 11],
                         "Close": [10.5, 11.5, 12.5], "Volume": [100, 200, 300]}, index=idx)

def _multi():
    f = _flat()
    cols = pd.MultiIndex.from_product([["Open", "Close"], ["AAA", "BBB"]])
    data = np.column_stack([f["Open"], f["Open"] * 10, f["Close"], [1.0, np.nan, 3.0]])
    m = pd.DataFrame(data, index=f.index, columns=cols); return m

F, M = _flat(), _multi()

def _roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        p = save_prices(F, Path(tmp) / "sub" / "prices.csv")
        back = load_prices(p)
        return (isinstance(back.index, pd.DatetimeIndex) and back.index.name == "Date"
                and list(back.columns) == list(F.columns) and np.allclose(back[["Open", "Close"]].values, F[["Open", "Close"]].values)
                and list(back.index) == list(F.index))
check("Ex1 CSV round-trip (values/columns/DatetimeIndex, nested path)", _roundtrip)
check("Ex2 flatten->unflatten restores columns; input untouched", lambda: (
    list(unflatten_columns(flatten_columns(M)).columns) == list(M.columns)
    and isinstance(M.columns, pd.MultiIndex)))
check("Ex2 flatten yields tuple columns", lambda: list(flatten_columns(M).columns)[:2] == [("Open", "AAA"), ("Open", "BBB")])

def _repair():
    raw = pd.read_csv(io.StringIO(CSV_TEXT)); fixed = repair_loaded_frame(raw)
    return (isinstance(fixed.index, pd.DatetimeIndex) and fixed.index.is_monotonic_increasing
            and "Date" not in fixed.columns and list(fixed["Close"]) == [10.5, 11.5, 12.5]
            and "Date" in raw.columns)  # input unmodified
check("Ex3 repair: DatetimeIndex, sorted, numeric, input untouched", _repair)
check("Ex3 repair: no Date column -> ValueError", lambda: raises(ValueError, lambda: repair_loaded_frame(F.reset_index(drop=True))))
check("Ex3 repair: duplicate dates -> ValueError", lambda: raises(ValueError, lambda: repair_loaded_frame(
    pd.DataFrame({"Date": ["2021-01-04", "2021-01-04"], "Close": [1.0, 2.0]}))))

check("Ex4 panel: all tickers in data order", lambda: list(get_close_panel(M).columns) == ["AAA", "BBB"])
check("Ex4 panel: requested order respected", lambda: list(get_close_panel(M, ["BBB", "AAA"]).columns) == ["BBB", "AAA"])
check("Ex4 panel: unknown ticker -> KeyError", lambda: raises(KeyError, lambda: get_close_panel(M, ["ZZZ"])))
def _copy_safe():
    panel = get_close_panel(M); before = M.loc[:, ("Close", "AAA")].iloc[0]
    panel.iloc[0, 0] = -999.0
    return M.loc[:, ("Close", "AAA")].iloc[0] == before
check("Ex4 panel: mutating result leaves source intact", _copy_safe)

check("Ex5 slice: inclusive bounds", lambda: len(slice_date_range(F, "2021-01-05", "2021-01-06")) == 2)
check("Ex5 slice: Saturday start tolerated", lambda: slice_date_range(F, "2021-01-02", "2021-01-05").index.min() == pd.Timestamp("2021-01-04"))
check("Ex5 slice: unsorted input handled", lambda: slice_date_range(F.iloc[[2, 0, 1]], "2021-01-04", "2021-01-06").index.is_monotonic_increasing)
check("Ex5 slice: empty window -> ValueError", lambda: raises(ValueError, lambda: slice_date_range(F, "2022-01-01", "2022-02-01")))
check("Ex5 slice: start>end -> ValueError", lambda: raises(ValueError, lambda: slice_date_range(F, "2021-02-01", "2021-01-01")))

def _project():
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "multi.csv"; M.to_csv(src)
        out = Path(tmp) / "deep" / "panel.csv"
        rep = build_close_panel_file(src, "2021-01-05", "2021-01-06", out)
        back = load_prices(out)
        return (rep["n_rows"] == 2 and rep["tickers"] == ["AAA", "BBB"]
                and rep["missing_by_ticker"] == {"AAA": 0, "BBB": 1}
                and list(back.columns) == ["AAA", "BBB"] and len(back) == 2)
check("F project: load multi -> close panel -> slice -> flat CSV + summary", _project)

print(f"\nSCORE: {sum(RESULTS)}/{len(RESULTS)} visible checks passing")
""")

md(r"""
---
## SECTION H — Knowledge Check

**H1 — Predict, then verify:** `pd.read_csv` *without* `header=[0,1]` on the multi-ticker file: what row appears first in the data, and what dtype does `Close` data end up with? Why?

✍️

**H2 — Explain why:** two students reload the same CSV; one gets an `Unnamed: 0` column, the other doesn't. Reconstruct each student's exact `read_csv` call.

✍️

**H3 — Defend your implementation:** state the three `read_csv` arguments your project uses and, for each, the specific corruption that returns if it is removed.

✍️

**H4 — What-if:** `yfinance` adds a third header row (exchange) tomorrow. Which of today's functions break, which survive, and what is the *first* diagnostic you'd run?

✍️

**H5 — Critique the number:** BANK's Close `std` dwarfs ORNG's in D2. Give the two-sentence refutation of "BANK is therefore the riskiest", and name the quantity Day 06 will use instead.

✍️

**H6 — Design:** Day 03 will *plot* this panel and immediately "see" that one line is higher than another. Predict why that chart will be honest-looking but analytically useless without one more transformation.

✍️
""")

md(r"""
---
## SECTION I — Reflection & Retrieval Practice

### What I learned (concepts, not activities)
-
-
-

### What I can now implement without the video
-
-

### What I still find difficult (bring back — Day 03 adapts)
-
-

### Retrieval practice — Day 01, from memory (answer first, check after)
1. `head(df)` fails because `head` is a _______. `len(df)` works because `len` is a _______. Give one more example of each.
2. On a DatetimeIndex, `close[-1]` vs `close.iloc[-1]`: which is label-based, and what silent wrong answer can label-position confusion produce on shuffled rows?
3. Name **four** rejections your Day 01 `validate_ohlcv` performs, and the exception type for each.
4. A frame passes all `validate_ohlcv` checks yet produces a nonsense backtest on Day 08. Give one concrete way.
5. Friday→Monday is not missing data. What *would* a genuinely missing trading day look like, and which attribute comparison detects it?

### Reimplementation challenge — Day 01's Exercise 3, from memory
""")
code(r"""
# SECTION I - from memory: Day 01 core skill
def first_and_last_close_from_memory(df):
    '''Flat OHLCV frame -> (earliest Close, latest Close) as floats BY DATE,
    regardless of row order. Empty frame -> ValueError.'''
    # TODO (from memory - no peeking at Day 01)
    pass

try:
    _ok = first_and_last_close_from_memory(df.iloc[::-1]) == (float(df["Close"].iloc[0]), float(df["Close"].iloc[-1]))
except Exception as exc:
    _ok = False; print("self-check raised:", type(exc).__name__, exc)
print("Day-01 reimplementation self-check:", "PASS" if _ok else "not yet - Day 01 needs a revisit before Day 03")
""")
md(r"""
### ✅ Completion checklist
- [ ] Watched **13:00–23:00**, summary written in my own words
- [ ] D1–D3 predictions written *before* running; modifications attempted
- [ ] Exercises 1–5 self-implemented; Ex. 3 three-defect diagnosis written
- [ ] **P0.2** built; output reloads cleanly through my own `load_prices`; `.describe()` bullets cite real numbers
- [ ] Section G green **after Kernel → Restart & Run All**
- [ ] Section H answered; retrieval attempted *from memory*; reimplementation honest

**Send back:** Section G score · your H3 defence · your "still difficult" list — and tell me if Day 01's reimplementation above passed first try. **Day 03** (23:00–44:40, visualisation & normalisation) is next; say **"produce the next"** when these are done.
""")

nb = new_notebook(cells=CELLS)
nb.metadata.update({
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.11"},
    "title": "Day 02 - Working With Data: Save, Reload, Segregate",
    "source_video": "https://www.youtube.com/watch?v=GDMkkmkJigw (13:00-23:00)",
})
out = ROOT / "notebooks" / "Day_02_Working_With_Data_Read_Write_Segregate.ipynb"
nbformat.write(nb, out)
print("wrote", out, "cells=", len(CELLS))
