#!/usr/bin/env python3
"""tools/journal.py - the 90-entry habit, made cheap enough to keep.

    make journal                      # create today's entry (idempotent)
    python tools/journal.py new       # same thing
    python tools/journal.py prompt    # just print today's prompt
    python tools/journal.py stats     # entries written, streak, gaps

One entry per day. Five fields, two minutes. The journal is 15% of your grade and
100% of your memory: in Week 13 you will not remember why P06 died.
"""

from __future__ import annotations

import argparse
import glob
import os
from datetime import date, datetime, timedelta

JOURNAL_DIR = "journal"
PROMPTS = [
    "What did I try to build today, and what broke first?",
    "What surprised me about the numbers today?",
    "Where might I be fooling myself right now?",
    "What did costs do to today's idea?",
    "Which assumption did I not test today?",
    "What would make this strategy fail in a way I have not imagined?",
    "What did I learn that changes a decision I already made?",
]

TEMPLATE = """# {today}

**Built:** {built}
**Broke:** {broke}
**Numbers:** {numbers}
**How I might be fooling myself:** {fooling}
**Tomorrow:** {tomorrow}

<!--
Prompts, if you are stuck: {prompt}
Keep this honest. Nobody reads it but you - and Week 13 you, who will need it.
-->
"""


def entry_path(day: date) -> str:
    return os.path.join(JOURNAL_DIR, "%s.md" % day.isoformat())


def stats() -> int:
    entries = sorted(glob.glob(os.path.join(JOURNAL_DIR, "*.md")))
    dated = [os.path.basename(p)[:-3] for p in entries if len(os.path.basename(p)) == 13]
    if not dated:
        print("no entries yet - run: make journal")
        return 1
    first, last = date.fromisoformat(dated[0]), date.fromisoformat(dated[-1])
    span = (last - first).days + 1
    missing = [first + timedelta(days=i) for i in range(span) if (first + timedelta(days=i)).isoformat() not in dated]
    streak = 0
    cursor = date.today()
    while cursor.isoformat() in dated:
        streak += 1
        cursor -= timedelta(days=1)
    print("%d entries, %s -> %s (%d of %d days covered, current streak %d)" % (len(dated), first, last, len(dated), span, streak))
    if missing:
        preview = ", ".join(d.isoformat() for d in missing[:8])
        print("gaps: %s%s" % (preview, " ..." if len(missing) > 8 else ""))
        print("A gap is fine. A silent gap is not: backfill it with what you remember, dated correctly.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", default="new", choices=["new", "prompt", "stats"])
    args = parser.parse_args()

    today = date.today()
    prompt = PROMPTS[today.toordinal() % len(PROMPTS)]

    if args.command == "prompt":
        print(prompt)
        return 0
    if args.command == "stats":
        return stats()

    os.makedirs(JOURNAL_DIR, exist_ok=True)
    path = entry_path(today)
    if os.path.exists(path):
        print("%s already exists - edit it, do not duplicate it." % path)
        print("Today's prompt: %s" % prompt)
        return 0
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(
            TEMPLATE.format(
                today=today.isoformat(),
                built="(what shipped today - even if ugly)",
                broke="(the first thing that failed, and the error message)",
                numbers="(one number you measured, with units and sample size)",
                fooling="(the assumption you did not test)",
                tomorrow="(the single next action)",
                prompt=prompt,
            )
        )
    print("wrote %s" % path)
    print("Today's prompt: %s" % prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
