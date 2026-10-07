# PyTrades student repo - every command you need, nothing you don't.
#
#   make doctor                                   # is my machine ready?
#   make data SYMBOLS="SPY QQQ" START=2010-01-01  # real bars into data/
#   make run S=S01_ma_cross NAME=baseline         # backtest + saved artifacts
#   make gate WEEK=1                              # am I allowed to move on?
#
# Until Week 4 the engine is kit/spine.py (the reference implementation).
# From Week 4:  make run E=engine.backtest S=... NAME=...

SHELL := /bin/bash
PY ?= python
ENGINE ?= kit.spine
S ?=
NAME ?=
A ?=
B ?=
WEEK ?= 1
SYMBOLS ?= SPY
START ?= 2010-01-01
END ?= $(shell date +%Y-%m-%d)
OOS_YEARS ?= 3

.PHONY: help doctor data validate list run costs compare breakeven report test test-kit test-contract journal gate gate-all scaffold clean

help:  ## show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

doctor:  ## check the environment before you blame the strategy
	@$(PY) tools/doctor.py

data:  ## fetch bars: make data SYMBOLS="SPY QQQ" START=2010-01-01
	@$(PY) -m kit.data_fetcher fetch $(SYMBOLS) --start $(START) --end $(END)

validate:  ## validate every cached CSV and print a coverage table
	@$(PY) tools/validate_all.py

list:  ## list strategy specs
	@$(PY) -m $(ENGINE) list

run:  ## backtest a spec: make run S=S01_ma_cross NAME=baseline [FEE=1 SLIP=2]
	@$(PY) -m $(ENGINE) run $(S) --name $(or $(NAME),$(S)) --fee-bps $(or $(FEE),0) --slippage-bps $(or $(SLIP),0)

costs:  ## cost sensitivity for a spec: make costs S=S01_ma_cross
	@$(PY) -m $(ENGINE) breakeven $(S)

compare:  ## compare two saved runs: make compare A=baseline B=with_costs
	@$(PY) -m $(ENGINE) compare $(A) $(B)

breakeven:  ## alias for costs, kept for muscle memory
	@$(PY) -m $(ENGINE) breakeven $(S)

report:  ## markdown tearsheet for a saved backtest: make report S=S01_ma_cross NAME=baseline
	@$(PY) tools/report.py $(or $(NAME),$(S))

test: test-kit test-contract  ## run every test
	@$(PY) -m pytest tests kit/tests -q

test-kit:  ## the reference metric tests (your oracle)
	@$(PY) -m pytest kit/tests/test_metrics.py -q

test-contract:  ## the spine contract, against the engine named by ENGINE
	@PYTRADES_ENGINE=$(ENGINE) $(PY) -m pytest kit/tests/test_spine_contract.py -q

journal:  ## create today's journal entry from the template
	@$(PY) tools/journal.py new

gate:  ## check a week's gate: make gate WEEK=1
	@$(PY) tools/check_gate.py --week $(WEEK) --engine $(ENGINE)

gate-all:  ## check every gate up to now and print your progress
	@$(PY) tools/check_gate.py --all --engine $(ENGINE)

scaffold:  ## create folders a later week expects (idempotent)
	@mkdir -p data config strategies papers live/log reports/backtests reports/debunks reports/sensitivity reports/figures journal tests
	@echo "scaffold: ok"

clean:  ## remove generated artifacts (never touches data/ or journal/)
	@rm -rf reports/backtests/* reports/figures/generated .pytest_cache
	@find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	@echo "clean: ok (data/, journal/, graveyard.md untouched)"
