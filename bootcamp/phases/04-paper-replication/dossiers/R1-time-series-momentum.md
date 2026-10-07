# Dossier R1 — Time-Series Momentum

**Paper:** Moskowitz, T., Ooi, Y.H., Pedersen, L.H. (2012). *Time Series Momentum*. Journal of
Financial Economics 104(2), 228-250.

**Why this paper:** it is the cleanest bridge from "a rule on a chart" to "a mechanism with a
diversification argument", and its central claim is testable on a retail data set in a week. It
also fails in an instructive way when you cannot access futures.

## The core claim

> Past 12-month excess return predicts the next 1-month return, for nearly every futures market,
> and volatility scaling makes the effect stable across regimes.

## The specification, as precisely as the paper gives it

| Element | Paper | Your version (ETF translation) |
| --- | --- | --- |
| Universe | 58 liquid futures (equities, bonds, currencies, commodities) | 8-12 liquid ETFs spanning the same asset classes |
| Signal | sign of the past 12-month excess return (`sign(P_t / P_{t-12} − 1)`) | identical on total-return ETF series |
| Position | volatility-scaled to a 40% annual target: `40% / σ_t`, where σ_t is an exponential estimate of recent return vol | start without the scaler, then add it (C17) |
| Rebalance | monthly, at month-end | monthly, at month-end |
| Costs | the paper's main results are gross; it discusses cost sensitivity | **net, always** - this is where the course diverges on purpose |
| Sample | 1965-2009 | whatever your data provides; report it |
| Reported numbers | positive 12-month predictability in every market; a diversified TSMOM portfolio with Sharpe ≈ 1 gross | your Sharpe will be lower, and the gap is the lesson |

## The mechanism (write this in your own words before implementing)

1. **Under-reaction then over-reaction.** Trend persistence is consistent with slow information
   diffusion and with flow-driven price impact (index funds, CTAs, retail chasing).
2. **Volatility clusters.** σ_t is predictable (GARCH effects) while the sign of the trend is
   persistent, so scaling *up* in calm markets and *down* in turbulent ones improves the
   risk-adjusted result rather than the raw return.
3. **Diversification across markets, not time.** TSMOM's impressive portfolio Sharpe comes from
   averaging many weakly correlated trends. If you run it on one instrument - or ten correlated
   equity ETFs - you should expect the individual-market numbers and not the portfolio number.

## Where it is vulnerable (your Thursday list)

| Attack | What to measure |
| --- | --- |
| Costs | sign flips plus the vol rescale's own turnover; annual drag in bps |
| Period dependence | 2008-2014 vs everything else; run both halves |
| Universe dependence | equities-only subset; does the mechanism still show? |
| Data frequency | monthly vs daily rebalance; monthly is cheaper and closer to the paper |
| Excess return definition | cash rate matters for futures (collateral); for ETFs use total return |
| Crowding | the effect after 2010, when TSMOM became a known product category |

## What a replication owes the reader

1. Your numbers next to the paper's, for Sharpe, vol, max drawdown, turnover, and sample period.
2. A named deviation for every gap, with the direction and approximate size of its effect.
3. A verdict sentence: replicated / partially replicated / did not replicate - and on which
   dimension (sign, magnitude, mechanism).

## Common failure modes in student replications

- Reporting the *gross* number because it matches the paper. The paper's number is not the target;
  the mechanism is.
- Using one asset and concluding TSMOM is dead, when the paper's result is a *portfolio* result.
- Applying vol scaling with a leverage cap of 1.0 and then reporting the paper's Sharpe - the cap
  changes the object you are testing, so say so.
- Skipping the monthly-vs-daily check, then wondering why costs ate a documented effect.
