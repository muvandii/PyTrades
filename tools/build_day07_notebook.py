"""Build Day 07 notebook. Instructor utility."""
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

# Day 07 — Alignment, Missing Data, Cumulative Returns & Drawdowns · 🏁 Milestone 2

| | |
|---|---|
| **Video segment** | **01:35:00–01:57:00** — *Reindexing* · *Forward fill and Backfill* · *Cumulative returns and drawdowns* ([watch](https://www.youtube.com/watch?v=GDMkkmkJigw&t=5700s)) |
| **Estimated study time** | **2.5–3.5 hours** (includes Milestone 2 bias-audit review) |
| **Prerequisites** | Days 01–06; returns (both kinds) fluent; crossover *signal* understood as measurement, not strategy |
| **Expected deliverable** | **🏁 Milestone 2:** wealth + drawdown report per ticker with a written **bias audit** (every place future data could have leaked into Week 1, and your evidence it didn't) |

## Learning objectives
1. **Reindex** a panel onto an explicit trading calendar and explain what NaNs that operation is *honestly* introducing.
2. **Choose a fill policy like an adult:** `ffill` (last known price, causal) vs `bfill` (next price — **look-ahead leakage**), and implement alignment that refuses `bfill` by default.
3. **Build wealth/cumulative-return curves** from simple returns (`(1+r).cumprod()`) and reconcile them with Day 03 rebasing and Day 06 log-additivity.
4. **Implement drawdown from scratch** (running peak → `wealth/peak − 1`) and report **max drawdown with its peak & trough dates**.
5. **Execute a Week-1 bias audit** against `projects/MILESTONE_2.md` and sign it.
""")

md(r"""
---
## SECTION B — Video Learning · 01:35:00–01:57:00

**Pre-watch:** 1) If ticker A trades Monday but B's exchange was shut, what *is* B's Monday price? 2) Filling a missing price with tomorrow's value: harmless housekeeping or time travel? 3) A strategy is "-40% in drawdown": 40% below *what*, exactly? 4) Two investments end +50%: can one have been far more painful on the way?

| Time | Chapter | Watch for |
|---|---|---|
| 01:35:00 | Reindexing | Building a target calendar and forcing series onto it — NaNs appear precisely where honesty requires |
| 01:37:45 | Forward fill and Backfill | Both are demonstrated. This programme's stance is stricter: ffill is a *causal modelling choice*, bfill inside analysis data is leakage — you'll encode that stance |
| 01:41:00 | Cumulative returns and drawdowns | Wealth index, previous peaks, drawdown curves and max drawdown — the video's ~80% drawdown example for buy-and-hold through crises should recalibrate your respect for "just hold" |
| 01:57:00 | ⛔ STOP | Strategies begin Day 08 — Week 2 |

Fallback: [01:35:00](https://www.youtube.com/watch?v=GDMkkmkJigw&t=5700s) · [01:41:00](https://www.youtube.com/watch?v=GDMkkmkJigw&t=6060s)
""")
code(r"""
# ▶️ SECTION B (code) - 01:35:00 to 01:57:00
from IPython.display import YouTubeVideo, display
display(YouTubeVideo("GDMkkmkJigw", start=5700, end=7020, width=800, height=450))
print("Fallback: https://www.youtube.com/watch?v=GDMkkmkJigw&t=5700s  (stop at 01:57:00)")
""")
md(r"""✍️ **3-bullet summary (edit me):** - · - · -""")

md(r"""
---
## SECTION C — Concept Notes

### C1. Reindexing: calendars first, values second
`df.reindex(target_index)` aligns rows to exactly those labels — missing labels become NaN rows, extra labels are dropped. It never invents data; it *exposes* absence in a regular shape. With BANK vs DEMO, reindexing BANK onto DEMO's 2020 calendar manufactures Jan–Mar NaN rows: a true statement ("BANK had no listed price then") in rectangular form.

### C2. Filling: every filled value is a claim about the world
- `ffill` claims "price = last traded price" — causal (uses only the past), standard for *valuing* a holding on a non-trading day. Prices may ffill; note that returns computed across an ffill seam then contain fake 0% days.
- `bfill` claims "price = next traded price" — uses the future. Inside anything feeding a backtest it is look-ahead bias with a friendly name. (Legitimate uses exist, e.g. aligning *labels* in supervised learning preprocessing — none occur in this course's backtests.)
- *No fill* (leave NaN, decide per-calculation) is often most honest. Policy must be stated per artifact.

### C3. Wealth & cumulative returns — three views of one object
From simple returns: `wealth = (1 + r).cumprod()` (start 1.0 or scale ×100 — Day 03's rebasing IS a wealth curve in disguise: `price/first × 100`). From log returns: `wealth = exp(cumsum(log r))`. NaN policy: the leading NaN return contributes factor 1.0 *if you say so*; interior NaNs must stop you thinking, not be silently zeroed by habit.

### C4. Drawdown: distance below your highest high-water mark
Running peak `peak_t = max(wealth_0..t)` (a.k.a. `cummax`), `drawdown_t = wealth_t/peak_t − 1 ≤ 0`. **Max drawdown** = the minimum (most negative) drawdown, reported *with* its peak date and trough date. Volatility (Day 04) measures wiggle; drawdown measures pain. Funds get redeemed over the second. The buggy shortcut — dividing by the *global* max — uses peaks that hadn't happened yet: Day 06's cheating devices wearing a new mask.

### C5. Time under water
Fraction of days (or longest stretch) spent below the running peak. Two curves with identical returns and volatility can differ brutally here; it's the investor-experience metric.

### C6. Week 1 ends with an audit, not a victory lap
Every Week-1 function touched data that *could* have leaked future information. Milestone 2 makes you enumerate the traps (bfill, `center=True`, `shift(-1)`, global-max drawdown, `iloc[0]` on unsorted data, price-level "volatility"/correlation) and point at the code/tests that defuse each.
""")

code(SETUP_CODE)

md(r"""
---
## SECTION D — Guided Exploration

### D1 — Reindex BANK onto DEMO's calendar
**Predict:** rows added? NaNs created? Does anything get *filled* by reindex itself?
""")
md(r"""✍️ **D1 prediction (edit me):** """)
code(r"""
# D1
bank = close_panel["BANK"].dropna()
reindexed = bank.reindex(close_panel.index)
print("original:", len(bank), "rows | reindexed:", len(reindexed), "| NaNs:", int(reindexed.isna().sum()))
print("ffill would fill the INTERNAL gaps only if any existed; leading NaNs (pre-listing) survive ffill too:",
      int(reindexed.ffill().isna().sum()), "NaNs remain after ffill")
print("bfill 'fixes' even those:", int(reindexed.bfill().isna().sum()), "<- by claiming BANK traded in January at April prices. Time travel.")
# TODO(modify): reindex DEMO onto a calendar of ALL 366 days of 2020 (pd.date_range). How many NaNs are weekends/holidays
# vs genuinely missing? ffill those and argue whether valuing on Saturdays at Friday close is honest. Record the argument.
""")
md(r"""
✍️ **D1 observed (edit me):** reindex _______ data; it never _______. `bfill` on pre-listing rows claims _______, which is _______ because _______.

### D2 — Wealth three ways
**Predict:** rebasing (Day 03), `cumprod(1+simple)`, `exp(cumsum(log))` — same curve×scale, or subtly different?
""")
md(r"""✍️ **D2 prediction (edit me):** """)
code(r"""
# D2
p = df["Close"]
rebased = p / p.iloc[0]
w_simple = (1 + p.pct_change().fillna(0)).cumprod()
w_log = np.exp(np.log(p / p.shift(1)).fillna(0).cumsum())
print("max |rebased - w_simple|:", float((rebased - w_simple).abs().max()))
print("max |rebased - w_log|   :", float((rebased - w_log).abs().max()))
ax = (rebased * 100).plot(figsize=(10, 3.5), title="DEMO wealth (start=100) - the three constructions coincide")
ax.set_ylabel("Wealth"); plt.tight_layout(); plt.show()
# TODO(modify): break it - replace fillna(0) with fillna(method="bfill")-style thinking on the FIRST return.
# What does the first wealth value become and why is even that small leak philosophically fatal?
""")
md(r"""
✍️ **D2 observed (edit me):** three constructions _______ to float precision. Day 03 normalisation was secretly _______. The `fillna(0)` on the first return asserts _______.

### D3 — Drawdown, seen
""")
code(r"""
# D3
wealth = (p / p.iloc[0]) * 100
peak = wealth.cummax(); dd = wealth / peak - 1
print("max drawdown (DEMO):", round(float(dd.min()) * 100, 2), "%  trough:", dd.idxmin().date(),
      "| peak before it:", wealth.loc[:dd.idxmin()].idxmax().date())
fig, axes = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
wealth.plot(ax=axes[0], title="DEMO wealth"); axes[0].set_ylabel("Wealth")
(dd * 100).plot(ax=axes[1], title="Drawdown % (underwater chart)", color="darkred"); axes[1].set_ylabel("%")
plt.tight_layout(); plt.show()
# TODO(modify): reproduce for ORNG and BANK (own spans). Who had the deepest pain vs who had Day 04's highest vol? Same answer?
""")
md(r"""✍️ **D3 observed (edit me):** DEMO max DD ___% (peak ___ → trough ___). Deepest pain vs highest vol: _______ — one number never tells the whole risk story because …""")

md(r"""
---
## SECTION E — Independent Practice

### Exercise 1 — Basic: alignment with a spine
""")
code(r"""
def align_to_calendar(panel, calendar, fill=None):
    '''Reindex panel (DataFrame or Series, DatetimeIndex) onto `calendar`
    (an index/array of dates). fill:
        None    -> leave NaNs where the calendar introduces them
        "ffill" -> forward-fill AFTER reindexing (leading NaNs stay NaN)
        "bfill" -> raise ValueError: look-ahead leakage is refused by this
                   programme (stricter than the video - message must say why)
    Any other fill -> ValueError. Calendar is sorted ascending in the result,
    duplicates in calendar -> ValueError. Input unmodified.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Validate `fill` first (fail fast on the dangerous option with an instructive message), normalise calendar via `pd.DatetimeIndex(calendar)`, check duplicates, reindex, optionally ffill.</details>
<details><summary>Hint 3 — clue</summary>Tests: calendar includes a Saturday (ffill picks Friday's value; None leaves NaN), a pre-history date (NaN even with ffill), bfill refused, dup calendar refused.</details>

### Exercise 2 — Modification: wealth with an explicit NaN policy
""")
code(r"""
def wealth_from_returns(returns, start_value=100.0):
    '''Wealth curve from SIMPLE returns (Series or DataFrame):
    wealth_t = start_value * prod_{i<=t}(1 + r_i).
    Policy (document in code): NaN returns contribute factor 1.0 (flat) -
    implement via fillna(0) AFTER deciding that is acceptable for leading NaNs;
    any return <= -1 -> ValueError (wealth would hit/pass zero: meaningless curve).
    Index/columns preserved.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>D2 with a contract. Domain check `(r <= -1)` on non-NaN values first; then `(1 + r.fillna(0)).cumprod() * start_value`.</details>
<details><summary>Hint 3 — clue</summary>Compare Day 06: converting prices→returns→wealth must reproduce rebasing. Tests include that round-trip plus the -100% guard.</details>

### Exercise 3 — Debugging: drawdown from the future

Run, diagnose, then implement the correct pair underneath (Ex 4). The buggy curve looks plausible — which is precisely the danger.
""")
code(r"""
# --- BUGGY CODE (study; do not edit) ---
def drawdown_buggy(wealth):
    return wealth / wealth.max() - 1          # <-- one word short of honest

_w = pd.Series([100., 120, 90, 130, 65], index=pd.bdate_range("2021-01-04", periods=5))
print("buggy drawdown at t0 (wealth=100, nothing lost yet):", round(float(drawdown_buggy(_w).iloc[0]) * 100, 1), "%  <-- claims a loss vs a peak 3 days in the FUTURE")
print("buggy 'max drawdown':", round(float(drawdown_buggy(_w).min()) * 100, 1), "% | honest peak-to-trough (130->65): -50.0%")
""")
md(r"""✍️ **Diagnosis (edit me):** `wealth.max()` is the _______ over the *whole* sample; the honest peak at t may only use _______. Early rows are charged for _______. One-word fix family: `c_m___`."""
)
code(r"""
def drawdown_series(wealth):
    '''Drawdown series wealth/running_peak - 1 (<= 0). wealth: Series (already a
    wealth/price curve - ratios are identical). Empty -> ValueError.
    NaNs: use only the valid span (dropna first) - state that in a comment.'''
    # TODO
    pass

def max_drawdown(wealth):
    '''Return {"max_drawdown": float (negative or 0.0), "peak_date": Timestamp,
    "trough_date": Timestamp} where peak_date is the date of the running peak
    that precedes the trough. A never-declining curve: max_drawdown 0.0, peak ==
    trough == first valid date.'''
    # TODO (compose drawdown_series + index gymnastics)
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>`peak = w.cummax()`; `dd = w/peak - 1`; trough = `dd.idxmin()`. For peak_date: the last date ≤ trough where wealth equalled its running peak — equivalently `w.loc[:trough].idxmax()` on the dropped-NaN span.</details>
<details><summary>Hint 3 — clue</summary>Ties/montonic-up edge: if `dd.min() == 0`, choose first valid date for both fields per contract. Tests use _w above (peak 130 @ idx 3, trough 65 @ idx 4, -50%) and a flat-rising curve.</details>

### Exercise 4 — Independent: time under water
""")
code(r"""
def time_under_water(wealth):
    '''Fraction (0..1, of VALID rows) where wealth is strictly below its running
    peak. Plus a second function below. Empty/all-NaN -> ValueError.'''
    # TODO
    pass

def longest_underwater_stretch(wealth):
    '''Length (in rows) of the longest consecutive run of valid rows strictly below
    the running peak. A curve at its peak breaks the run. Monotonic-up -> 0.'''
    # TODO (loops from Day 05 are welcome here; prove it on _w by hand)
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Boolean mask `w < w.cummax()`: fraction = mask.mean(); longest run = scan the mask counting consecutive True (reset on False).</details>

### Exercise 5 — Transfer: prices → risk summary in one honest pipeline
""")
code(r"""
def price_risk_summary(prices):
    '''For a price Series return {"total_return": float, "max_drawdown": float,
    "peak_date": Timestamp, "trough_date": Timestamp, "time_under_water": float}.
    Build wealth by rebasing prices to their first valid value (Day 03) OR via
    returns (Day 06/Ex2) - both must agree; pick one and note the equivalence.
    <2 valid prices -> ValueError; non-positive price -> ValueError.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>This is Week 1 in miniature: validate-ish guards (Day 01), rebase (03), pain metrics (today). Tests cross-check `total_return` against `last/first - 1` and max DD against a hand curve.</details>
""")

md(r"""
---
## SECTION F — Mini-Project · 🏁 Milestone 2 Wealth & Drawdown Report (+ Bias Audit)

### Specification — `build_drawdown_report(panel, output_csv)`
- For each ticker in a price panel: `price_risk_summary` over its own valid span.
- Write a summary CSV (index=ticker, columns `total_return,max_drawdown,peak_date,trough_date,time_under_water`), parents created.
- Return that summary as a DataFrame (dates as Timestamps in the *returned* frame).

**Then:** run on `close_panel` → `data/processed/day07_drawdown_report.csv`; plot wealth (top) + drawdown% (bottom) for all three tickers (shared x-axis; BANK starts April — the chart must *show* that, not hide it); complete the **bias audit** cell per `projects/MILESTONE_2.md`.

**Acceptance:** G project check on unseen 2-ticker panel · audit signed with code references · chart does not bfill BANK into January.
""")
code(r"""
def build_drawdown_report(panel, output_csv):
    '''See Section F.'''
    # TODO
    pass
""")
code(r"""
# SECTION F (apply)
try:
    summ = build_drawdown_report(close_panel, PROCESSED / "day07_drawdown_report.csv")
    print(summ)
    if summ is not None:
        wealth_all = close_panel.div(close_panel.apply(lambda s: s.loc[s.first_valid_index()])) * 100
        dd_all = wealth_all / wealth_all.cummax() - 1
        fig, axes = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
        wealth_all.plot(ax=axes[0], title="Wealth (first valid = 100) - note BANK starts April"); axes[0].set_ylabel("Wealth")
        (dd_all * 100).plot(ax=axes[1], title="Drawdown %"); axes[1].set_ylabel("%"); plt.tight_layout(); plt.show()
except Exception as exc:
    print("report not ready yet:", type(exc).__name__, exc)
""")
md(r"""
✍️ **Bias audit — Week 1 (edit me; use `projects/MILESTONE_2.md`):** For EACH trap: status (absent? where's the proof?):
bfill in analysis data: … · `center=True`: … · `shift(-1)`: … · global-max drawdown: … · `iloc[0]` on unsorted/NaN-first data: … · price-level vol/corr: … · partial-window "SMA200": … · Signed: (name/date)

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

_idx = pd.bdate_range("2021-01-04", periods=5)   # Mon 4th .. Fri 8th
S = pd.Series([10., 11, 12, 13, 14], index=_idx)
_cal = list(_idx) + [pd.Timestamp("2021-01-09")]  # + Saturday
check("Ex1 ffill carries Friday to Saturday; None leaves NaN", lambda: (
    float(align_to_calendar(S, _cal, fill="ffill").iloc[-1]) == 14.0 and bool(np.isnan(align_to_calendar(S, _cal).iloc[-1]))))
check("Ex1 pre-history date stays NaN even ffilled", lambda: bool(np.isnan(
    align_to_calendar(S, [pd.Timestamp("2021-01-01")] + list(_idx), fill="ffill").iloc[0])))
check("Ex1 bfill REFUSED (look-ahead)", lambda: raises(ValueError, lambda: align_to_calendar(S, _cal, fill="bfill")))
check("Ex1 dup calendar & bad fill -> ValueError", lambda: (
    raises(ValueError, lambda: align_to_calendar(S, list(_idx) + [_idx[0]]))
    and raises(ValueError, lambda: align_to_calendar(S, _cal, fill="zero"))))

_r = pd.Series([np.nan, 0.10, -0.10, 0.10], index=_idx[:4])
check("Ex2 wealth: NaN->flat, compounds after", lambda: np.allclose(
    wealth_from_returns(_r, start_value=100.0), [100., 110., 99., 108.9]))
check("Ex2 prices->returns->wealth reproduces rebasing", lambda: (
    lambda p: np.allclose(wealth_from_returns(p.pct_change(), 100.0), p / p.iloc[0] * 100))(pd.Series([50., 55, 44, 66], index=_idx[:4])))
check("Ex2 return <= -1 -> ValueError", lambda: raises(ValueError, lambda: wealth_from_returns(pd.Series([0.1, -1.0]))))

_w = pd.Series([100., 120, 90, 130, 65], index=_idx)
check("Ex3/4 drawdown uses RUNNING peak (t0 == 0)", lambda: float(drawdown_series(_w).iloc[0]) == 0.0 and np.allclose(
    drawdown_series(_w), [0., 0., 90/120-1, 0., 65/130-1]))
check("Ex4 max drawdown value + peak/trough dates", lambda: (
    lambda r: abs(r["max_drawdown"] - (-0.5)) < 1e-12 and r["peak_date"] == _idx[3] and r["trough_date"] == _idx[4])(max_drawdown(_w)))
check("Ex4 monotonic-up: 0.0, peak==trough==first", lambda: (
    lambda r: r["max_drawdown"] == 0.0 and r["peak_date"] == _idx[0] and r["trough_date"] == _idx[0])(max_drawdown(S)))
check("Ex4b time under water (2 of 5)", lambda: abs(time_under_water(_w) - 0.4) < 1e-12)
_w2 = pd.Series([100., 90, 80, 100, 95, 100, 105], index=pd.bdate_range("2021-01-04", periods=7))
check("Ex4b longest underwater stretch == 2", lambda: longest_underwater_stretch(_w2) == 2)

check("Ex5 summary cross-checks (total, DD, TUW)", lambda: (
    lambda r: abs(r["total_return"] - (65/100 - 1)) < 1e-12 and abs(r["max_drawdown"] + 0.5) < 1e-12 and abs(r["time_under_water"] - 0.4) < 1e-12)(price_risk_summary(_w)))
check("Ex5 bad prices -> ValueError", lambda: raises(ValueError, lambda: price_risk_summary(pd.Series([10., 0.0, 5.]))))

def _proj():
    panel = pd.DataFrame({"AAA": _w.values, "BBB": [10., 11, 12, 13, 14]}, index=_idx)
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "r" / "dd.csv"; r = build_drawdown_report(panel, out)
        back = pd.read_csv(out, index_col=0)
        return (abs(r.loc["AAA", "max_drawdown"] + 0.5) < 1e-12 and abs(back.loc["BBB", "max_drawdown"] - 0.0) < 1e-12
                and list(r.columns) == ["total_return", "max_drawdown", "peak_date", "trough_date", "time_under_water"])
check("F project: per-ticker summary + CSV", _proj)
print(f"\nSCORE: {sum(RESULTS)}/{len(RESULTS)} visible checks passing")
""")

md(r"""
---
## SECTION H — Knowledge Check
**H1** Reindex vs ffill vs bfill in one line each, classifying by *what values they invent*. ✍️
**H2** Your `align_to_calendar` refuses bfill. A teammate calls that paternalistic. Two-sentence defence, then one legitimate bfill use *outside* backtest inputs. ✍️
**H3 Defend** reporting peak+trough dates with max drawdown: what decision changes if trough→recovery took 3 years vs 3 weeks at the same −50%? ✍️
**H4** Wealth via rebasing vs via returns disagree by 0.3% on real data with an interior NaN. Where do you look first, and which policy difference does that implicate? ✍️
**H5** Video's buy-and-hold crises showed drawdowns revisiting most people's resolve. Connect: why does Day 09's "which strategy is better?" *require* drawdown alongside return and volatility? ✍️
**H6 Design (Week-2 bridge)** Day 08 multiplies returns by *positions*. Predict where alignment/ffill decisions from *today* could silently corrupt that multiplication. ✍️
""")

md(r"""
---
## SECTION I — Reflection & Retrieval Practice
### Learned · Can implement · Still difficult ✍️
### Retrieval — Days 06, 05, 04, 03 (widening)
1. Log returns ___ over time; simple returns ___; conversions use ___ and ___.
2. Two cheating devices from Day 06, named exactly, and their common category.
3. Correlation must be computed on ___, with BANK pairs effectively covering ___. Off-by-trend price corr inflates toward ___.
4. Annualised vol: formula, input, assumption; the level-invariance check from Day 04's tests in words.
5. Normalisation (Day 03) *is* a wealth curve because … (one clause).
6. Warm-up: SMA50 has ___ leading NaNs and a crossover signal there must read ___.
""")
code(r"""
def max_drawdown_from_memory(wealth):
    '''Running-peak drawdown MINIMUM as a float (<=0) for a wealth Series.
    FROM MEMORY (Day 07 core in 3 moves: cummax, ratio, min).'''
    # TODO
    pass

try:
    _ok = abs(max_drawdown_from_memory(_w) + 0.5) < 1e-12
except Exception as exc:
    _ok = False; print("self-check raised:", type(exc).__name__, exc)
print("drawdown-from-memory self-check:", "PASS" if _ok else "not yet")
""")
md(r"""
### ✅ Completion checklist — Milestone 2 / Week 1 gate
- [ ] Video + D1–D3 with the bfill time-travel case argued in own words
- [ ] Ex 1–5 mine; bfill refusal message *teaches* · - [ ] Report + two-panel chart where BANK honestly starts in April
- [ ] **Bias audit signed** vs `projects/MILESTONE_2.md` with pointers to code/tests
- [ ] All seven notebooks green after Restart & Run All (Week 1 regression rule)

**Send back:** G score · signed bias audit · H5. Week 2 (Days 08–13: backtesting → functions → classes → APIs → capstone) is specified in `WEEK2_AUTHORING_GUIDE.md`.
""")

nb = new_notebook(cells=CELLS)
nb.metadata.update({"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                    "language_info": {"name": "python", "version": "3.11"},
                    "title": "Day 07 - Alignment, Cumulative Returns, Drawdowns",
                    "source_video": "https://www.youtube.com/watch?v=GDMkkmkJigw (01:35:00-01:57:00)"})
out = ROOT / "notebooks" / "Day_07_Alignment_Cumulative_Returns_Drawdowns.ipynb"
nbformat.write(nb, out); print("wrote", out, "cells=", len(CELLS))
