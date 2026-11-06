"""Build Day 09 notebook. Instructor utility."""
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

# Day 09 — Long-Only Bias, Transaction Costs & Honest Comparison · 🏁 Milestone 3

| | |
|---|---|
| **Video segment** | **02:11:40–02:16:30** — *Long bias Strategy* · **Challenge 3** ([watch](https://www.youtube.com/watch?v=GDMkkmkJigw&t=7900s)) |
| **Estimated study time** | **2.5–3 hours** (short 5-minute video; deep analytical comparison + Milestone 3 gate) |
| **Prerequisites** | Day 08 green: `positions_from_signal`, `performance_summary`, `trade_count`, equal-window benchmarking |
| **Data** | `df_long` — **synthetic** ~10-year index history (`data/sample/long_spy_like.csv`, seed 808) |
| **Expected deliverable** | **🏁 Milestone 3:** 3-way comparison CSV + Challenge 3 drawdown plots + 1-page evidence-backed verdict (`projects/MILESTONE_3.md`) |

## Learning objectives — by the end of today you will be able to

1. **Derive** causal long-only positions (`{0, 1}`) from a `{-1, 0, +1}` crossover signal while preserving `.shift(1)` timing discipline.
2. **Apply** flat transaction costs per unit position change (`cost_rate × |Δposition|`, **[programme addition]**) in log-return space and state why it is a first-order research approximation.
3. **Diagnose** two high-frequency backtest bugs: charging transaction costs on every held bar and charging them on the unshifted signal.
4. **Execute Challenge 3** by building a symmetric 3-way comparison (`buy_and_hold`, `long_short`, `long_only`) on identical windows across total return, annualised vol, max drawdown, trade count, and time in market.
5. **Run a cost-breakeven scan** and defend a nuanced *"better, for whom?"* verdict that explicitly names its statistical and modelling limitations.
""")

md(r"""
---
## SECTION B — Video Learning · 02:11:40–02:16:30

**Pre-watch questions** (write your guesses first; checked in Section H):
1. Broad equity indices tend to drift upward over decades (inflation + earnings growth). When an SMA crossover goes `-1` (short) during mild pullbacks, what happens to its P&L when the market V-rebounds before the slow average turns up?
2. Changing `-1 → 0` turns a long/short strategy into a **long-only (cash-when-bearish)** strategy. On days when position is `0`, what is your daily return (assuming zero cash yield) and what happens to your strategy's volatility?
3. When flipping from `+1` to `-1` vs stepping from `+1` to `0`, how many *units* of stock do you trade in each move?
4. Predict **Challenge 3** (~02:15:30): after comparing returns of Buy&Hold, Long/Short, and Long-Only, which risk metric from Day 07 will he challenge you to compare across all three?

| Time | Chapter | Watch for |
|---|---|---|
| 02:11:40 | Long bias Strategy | Replacing `-1` with `0` (`np.where(SMA_S > SMA_L, 1, 0)`) because equities carry a secular upward drift |
| 02:15:30 | **Challenge 3** | Compute and compare **maximum drawdowns** across Buy & Hold, Long/Short, and Long-Only |
| 02:16:30 | ⛔ STOP | *Creating a function* is Day 10 |

Fallback: [02:11:40](https://www.youtube.com/watch?v=GDMkkmkJigw&t=7900s) · [Challenge 3 ~02:15:30](https://www.youtube.com/watch?v=GDMkkmkJigw&t=8130s) · [stop at 02:16:30](https://www.youtube.com/watch?v=GDMkkmkJigw&t=8190s)
""")

code(r"""
# ▶️ SECTION B (code) - 02:11:40 to 02:16:30
from IPython.display import YouTubeVideo, display
display(YouTubeVideo("GDMkkmkJigw", start=7900, end=8190, width=800, height=450))
print("Fallback: https://www.youtube.com/watch?v=GDMkkmkJigw&t=7900s  (stop at 02:16:30)")
""")

md(r"""✍️ **My 3-bullet summary + Challenge 3 in one sentence (edit me):** - · - · Challenge 3 = …""")

md(r"""
---
## SECTION C — Concept Notes

### C1. Why long-only (`{0, 1}`) rescues trend-following on upward-drifting assets
Split the tradable calendar into days where the shifted signal is bullish (`in`) and days where it is bearish (`out`), with cumulative market log returns `L_in` and `L_out`:
- **Buy & Hold:** `L_in + L_out` (always `+1`)
- **Long-Only:** `L_in` (`+1` when bullish, `0` when bearish)
- **Long/Short:** `L_in − L_out` (`+1` when bullish, `-1` when bearish)

Whenever `L_out > 0` — common on equity indices where sharp V-recoveries start *before* `SMA50` crosses back above `SMA100` — shorting loses `L_out` instead of earning `0`, forcing `Buy & Hold > Long-Only > Long/Short` in gross return. Meanwhile, sitting in `0` during bear stretches zeroes out daily variance and cushions crisis drawdowns (**Challenge 3**).

### C2. Transaction costs per unit turnover **[programme addition]**
The video charges `$0` to trade. In reality, commissions, bid-ask spread, and market impact bite **when your position changes**, proportional to units traded:
`turnover_t = |position_t − position_{t−1}|` (with `position_{-1} = 0`, starting from cash).
- Steady hold (`+1 → +1` or `0 → 0`): `turnover = 0` → **zero cost**.
- Enter or exit long-only (`0 → +1` or `+1 → 0`): `turnover = 1` → cost `1 × cost_rate`.
- Direct reversal (`+1 → −1` or `−1 → +1`): `turnover = 2` (sell 1 long *and* sell 1 short) → cost `2 × cost_rate`.

We subtract `cost_rate * turnover_t` directly from `strategy_log_returns` (`[approximation note]`: exact in log space would be `ln(1 − cost_rate * turnover_t)` for unlevered capital, which matches `−cost_rate * turnover_t` to `O(cost_rate²)` — e.g. at `10 bps = 0.001`, `0.001` vs `0.0010005` — clean and transparent for research sketches). For symmetric fairness, passive Buy & Hold (`position = [1, 1, …, 1]`) also runs through the exact same cost function, paying `1 × cost_rate` on day 0.

### C3. "Better" is a vector, never a scalar
Day 04 needed two numbers (return + vol); Day 07 added a third (max drawdown); Day 08–09 add **turnover/costs** and **time in market**. A pension fund that cannot stomach a `-38%` drawdown and a 25-year-old accumulator who hates giving up upside during V-recoveries can look at the *exact same* table and rationally pick different rows. Milestone 3 grades the **honesty of that trade-off argument**, not cheerleading for a winner.

### C4. Window cherry-picking: how honest researchers fool themselves
Pick a bear-heavy sub-window (e.g. `2018–2023` on `df_long`) and Long-Only beats Buy & Hold even after modest costs; zoom out to the full `2015–2024` decade and Buy & Hold leads on terminal wealth. Testing multiple windows or SMA pairs (`50/100`, `20/100`, `50/200`) and reporting only the flattering one is **selection / cherry-picking bias**. Always report the full sample first.
""")

code(WEEK2_SETUP_CODE)

md(r"""
---
## SECTION D — Guided Exploration

### D1 — Gross 3-way comparison + Challenge 3 drawdowns on `df_long`
**Predict:** on `df_long` (`SMA50/100`, `cost_rate=0`), rank `[Buy & Hold, Long/Short, Long-Only]` by (a) terminal `$1` wealth and (b) shallowest max drawdown (closest to `0%`).
""")
md(r"""✍️ **D1 prediction (edit me):** wealth rank: 1) ___ 2) ___ 3) ___ · shallowest maxDD rank: 1) ___ 2) ___ 3) ___""")
code(r"""
# D1 - gross 3-way wealth + Challenge 3 drawdowns on identical 2,420-day window
p = df_long["Close"]
lr = np.log(p / p.shift(1))
f50, s100 = p.rolling(50, min_periods=50).mean(), p.rolling(100, min_periods=100).mean()
raw_sig = pd.Series(np.where(f50 > s100, 1, np.where(f50 < s100, -1, 0)), index=p.index)
pos_ls = raw_sig.shift(1, fill_value=0).iloc[100:]
pos_lo = pos_ls.clip(lower=0)
bh_r = lr.iloc[100:]

