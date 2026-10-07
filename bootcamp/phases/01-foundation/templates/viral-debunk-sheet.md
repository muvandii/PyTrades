# Viral debunk sheet (the 30-minute intake checklist)

> One page, printable. This is the paper version of milestone M1: fill it for every claim
> before touching code, and the timed run becomes boring - which is the goal.

## 1. The claim (2 min)

- Source (URL, date):
- Claim, verbatim:
- Instrument / universe:
- Period:
- Headline numbers asserted: return __ · win rate __ · drawdown __
- What is actually being claimed? (circle) **rule** / **result** / **feeling**
- My translation into a codable rule (if "feeling"):
- My prior before testing: debunked / survives / inconclusive, because:

## 2. Reconstruct (8 min - or beforehand)

- Entry condition:
- Exit condition:
- Position sizing:
- Rebalance frequency:
- What the claim omits that I had to invent: (these omissions are where the illusion usually lives)

## 3. Data (3 min)

- Symbols used, period, and the sha256 from `data/*.meta.json`:
- Validation verdict per symbol: ok / issues (list them)

## 4. Reproduce the claim's own numbers (8 min)

| metric | claimed | reproduced | note |
| --- | --- | --- | --- |
| total return | | | |
| win rate | | | |
| max drawdown | | | |
| trades | | | |

## 5. Break it (8 min)

| check | action | measured effect | verdict |
| --- | --- | --- | --- |
| Execution | add `shift(1)` / next-open fills | ΔSharpe = __, Δreturn = __ | |
| Costs | apply fee+slippage, find breakeven | breakeven = __ bps | |
| Sample | count independent bets, CI on win rate | bets = __, CI = [__, __] | |

## 6. Verdict (1 min)

**debunked / survives (partially) / inconclusive** — decided by: (one mechanism)

Graveyard line: `<name> — <date> — <cause> — <path to this file>`

## Timer

start __:__ · finish __:__ · total __ min · where the time went:
