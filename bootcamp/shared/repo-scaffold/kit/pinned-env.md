# Pinning your environment (do this in Week 1, thank yourself in Week 12)

Numbers that change between library versions are numbers you cannot defend. Pin once.

```bash
# 1. pick an interpreter and write it down
python -V                      # e.g. Python 3.11.9  -> record it in README

# 2. install from requirements, then freeze what you actually got
pip install -r requirements.txt
pip freeze > requirements.lock.txt

# 3. record the floating-point stack (this is the part that bites)
python -c "import pandas, numpy; print(pandas.__version__, numpy.__version__)" | tee reports/env.txt
```

Rules:

- `requirements.txt` states intent (ranges). `requirements.lock.txt` states reality (exact).
- Any time you install something new, re-freeze and note it in the journal.
- If a number changes after an upgrade, you have two possible stories: a bug fix, or a
  regression. Re-run the same saved spec and compare `meta.json` fingerprints. If the
  fingerprints match and the result does not, the library changed the arithmetic - say so.