curves = pd.DataFrame({
    "Buy & Hold": np.exp(bh_r.cumsum()),
    "Long/Short (+-1)": np.exp((pos_ls * bh_r).cumsum()),
    "Long-Only (1/0)": np.exp((pos_lo * bh_r).cumsum()),
})
dd_curves = curves.div(curves.cummax().clip(lower=1.0)) - 1.0
for col in curves.columns:
    print(f"{col:18s} | terminal $1 = {curves[col].iloc[-1]:.3f} | maxDD = {dd_curves[col].min()*100:.2f}%")
# TODO(modify): verify C1's identity: print bh_r[pos_lo == 1].sum() (L_in) and bh_r[pos_lo == 0].sum() (L_out).
""")
md(r"""
✍️ **D1 observed (edit me):** `L_in = ____`, `L_out = ____`. Because `L_out > 0`, switching `-1 → 0` lifted terminal `$1` from `$____` to `$____`, while cutting Buy & Hold's max drawdown from `____%` to `____%`.

### D2 — Turnover asymmetry: why Long/Short pays ~2× Long-Only's friction
**Predict:** if `pos_lo` changes state `20` times over the decade (`0 ↔ 1`), roughly how many **units** (`sum(|Δpos|)`) does `pos_lo` trade vs `pos_ls` (`-1 ↔ +1`)?
""")
md(r"""✍️ **D2 prediction (edit me):** """)
code(r"""
# D2 - count rebalance bars vs total unit turnover
turn_bh = (pd.Series(1, index=bh_r.index) - pd.Series(1, index=bh_r.index).shift(1, fill_value=0)).abs()
turn_lo = (pos_lo - pos_lo.shift(1, fill_value=0)).abs()
turn_ls = (pos_ls - pos_ls.shift(1, fill_value=0)).abs()
print("Buy & Hold | change bars:", int((turn_bh > 0).sum()), "| total units traded:", int(turn_bh.sum()))
print("Long-Only  | change bars:", int((turn_lo > 0).sum()), "| total units traded:", int(turn_lo.sum()))
print("Long/Short | change bars:", int((turn_ls > 0).sum()), "| total units traded:", int(turn_ls.sum()))
for bps in (0, 10, 25, 50):
    c = bps / 10_000
    print(f"cost={bps:2d} bps -> LO terminal $1: {np.exp((pos_lo*bh_r - c*turn_lo).cumsum().iloc[-1]):.3f} "
          f"| LS terminal $1: {np.exp((pos_ls*bh_r - c*turn_ls).cumsum().iloc[-1]):.3f}")
