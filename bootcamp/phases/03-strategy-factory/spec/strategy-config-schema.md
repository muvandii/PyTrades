# Strategy spec format (the `config/<id>.json` file)

Every strategy in this course is described by one JSON file. The file is the contract: the engine
reads it, the fingerprint hashes it, and the verdict quotes it. If it is not in the spec, it did
not happen.

## The canonical schema

```json
{
  "id": "S05_momentum",
  "name": "Cross-sectional momentum 12-1, top 3 of ETF set",
  "universe": ["SPY", "QQQ", "IWM", "TLT", "IEF", "GLD", "EEM", "EFA", "DBC", "UUP"],
  "params": {"lookback": 252, "skip": 21, "top_n": 3},
  "thesis": "Assets that outperformed over the past year keep outperforming for the next month, because information and flows diffuse slowly.",
  "tags": ["momentum", "cross-sectional", "tier3"],
  "long_only": true,
  "max_gross_exposure": 1.0,
  "rebalance": "monthly"
}
```

The machine-readable copy lives at `shared/templates/strategy-config.schema.json`.

| Field | Type | Rules |
| --- | --- | --- |
| `id` | string | matches the filename and the directory `strategies/<id>/` |
| `name` | string | human label; it appears in tearsheets |
| `universe` | list[string] | symbols present in `data/`; the engine fails loudly on a missing symbol |
| `params` | object | everything the signal function reads; numbers only (no paths, no code) |
| `thesis` | string | one sentence: the claim and the mechanism. Required - the engine will not run a spec without it |
| `tags` | list[string] | family and tier tags, used by the registry |
| `long_only` | bool | true forbids negative weights, enforced as an error |
| `max_gross_exposure` | number | target weights are *scaled* to respect this, never truncated |
| `rebalance` | string | `daily`, `weekly`, or `monthly` - sets the target-update grid |

## Why the spec exists (and what a spec is not)

1. **Reproducibility.** The fingerprint (`StrategySpec.fingerprint()` hashes the spec *and* the
   signal file's contents) is stamped into every result's `meta.json`. A number without a
   fingerprint is a rumour.
2. **Comparability.** Two runs with different specs are different objects. Changing a parameter
   and overwriting the old result is how students quietly delete their own evidence. Change the
   spec, run under a new `NAME`, and keep both.
3. **A spec is not a conclusion.** It states what you believed when you started. The verdict
   states what you learned. Keeping the original thesis text - unedited - is what makes the
   "I was wrong about the mechanism" sentence in a verdict meaningful.

## The one rule that cannot be automated

`thesis` must contain a mechanism, not a hope. Compare:

- Hope: "momentum works because prices trend." (a restatement of the claim)
- Mechanism: "assets that outperformed keep outperforming because flows chase performance and
  information diffuses slowly, so the marginal buyer arrives after the price move."
- Hope: "oversold bounces are real." (an adjective with a direction)
- Mechanism: "index-ETF selling is partly mechanical (redemptions, rebalancing, stop cascades),
  so price temporarily deviates from the level information alone would imply."

Both fields are one sentence long. Only one of each pair can be falsified by an experiment, and
that is the test: **if no result could contradict your thesis sentence, it is not a thesis.**

## Multi-symbol specs

- Weights sum to ≤ `max_gross_exposure` at every bar (the engine asserts this).
- `rebalance: monthly` means the *target* updates monthly while the engine still marks positions
  daily; that is the standard convention here.
- The universe must be homogeneous in frequency. Mixing a daily ETF with a monthly series is an
  error, not an adventure.

## Worked example

`phases/03-strategy-factory/worked-example/config.json` is a complete, runnable spec (a tight
Bollinger variant on the lab series) with its tearsheet, verdict and graveyard entry. Copy its
structure; never copy its parameters.
