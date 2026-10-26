# 🏁 Milestone 2 — Analytics + Bias Audit (end of Day 07 / Week 1)

## Gate criteria

1. **Notebooks 01–07** all green after Kernel → Restart & Run All (Week-1 regression rule:
   no earlier day may be broken by later work).
2. **Drawdown report** (`data/processed/day07_drawdown_report.csv`) regenerable from
   Day 07 Section F; BANK is *not* backfilled into pre-listing dates anywhere.
3. **Signed bias audit** in Day 07 Section F covering, with pointers to the
   function/test that defuses each:
   - `bfill` into analysis/backtest inputs → refused by `align_to_calendar`
   - `rolling(center=True)` → absent; SMA uses trailing windows only
   - `shift(-1)` returns → absent; signal uses data up to t only
   - global-max drawdown → replaced by running `cummax`
   - `iloc[0]` assumptions on unsorted or NaN-first data → sort + first-valid anchoring
   - price-level volatility/correlation → computed on returns since Day 04/05
   - partial-window moving averages labelled as full → `min_periods == window` enforced
4. **Function inventory updated** from Milestone 1 with the analytics layer
   (returns, SMA/EMA, signal, wealth, drawdown) — this becomes the source code
   harvested into `pytrades/` on Days 10–11.

## Review prompts

- Hand-trace max drawdown (value, peak, trough) on `[100, 120, 90, 130, 65]`.
- Name one remaining place Week 1 code could still mislead in Week 2
  (good candidates: pairwise-mixed correlation windows; wealth NaN policy on interior gaps;
  metrics computed over unequal ticker spans).
- Why is an SMA-crossover *signal* still not a strategy? List what's missing.