# TODO(modify): why did Long/Short trade 2x-1 units instead of exactly 2x? (Look at bar 0's initial entry from cash!)
""")
md(r"""
✍️ **D2 observed (edit me):** every interior reversal flips `+1 ↔ -1` (`|Δ| = ____`) vs `0 ↔ 1` (`|Δ| = ____`), so transaction costs punish `________` roughly twice as fast per crossover.

### D3 — Window sensitivity & cost breakeven (`2018–2023` vs full `2015–2024`)
**Predict:** on the crash-and-bear sub-window `2018-01-01 .. 2023-06-30`, Long-Only starts *ahead* of Buy & Hold at `0 bps`. Roughly where (`10 bps`? `85 bps`? `300 bps`?) will transaction costs erase Long-Only's return edge?
""")
md(r"""✍️ **D3 prediction (edit me):** """)
code(r"""
# D3 - sub-window breakeven + cherry-picking lesson
sub = df_long["Close"].loc["2018-01-01":"2023-06-30"]
f_s, s_s = sub.rolling(50, min_periods=50).mean(), sub.rolling(100, min_periods=100).mean()
lr_s = np.log(sub / sub.shift(1)).iloc[100:]
sig_s = pd.Series(np.where(f_s > s_s, 1, np.where(f_s < s_s, -1, 0)), index=sub.index)
pos_s = sig_s.shift(1, fill_value=0).iloc[100:].clip(lower=0)
turn_s = (pos_s - pos_s.shift(1, fill_value=0)).abs()
bh_turn_s = pd.Series([1] + [0] * (len(lr_s) - 1), index=lr_s.index)
for c in [0.0, 0.002, 0.005, 0.008, 0.010, 0.012]:
    lo_tot = float(np.exp((pos_s * lr_s - c * turn_s).sum()) - 1)
    bh_tot = float(np.exp((lr_s - c * bh_turn_s).sum()) - 1)
    print(f"cost={c*10_000:5.0f} bps | BH={bh_tot:+.4f} | LO={lo_tot:+.4f} | excess={lo_tot - bh_tot:+.4f}")
# TODO(modify): run the exact same loop on the FULL `df_long["Close"]`. Does LO ever beat BH on total return there?
""")
md(r"""✍️ **D3 observed (edit me):** on `2018–2023`, LO beats BH until ~`____ bps`; on full `2015–2024`, `____` leads at every cost rate. Cherry-picking `2018–2023` in a pitch deck would be dishonest because `____`.""")

md(r"""
---
## SECTION E — Independent Practice

### Exercise 1 — Basic: causal long-only positions
""")
code(r"""
def long_only_positions(signal):
    '''Map a 1D crossover signal Series (entries in {-1, 0, 1}, NaNs treated as 0)
    to causal long-only positions in {0, 1} via a +1 bar shift:
      - Negative signals (-1) become flat (0); +1 stays 1; 0/NaN stay 0.
      - Row 0 is 0 (shifted in from initial cash state).
      - Returns int-dtype Series with index preserved and name="position".
      - Empty Series or any non-NaN value outside {-1, 0, 1} -> ValueError.
      - Input unmodified.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Validate `signal` exactly as in Day 08's `positions_from_signal`, replace `-1` (and `NaN`) with `0`, then shift forward by 1 bar with `fill_value=0`.</details>
<details><summary>Hint 2 — clue</summary>`clean = signal.fillna(0)`; check `set(np.unique(clean)).issubset({-1, 0, 1})`, then `clean.clip(lower=0).shift(1, fill_value=0).astype(int)` with `.name = "position"`.</details>

### Exercise 2 — Modification: `apply_transaction_costs` **[programme addition]**
""")
code(r"""
def apply_transaction_costs(strategy_log_returns, positions, cost_rate=0.001):
    '''Subtract flat per-unit turnover costs from `strategy_log_returns` (C2):
      net_t = strategy_log_returns_t - cost_rate * |positions_t - positions_{t-1}|
    where `positions_{-1} = 0` (initial cash state via `shift(1, fill_value=0)`).
    Validation:
      - `cost_rate` must be a non-negative real number (`>= 0`, not bool) -> else ValueError.
      - `strategy_log_returns` and `positions` must be non-empty 1D Series with
        identical indices (`index.equals`) and no NaNs in `positions` -> else ValueError.
    Return float Series named "net_log_returns"; inputs unmodified.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Compute unit turnover `|positions - positions.shift(1, fill_value=0)|` and subtract `cost_rate * turnover` from a float copy of `strategy_log_returns`.</details>
<details><summary>Hint 2 — approach</summary>Guard `isinstance(cost_rate, (int, float, np.number)) and not isinstance(cost_rate, bool) and cost_rate >= 0`. Check `positions.index.equals(strategy_log_returns.index)` before subtracting so silent pandas alignment NaNs cannot happen.</details>
<details><summary>Hint 3 — clue</summary>Sanity-check three cases: all-zero positions → zero cost; constant `[1, 1, 1]` → cost `1 * cost_rate` on bar 0 only; `[1, -1]` → bar 0 pays `1 * cost_rate`, bar 1 pays `2 * cost_rate`.</details>

### Exercise 3 — Debugging: two classic transaction-cost blunders

Study the buggy function, diagnose **both** errors in prose, then implement `position_turnover(positions)` cleanly below.
""")
code(r"""
# --- BUGGY COST MODEL (study; do not edit) ---
def apply_costs_buggy(gross_log_returns, raw_signal, cost_rate=0.001):
    pos = raw_signal.shift(1, fill_value=0)
    holding_drag = cost_rate * pos.abs()                       # bug 1
    wrong_day_fee = cost_rate * raw_signal.diff().abs().fillna(0)  # bug 2
    return gross_log_returns - holding_drag - wrong_day_fee

_sig_demo = pd.Series([1, 1, 1, 1, 1], index=pd.bdate_range("2022-01-03", periods=5))
_gross_demo = pd.Series([0.0] * 5, index=_sig_demo.index)
print("Buggy net returns on 5 flat-price days while holding +1:\n",
      apply_costs_buggy(_gross_demo, _sig_demo, cost_rate=0.001))
