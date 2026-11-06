# 🏁 Milestone 3 — Backtest v1 Review & Honest Verdict (end of Day 09)

**Scope:** your first end-to-end vectorised backtests (Days 08–09): causal position
shifting, equal-window benchmarking, long/short vs long-only vs buy-and-hold,
Challenge 3 drawdowns, and flat transaction-cost sensitivity.

## Gate criteria (all must hold)

1. **Notebooks 01–09** all green after Kernel → Restart & Run All (no Week-1 or Day-08
   regressions; zero network reliance).
2. **Symmetric 3-way comparison artifact** (`data/processed/day09_milestone3_comparison.csv`)
   regenerable from Day 09 Section F, covering `buy_and_hold`, `long_short`, and
   `long_only` on the **exact same** post-warm-up tradable dates (`n_days` identical).
3. **Challenge 3 two-panel chart** rendered to Day-03/07 standards: net `$1` wealth
   curves (top) + underwater drawdown `%` curves (bottom) with `$1.00` high-water-mark
   anchoring.
4. **1-page Milestone 3 verdict** completed in Day 09 Section F containing:
   - **Mandate-specific recommendation** (*"better, for whom?"* — contrasting a
     drawdown-constrained investor vs a terminal-wealth maximiser using return,
     annualised vol, max drawdown, trade count, and time in market).
   - **Cost sensitivity & breakeven analysis** from `cost_breakeven_scan`, contrasting
     the full ~10-year sample against the `2018–2023` bear-heavy sub-window.
   - **At least 5 explicit limitations**, covering: single synthetic series, `50/100`
     parameter-selection / cherry-picking risk, flat per-turnover log-space cost
     approximation (no spread widening or market impact), zero cash yield when flat
     (`position == 0`), and close-to-close execution assumptions.

## Review prompts (used when you report back)

- Using `L_in` and `L_out`, explain in two sentences why Long/Short trailed Long-Only
  on `df_long` even before transaction costs.
- Why does flipping `+1 → -1` pay `2 × cost_rate` while stepping `+1 → 0` pays
  `1 × cost_rate`?
- Show why reporting only the `2018–2023` sub-window would invert the headline
  conclusion vs Buy & Hold — and state the rule that prevents that mistake in Day 13.
