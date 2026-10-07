# WRITEUP.md — public writeup template

Publish this file (repo root, or a blog post linking to the repo). One page. Every number here
must be reproducible from the repo; every claim must have an artifact behind it.

---

# What I built, what I found, and what I'm not claiming

**Author:** `<name>` · **Repo:** `<public url>` · **Period:** `<start>` → `<end>`

## The question

> `<One sentence. Not "I learned quantitative finance." What did your thirteen weeks actually test? e.g. "Which simple signal families survive realistic costs and out-of-sample testing on liquid ETFs, and how much of my live paper divergence was structural?">`

## The method (five lines)

1. **Engine:** `<your backtester>`, event-driven, costs charged on turnover inside the loop.
2. **Costs:** `<fees + slippage per side>`; breakeven bps published for every strategy.
3. **Out-of-sample:** pooled walk-forward (3y train / 6mo test / 1 bar embargo), reported OOS/IS ratio.
4. **Tests:** contract suite + time-travel + shift-premium, `make test` green.
5. **Live:** `<paper adapter or Alpaca>`, `<N>` days, reconciliation in `live/reconciliation.md`.

## The three artifacts I would show you first

| Artifact | Why this one |
| --- | --- |
| [`<path to best tearsheet>`](<link>) | `<the number and what it proves>` |
| [`live/reconciliation.md`](<link>) | `<what surprised me>` |
| [`graveyard.md`](<link>) | `<the ranked taxonomy>` |

## The three deaths that taught me the most

1. **`<strategy>`** — died of `<cause>`; killer number `<breakeven bps / OOS Sharpe / turnover>`; I now `<habit changed>`.
2. **`<strategy>`** — died of `<cause>`; ...
3. **`<rule or variant>`** — died of `<cause>`; ...

## What I am not claiming

> `<The largest caveat, stated by you first. e.g. "My out-of-sample window is one regime; my universe is ten correlated ETFs; my live window is 30 days and its realised vol was 0.8× my backtest's median. None of these results should be read as evidence about futures, options, or capacity.">`

## The numbers (headline table)

| Metric | Value | Artifact |
| --- | --- | --- |
| Strategies tested / killed | `<n>` / `<n>` | `strategies/index.md`, `graveyard.md` |
| Survivors with OOS CI excluding zero | `<n>` | `reports/bootstrap.md` |
| Best survivor's OOS Sharpe | `<x>` | `<tearsheet path>` |
| Live vs backtest divergence | `<bps/month>` | `live/reconciliation.md` |
| Unexplained share of divergence | `<%>` | `live/reconciliation.md` |
| Journal entries written | `<n>` | `journal/` |

## What is next (and what would make me stop)

1. **`<experiment>`** — hypothesis `<...>`; kill criterion `<observable>`.
2. **`<experiment>`** — hypothesis `<...>`; kill criterion `<observable>`.
3. **`<experiment>`** — hypothesis `<...>`; kill criterion `<observable>`.

## How to run this

```bash
git clone <public url> && cd <repo>
make data && make run && make tearsheet     # reproduces the headline number
make test                                   # contract suite, green
```

---

## Writing rules (delete this section before publishing)

1. **No number without an artifact.** If you cannot link it, it does not go in.
2. **The caveat paragraph is mandatory** and must be written by you, not softened.
3. **Write the deaths before the victories.** A writeup with no graveyard reads as advertising.
4. **One page.** The repo holds the detail; the writeup is the doorway.
5. **Verbs, not adjectives**: "turned over 38×/year and died at 16 bps" beats "quite high turnover".
