# PyTrades — ALX-style Algorithmic Trading Programme (from one YouTube tutorial)

A project-based conversion of **"Algorithmic Trading Python for Beginners - FULL TUTORIAL"**
by QuantProgram (3:00:48) into **13 learning days, one Jupyter notebook per day**.

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
├── requirements.txt
├── data/
│   ├── sample/demo_ohlcv.csv  ← synthetic, deterministic (seed 42) — assessed work runs offline
│   └── processed/             ← your generated outputs (git-ignored)
├── notebooks/
│   └── Day_01_Environment_and_First_Market_Data.ipynb   ← START HERE
├── projects/                  ← milestone/capstone specs (added as you reach them)
├── assessments/               ← how marking works (visible vs unseen tests)
└── tools/                     ← instructor utilities (sample-data generator, notebook builder)
```

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
Every video cell has a plain clickable fallback link with timestamps.

## Progress

| Day | Notebook | Status |
|---|---|---|
| 01 | Environment & first market data | ✅ |
| 02 | Working with data: read/write, segregate | ✅ |
| 03 | Visualisation, normalisation, creating data | ✅ |
| 04 | Resampling & first risk numbers (🏁 Milestone 1) | ✅ |
| 05 | Loops, correlation, covariance — Challenge 1 | ✅ |
| 06 | Returns & moving averages — Challenge 2 | ✅ |
| 07 | Alignment, cumulative returns, drawdowns (🏁 Milestone 2) | ✅ **← Week 1 complete** |
| 08–13 | Backtesting → functions → classes → APIs → capstone | 📐 Fully specified in [WEEK2_AUTHORING_GUIDE.md](WEEK2_AUTHORING_GUIDE.md); authored in 3 batches as you progress. **Total: 13 learning days (≤ 2 weeks)** |

**When you finish a day**, bring back: your Section G score, your answers in
Sections H–I, and any error you could not explain — or say **"produce the next"**
to have Day 08 (the first backtest) authored. Each day assumes the previous
checklists are green; milestone gates are in `projects/`.
