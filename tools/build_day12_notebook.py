"""Build Day 12 notebook. Instructor utility."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _day_setup import WEEK2_SETUP_CODE
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

ROOT = Path(__file__).resolve().parents[1]
CELLS = []
def md(t): CELLS.append(new_markdown_cell(t.strip("\n")))
def code(t): CELLS.append(new_code_cell(t.strip("\n")))

md(r"""
## SECTION A — Learning Mission

# Day 12 — APIs, Vendor Payloads & Data You Don't Control (`pytrades` v0.3)

| | |
|---|---|
| **Video segment** | **02:51:00–03:00:48** — *API* · *Working with API (Alpha Vantage)* ([watch](https://www.youtube.com/watch?v=GDMkkmkJigw&t=10260s)) |
| **Estimated study time** | **2.5–3 hours** |
| **Prerequisites** | Day 01 `validate_ohlcv` contract; `pytrades` v0.2 (`SMACrossoverStrategy`) green |
| **Data** | **100% offline canned vendor JSON payloads** generated in setup (no live API key is ever required or graded) |
| **Expected deliverable** | **P2.4:** `pytrades` v0.3 (`pytrades/data.py` vendor adapters) running a full SMA crossover backtest end-to-end from canned Alpha-Vantage JSON |

## Learning objectives — by the end of today you will be able to

1. **Parse** an Alpha-Vantage-style daily JSON payload (descending date keys, string numbers, `"4. close"` vendor headers) into the exact Day-01 validated OHLCV `DataFrame` contract.
2. **Distinguish and raise** explicit exceptions for three real-world API failure modes — **rate-limit / vendor notices** (`RateLimitError`), **empty time series** (`EmptyPayloadError`), and **missing/malformed schema fields** (`SchemaMismatchError`) — never mistaking HTTP 200 error notes for empty market data.
3. **Keep API secrets out of source code** via environment variables (`os.environ` / `.env`, **[programme addition]**) and eliminate silent `except: pass` error swallowing.
4. **Implement** `fetch_daily(symbol, api_key=None, _get=None)` with an injectable transport so network adapters are 100% deterministic in offline unit tests.
5. **Explain** why data-vendor choices (raw vs split/dividend-adjusted closes, survivorship-free universes) change backtest results even when strategy code is identical.
""")

md(r"""
---
## SECTION B — Video Learning · 02:51:00–03:00:48

**Pre-watch questions** (write guesses first; checked in Section H):
1. What is an **API** in one plain sentence, and why do data vendors issue per-user **API keys**?
2. The presenter pastes an Alpha Vantage key directly inside a notebook cell on screen. What happens the moment you `git push` a notebook like that to a public GitHub repository?
3. Look closely at the column names returned by Alpha Vantage (`"1. open"`, `"4. close"`, …) and the row order. Why would passing that raw table straight into `SMACrossoverStrategy` fail or compute backwards indicators?
4. When he discusses paid/institutional vendors (Polygon, Norgate) near the end of the tutorial, what data-quality problems in free feeds is he warning you about?

| Time | Chapter | Watch for |
|---|---|---|
| 02:51:00 | API | Conceptual overview: client request → vendor server → structured response, rate limits, keys |
| 02:53:30 | Working with API (Alpha Vantage) | `pip install alpha_vantage`, `TimeSeries(key=..., output_format="pandas")`, `get_daily(...)`, vendor-named columns (`1. open` .. `5. volume`), and remarks on data vendors (Polygon, Norgate) |
| 03:00:48 | 🏁 End of tutorial video | Tomorrow (Day 13) is your independent capstone — zero new video |

Fallback: [02:51:00](https://www.youtube.com/watch?v=GDMkkmkJigw&t=10260s) · [02:53:30](https://www.youtube.com/watch?v=GDMkkmkJigw&t=10410s)
""")

code(r"""
# ▶️ SECTION B (code) - 02:51:00 to 03:00:48 (final segment of the 3h tutorial)
from IPython.display import YouTubeVideo, display
display(YouTubeVideo("GDMkkmkJigw", start=10260, end=10848, width=800, height=450))
print("Fallback: https://www.youtube.com/watch?v=GDMkkmkJigw&t=10260s  (watch to 03:00:48)")
""")

md(r"""✍️ **My 3-bullet summary + 1 habit from the video I will NOT copy (edit me):** - · - · Will NOT copy: …""")

md(r"""
---
## SECTION C — Concept Notes

### C1. The Adapter Boundary: quarantine vendor quirks inside `pytrades/data.py`
Every market-data vendor invents its own dialect:
- **Alpha Vantage JSON:** nested dict `"Time Series (Daily)" -> {"2024-05-10": {"1. open": "184.2000", "4. close": "185.1000", ...}}` — **strings** instead of floats, **newest-first** dates, numbered column labels.
- **Row-list REST APIs (Polygon / Tiingo style):** `{"ticker": "XYZ", "results": [{"t": "2024-05-09", "o": 183.0, "c": 184.2, ...}]}`.

Your indicators and strategy classes must **never** know which vendor supplied the bars. An **adapter** in `pytrades/data.py` translates any external payload into Day 01's single canonical contract: ascending `DatetimeIndex` named `"Date"`, positive `float` columns `["Open", "High", "Low", "Close", ...]` and non-negative numeric `"Volume"`, verified by `validate_ohlcv`.

### C2. HTTP 200 Lies: rate-limit notes vs empty data
Free financial APIs often return HTTP status `200 OK` when throttling you, replacing `"Time Series (Daily)"` with:
`{"Note": "Thank you for using Alpha Vantage! Our standard API call frequency is 25 requests per day..."}` or `{"Information": ...}` or `{"Error Message": ...}`.
Naive code (`payload.get("Time Series (Daily)", {})`) turns a rate limit into an **empty DataFrame** and silently skips the ticker! Your parser must inspect notice keys *first* and raise `RateLimitError` (or a specific vendor error) loudly.

### C3. Secrets management **[programme addition]**
The video types an API key into a cell for convenience. **Hard rule in professional code and in this repo:** keys live in environment variables (`export ALPHAVANTAGE_API_KEY=...` or a git-ignored `.env` file — check `.gitignore` line 7!), read via `os.environ.get("ALPHAVANTAGE_API_KEY")`. Never commit keys, and never echo key values inside exception messages or logs.

### C4. Dependency injection (`_get=None`) for offline testing
How do you test `fetch_daily("DEMO")` with zero internet and zero real API key? Accept an optional callable `_get=None`. In production (`_get is None`), `fetch_daily` performs the real HTTP request; in tests, callers pass `lambda sym, key: CANNED_PAYLOAD`, testing 100% of key resolution, call wiring, parsing, and error handling deterministically in 1 millisecond.

### C5. Why vendor choice changes backtest conclusions
1. **Raw Close vs Split/Dividend-Adjusted Close:** a 4-for-1 stock split drops raw `Close` by `-75%` overnight (`ln(0.25) = -1.386` fake crash!), triggering bogus moving-average crossovers unless historical prices are split-adjusted; omitting dividends understates Buy & Hold vs a strategy sitting in cash (`Day 09`).
2. **Survivorship bias:** free APIs often serve *currently listed* tickers only; delisted bankruptcies vanish from historical universes (Norgate's selling point mentioned in the video).
""")

code(WEEK2_SETUP_CODE + r"""
import json, os
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

# Deterministic canned vendor payloads (160 bars -> supports SMA 20/50 end-to-end offline!)
def _build_canned_payloads():
    src = _one(seed=1212, start_price=150.0, mu=0.0005, sigma=0.012, n=160)
    # Reverse order (newest first) + string formatting to match Alpha Vantage's real wire shape
    ts_daily = {}
    for dt in reversed(src.index):
        row = src.loc[dt]
        ts_daily[dt.strftime("%Y-%m-%d")] = {
            "1. open": f"{row['Open']:.4f}",
            "2. high": f"{row['High']:.4f}",
            "3. low": f"{row['Low']:.4f}",
            "4. close": f"{row['Close']:.4f}",
            "5. volume": str(int(row["Volume"])),
        }
    av_ok = json.dumps({
        "Meta Data": {"1. Information": "Daily Prices (Synthetic Canned)", "2. Symbol": "SYNA"},
        "Time Series (Daily)": ts_daily,
    })
    av_rate = json.dumps({
        "Note": "Thank you for using Alpha Vantage! Our standard API call frequency is 25 requests per day."
    })
    av_info = json.dumps({
        "Information": "Please consider spreading out your free API requests."
    })
    av_empty = json.dumps({
        "Meta Data": {"2. Symbol": "EMPTY"}, "Time Series (Daily)": {}
    })
    av_missing_col = json.dumps({
        "Meta Data": {"2. Symbol": "BROKEN"},
        "Time Series (Daily)": {"2020-01-03": {"1. open": "100.0", "2. high": "101.0", "3. low": "99.0", "5. volume": "1000"}},
    })
    # Second vendor wire format: list-of-row-dicts with extra vendor columns (`vw`, `n`)
    rows_b = [
        {"t": dt.strftime("%Y-%m-%d"), "o": float(src.loc[dt, "Open"]), "h": float(src.loc[dt, "High"]),
         "l": float(src.loc[dt, "Low"]), "c": float(src.loc[dt, "Close"]), "v": int(src.loc[dt, "Volume"]),
         "vw": round(float((src.loc[dt, "High"] + src.loc[dt, "Low"]) / 2), 4), "n": 4200}
        for dt in src.index[:30]
    ]
    vendor_b = json.dumps({"ticker": "SYNB", "status": "OK", "results": rows_b})
    return av_ok, av_rate, av_info, av_empty, av_missing_col, vendor_b

(CANNED_AV_SUCCESS_JSON, CANNED_AV_RATELIMIT_JSON, CANNED_AV_INFO_JSON,
 CANNED_AV_EMPTY_JSON, CANNED_AV_MISSING_COL_JSON, CANNED_VENDOR_B_JSON) = _build_canned_payloads()
print("Canned payloads ready | AV success bytes:", len(CANNED_AV_SUCCESS_JSON))
""")

md(r"""
---
## SECTION D — Guided Exploration

### D1 — Inspect the raw wire JSON before writing a line of parser code
**Predict:** in `CANNED_AV_SUCCESS_JSON`, what Python type is `"4. close"` (`float` or `str`), and are the date keys ordered oldest-first or newest-first?
""")
md(r"""✍️ **D1 prediction (edit me):** value type = ___ · date order = ___""")
code(r"""
# D1 - inspect raw vendor wire format
raw_obj = json.loads(CANNED_AV_SUCCESS_JSON)
dates_preview = list(raw_obj["Time Series (Daily)"].keys())[:4]
first_bar = raw_obj["Time Series (Daily)"][dates_preview[0]]
print("Top-level keys:", list(raw_obj.keys()))
print("First 4 date keys on wire:", dates_preview)
print("Sample bar:", first_bar, "| type of '4. close':", type(first_bar["4. close"]).__name__)
# TODO(modify): build `pd.DataFrame.from_dict(raw_obj["Time Series (Daily)"], orient="index")` WITHOUT sorting or astype(float).
# What happens if you take `.pct_change()` on strings or on newest-first rows?
""")
md(r"""
✍️ **D1 observed (edit me):** on the wire, prices arrive as `____` and dates run `________`. Computing `.shift(1)` on descending dates would shift **tomorrow into today** (instant look-ahead bias!).

### D2 — How HTTP 200 rate-limit payloads masquerade as empty data
**Predict:** what does `json.loads(CANNED_AV_RATELIMIT_JSON).get("Time Series (Daily)", {})` return — an exception, or `{}`?
""")
md(r"""✍️ **D2 prediction (edit me):** """)
code(r"""
# D2 - silent empty dict vs explicit notice detection
rl_obj = json.loads(CANNED_AV_RATELIMIT_JSON)
naive = pd.DataFrame.from_dict(rl_obj.get("Time Series (Daily)", {}), orient="index")
print("Naive parser output shape:", naive.shape, "<-- zero error raised! Looks like 'no rows today'.")
print("Actual vendor payload keys:", list(rl_obj.keys()), "->", rl_obj["Note"][:70] + "...")
# TODO(modify): check `CANNED_AV_INFO_JSON` too. Which three top-level keys signal a vendor notice/error in Alpha Vantage?
""")
md(r"""
✍️ **D2 observed (edit me):** naive `.get(..., {})` returned shape `____`, hiding the rate limit completely. Checking `"Note"`, `"Information"`, and `"Error Message"` first turns a silent bug into an actionable exception.

### D3 — Why unadjusted stock splits wreck naive indicators
**Predict:** a stock trades steady at `$200`, undergoes a **4-for-1 split** (`$200 → $50` overnight with zero change in shareholder wealth!), and trades steady at `$50`. What single-day log return and `SMA20` distortion does **unadjusted** `Close` hallucinate on split day?
""")
md(r"""✍️ **D3 prediction (edit me):** """)
code(r"""
# D3 - synthetic 4-for-1 split on unadjusted vs split-adjusted Close
raw_split = pd.Series([200.0] * 25 + [50.0] * 25, index=pd.bdate_range("2023-01-02", periods=50))
adj_split = pd.Series([50.0] * 50, index=raw_split.index)   # pre-split prices divided by 4
print("Unadjusted split-day log return:", round(float(np.log(raw_split / raw_split.shift(1)).min()), 4), "(-75% phantom crash!)")
print("Adjusted split-day log return  :", round(float(np.log(adj_split / adj_split.shift(1)).min()), 4))
print("Unadjusted SMA10 vs SMA20 day after split:", float(raw_split.rolling(10).mean().iloc[25]),
      "vs", float(raw_split.rolling(20).mean().iloc[25]), "-> triggers fake bearish crossover!")
# TODO(modify): add a $2.00 cash dividend drop ($50 -> $48 ex-dividend). Which series measures total shareholder return?
""")
md(r"""✍️ **D3 observed (edit me):** unadjusted `Close` invented a `____%` crash and a fake crossover on a zero-economic-loss split. That is why vendor adjustment policy belongs in every backtest's methodology section.""")

md(r"""
---
## SECTION E — Independent Practice

### Exercise 1 — Basic: `parse_av_daily` with distinct failure exceptions
""")
code(r"""
class RateLimitError(ValueError):
    '''Raised when a vendor payload reports throttling, quota, or API-call errors.'''

class EmptyPayloadError(ValueError):
    '''Raised when a vendor payload contains no time-series bars.'''

class SchemaMismatchError(ValueError):
    '''Raised when required OHLCV fields or valid numeric/date values are missing.'''


def parse_av_daily(payload):
    '''Parse an Alpha-Vantage daily `payload` (`dict` or JSON `str`) into a Day-01
    validated OHLCV DataFrame:
      1. If `payload` is a `str`, `json.loads` it (invalid JSON -> SchemaMismatchError).
         Non-(dict/str) -> SchemaMismatchError.
      2. If top-level dict contains `"Note"`, `"Information"`, or `"Error Message"`:
         raise `RateLimitError` including a short reason.
      3. If `"Time Series (Daily)"` is missing or its mapping is empty (`len == 0`):
         raise `EmptyPayloadError`.
      4. Rename `"1. open"->"Open"`, `"2. high"->"High"`, `"3. low"->"Low"`,
         `"4. close"->"Close"`, `"5. volume"->"Volume"` (missing any of the 5 ->
         `SchemaMismatchError`), convert values to float, set ascending `DatetimeIndex`
         named `"Date"` (duplicate dates, non-positive prices, or negative volume ->
         `SchemaMismatchError` / `ValueError`), and return columns in exact order
         `["Open", "High", "Low", "Close", "Volume"]`.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Check failure modes in strict order: JSON/type validity → notice keys (`"Note"`, `"Information"`, `"Error Message"`) → presence & non-emptiness of `"Time Series (Daily)"` → column mapping & numeric conversion → ascending date sort & Day-01 OHLCV domain checks.</details>
<details><summary>Hint 2 — approach</summary>`pd.DataFrame.from_dict(ts_dict, orient="index")`; verify all 5 vendor column keys exist *before* selecting/renaming them; convert index with `pd.to_datetime(..., errors="raise")` and sort ascending via `.sort_index()`.</details>
<details><summary>Hint 3 — clue</summary>Wrap `astype(float)` in `try ... except (TypeError, ValueError) as exc: raise SchemaMismatchError(...) from exc`, then check `(out[["Open", "High", "Low", "Close"]] <= 0).values.any()` and `(out["Volume"] < 0).values.any()`.</details>

### Exercise 2 — Modification: generic `normalise_vendor_columns`
""")
code(r"""
def normalise_vendor_columns(df, mapping):
    '''Normalise an arbitrary vendor DataFrame `df` using `{vendor_col: canonical_col}`:
      - Every required canonical field `{"Open", "High", "Low", "Close", "Volume"}`
        must be produced after renaming -> else raise `SchemaMismatchError`.
      - Extra unmapped vendor columns are dropped cleanly; optional `"Adj Close"` is
        kept if mapped (`["Open", "High", "Low", "Close", "Adj Close", "Volume"]`),
        otherwise `["Open", "High", "Low", "Close", "Volume"]`.
      - Convert index to ascending `DatetimeIndex` named `"Date"` (empty frame,
        duplicate dates, non-numeric strings, non-positive prices, or negative volume
        -> `SchemaMismatchError` / `ValueError`).
      - Caller's `df` must not be modified.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Separate *column vocabulary* (`mapping`) from *invariant enforcement* (canonical column order, float dtypes, sorted `DatetimeIndex`, positive prices). Notice `parse_av_daily` can even delegate its step 4 right to `normalise_vendor_columns`!</details>
<details><summary>Hint 2 — clue</summary>Work on `work = df.copy()`; select only keys of `mapping` present in `work.columns`, `.rename(columns=mapping)`, verify `{"Open", "High", "Low", "Close", "Volume"}.issubset(renamed.columns)`, order columns, cast `float`, sort `DatetimeIndex`, and run OHLCV guards.</details>

### Exercise 3 — Debugging: hard-coded key + silent `except: pass`

Diagnose **both** professional-grade hazards in `fetch_av_buggy`, then implement `resolve_api_key`.
""")
code(r"""
# --- BUGGY / INSECURE ADAPTER (study; do not edit) ---
API_KEY_HARDCODED = "EXAMPLE_HARDCODED_KEY_NEVER_COMMIT_SECRETS"   # hazard 1

def fetch_av_buggy(symbol, payload_override=None):
    try:
        raw = payload_override or "{}"
        data = json.loads(raw)["Time Series (Daily)"]
        return pd.DataFrame.from_dict(data, orient="index")
    except Exception:                                               # hazard 2
        return pd.DataFrame()

print("Buggy return on a RATE-LIMIT response:", fetch_av_buggy("SYNA", CANNED_AV_RATELIMIT_JSON).shape)
""")
md(r"""✍️ **Diagnosis (edit me):** Hazard 1 (security): hard-coding `API_KEY_HARDCODED` in tracked source leaks credentials into `____` history forever (even deleting it in a later commit leaves it in `git log`). Hazard 2 (reliability): `except Exception: return pd.DataFrame()` turns rate limits, bad keys, and schema changes into `____`, poisoning downstream pipelines silently.""")
code(r"""
def resolve_api_key(api_key=None, env_var="ALPHAVANTAGE_API_KEY"):
    '''Return a non-empty stripped API key string from `api_key` if provided, else
    from `os.environ.get(env_var)`.
      - If neither yields a non-empty string (or `api_key` is not `None`/`str`),
        raise `ValueError` naming `env_var` in the message (NEVER echo secret values!).'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — clue</summary>Reject non-string `api_key` when `api_key is not None` (`if not isinstance(api_key, str): raise ValueError(...)`); strip whitespace; fall back to `os.environ.get(env_var, "").strip()`; if still `""`, `raise ValueError(f"Missing API key; set {env_var} in environment")`.</details>

### Exercise 4 — Independent: offline-testable `fetch_daily` (`pytrades/data.py` v0.3)
""")
code(r"""
def fetch_daily(symbol, api_key=None, _get=None):
    '''Fetch & parse daily OHLCV bars for `symbol` into a Day-01 validated DataFrame:
      - Validate `symbol` is a non-empty `str` (strip & `.upper()`); else ValueError.
      - Resolve key via `resolve_api_key(api_key)` (raises ValueError if unavailable).
      - If `_get` is provided (callable), invoke `payload = _get(clean_symbol, key)`.
        If `_get` is None, perform a live Alpha Vantage `TIME_SERIES_DAILY` GET via
        `requests.get` (`timeout=15`, `.raise_for_status()`, `.json()`).
      - Parse and validate `payload` via `parse_av_daily(payload)` and return the frame.
    Also add `RateLimitError`, `EmptyPayloadError`, `SchemaMismatchError`,
    `parse_av_daily`, `normalise_vendor_columns`, `resolve_api_key`, and `fetch_daily`
    to `pytrades/data.py` and bump `pytrades/__init__.py` to `__version__ = "0.3.0"`.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Dependency injection in 6 lines: `clean_symbol = symbol.strip().upper()`; `key = resolve_api_key(api_key)`; call `_get(clean_symbol, key)` when `_get is not None`; feed straight to `parse_av_daily`.</details>
<details><summary>Hint 2 — clue</summary>Check `isinstance(symbol, str) and len(symbol.strip()) > 0` before calling `resolve_api_key`. Every Section G check passes a custom `_get`, so zero network traffic ever occurs during testing.</details>

### Exercise 5 — Transfer: second vendor shape (`parse_row_records_daily`)
""")
code(r"""
def parse_row_records_daily(payload):
    '''Parse a row-list vendor payload (`dict` or JSON `str`) shaped like
    `CANNED_VENDOR_B_JSON` (`{"ticker": "...", "results": [{"t": ..., "o": ...,
    "h": ..., "l": ..., "c": ..., "v": ..., ...}]}`) into the exact same Day-01
    OHLCV DataFrame contract (`["Open", "High", "Low", "Close", "Volume"]`,
    ascending `DatetimeIndex` named `"Date"`, float dtypes), reusing
    `normalise_vendor_columns`.
      - Missing `"results"` -> `SchemaMismatchError`; empty `"results"` list -> `EmptyPayloadError`.'''
    # TODO
    pass
""")
md(r"""
<details><summary>Hint 1 — concept</summary>Decode JSON if string, check `"results"` exists (`SchemaMismatchError`) and is non-empty (`EmptyPayloadError`), build `pd.DataFrame(rows).set_index("t")`, and pass `{"o": "Open", "h": "High", "l": "Low", "c": "Close", "v": "Volume"}` into your `normalise_vendor_columns`!</details>
<details><summary>Hint 2 — clue</summary>Guard that every row in `"results"` has `"t"` before `.set_index("t")` (missing `"t"` → `SchemaMismatchError`). Extra vendor fields `"vw"` and `"n"` are dropped automatically by `normalise_vendor_columns`!</details>
""")

md(r"""
---
## SECTION F — Mini-Project · P2.4 Canned-API → `pytrades` Backtest End-to-End

### Specification — `run_canned_api_backtest(canned_payload, fast=20, slow=50, cost_rate=0.001)`
- Import `fetch_daily` from **`pytrades.data`** and `SMACrossoverStrategy` from **`pytrades.strategy`**.
- Call `fetch_daily("SYNA", api_key="TEST_ONLY_PLACEHOLDER", _get=lambda sym, k: canned_payload)` to obtain the validated OHLCV `DataFrame`.
- Run `SMACrossoverStrategy(ohlcv["Close"], fast=fast, slow=slow, long_only=True, cost_rate=cost_rate)` and return `(ohlcv, strat.run(), strat.summary())`.
""")
code(r"""
import importlib

def run_canned_api_backtest(canned_payload, fast=20, slow=50, cost_rate=0.001):
    '''See Section F specification. Pipes pytrades.data.fetch_daily -> pytrades.strategy.SMACrossoverStrategy.'''
    # TODO
    pass
""")
code(r"""
# SECTION F (apply) - zero network, zero live key, full end-to-end pipeline!
try:
    ohlcv_api, bt_api, sum_api = run_canned_api_backtest(CANNED_AV_SUCCESS_JSON, fast=20, slow=50, cost_rate=0.001)
    print("Parsed OHLCV shape:", ohlcv_api.shape,
          f"| ascending? {ohlcv_api.index.is_monotonic_increasing}",
          f"| span {ohlcv_api.index[0].date()}..{ohlcv_api.index[-1].date()}")
    print("End-to-end SMA(20,50) summary on canned vendor feed:\n", pd.Series(sum_api))
    ax = bt_api[["benchmark_wealth", "strategy_wealth"]].plot(
        figsize=(9, 3.8), title="P2.4: Canned Alpha-Vantage JSON -> pytrades.data -> SMACrossoverStrategy"
    )
    ax.set_ylabel("Wealth ($1)"); plt.tight_layout(); plt.show()
except Exception as exc:
    print("P2.4 end-to-end adapter not ready yet:", type(exc).__name__, exc)
""")
md(r"""
✍️ **P2.4 Adapter & Vendor Quality Note (edit me):**
- **Three bugs `parse_av_daily` prevented before `SMACrossoverStrategy` ever saw the data:** 1) … 2) … 3) …
- **If switching from unadjusted daily closes to split-and-dividend-adjusted closes in real research, which metrics in `sum_api` could change and why?** …

---
## SECTION G — Automated Assessment
""")
code(r"""
# SECTION G - harness + visible checks (100% offline on canned payloads!)
RESULTS = []
def check(name, fn):
    try: ok = bool(fn()); msg = ""
    except Exception as exc: ok = False; msg = f"{type(exc).__name__}: {exc}"
    RESULTS.append(ok); print(("PASS" if ok else "FAIL"), "-", name, (("| " + msg) if msg else ""))
def raises(t, fn):
    try: fn()
    except Exception as exc:
        return isinstance(exc, t) or (isinstance(exc, ValueError) and type(exc).__name__ == t.__name__)
    return False

def _ex1_happy():
    f = parse_av_daily(CANNED_AV_SUCCESS_JSON)
    return (list(f.columns) == ["Open", "High", "Low", "Close", "Volume"]
            and len(f) == 160 and isinstance(f.index, pd.DatetimeIndex)
            and f.index.name == "Date" and f.index.is_monotonic_increasing
            and all(f[c].dtype.kind == "f" for c in ["Open", "High", "Low", "Close"]))
check("Ex1 parse_av_daily: 160 rows sorted ascending, float dtypes, canonical columns", _ex1_happy)
check("Ex1 RateLimitError raised on 'Note', 'Information', and 'Error Message'", lambda: (
    raises(RateLimitError, lambda: parse_av_daily(CANNED_AV_RATELIMIT_JSON))
    and raises(RateLimitError, lambda: parse_av_daily(CANNED_AV_INFO_JSON))
    and raises(RateLimitError, lambda: parse_av_daily({"Error Message": "Invalid API call"}))))
check("Ex1 EmptyPayloadError raised on empty Time Series (Daily)", lambda: (
    raises(EmptyPayloadError, lambda: parse_av_daily(CANNED_AV_EMPTY_JSON))
    and raises(EmptyPayloadError, lambda: parse_av_daily({"Meta Data": {}}))))
check("Ex1 SchemaMismatchError on missing '4. close' or malformed JSON", lambda: (
    raises(SchemaMismatchError, lambda: parse_av_daily(CANNED_AV_MISSING_COL_JSON))
    and raises(SchemaMismatchError, lambda: parse_av_daily("{not-valid-json"))))
check("Ex1 rejects non-positive price in vendor payload", lambda: raises(ValueError, lambda: parse_av_daily({
    "Time Series (Daily)": {"2020-01-03": {"1. open": "10", "2. high": "11", "3. low": "0", "4. close": "10", "5. volume": "100"}}
})))

def _ex2_norm():
    raw = pd.DataFrame({
        "op": ["10.5", "10.0"], "hi": ["11.0", "10.5"], "lo": ["10.0", "9.5"],
        "cl": ["10.8", "10.2"], "vol": ["500", "400"], "junk_col": ["x", "y"]
    }, index=["2022-01-05", "2022-01-04"])
    snap = list(raw.columns)
    out = normalise_vendor_columns(raw, {"op": "Open", "hi": "High", "lo": "Low", "cl": "Close", "vol": "Volume"})
    return (list(out.columns) == ["Open", "High", "Low", "Close", "Volume"]
            and out.index[0] == pd.Timestamp("2022-01-04") and float(out["Close"].iloc[0]) == 10.2
            and list(raw.columns) == snap
            and raises(SchemaMismatchError, lambda: normalise_vendor_columns(raw.drop(columns=["cl"]),
                       {"op": "Open", "hi": "High", "lo": "Low", "cl": "Close", "vol": "Volume"})))
check("Ex2 normalise_vendor_columns renames, drops extras, sorts dates & checks schema", _ex2_norm)

def _ex3_key():
    env_name = "_PYTRADES_TEST_KEY_TMP"
    os.environ[env_name] = "  env_secret_value  "
    try:
        k1 = resolve_api_key(None, env_var=env_name)
        k2 = resolve_api_key(" explicit_val ", env_var=env_name)
    finally:
        os.environ.pop(env_name, None)
    miss = raises(ValueError, lambda: resolve_api_key(None, env_var="_DEFINITELY_UNSET_PYTRADES_VAR"))
    empty = raises(ValueError, lambda: resolve_api_key("   ", env_var="_DEFINITELY_UNSET_PYTRADES_VAR"))
    return k1 == "env_secret_value" and k2 == "explicit_val" and miss and empty
check("Ex3 resolve_api_key reads env var, strips whitespace & fails loudly when unset", _ex3_key)

def _ex4_fetch():
    seen = {}
    def fake_transport(sym, key):
        seen["call"] = (sym, key)
        return CANNED_AV_SUCCESS_JSON
    f = fetch_daily("  syna ", api_key="unit_test_token", _get=fake_transport)
    rl = raises(RateLimitError, lambda: fetch_daily("syna", api_key="tok", _get=lambda s, k: CANNED_AV_RATELIMIT_JSON))
    bad_sym = raises(ValueError, lambda: fetch_daily("   ", api_key="tok", _get=fake_transport))
    return seen.get("call") == ("SYNA", "unit_test_token") and len(f) == 160 and rl and bad_sym
check("Ex4 fetch_daily normalises symbol, injects _get transport & propagates RateLimitError", _ex4_fetch)

def _ex5_vendor_b():
    fb = parse_row_records_daily(CANNED_VENDOR_B_JSON)
    exp = parse_av_daily(CANNED_AV_SUCCESS_JSON).iloc[:30]
    return (list(fb.columns) == ["Open", "High", "Low", "Close", "Volume"]
            and len(fb) == 30 and np.allclose(fb["Close"].values, exp["Close"].values)
            and raises(EmptyPayloadError, lambda: parse_row_records_daily({"ticker": "X", "results": []}))
            and raises(SchemaMismatchError, lambda: parse_row_records_daily({"ticker": "X"})))
check("Ex5 parse_row_records_daily adapts 2nd vendor shape to identical OHLCV contract", _ex5_vendor_b)

def _ex4_pkg_v03():
    import pytrades, pytrades.data as pd_mod
    importlib.reload(pd_mod); importlib.reload(pytrades)
    f = pd_mod.fetch_daily("SYNA", api_key="tok", _get=lambda s, k: CANNED_AV_SUCCESS_JSON)
    return len(f) == 160 and pd_mod.validate_ohlcv(f) is True
check("Ex4 pytrades.data v0.3 exports working fetch_daily + validate_ohlcv", _ex4_pkg_v03)

def _proj_ok():
    ohlcv_f, bt_f, summ = run_canned_api_backtest(CANNED_AV_SUCCESS_JSON, fast=20, slow=50, cost_rate=0.001)
    return (len(ohlcv_f) == 160 and len(bt_f) == 110 and summ["n_days"] == 110
            and abs(float(bt_f["strategy_wealth"].iloc[-1]) - 1.0 - summ["total_return"]) < 1e-12)
check("F project: canned JSON -> pytrades.data.fetch_daily -> SMACrossoverStrategy end-to-end", _proj_ok)
print(f"\nSCORE: {sum(RESULTS)}/{len(RESULTS)} visible checks passing")
""")

md(r"""
---
## SECTION H — Knowledge Check

**H1 (Pre-watch #2 revisited)** You accidentally commit a notebook containing a real API key, notice 30 seconds later, delete the key, and `git commit -m "remove key"`. Why is the key **still compromised**, and what two immediate actions must you take? ✍️
**H2 (Pre-watch #3 revisited)** Suppose a teammate skips `.sort_index()` in `parse_av_daily` so rows remain newest-first (`2024 → 2015`). Trace what `.shift(1)` in `positions_from_signal` actually computes on a newest-first frame! ✍️
**H3 Defend** raising three distinct subclasses (`RateLimitError`, `EmptyPayloadError`, `SchemaMismatchError`) instead of returning `None` on bad payloads. How should a retry script react differently to `RateLimitError` vs `SchemaMismatchError`? ✍️
**H4 Dependency injection** Explain how `_get=None` in `fetch_daily` let Section G test symbol normalisation, key resolution, rate-limit handling, and backtest integration in `<0.1s` with zero internet access. ✍️
**H5 Vendor bias** Two students run the *exact same* `SMACrossoverStrategy(prices, 50, 200)` on AAPL from 2010–2024: Student A uses unadjusted `Close` (AAPL had a 7-for-1 split in 2014 and a 4-for-1 split in 2020); Student B uses split-and-dividend-adjusted `Close`. Predict how their trade counts and returns differ and why. ✍️
**H6 Bridge to Day 13 (Capstone)** Before starting Day 13 tomorrow, choose **one** non-video strategy family from `projects/CAPSTONE.md` (`Price > SMA200` filter, `EMA crossover`, or `Donchian breakout`) and write down your parameter values **now** — *before* ever plotting `unseen_df` — explaining why pre-committing parameters matters. ✍️
""")

md(r"""
---
## SECTION I — Reflection & Retrieval Practice

### What I learned · Can implement unaided · Still difficult ✍️

### Retrieval — Days 01 (n−11, full circle!), 08 (n−4), 06 (n−6)
1. **Day 01:** List all validation invariants enforced by `validate_ohlcv(df)` (index type, order, duplicates, columns, price domain, volume domain).
2. **Day 08:** Why did `run_canned_api_backtest` on 160 daily bars with `fast=20, slow=50` produce `110` tradable rows (`160 - 50`), not `111`?
3. **Day 06:** Why does `log_returns` raise `ValueError` on `0.0` or negative prices instead of letting `np.log` emit `-inf` / `NaN`?
""")
code(r"""
# Full-circle Day-01 retrieval: reimplement `validate_ohlcv_from_memory(df)` without peeking!
def validate_ohlcv_from_memory(df):
    '''Return True if `df` has a sorted, duplicate-free DatetimeIndex, required columns
    Open/High/Low/Close/Volume, strictly positive prices, and non-negative Volume;
    otherwise raise ValueError.'''
    # TODO
    pass

try:
    _good = parse_av_daily(CANNED_AV_SUCCESS_JSON) if callable(parse_av_daily) and parse_av_daily(CANNED_AV_SUCCESS_JSON) is not None else df.iloc[:5].copy()
    _bad = _good.copy(); _bad.iloc[0, 0] = 0.0
    _threw = False
    try: validate_ohlcv_from_memory(_bad)
    except ValueError: _threw = True
    _ok = (validate_ohlcv_from_memory(_good) is True) and _threw
except Exception as exc:
    _ok = False; print("self-check raised:", type(exc).__name__, exc)
print("Day-01 validate_ohlcv from-memory self-check:", "PASS" if _ok else "not yet")
""")
md(r"""
### ✅ Completion checklist
- [ ] Final video segment `02:51:00–03:00:48` watched (entire 3h00m48s tutorial now covered!)
- [ ] Ex 1–5 green (`11/11` checks in Section G), zero network calls or hard-coded secrets
- [ ] `pytrades` v0.3 (`pytrades/data.py`) exports `parse_av_daily`, `normalise_vendor_columns`, `resolve_api_key`, `fetch_daily`
- [ ] P2.4 end-to-end canned-JSON → `SMACrossoverStrategy` backtest green
- [ ] **H6 pre-commitment written** (capstone strategy family + parameters chosen *before* opening Day 13!)

**Send back:** Section G score · your H6 pre-committed capstone topic & parameter choice · H1 security response. Day 13 is your **🏁 Capstone**.
""")

nb = new_notebook(cells=CELLS)
nb.metadata.update({"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                    "language_info": {"name": "python", "version": "3.11"},
                    "title": "Day 12 - APIs and External Market Data (pytrades v0.3)",
                    "source_video": "https://www.youtube.com/watch?v=GDMkkmkJigw (02:51:00-03:00:48)"})
out = ROOT / "notebooks" / "Day_12_APIs_and_External_Market_Data.ipynb"
nbformat.write(nb, out); print("wrote", out, "cells=", len(CELLS))
