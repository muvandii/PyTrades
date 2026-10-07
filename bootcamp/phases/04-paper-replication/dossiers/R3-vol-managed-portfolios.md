# Dossier R3 — Vol-Managed Portfolios

**Paper:** Moreira, A., Muir, T. (2017). *Volatility-Managed Portfolios*. Journal of Finance 72(4),
1611-1644. **Critique:** Harvey, C.R., Hoyle, E., Korgaonkar, R., Rattray, S., Van Hemert, O.
(2018). *The Impact of Volatility Targeting* (and related replication work).

**Why this paper:** it is the clearest case of a result that is *statistically* real and
*economically* contested - which is exactly the judgement this phase is training. It also
completes the toolkit: TSMOM uses vol scaling as a position sizer, this paper makes vol scaling
the object of study.

## The core claim

> Scaling exposure inversely to recent realised volatility raises risk-adjusted returns, because
> vol clusters and returns do not scale with it.

## The specification, as precisely as the paper gives it

| Element | Paper | Your version |
| --- | --- | --- |
| Base portfolio | the market (and a range of factor portfolios) | your multi-asset portfolio, equal-weight then vol-managed |
| Scaling rule | `w_t = c / σ²_t` (inverse-variance) in the paper's baseline; simpler practitioners use inverse-vol | run inverse-vol first, then try inverse-variance if you want the exact object |
| σ estimator | realised volatility from daily returns over the past month (variance computed at the end of the previous month) | three estimators: 20-day simple, 60-day EWMA, 20-day squared-return |
| Constraint | leverage possible, no explicit cap in the baseline | cap your scaling factor; report the cap and how often it binds |
| Sample | 1926-2015 (US market and factors) | your sample and universe, stated |
| Reported effect | Sharpe improvements of roughly +0.1 to +0.3 for the market factor, larger for some factors | the improvement direction is the claim; the size is what you test |

## The mechanism (and its critics)

**Pro:** volatility is highly predictable while the mean return is nearly unforecastable; taking
less risk when risk is high lowers the volatility of the *whole path* more than it lowers the
return, so Sharpe rises. Vol also tends to rise before bad returns (feedback effects, leverage
cycles).

**Con (the Harvey et al. line of criticism):**
1. The measured improvement is partly an artefact of the vol estimator's look-ahead: using
   contemporaneous or in-sample volatility flatters the result. Use only trailing, causal estimates.
2. Vol targeting generates turnover whenever σ changes - a strategy that "does nothing" in signal
   terms still trades constantly. Costs and financing eat the improvement.
3. The result is sensitive to the (unstated) volatility target and leverage cap; the "improvement"
   can be a rescaling artefact when comparing leveraged vs unlevered portfolios.
4. Statistical significance across different samples is weaker than the headline suggests.

## Where it is vulnerable (your Wednesday list)

| Attack | What to measure |
| --- | --- |
| Estimator look-ahead | Sharpe with trailing σ vs a (deliberately wrong) in-sample σ |
| Cost of rescaling | turnover of scaled vs unscaled; drag in bps |
| Cap and target | sweep cap ∈ {1.0, 1.5, 2.0} × target vol ∈ {8%, 10%, 12%} |
| Asset dependence | which assets improve, which worsen; the average hides both |
| Regime dependence | the improvement in 2008-2009 and 2020 vs the rest |
| Statistical strength | bootstrap CI on the Sharpe *difference*, not on each Sharpe |

## What a replication owes the reader

1. The estimator choice, in the writeup, next to the number it produced.
2. Turnover for both the scaled and unscaled versions.
3. The Sharpe difference with a CI, and a separate sentence on economic significance.
4. The cap/target grid, so a reader can see whether the result is a rescaling artefact.

## Common failure cases in student replications

- Using realised vol that includes the return being predicted (in-sample vol): this alone can
  manufacture a "result".
- Comparing a leveraged vol-managed portfolio to an unlevered base - not the same object.
- Reporting the mean improvement across assets and hiding that the improvement is concentrated in
  one or two assets.
- Ignoring financing: a portfolio that runs at 1.5× average exposure has a funding cost, which on
  a low-Sharpe base portfolio can exceed the improvement.
