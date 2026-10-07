# HANDOFF — maintaining this course

This document is for whoever owns the course next (including future you). It explains what is
generated, what is hand-written, and how to change either without breaking the other.

## The single source of truth

`bootcamp/registry.json` defines the course: phases, weeks, deliverables, concepts, milestones,
gates, grading weights and the live-paper policy. Everything else is either generated from it or
checked against it.

## Generated artifacts (never edit by hand)

| Artifact | Generator | Consumed by |
| --- | --- | --- |
| `bootcamp/syllabus.md` tables | `bootcamp/tools/build_syllabus.py` | humans; `verify_course.py` checks for drift |
| `bootcamp/shared/repo-scaffold/gates.json` | `bootcamp/tools/sync_gates.py` | the student repo's `tools/check_gate.py` |
| `bootcamp/shared/sample-data/*.csv` + `truth.json` | `bootcamp/tools/make_sample_data.py` | the Week 1-2 labs (and the worked example) |

Run all three after touching the registry, then run the verifier:

```bash
python bootcamp/tools/build_syllabus.py
python bootcamp/tools/sync_gates.py
python bootcamp/tools/make_sample_data.py --check     # only if the labs changed
python bootcamp/tools/verify_course.py
python bootcamp/tools/test_the_course.py
```

## What the verifier enforces (and why you should not weaken it)

`verify_course.py` runs 14 check groups over the package: counts, registry integrity, structure,
week files (7 daily tasks, objective, deliverable, gate, graveyard prompt, concept links), concept
format (WHY NOW / FORMULA / CODE / EXAMPLE / TIME / DONE WHEN + the explain-and-spot requirement),
deliverable sheets, milestone cards (verbatim pass conditions + Fail/Remediate), gate documentation,
evidence annotations, internal links, python hygiene, placeholder bans, generated-block sync, and
the spec's acceptance criteria CA1-CA8.

`test_the_course.py` then applies 14 mutations (delete a week file, break a link, strip a DONE
WHEN, drift the registry, corrupt the metrics mirror, and so on) and asserts each one is caught. If
you add a structural rule, add a mutation for it - a check nobody has seen fail is a check nobody
knows works.

## The concept format is a contract

Every `phases/*/concepts/C##-*.md` file must contain the literal blocks `**WHY NOW:**`,
`**FORMULA:**`, `**CODE:**`, `**EXAMPLE:**`, `**TIME:**`, `**DONE WHEN:**`, a fenced code block, and
a DONE WHEN paragraph containing both "explain" and "spot". The point is not ceremony: a concept
without a triggering failure and a spot-the-error test is a lecture, and this course does not
contain lectures.

## The student-side kit and its mirrors

`bootcamp/shared/repo-scaffold/kit/` is canonical for `metrics.py`, `data_fetcher.py` and
`spine.py`. The module guides mirror two of them:

- `bootcamp/shared/metrics-module/kit/metrics.py`
- `bootcamp/shared/data-fetcher/kit/data_fetcher.py`

After changing a canonical module, copy it to its mirror (keep them byte-identical; the mutation
suite targets the metrics mirror because it must stay a real, compiling copy).

## Known design decisions worth preserving

1. **The reference kit is simple on purpose.** `kit/spine.py` restrikes target weights each bar;
   the student's `engine/` must track quantities so weights drift between rebalances. The
   `next_open` decomposition in the kit docstring is pinned by a contract test - if you change the
   semantics, change the test and the engine spec together (they are the same claim in three
   places).
2. **`kit/data_fetcher.py` never silently uses synthetic data.** `provider="synthetic"` and the
   no-network `allow_synthetic=True` fallback both write a `synthetic: true` flag into
   `data/<SYM>.meta.json`, and `assert_not_synthetic()` refuses such frames in graded runs.
3. **The 30-day live clock starts in Week 5.** Do not move it later; the calendar is the one
   resource you cannot compress, and M5 depends on it.
4. **Gate checks that run commands must be satisfiable by the ship-dated repository.** G1.6 runs
   `python tools/check_gate.py --week 1 --self-test`, which exists for exactly that reason.
5. **Placeholders are banned outside `templates/`, `solutions/`, `instructor/` and
   `worked-example/`.** If you need a "fill this in" marker, put it in a template.

## How to add a week

1. Add the week, its deliverable(s), concept(s) and gate to `registry.json`.
2. Run `build_syllabus.py` and `sync_gates.py`.
3. Create `phases/<phase>/week-NN.md` (front matter must match the registry exactly), the gate
   file (naming every check id), the deliverable sheet (with the annotation marker and the
   registry's evidence file names), the concept files (format above), and update the phase
   `README.md`/`rubric.md`.
4. Run `verify_course.py` until green, then `test_the_course.py` to confirm the new material is
   covered by the verifier.
