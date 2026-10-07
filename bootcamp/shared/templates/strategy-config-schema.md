# Strategy config schema (contract 2)

Every strategy is one JSON file in `config/<strategy_id>.json`. The engine reads it,
`spec_fingerprint` hashes it (with the signal code), and every result records that hash.
A strategy without a config is a notebook cell, not an experiment.

## Required fields

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | must equal the folder name under `strategies/` |
| `name` | string | human label for tearsheets |
| `universe` | list[string] | symbols the signal may use; all must exist in `data/` |
| `params` | object | every knob the signal reads, with the values you chose |

## Optional fields (defaults in brackets)

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `thesis` | string | `""` | one sentence from `templates/thesis.md` |
| `tags` | list[string] | `[]` | family labels: trend, reversion, carry, pairs, vol |
| `long_only` | bool | `true` | engine rejects shorts when true |
| `signal_file` | string | `"signal.py"` | relative to `strategies/<id>/` |
| `max_gross_exposure` | float | `1.0` | engine rejects weight sums above this |
| `rebalance` | string | `"daily"` | `daily`, `weekly`, `monthly` |

## Full example

```json
{
  "id": "S04_donchian",
  "name": "Donchian 20/10 breakout on ETFs",
  "universe": ["SPY", "QQQ", "IWM", "GLD"],
  "params": {"entry": 20, "exit": 10, "atr_stop": 2.0},
  "thesis": "Breakouts persist because positioning is slow; 20-day highs attract flows that take days to complete.",
  "tags": ["trend", "tier2"],
  "long_only": true,
  "signal_file": "signal.py",
  "max_gross_exposure": 1.0,
  "rebalance": "daily"
}
```

## Rules that keep experiments honest

1. **One spec per experiment.** Do not edit a spec and re-run it under the same name:
   copy it to a new id (`S04_donchian__atr3`) so the old result stays reproducible.
2. **Parameters live here, not in the signal file.** The fingerprint must change when
   a parameter changes; otherwise your saved results lie about what produced them.
3. **The universe is a promise.** If the signal reads a symbol that is not in
   `universe`, the engine refuses to run - that is how accidental look-ahead across
   markets gets caught early.
4. **Validate before you run:**
   ```bash
   python tools/validate_spec.py config/S04_donchian.json
   ```
   The validator checks the schema, that the folder and signal exist, that data is
   cached, and that `max_gross_exposure` and `long_only` are consistent with what the
   signal actually emits.
