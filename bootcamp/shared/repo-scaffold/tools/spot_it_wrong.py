#!/usr/bin/env python3
"""tools/spot_it_wrong.py - the concept self-check. Every concept ends here.

A concept is only "learned" when you can code it, explain it in two sentences,
AND spot it wrong in someone else's code. This quiz is the third part.

    python tools/spot_it_wrong.py             # 5 random snippets, interactive
    python tools/spot_it_wrong.py --tier 1    # only tier-1 bugs
    python tools/spot_it_wrong.py --id LK2    # one specific snippet
    python tools/spot_it_wrong.py --show-all  # study mode: bug + explanation

No scoring theatre: it tells you which concept to go re-read, then you re-take it.
"""

from __future__ import annotations

import argparse
import random
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"


@dataclass
class Snippet:
    id: str
    title: str
    tier: int
    concept: str
    code: str
    options: List[str]
    correct: int
    explanation: str


SNIPPETS: List[Snippet] = [
    Snippet(
        "LK1", "Trading today's close with today's signal", 1, "C01 look-ahead",
        """
def backtest(prices, params):
    signal = (prices["close"] > prices["close"].rolling(20).mean()).astype(float)
    returns = prices["close"].pct_change()
    strategy = signal * returns          # <- line under suspicion
    return (1 + strategy).cumprod()
""",
        [
            "The rolling window uses close prices",
            "signal[t] is multiplied by returns[t]: the position is decided with the same bar's close it trades on",
            "pct_change() should be log returns",
            "cumprod hides the compounding",
        ],
        1,
        "signal[t] uses close[t], so trading at returns[t] means acting on information you only have at the close. Fix: shift the signal by one bar (signal.shift(1)) or trade at the next open. This is the single most common bug in viral strategy code.",
    ),
    Snippet(
        "LK2", "Normalising with the full sample", 1, "C15 overfitting",
        """
x = price - price.mean()
z = x / price.std()
positions = (z < -2).astype(float) * 1.0
equity = (positions.shift(1) * price.pct_change()).cumsum()
""",
        [
            "The position size should be scaled by volatility",
            "shift(1) is missing again",
            "mean() and std() are computed over the whole series, including the future",
            "astype(float) changes the dtype",
        ],
        2,
        "Using the full-sample mean and standard deviation leaks the future into every bar, including the beginning. In 2020 your strategy 'knows' the 2024 average. Fix: expanding()/rolling() statistics, or fit on a training window only.",
    ),
    Snippet(
        "WR1", "The 90% win rate", 1, "C03 win rate vs edge",
        """
trades = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -18]
win_rate = sum(t > 0 for t in trades) / len(trades)     # 94.7%
print("94.7% win rate - profitable!")
""",
        [
            "The list is too short to matter",
            "Win rate says nothing about expectancy: 18 wins of +1 do not pay for one loss of -18",
            "Negative trades should be excluded as outliers",
            "1 is not a return, it is a currency amount",
        ],
        1,
        "Expectancy = win_rate*avg_win - loss_rate*avg_loss. Here it is 0.947*1 - 0.053*18 = -0.006. A high win rate with negative expectancy is the most common shape of a losing strategy sold as a winning one. Always compute breakeven_win_rate().",
    ),
    Snippet(
        "SS1", "Eleven trades is not a finding", 1, "C04 sample size",
        """
trades = [12, -4, 8, 15, -6, 9, 11, -3, 14, 7, 10]
print("avg per trade:", sum(trades) / len(trades))
print("t-stat:", (sum(trades) / len(trades)) / (std(trades) / len(trades) ** 0.5))
""",
        [
            "The t-stat formula uses the wrong denominator",
            "Nothing is wrong - the code is right, the sample is 11 trades",
            "std() needs ddof=1",
            "The mean should be geometric",
        ],
        1,
        "The math is fine; the evidence is not. Eleven trades in a fat-tailed distribution produce a t-stat you cannot trust either way. Ask: how many independent bets? A 3-year daily backtest of a 20-day holding strategy has ~36 independent bets, not 750 bars.",
    ),
    Snippet(
        "AN1", "Sharpe on daily returns, multiplied by the wrong thing", 2, "C07 Sharpe ratio",
        """
daily = equity.pct_change().dropna()
sharpe = daily.mean() / daily.std() * 12
""",
        [
            "Should be sqrt(252), not 12",
            "mean()/std() ignores the risk-free rate, which is fine",
            "pct_change() drops NaN rows",
            "Nothing - 12 is the right annualisation for daily data",
        ],
        0,
        "The Sharpe ratio annualises by sqrt(periods per year): 252 for daily, 52 for weekly, 12 for monthly. Using 12 understates it by a factor of 4.6. Teaching point: annualisation always scales a mean linearly and a deviation by the square root.",
    ),
    Snippet(
        "DD1", "Max drawdown of a return series", 2, "C08 max drawdown",
        """
returns = equity.pct_change().dropna()
max_dd = returns.min()
print("max drawdown:", max_dd)
""",
        [
            "Should be returns.cumsum().min()",
            "The worst single-bar return is not the drawdown: you need the peak-to-trough decline of the equity curve",
            "pct_change() should be on the log scale",
            "min() should be abs().min()",
        ],
        1,
        "A -8% day inside a -45% drawdown understates reality by an order of magnitude. Drawdown is measured on cumulative equity: equity/equity.cummax() - 1, then take the minimum (and remember it is negative by convention).",
    ),
    Snippet(
        "CP1", "Adding returns", 1, "C01 compounding",
        """
total = returns.sum()          # "total return"
ann = returns.mean() * 252     # "annual return"
""",
        [
            "should be returns.prod() - 1 for total, and the annual version is geometric",
            "nothing wrong, both are standard",
            "should multiply by 252 * 100",
            "returns should be log returns for this to work",
        ],
        1,
        "Summing returns assumes you rebalance to a fixed capital base every bar - the opposite of compounding. Total: (1+r).prod()-1. Annual: the geometric rate that gets you from start to end. Arithmetic mean * 252 is a legitimate number but it is not what the student earned.",
    ),
    Snippet(
        "CO1", "Costs as an afterthought", 2, "C10 transaction costs",
        """
net = strategy_returns - 0.0005
""",
        [
            "A fixed 5 bps per bar ignores how often the position actually changes",
            "5 bps is too high for liquid equities",
            "This double-counts slippage",
            "Nothing - a constant drag is standard practice",
        ],
        0,
        "Costs scale with turnover, not with time. A strategy that trades 3 times a year pays it 3 times; a strategy that rebalances daily pays it ~252 times. That is why the same 'edge' survives in one asset class and dies in another. Charge |Δweight| * cost.",
    ),
    Snippet(
        "OP1", "The 300-parameter sweep", 3, "C13 parameter sensitivity",
        """
best = None
for fast in range(2, 30):
    for slow in range(fast + 1, 60):
        s = sharpe(run(fast, slow))
        if best is None or s > best[0]:
            best = (s, fast, slow)
print("optimal:", best)
""",
        [
            "range() should include 60",
            "Nothing - this is how you find good parameters",
            "Choosing the best of ~1,600 backtests in-sample and reporting its Sharpe is selection bias, not an edge",
            "sharpe() should be computed on net returns first",
        ],
        2,
        "You found the luckiest of 1,600 draws in one dataset. The honest move: hold out a period, sweep only inside the training window, report the out-of-sample number, and check whether the neighbours of (fast, slow) are also positive. If the edge is a single spike, the edge is your search.",
    ),
    Snippet(
        "WF1", "Walk-forward that looks forward", 3, "C15 walk-forward",
        """
for train, test in splits(prices):
    params = optimise(model, prices.loc[:test.index[-1]])
    results.append(evaluate(model, params, test))
""",
        [
            "optimise() sees the test window: the model is fitted on data that includes the period it is evaluated on",
            "splits() should be expanding",
            "results should be a DataFrame",
            "Nothing wrong, this is standard walk-forward",
        ],
        0,
        "The training window must end before the test window starts. `prices.loc[:test.index[-1]]` includes every test bar. The fix is `prices.loc[:train.index[-1]]`. Walk-forward is only honest if the boundary is the previous test period's end.",
    ),
    Snippet(
        "SV1", "Trading a universe that only exists in the past", 3, "C04 base rates / survivorship",
        """
symbols = ["NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA"]
# backtest 2012-2024 on these seven names
""",
        [
            "The list is too short for cross-sectional work",
            "These are today's winners: in 2012 you did not know to exclude Lehman, Enron, Nokia, Yahoo, BlackBerry, Sears",
            "Should include indices as well",
            "Nothing - large caps always win",
        ],
        1,
        "Survivorship bias: you selected the universe with 2024 knowledge. The result tells you what happened to the winners, not what the rule would have made. Fix: a point-in-time universe, or an index membership snapshot (S&P 500 constituents as of each January).",
    ),
    Snippet(
        "BF1", "Backfilling fundamentals", 2, "C10/C01 data alignment",
        """
df["eps"] = df["eps"].bfill()
signal = (df["price"] / df["eps"] > 15).astype(float)
""",
        [
            "bfill() pulls future values backwards into the past",
            "should use ffill() for all missing data",
            "the ratio should use log prices",
            "the comparison should be < 15",
        ],
        0,
        "`bfill` is time travel: it fills Monday's missing value with Tuesday's number. In price data it is usually harmless-ish; in fundamentals it is fatal. Rule: missing data is filled with what was known at the time (ffill), never with what came later.",
    ),
    Snippet(
        "SAME1", "Filling at the close you decided on", 2, "C23 slippage & latency",
        """
signal = compute(prices.loc[t])            # needs close[t]
fill_price = prices.loc[t, "close"]        # same bar
pnl = signal * (prices.loc[t + 1, "close"] / fill_price - 1)
""",
        [
            "The fill uses close[t] even though the decision also used close[t]: that fill was not available",
            "pnl should use open prices",
            "signal should be lagged by two bars",
            "Nothing - decisions at the close can be executed at the close",
        ],
        0,
        "In reality the close is printed before you can act on it (or simultaneously, with worse information). Every realistic backtest fills at the next bar's open or close. The gap between 'fill at decision-bar close' and 'fill at next open' is exactly the slippage you will meet live in Weeks 11-12.",
    ),
    Snippet(
        "RF1", "Risk-free rate applied per bar", 2, "C07 Sharpe ratio",
        """
sharpe = (daily.mean() - 0.05) / daily.std() * np.sqrt(252)
""",
        [
            "0.05 is an annual rate and must be divided by 252 (or 252*something) before subtracting from a daily mean",
            "np.sqrt(252) should be 252",
            "daily.std() needs ddof=1",
            "Nothing - 5% is the standard risk-free assumption",
        ],
        0,
        "Subtracting an annual 5% from a daily mean makes the numerator 5% too small, badly distorting Sharpe at daily frequency. Convert: rf_per_bar = rf_annual / periods_per_year. The same trap appears with quarterly and monthly data.",
    ),
    Snippet(
        "MC1", "Correlation-blind diversification", 4, "C20 portfolio variance",
        """
combined = (leg_a + leg_b + leg_c) / 3
sharpe_combined = sharpe(combined)
assert sharpe_combined > max(sharpe(a), sharpe(b), sharpe(c))
""",
        [
            "The average of three strategies is not the optimal combination, and its Sharpe is bounded by the correlation between them",
            "Should divide by sqrt(3)",
            "Should use geometric averages",
            "Nothing wrong if the legs are uncorrelated",
        ],
        0,
        "If all three legs are the same trade in different clothing (correlation 0.9), the 'diversified' portfolio has the same Sharpe as one leg with more leverage. Sharpe of a blend depends on correlation: with ρ=1 the blend's Sharpe equals the legs'; with ρ=0 it improves by up to sqrt(N). Measure the correlation matrix before you claim diversification.",
    ),
    Snippet(
        "KL1", "Full Kelly on a fat-tailed strategy", 4, "C21 Kelly",
        """
edge, variance = estimate_edge_and_risk()
f = edge / variance           # Kelly fraction
position = f * capital        # go all in on the estimate
""",
        [
            "edge and variance are estimated with error; full Kelly on estimated inputs overbets and has brutal drawdowns",
            "variance should be standard deviation",
            "capital should be equity",
            "Nothing - Kelly is the growth-optimal fraction",
        ],
        0,
        "Kelly assumes you know the true edge and variance. You do not: estimation error means full Kelly on your estimate is systematically too large. Practitioners size at 1/4 to 1/2 Kelly, target volatility instead of fractions, and cap gross exposure. Expectation: you give up a little growth to survive your own estimation error.",
    ),
    Snippet(
        "LIVE1", "Live vs backtest, unexplained", 5, "C24 divergence",
        """
expected = backtest_sharpe * np.sqrt(30 / 252)
actual_30d_return = live_equity[-1] / live_equity[0] - 1
print("live is worse than expected" if actual_30d_return < expected else "on track")
""",
        [
            "Comparing a 30-day realised return to an annualised Sharpe expectation ignores the sampling noise: a month is ~20 independent bets",
            "The sqrt(30/252) scaling is wrong by a factor of 2",
            "live_equity should be log-scaled",
            "Nothing - keep the comparison simple",
        ],
        0,
        "One month of daily data cannot confirm or refute a Sharpe. Do the arithmetic on the dispersion: with Sharpe 1.0 annual and vol 15%, the 1-month return has a standard deviation of ~4.3%, so -8% or +8% months are both 'expected'. What you CAN check: turnover, slippage per trade, hit rate of submitted vs filled orders, and whether signals matched the backtest's state_at() positions.",
    ),
    Snippet(
        "REG1", "One regime, one verdict", 5, "C25 regime detection",
        """
# 2010-2021: trend following made money      -> "trend following works"
# the test period had falling rates + QE
""",
        [
            "The conclusion generalises from one macro regime (disinflation, QE, low vol) to all regimes",
            "Trend following never works",
            "The sample is too long",
            "Nothing - 11 years is a robust sample",
        ],
        0,
        "Eleven years can be one regime. A strategy's edge is conditional: it exists because of something structural that may stop (vol regime, participation, macro policy). Report results BY regime (e.g. vol terciles, rate-hike periods), not just in total - and expect the next regime to look different.",
    ),
    Snippet(
        "POS1", "The same idea twice", 3, "C20 correlation",
        """
s1 = backtest(momentum, ["AAPL", "MSFT", "NVDA"])
s2 = backtest(momentum, ["GOOGL", "META", "AMZN"])
port = 0.5 * s1 + 0.5 * s2
print("two strategies -> diversification")
""",
        [
            "Both legs are the same signal family on overlapping universes: this is one bet with double the leverage",
            "50/50 is never optimal",
            "Should use inverse-vol weights",
            "Nothing - different tickers means uncorrelated",
        ],
        0,
        "Correlation comes from the mechanism, not the ticker list. Two cross-sectional momentum books in US tech share a factor. Real diversification in this course comes from mechanisms with different failure modes: trend (crashes in chop) + mean reversion (crashes in trends) + carry/vol.",
    ),
]

