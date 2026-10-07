# Week 11 gate — you do not advance until this passes

Run it: `make gate WEEK=11`.

**Checkpoint:** the bot runs unattended for 7 consecutive days - signals generated, orders submitted or explicitly skipped, every day logged, dashboard rebuilt - and the run is longer than that, because the 30-day clock started in Week 5.

## Automated checks

| id | what it checks | why it matters |
| --- | --- | --- |
| G11.1 | `live/bot.py` exists | the harness is code, not a habit |
| G11.2 | 7+ files in `live/log/*.json` | seven consecutive days of logged decisions |
| G11.3 | `live/dashboard.html` exists | the report is generated, not assembled by hand |
| G11.4 | 5+ journal entries dated in week 11 | the habit continues |
| G11.5 | *(manual)* the bot ran unattended: no manual order edits in the log window | unattended operation is the claim being graded |

Confirm G11.5 with: `python tools/check_gate.py --week 11 --confirm G11.5`

## The G11.5 standard

"Unattended" means: you did not place, cancel, or edit an order by hand; you did not restart the
bot to make a decision for it; you did not fix a signal by editing a file mid-run. Restarting after
a crash is fine and expected - log it. Editing a position because the bot "got it wrong" is a
manual intervention, and it converts the run into a different (undisclosed) strategy. Log it as a
killed variant and start a fresh window for the policy claim.

## If it fails

- **Fewer than 7 logs**: schedule the job and let it run; there is no shortcut, and 7 was chosen as the minimum that catches weekday/weekend and timezone bugs.
- **Dashboard hand-edited**: regenerate it from the JSON logs with a script; a dashboard that can drift from the logs is worse than no dashboard.
- **Silent duplicate orders**: add the idempotency guard, then test it by running the bot twice in a row - the second run must produce zero orders.
- **Stale-data trading**: add the freshness guard before the next run; trading on a stale signal is the operational equivalent of a look-ahead bug.
