# The six templates (what to copy, and what each family will teach you)

| id | Family | Copy from | Expected fate | The lesson it carries |
| --- | --- | --- | --- | --- |
| S01 | trend (MA cross) | [signal_S01_ma_cross.py](signal_S01_ma_cross.py) + [configs/S01_ma_cross.json](configs/S01_ma_cross.json) | survives costs, modest OOS edge or tie with buy-and-hold | patience is cheap; whipsaw is the enemy |
| S02 | reversion (RSI) | [signal_S02_rsi_reversion.py](signal_S02_rsi_reversion.py) + [configs/S02_rsi_reversion.json](configs/S02_rsi_reversion.json) | gross positive, `cost death` at 5-20 bps | turnover is the tax your signal pays for its own existence |
| S03 | reversion (Bollinger) | [signal_S03_bollinger.py](signal_S03_bollinger.py) + [configs/S03_bollinger.json](configs/S03_bollinger.json) | gross Sharpe ~1, net ~0 | the worked example: how a good gross idea dies honestly |
| S04 | trend (breakout) | [signal_S04_donchian.py](signal_S04_donchian.py) + [configs/S04_donchian.json](configs/S04_donchian.json) | sub-40% win rate, profit factor ~1, cost-tolerant | win rate and edge are different animals |
| S05 | momentum (cross-sectional) | [signal_S05_momentum.py](signal_S05_momentum.py) + [configs/S05_momentum.json](configs/S05_momentum.json) | the most likely survivor; crashes occasionally | diversification across assets, not just time |
| S06 | pairs (relative value) | [signal_S06_pairs.py](signal_S06_pairs.py) + [configs/S06_pairs.json](configs/S06_pairs.json) | works in-sample, decays later | relationships are properties of periods, not of pairs |

## How to use a template

```bash
mkdir -p strategies/S01_ma_cross && cp <course>/templates/signal_S01_ma_cross.py strategies/S01_ma_cross/signal.py
cp <course>/templates/configs/S01_ma_cross.json config/S01_ma_cross.json
make run E=engine.backtest S=S01_ma_cross NAME=s01_is
make costs S=S01_ma_cross
```

Then change parameters and re-run under a **new name** - never overwrite an artifact you have
already written a verdict about. The template is a starting point, not a result: the verdict is
about *your* run with *your* universe and period, and the fingerprints in `meta.json` are the
proof of that.

## Deliberate omissions in the templates

- **No stops.** Stop-loss rules are a separate experiment (and usually a separate graveyard
  entry). Adding one to the template would hide the signal's own behaviour.
- **No volatility scaling.** That arrives in Phase 4 (C17). Templates stay at fixed exposure so
  the family's raw edge is visible.
- **No parameter tuning.** The parameters are textbook defaults, deliberately not the best ones.
  If your first run is beautiful, you have probably not looked hard enough at the grid.

## Multi-asset note

S05 and S06 need more than one symbol cached. If your `data/` directory is thin, fetch the
universe first (`make data SYMBOLS="SPY QQQ IWM TLT IEF GLD EEM EFA DBC UUP" START=2005-01-01`)
or use the laboratory series in `shared/sample-data/` to rehearse the mechanics.