BY_ID: Dict[str, Snippet] = {s.id: s for s in SNIPPETS}


def ask(snippet: Snippet) -> bool:
    print()
    print("=" * 74)
    print("%s  [%s]  tier %d" % (snippet.title, snippet.id, snippet.tier))
    print("=" * 74)
    print(snippet.code.rstrip())
    print()
    for i, option in enumerate(snippet.options, start=1):
        print("  %d) %s" % (i, option))
    try:
        raw = input("\nYour answer (number, or 'q' to quit): ").strip()
    except EOFError:
        raw = "q"
    if raw.lower() in {"q", "quit"}:
        return False
    correct = str(snippet.correct + 1)
    if raw == correct:
        print("%sCORRECT%s - %s" % (GREEN, RESET, snippet.explanation))
        return True
    print("%sWRONG%s - the answer is %s) %s" % (RED, RESET, correct, snippet.options[snippet.correct]))
    print("%sconcept: %s%s" % (YELLOW, snippet.concept, RESET))
    print(snippet.explanation)
    return True


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tier", type=int, default=None)
    parser.add_argument("--id", default=None)
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--show-all", action="store_true", help="study mode: print every snippet with its answer")
    args = parser.parse_args(argv)

    if args.list:
        for snippet in SNIPPETS:
            print("%-6s tier %d  %s  (%s)" % (snippet.id, snippet.tier, snippet.title, snippet.concept))
        return 0

    if args.show_all:
        for snippet in SNIPPETS:
            print("=" * 74)
            print("%s [%s] tier %d" % (snippet.title, snippet.id, snippet.tier))
            print(snippet.code.rstrip())
            print("\nanswer: %d) %s" % (snippet.correct + 1, snippet.options[snippet.correct]))
            print("concept: %s" % snippet.concept)
            print(snippet.explanation)
            print()
        return 0

    pool = list(SNIPPETS)
    if args.id:
        if args.id not in BY_ID:
            print("unknown id %s (see --list)" % args.id, file=sys.stderr)
            return 2
        pool = [BY_ID[args.id]]
    elif args.tier is not None:
        pool = [s for s in pool if s.tier <= args.tier]
    else:
        random.Random(args.seed).shuffle(pool)
        pool = pool[: args.count]

    asked = 0
    for snippet in pool:
        if not ask(snippet):
            break
        asked += 1
    print()
    print("Reviewed %d snippet(s). Anything you got wrong is a concept to re-read - and to describe in two sentences in your journal." % asked)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
