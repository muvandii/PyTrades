# Module: data-fetcher

**Canonical code:** `../repo-scaffold/kit/data_fetcher.py` (ships inside your repo as `kit/data_fetcher.py`)
**Used in:** Weeks 1-2 (D01), and every later week that adds a symbol
**Student artifact:** a validated `data/` directory + `reports/data-validation.md`

## What it does

Real bars from keyless sources, cached with provenance, validated structurally:

```bash
make data SYMBOLS="SPY QQQ IWM TLT GLD EEM EFA DBC UUP IEF" START=2005-01-01
make validate
```

```python
from kit import data_fetcher as df
bars = df.load("SPY")                       # cached, identical bytes every run
report = df.validate(bars, "SPY")           # issues (fatal) vs warnings (not)
df.assert_clean(bars, "SPY")                # raises instead of letting garbage through
frames = df.fetch_many(df.universe("etf_core"), "2005-01-01")
df.aligned_frame(frames, "close")           # wide close frame with a coverage floor
```

## What it deliberately does NOT do

- Adjust for dividends/splits silently. It records what the provider returned, and
  validation flags >35% daily moves so you notice.
- Fill gaps for you. Gaps are information.
- Serve synthetic data quietly: `synthetic()` exists for offline smoke tests, is
  labelled in `meta.json`, and `assert_clean()` refuses to let it near a verdict.

## The validation table you must produce (D01)

`reports/data-validation.md` contains one row per symbol and one paragraph of
interpretation. A row that says "ok" with no evidence is not a row.

| symbol | rows | first | last | issues | warnings | source | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SPY | 5289 | 2005-01-03 | 2024-12-31 | 0 | 1 | stooq | ok |

Then answer, in writing: which warnings do you accept, which do you reject, and what
would change your mind? (Typical answer: "1 zero-volume bar in 2011; accepted, it is a
holiday half-session; rejected the symbol with 12 repeated closes - that feed was stale.")

## Offline / no-network fallback

`sample-data/` (see its README) contains simulated series with **known planted
properties**. You may use them to smoke-test code, and you may cite them as
"laboratory" evidence while your data download is blocked - but any graded verdict
needs real bars, and that is not negotiable.
