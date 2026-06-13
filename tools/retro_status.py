#!/usr/bin/env python3
"""
Retro staleness helper. Reports days since the newest retro note in KB/Notes/Retro/.
Drives the warmup staleness ratchet (CHARLIE.md section 7.2) and the advisory Stop hook.

Stock Python 3 standard library only.

Modes:
  python3 tools/retro_status.py          -> human + machine-readable status on stdout, exit 0
  python3 tools/retro_status.py --hook   -> advisory reminder on stderr if overdue, exit 0

A retro is "overdue" when more than 1 day has passed since the newest retro note.
"""

import sys
import re
from pathlib import Path
from datetime import date, datetime

THRESHOLD_DAYS = 1
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def newest_retro(retro_dir):
    """Return (date, path) of the newest retro note, or (None, None)."""
    best = None
    best_path = None
    if not retro_dir.exists():
        return None, None
    for p in retro_dir.glob("*.md"):
        m = DATE_RE.search(p.name)
        if m:
            try:
                d = datetime.strptime(m.group(1), "%Y-%m-%d").date()
            except ValueError:
                d = date.fromtimestamp(p.stat().st_mtime)
        else:
            d = date.fromtimestamp(p.stat().st_mtime)
        if best is None or d > best:
            best, best_path = d, p
    return best, best_path


def main():
    here = Path(__file__).resolve().parent   # tools/ (inside the vault)
    vault = here.parent                       # the vault root (OBSIDIAN)
    retro_dir = vault / "Notes" / "Retro"

    d, path = newest_retro(retro_dir)
    today = date.today()
    hook = "--hook" in sys.argv[1:]

    if d is None:
        if hook:
            print("[memory] No retro notes found yet -- run a retro to set the baseline.",
                  file=sys.stderr)
            return 0
        print("days_since_retro=NONE")
        print("No retro notes found. Run a retro to establish the baseline.")
        return 0

    days = (today - d).days
    overdue = days > THRESHOLD_DAYS

    if hook:
        if overdue:
            print(f"[memory] Retro is {days} days overdue (newest: {path.name}). "
                  f"Consider running a retro before ending. Say 'retro'.", file=sys.stderr)
        return 0

    print(f"days_since_retro={days}")
    print(f"newest_retro={path.name}")
    print(f"overdue={'yes' if overdue else 'no'} (threshold {THRESHOLD_DAYS} day)")
    if overdue:
        print(f"Retro is {days} days overdue -- run it now before new work "
              f"(say 'defer' to override).")
    else:
        print("Retro is current.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
