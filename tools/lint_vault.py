#!/usr/bin/env python3
"""
Vault schema linter for the memory system.

The vault (the folder that contains this tools/ dir -- OBSIDIAN -- by default) hosts both the
operating/working files and the durable notes. This linter checks ONLY the durable-note subtree:
`Notes/`, `Inbox/`, `Archive/`, and the two root hub files. Operating files that share the vault
(CHARLIE.md, the pinned set, the daily folders, tools/, etc.) are not durable notes and are
skipped. Enforces the schema defined in CHARLIE.md.

Stock Python 3 standard library only -- no pip installs (policy: enforcement tooling depends
only on a stock dev install, so it survives tooling changes).

Do not invoke this file directly in normal use. Use tools/lint.sh -- the only sanctioned form.

Output: one violation per line, `FILE :: RULE :: DETAIL`, then a summary block.
Exit code: 0 = clean, 1 = one or more violations.
"""

import sys
import re
from pathlib import Path
from datetime import datetime

# --- schema constants ------------------------------------------------------

FOLDER_TYPE = {
    "People": "person",
    "Systems": "system",
    "Projects": "project",
    "Decisions": "decision",
    "Playbooks": "playbook",
    "Concepts": "concept",
    "Meetings": "meeting",
    "Retro": "retro",
}
VALID_TYPES = set(FOLDER_TYPE.values())
VALID_STATUS = {"active", "superseded", "archived"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

SKIP_DIRS = {".obsidian", ".trash", ".git"}

# The durable-note subtree -- the only thing schema-checked. Everything else in the vault
# (operating docs, the pinned set, daily folders, tools/) is working material, not a note.
NOTE_DIRS = {"Notes", "Inbox", "Archive"}
HUB_FILES = {"Meta-Cognition.md", "Retrieval Strategies.md"}


# --- frontmatter parsing ---------------------------------------------------

def parse_frontmatter(text):
    """Return (fields_dict, error_or_None). Flat `key: value` YAML only."""
    lines = [ln.rstrip("\r") for ln in text.split("\n")]
    if not lines or lines[0].strip() != "---":
        return None, "no opening '---' frontmatter fence"
    close = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close = i
            break
    if close is None:
        return None, "frontmatter fence not closed"
    fields = {}
    for ln in lines[1:close]:
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        if ":" not in ln:
            continue
        key, val = ln.split(":", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'").strip()
        fields[key] = val
    return fields, None


def normalize_stem(name):
    """Lowercase, alphanumeric-only stem -- collapses case/space/punctuation variants."""
    return re.sub(r"[^a-z0-9]", "", name.lower())


# --- linter ----------------------------------------------------------------

def lint(vault):
    vault = vault.resolve()
    violations = []
    by_type = {}
    by_status = {}
    inbox_depth = 0
    note_count = 0
    stem_map = {}  # normalized stem -> [relpaths]

    def add(rel, rule, detail):
        violations.append(f"{rel} :: {rule} :: {detail}")

    md_files = []
    for p in sorted(vault.rglob("*.md")):
        rel = p.relative_to(vault)
        parts = rel.parts
        if any(part in SKIP_DIRS for part in parts):
            continue
        in_note_dir = len(parts) > 1 and parts[0] in NOTE_DIRS
        is_hub = len(parts) == 1 and p.name in HUB_FILES
        if not (in_note_dir or is_hub):
            continue  # operating/working file sharing the vault -- not a durable note
        md_files.append(p)

    for p in md_files:
        rel = p.relative_to(vault)
        relstr = rel.as_posix()
        parts = rel.parts
        note_count += 1

        # track for near-duplicate detection
        stem_map.setdefault(normalize_stem(p.stem), []).append(relstr)

        # location category
        top = parts[0] if len(parts) > 1 else None
        is_root = len(parts) == 1
        is_inbox = top == "Inbox"
        is_archive = top == "Archive"
        is_notes = top == "Notes"
        if is_inbox:
            inbox_depth += 1

        # frontmatter
        try:
            text = p.read_text(encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            add(relstr, "READ", f"could not read file: {e}")
            continue
        fm, err = parse_frontmatter(text)
        if err:
            add(relstr, "FRONTMATTER", err)
            continue

        ntype = fm.get("type")
        created = fm.get("created")
        status = fm.get("status")
        superseded_by = fm.get("superseded_by")

        # type
        if not ntype:
            add(relstr, "TYPE", "missing 'type'")
        elif ntype not in VALID_TYPES:
            add(relstr, "TYPE", f"invalid type '{ntype}' (allowed: {sorted(VALID_TYPES)})")
        else:
            by_type[ntype] = by_type.get(ntype, 0) + 1

        # created
        if not created:
            add(relstr, "CREATED", "missing 'created'")
        elif not DATE_RE.match(created):
            add(relstr, "CREATED", f"'{created}' is not YYYY-MM-DD")
        else:
            try:
                datetime.strptime(created, "%Y-%m-%d")
            except ValueError:
                add(relstr, "CREATED", f"'{created}' is not a real calendar date")

        # status
        if not status:
            add(relstr, "STATUS", "missing 'status'")
        elif status not in VALID_STATUS:
            add(relstr, "STATUS", f"invalid status '{status}' (allowed: {sorted(VALID_STATUS)})")
        else:
            by_status[status] = by_status.get(status, 0) + 1

        # folder <-> type law (Notes/<Sub>/ only; root, Inbox, Archive exempt)
        if is_notes:
            if len(parts) < 3:
                add(relstr, "FOLDER_TYPE", "file sits directly in Notes/ (must be in a typed subfolder)")
            else:
                sub = parts[1]
                expected = FOLDER_TYPE.get(sub)
                if expected is None:
                    add(relstr, "FOLDER_TYPE", f"unknown Notes subfolder '{sub}'")
                elif ntype and ntype in VALID_TYPES and ntype != expected:
                    add(relstr, "FOLDER_TYPE", f"type '{ntype}' but folder '{sub}' expects '{expected}'")

        # archive requires status archived
        if is_archive and status and status != "archived":
            add(relstr, "ARCHIVE_STATUS", f"in Archive/ but status is '{status}' (must be 'archived')")

        # supersession (required iff status == superseded)
        if status == "superseded":
            if not superseded_by:
                add(relstr, "SUPERSEDED", "status 'superseded' but no 'superseded_by'")
            else:
                target = (vault / superseded_by).resolve()
                if not target.exists() or not target.is_file():
                    add(relstr, "SUPERSEDED_BY", f"superseded_by '{superseded_by}' does not resolve to a file")
        elif superseded_by:
            add(relstr, "SUPERSEDED_BY", f"superseded_by present but status is '{status}' (must be 'superseded')")

    # near-duplicate filenames (canonical-note-first heuristic)
    for stem, paths in sorted(stem_map.items()):
        if len(paths) > 1:
            for pth in paths:
                others = [x for x in paths if x != pth]
                add(pth, "NEAR_DUPLICATE", f"filename collides with: {', '.join(others)}")

    return violations, {
        "notes": note_count,
        "by_type": by_type,
        "by_status": by_status,
        "inbox_depth": inbox_depth,
    }


def main():
    here = Path(__file__).resolve().parent          # tools/ (lives inside the vault)
    vault_default = here.parent                      # the vault root (OBSIDIAN)
    vault = Path(sys.argv[1]) if len(sys.argv) > 1 else vault_default

    if not vault.exists():
        print(f"VAULT NOT FOUND :: {vault}", file=sys.stderr)
        return 2

    violations, summary = lint(vault)

    for v in violations:
        print(v)

    bt = " ".join(f"{k}={summary['by_type'][k]}" for k in sorted(summary["by_type"])) or "(none)"
    bs = " ".join(f"{k}={summary['by_status'][k]}" for k in sorted(summary["by_status"])) or "(none)"
    print("-- summary --")
    print(f"vault: {vault}")
    print(f"notes: {summary['notes']}")
    print(f"by type: {bt}")
    print(f"by status: {bs}")
    print(f"inbox depth: {summary['inbox_depth']}")
    print(f"violations: {len(violations)}")

    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