""")
md(r"""✍️ **Diagnosis (edit me):** Bug 1 (`cost_rate * pos.abs()`): charges `____` instead of trading events — at `10 bps`, holding for 252 days bleeds `____%`/yr! Bug 2 (`raw_signal.diff()`): timestamps the commission on `____` instead of the execution bar `____` (and misses bar 0's initial entry from cash).""")
code(r"""
def position_turnover(positions):
    '''Return a float Series named "turnover" of |positions_t - positions_{t-1}|
    assuming cash (`0`) prior to bar 0 (`shift(1, fill_value=0)`).
    Empty Series or any NaN in `positions` -> ValueError. Input unmodified.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Isolate the exact turnover calculation that Bug 1 and Bug 2 mangled, so `apply_transaction_costs` and `compare_strategies` can compose it cleanly.</details>
<details><summary>Hint 2 — clue</summary>`(positions - positions.shift(1, fill_value=0)).abs().astype(float)` with `.name = "turnover"` after checking `isinstance(positions, pd.Series)`, `len(positions) > 0`, and `not positions.isna().any()`.</details>

### Exercise 4 — Independent: symmetric 3-way `compare_strategies` (Challenge 3 + costs)
""")
code(r"""
def compare_strategies(prices, fast=50, slow=100, cost_rate=0.0):
    '''Compare Buy & Hold, Long/Short (+-1), and Long-Only (1/0) on the IDENTICAL
    post-warm-up tradable window `prices.index[slow:]`, net of `cost_rate`:
      - Index (exact order): ["buy_and_hold", "long_short", "long_only"]
      - Columns (exact order): ["total_return", "annualised_vol", "max_drawdown", "trades", "n_days"]
      - All 3 legs start at `prices.index[slow]` (`n_days == len(prices) - slow`),
        use Day-08 semantics (3-state signal: > -> +1, < -> -1, == -> 0; shifted +1;
        $1.00 drawdown peak anchor; ddof=1 vol * sqrt(252)), and pass through
        `apply_transaction_costs(..., cost_rate=cost_rate)` (Buy & Hold holds
        position 1 on every tradable bar, so trades == 1 and day-0 entry pays cost_rate).
    Validation: same as Day 08 (`1 <= fast < slow`, `len(prices) > slow`, positive
    NaN-free Series, `cost_rate >= 0`) -> else ValueError.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Build the full-length signal once, derive shifted `pos_ls` and `pos_lo` (`long_only_positions`), slice `.iloc[slow:]` for `bh_pos = pd.Series(1, index=tradable_idx)`, `pos_ls`, `pos_lo`, and market `lr`, then run one loop over the 3 legs.</details>
<details><summary>Hint 2 — approach</summary>Notice a subtle boundary check on `pos_lo.iloc[slow:]`: because `pos_lo` is sliced to `tradable_idx`, passing `pos_lo_tradable` into `apply_transaction_costs` and Day-08's `trade_count` treats prior cash state as `0` right before `tradable_idx[0]` — matching `bh_pos` (`[1, 1, ...]`, 1 initial entry from cash) symmetrically!</details>
<details><summary>Hint 3 — clue</summary>Verify `df_out.loc[:, "n_days"]` has identical `int` values across all 3 rows, and at `cost_rate=0.0` `long_only`'s `max_drawdown` matches D1 (`>= buy_and_hold`'s `max_drawdown`, i.e. less negative, on `df_long`).</details>

### Exercise 5 — Transfer: `cost_breakeven_scan`
""")
code(r"""
def cost_breakeven_scan(prices, fast=50, slow=100,
                        cost_rates=(0.0, 0.0005, 0.001, 0.002, 0.005, 0.01)):
    '''Evaluate `compare_strategies(prices, fast, slow, cost_rate=c)` across `cost_rates`
    (sorted ascending) and return a DataFrame (RangeIndex) with exact columns:
      ["cost_rate", "buy_and_hold_return", "long_only_return", "excess_return"]
    where `excess_return = long_only_return - buy_and_hold_return`.
    Empty `cost_rates` or any negative/bool rate -> ValueError.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Turn D3's manual loop into a clean table-returning function (no plotting inside). Where `excess_return` flips from `> 0` to `<= 0` is the strategy's friction ceiling.</details>
<details><summary>Hint 2 — clue</summary>Materialise `rates = sorted(float(c) for c in cost_rates)` after checking non-empty and non-bool `c >= 0`; call `compare_strategies` per rate and collect rows.</details>
""")

md(r"""
---
## SECTION F — Mini-Project · 🏁 Milestone 3 Verdict & Challenge 3 Report

### Specification — `build_milestone3_report(prices, output_csv, fast=50, slow=100, cost_rate=0.001)`
- Start from `compare_strategies(prices, fast=fast, slow=slow, cost_rate=cost_rate)`.
- Append column `"time_in_market"` (`float` in `[0, 1]`, fraction of tradable bars with `position != 0` for each leg: `1.0` for `buy_and_hold`, active fraction for `long_short` and `long_only`).
- Save to `output_csv` (parents created, index label `"strategy"`) and return the 6-column DataFrame.

**Then:** run on `df_long["Close"]` at `cost_rate=0.001` (`10 bps`) → `data/processed/day09_milestone3_comparison.csv`, plot the two-panel **Challenge 3 chart** (`$1` net wealth top + underwater drawdown `%` bottom), run `cost_breakeven_scan`, and complete the **1-page Milestone 3 verdict** below against `projects/MILESTONE_3.md`.
""")
code(r"""
def build_milestone3_report(prices, output_csv, fast=50, slow=100, cost_rate=0.001):
    '''See Section F specification.'''
    # TODO
    pass
""")
code(r"""
# SECTION F (apply)
try:
    m3_tbl = build_milestone3_report(
        df_long["Close"], PROCESSED / "day09_milestone3_comparison.csv", fast=50, slow=100, cost_rate=0.001
    )
    print("=== Full ~10y comparison (net of 10 bps) ===")
    print(m3_tbl.round(4))
    print("\n=== Cost scan (2018-2023 bear-heavy window vs full sample) ===")
    print(cost_breakeven_scan(df_long["Close"].loc["2018-01-01":"2023-06-30"], 50, 100).round(4))

    # Challenge 3 two-panel chart (net of 10 bps)
    _p = df_long["Close"]; _lr = np.log(_p / _p.shift(1)).iloc[100:]
    _f, _s = _p.rolling(50).mean(), _p.rolling(100).mean()
    _sig = pd.Series(np.where(_f > _s, 1, np.where(_f < _s, -1, 0)), index=_p.index)
    _pls = _sig.shift(1, fill_value=0).iloc[100:]
    _plo = long_only_positions(_sig).iloc[100:]
    _pbh = pd.Series(1, index=_lr.index)
    _w = pd.DataFrame({
        "Buy & Hold (net)": np.exp(apply_transaction_costs(_lr, _pbh, 0.001).cumsum()),
        "Long/Short (net)": np.exp(apply_transaction_costs(_pls * _lr, _pls, 0.001).cumsum()),
        "Long-Only (net)": np.exp(apply_transaction_costs(_plo * _lr, _plo, 0.001).cumsum()),
    })
    _dd = (_w.div(_w.cummax().clip(lower=1.0)) - 1.0) * 100
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    _w.plot(ax=axes[0], title="Milestone 3 / Challenge 3: Net $1 Wealth (10 bps cost, synthetic ~10y)")
    axes[0].set_ylabel("Wealth ($)")
    _dd.plot(ax=axes[1], title="Challenge 3: Underwater Drawdown (%)")
    axes[1].set_ylabel("Drawdown (%)"); plt.tight_layout(); plt.show()
except Exception as exc:
    print("Milestone 3 report not ready yet:", type(exc).__name__, exc)
""")
md(r"""
✍️ **🏁 Milestone 3 — 1-Page Backtest v1 Verdict (edit me; check `projects/MILESTONE_3.md`):**

1. **Recommendation ("Better, for whom?"):**
   - *For a drawdown-constrained mandate:* …
   - *For an unconstrained long-horizon accumulator:* …
2. **Evidence summary (cite exact numbers from `m3_tbl` at `10 bps`):** …
3. **Transaction-cost & window sensitivity (full decade vs `2018–2023` scan):** …
4. **Explicit limitations (minimum 5 — single synthetic asset, parameter `50/100` selection risk, flat log-space cost approximation, zero cash yield while flat, close-to-close execution assumption):**
   - …
   - …
   - …
   - …
   - …

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

_idx6 = pd.bdate_range("2022-01-03", periods=6)
check("Ex1 long_only_positions maps -1->0, shifts +1, row 0 is 0, int dtype", lambda: (
    lambda p: list(p.values) == [0, 1, 0, 1, 0, 0] and p.dtype.kind in "iu" and p.name == "position")(
        long_only_positions(pd.Series([1, -1, 1, -1, 0, 1], index=_idx6))))
check("Ex1 NaNs->0; invalid signal values or empty -> ValueError", lambda: (
    list(long_only_positions(pd.Series([np.nan, -1.0, 1.0], index=_idx6[:3])).values) == [0, 0, 0]
    and raises(ValueError, lambda: long_only_positions(pd.Series([0, 2, -1])))
    and raises(ValueError, lambda: long_only_positions(pd.Series([], dtype=float)))))

_zero_lr = pd.Series([0.0] * 5, index=_idx6[:5])
check("Ex2 flat 0 position -> zero transaction cost everywhere", lambda: np.allclose(
    apply_transaction_costs(_zero_lr, pd.Series([0, 0, 0, 0, 0], index=_idx6[:5]), 0.005), 0.0))
check("Ex2 steady hold [1,1,1,1,1] pays cost ONLY on bar 0 entry", lambda: np.allclose(
    apply_transaction_costs(_zero_lr, pd.Series([1, 1, 1, 1, 1], index=_idx6[:5]), 0.002),
    [-0.002, 0.0, 0.0, 0.0, 0.0]))
check("Ex2 direct reversal +1 -> -1 charges 2x unit cost_rate", lambda: np.allclose(
    apply_transaction_costs(_zero_lr, pd.Series([1, 1, -1, -1, 0], index=_idx6[:5]), 0.001),
    [-0.001, 0.0, -0.002, 0.0, -0.001]))
check("Ex2 negative cost_rate or index mismatch -> ValueError", lambda: (
    raises(ValueError, lambda: apply_transaction_costs(_zero_lr, pd.Series([1]*5, index=_idx6[:5]), -0.001))
    and raises(ValueError, lambda: apply_transaction_costs(_zero_lr, pd.Series([1]*5), 0.001))))

check("Ex3 position_turnover values + name", lambda: (
    lambda t: t.name == "turnover" and np.allclose(t.values, [1., 0., 2., 1.]))(
        position_turnover(pd.Series([1, 1, -1, 0], index=_idx6[:4]))))

# Unseen crash-then-flat path where gross Long-Only beats Buy & Hold, then costs erode it
_regime_p = pd.Series(
    [100., 103., 107., 112., 118., 112., 102., 90., 80., 72., 72., 72., 75., 80., 86.],
    index=pd.bdate_range("2022-04-01", periods=15), name="Close"
)
def _ex4_ok():
    tbl0 = compare_strategies(_regime_p, fast=2, slow=4, cost_rate=0.0)
    tblc = compare_strategies(_regime_p, fast=2, slow=4, cost_rate=0.01)
    return (list(tbl0.index) == ["buy_and_hold", "long_short", "long_only"]
            and list(tbl0.columns) == ["total_return", "annualised_vol", "max_drawdown", "trades", "n_days"]
            and len(set(tbl0["n_days"])) == 1 and int(tbl0.loc["buy_and_hold", "n_days"]) == 11
            and int(tbl0.loc["buy_and_hold", "trades"]) == 1
            and tbl0.loc["long_only", "max_drawdown"] >= tbl0.loc["buy_and_hold", "max_drawdown"]
            and tblc.loc["long_only", "total_return"] < tbl0.loc["long_only", "total_return"])
check("Ex4 compare_strategies: shape, equal windows, Challenge-3 DD ordering & cost impact", _ex4_ok)
check("Ex4 flat prices -> 0 trades on active legs, 0 vol", lambda: (
    lambda t: int(t.loc["long_short", "trades"]) == 0 and int(t.loc["long_only", "trades"]) == 0
    and abs(t.loc["long_only", "total_return"]) < 1e-12)(
        compare_strategies(pd.Series([100.] * 10, index=pd.bdate_range("2022-05-02", periods=10)), 2, 4, 0.002)))

def _ex5_ok():
    scan = cost_breakeven_scan(_regime_p, fast=2, slow=4, cost_rates=[0.20, 0.0, 0.05, 0.10])
    return (list(scan.columns) == ["cost_rate", "buy_and_hold_return", "long_only_return", "excess_return"]
            and list(scan["cost_rate"]) == [0.0, 0.05, 0.10, 0.20]
            and np.allclose(scan["excess_return"], scan["long_only_return"] - scan["buy_and_hold_return"])
            and scan["excess_return"].iloc[0] > 0 and scan["excess_return"].iloc[-1] < 0)
check("Ex5 cost_breakeven_scan sorts grid & captures excess-return sign flip", _ex5_ok)
check("Ex5 empty or negative cost_rates -> ValueError", lambda: (
    raises(ValueError, lambda: cost_breakeven_scan(_regime_p, 2, 4, []))
    and raises(ValueError, lambda: cost_breakeven_scan(_regime_p, 2, 4, [0.0, -0.01]))))

def _proj_ok():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "m3" / "comp.csv"
        rep = build_milestone3_report(_regime_p, out, fast=2, slow=4, cost_rate=0.001)
        back = pd.read_csv(out, index_col=0)
        return (list(rep.columns) == ["total_return", "annualised_vol", "max_drawdown", "trades", "n_days", "time_in_market"]
                and abs(float(rep.loc["buy_and_hold", "time_in_market"]) - 1.0) < 1e-12
                and 0.0 < float(rep.loc["long_only", "time_in_market"]) < 1.0
                and list(back.index) == ["buy_and_hold", "long_short", "long_only"])
check("F project: Milestone 3 CSV round-trips + time_in_market bounds", _proj_ok)
print(f"\nSCORE: {sum(RESULTS)}/{len(RESULTS)} visible checks passing")
""")

md(r"""
---
## SECTION H — Knowledge Check

**H1 (Pre-watch #1 & #2 revisited)** On `df_long`, Long-Only spent roughly a third of the decade in cash (`position == 0`). Explain why its annualised volatility dropped from `~17.9%` to `~14.3%` *without* needing smaller daily moves on the days it was invested. ✍️
**H2 (Pre-watch #3 revisited)** Prove that for `K` interior round-trip regime switches (starting long on bar 0 and ending long), `Long/Short` trades `1 + 2K` units while `Long-Only` trades `1 + K` units. ✍️
**H3 Defend** running passive `Buy & Hold` through `apply_transaction_costs` too (charging `1 × cost_rate` on day 0) instead of hard-coding its cost to `0`. When could even that 1-trade cost matter? ✍️
**H4 Critique the model** Our cost model subtracts `cost_rate * |Δpos|` in log space and assumes `0%` interest on cash when `pos == 0`. Which way does ignoring `4%` Treasury-bill interest bias the Long-Only vs Buy & Hold comparison? ✍️
**H5 What-if (cherry-picking)** A classmate sweeps 40 SMA pairs on `df_long`, finds `(37, 83)` beats Buy & Hold by `+9%`, and puts only `(37, 83)` in their Milestone 3 report. Name the bias and state how Day 13's unseen ticker defeats it. ✍️
**H6 Bridge to Day 10** Today you wrote bespoke loops over `(fast, slow)` and strategies inside notebook cells. List three failure modes of copy-pasting backtest cells across 5 notebooks that refactoring into a pure, zero-global `pytrades/` module will eliminate tomorrow. ✍️
""")

md(r"""
---
## SECTION I — Reflection & Retrieval Practice

### What I learned · Can implement unaided · Still difficult ✍️

### Retrieval — Days 08 (n−1), 06 (n−3), 03 (n−6)
1. **Day 08:** Why is `prices.index[slow]` (not `prices.index[slow - 1]`) the first tradable return date for an `SMA(fast, slow)` crossover?
2. **Day 08:** State the 3-state tie rule when `SMA(fast) == SMA(slow)` and the bug it prevents on flat series.
3. **Day 06:** Convert a `-0.002` log-return cost deduction into its exact simple-return fraction `1 - exp(-0.002)`. How many basis points of approximation error is that?
4. **Day 06:** Two look-ahead cheating devices banned in indicator code.
5. **Day 03:** Why did `normalise` divide by `first_valid_index()` rather than `iloc[0]`, and how is today's `exp(cumsum(r))` curve related to Day 03 rebasing?
""")
code(r"""
def positions_from_signal_from_memory(signal):
    '''Day 08 Ex3 contract FROM MEMORY: {-1, 0, 1} (NaN->0), shift +1 with row 0 = 0,
    int dtype, name="position", invalid/empty -> ValueError.'''
    # TODO
    pass

try:
    _s_mem = pd.Series([1, -1, np.nan, 1], index=pd.bdate_range("2022-01-03", periods=4))
    _p_mem = positions_from_signal_from_memory(_s_mem)
    _ok = list(_p_mem.values) == [0, 1, -1, 0] and _p_mem.dtype.kind in "iu" and _p_mem.name == "position"
except Exception as exc:
    _ok = False; print("self-check raised:", type(exc).__name__, exc)
print("positions_from_signal reimplementation self-check:", "PASS" if _ok else "not yet")
""")
md(r"""
### ✅ Completion checklist — 🏁 Milestone 3 gate
- [ ] Video `02:11:40–02:16:30` watched; Challenge 3 drawdown comparison plotted
- [ ] Ex 1–5 mine; Ex 3 diagnoses both daily-drag and unshifted-commission bugs
- [ ] `data/processed/day09_milestone3_comparison.csv` generated; `cost_breakeven_scan` interpreted on both windows
- [ ] **1-page Milestone 3 verdict** complete with numbers + ≥5 explicit limitations (`projects/MILESTONE_3.md`)
- [ ] Days 01–09 all green after Restart & Run All

**Send back:** Section G score · your 1-page Milestone 3 verdict · H4 & H5 answers. Day 10 graduates your notebook code into a clean, importable `pytrades/` function library.
""")

nb = new_notebook(cells=CELLS)
nb.metadata.update({"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                    "language_info": {"name": "python", "version": "3.11"},
                    "title": "Day 09 - Long-Only Bias and Honest Comparison (Milestone 3)",
                    "source_video": "https://www.youtube.com/watch?v=GDMkkmkJigw (02:11:40-02:16:30)"})
out = ROOT / "notebooks" / "Day_09_Long_Only_Bias_and_Honest_Comparison.ipynb"
nbformat.write(nb, out); print("wrote", out, "cells=", len(CELLS))
