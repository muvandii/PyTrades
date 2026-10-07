# Debunk: <name of claim + source>

> One file per viral claim. Target: 30 minutes start to finish (that speed IS the
> deliverable - milestone M1 is timed). Record the elapsed time honestly.

**Claim source:** <URL / video / tweet / newsletter - keep the link, it is the receipt>
**Claim (verbatim):** "..." (quote it)
**Claimed results:** <return, win rate, timeframe, instrument>
**Elapsed time:** __ minutes (start: __:__ → finish: __:__)

## Step 1 - Reconstruct (10 min)

What exactly is the rule? Signal, entry, exit, size, universe, period. Write it as if
you were going to code it, then code the smallest version.

```
<pseudo-code or the actual 10-line implementation>
```

## Step 2 - Data (5 min)

| Item | Value |
| --- | --- |
| Symbol(s) | |
| Period | |
| Source + hash | `data/<SYM>.csv` sha256 from `meta.json` |
| Validation | ok / issues |

## Step 3 - Measure (10 min)

Recompute the claim's own headline numbers first. Does the claim reproduce on its own terms?

| Metric | Claimed | Reproduced | Notes |
| --- | --- | --- | --- |
| Total return | | | |
| Win rate | | | |
| Max drawdown | | | |
| Trades | | | |
| Time in market | | | |

## Step 4 - Break it (5 min)

Check the three killers in order. Stop when one of them kills it.

1. **Execution:** does the signal use the same bar it trades? Is `shift(1)` present?
2. **Costs:** turnover × (fee+slippage)? At what bps does the edge die?
3. **Sample:** how many independent bets? win-rate confidence interval? one regime or several?

## Verdict

**`debunked` / `survives (partially)` / `inconclusive`** + the ONE mechanism that decided it.

## Graveyard line

`<name> — <date> — <cause> — reports/debunks/<file>.md`
