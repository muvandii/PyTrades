# PyTrades — ALX-style Algorithmic Trading Programme (from one YouTube tutorial)

A project-based conversion of **"Algorithmic Trading Python for Beginners - FULL TUTORIAL"**
by QuantProgram (3:00:48) into **13 learning days (≤ 2 weeks), one Jupyter notebook per day**.

🎥 Source video: https://www.youtube.com/watch?v=GDMkkmkJigw
🗺️ Full plan, timestamps and milestones: **[COURSE_MAP.md](COURSE_MAP.md)**

> **Rule of this programme:** a day is complete when you can *implement and explain*
> the day's concepts without the video — not when the video ends.
> Nothing in this repository is financial advice. Backtests here are educational
> research sketches, not trading systems.

## Repository layout

```text
PyTrades/
├── README.md                  ← you are here
├── COURSE_MAP.md              ← 13-day map: segment, objectives, deliverable per day
├── WEEK2_AUTHORING_GUIDE.md   ← instructor design system & Week-2 specification
├── requirements.txt
├── data/
│   ├── sample/
│   │   ├── demo_ohlcv.csv         ← synthetic 1y OHLCV (seed 42, Week 1)
│   │   ├── multi_ticker_ohlcv.csv ← synthetic 3-ticker MultiIndex panel (Week 1)
│   │   └── long_spy_like.csv      ← synthetic ~10y OHLCV (2,520 bars, seed 808, Week 2)
│   └── processed/             ← your generated outputs (git-ignored)
├── notebooks/
│   ├── Day_01_Environment_and_First_Market_Data.ipynb   ← START HERE
│   ├── ...
│   └── Day_13_Capstone_Unseen_Strategy_and_Critique.ipynb
├── projects/                  ← Milestone 1–3 gates, pytrades/ package spec & Capstone rubric
├── assessments/               ← how marking works (visible vs unseen tests)
└── tools/                     ← instructor utilities (sample-data generator, notebook builders)
```

*(On Days 10–12 you will also create `pytrades/` at the repository root — graduating from
notebooks to your own importable Python package per [`projects/PACKAGE_SPEC.md`](projects/PACKAGE_SPEC.md).)*

## Quick start

**Option A — as in the video:** install Anaconda, open Anaconda Navigator → Jupyter Notebook.

**Option B — venv (equivalent):**

```bash
cd PyTrades
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook notebooks/Day_01_Environment_and_First_Market_Data.ipynb
```

Embedded video cells need internet + a Jupyter frontend that allows iframes.
Every video cell has a plain clickable fallback link with timestamps, and **all
graded exercises and tests run 100% offline** on bundled/canned synthetic data.

## Progress — Full 13-Day Programme

| Day | Notebook | Status |
|---|---|---|
| 01 | [Environment & first market data](notebooks/Day_01_Environment_and_First_Market_Data.ipynb) | ✅ |
| 02 | [Working with data: read/write, segregate](notebooks/Day_02_Working_With_Data_Read_Write_Segregate.ipynb) | ✅ |
| 03 | [Visualisation, normalisation, creating data](notebooks/Day_03_Visualisation_Normalisation_Creating_Data.ipynb) | ✅ |
| 04 | [Resampling & first risk numbers](notebooks/Day_04_Resampling_and_First_Risk_Numbers.ipynb) (**🏁 Milestone 1**) | ✅ |
| 05 | [Loops, correlation, covariance — Challenge 1](notebooks/Day_05_Loops_Correlation_Covariance_Challenge1.ipynb) | ✅ |
| 06 | [Returns & moving averages — Challenge 2](notebooks/Day_06_Returns_and_Moving_Averages.ipynb) | ✅ |
| 07 | [Alignment, cumulative returns, drawdowns](notebooks/Day_07_Alignment_Cumulative_Returns_Drawdowns.ipynb) (**🏁 Milestone 2 — Week 1 complete**) | ✅ |
| 08 | [First vectorised backtest: SMA crossover](notebooks/Day_08_First_Vectorised_Backtest_SMA_Crossover.ipynb) | ✅ |
| 09 | [Long-only bias, costs & honest comparison — Challenge 3](notebooks/Day_09_Long_Only_Bias_and_Honest_Comparison.ipynb) (**🏁 Milestone 3**) | ✅ |
| 10 | [Functions: reusable strategy tester & `pytrades` v0.1](notebooks/Day_10_Functions_Reusable_Strategy_Tester.ipynb) | ✅ |
| 11 | [Classes: importable strategy object & Challenge 4 (`pytrades` v0.2)](notebooks/Day_11_Classes_Importable_Strategy_Object.ipynb) | ✅ |
| 12 | [APIs & external vendor data (`pytrades` v0.3)](notebooks/Day_12_APIs_and_External_Market_Data.ipynb) | ✅ |
| 13 | [Capstone: unseen strategy, unseen ticker & critique](notebooks/Day_13_Capstone_Unseen_Strategy_and_Critique.ipynb) (**🏁 Capstone — Week 2 complete**) | ✅ |

**When you finish a day**, bring back: your Section G score, your answers in
Sections H–I, and any error you could not explain. Each day assumes the previous
checklists are green; milestone gates and rubrics live in [`projects/`](projects/README.md).
