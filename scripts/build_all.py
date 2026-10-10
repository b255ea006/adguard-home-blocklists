#!/usr/bin/env python3
"""Rebuild lists/all.txt from ads + tracking + malware (rules only, single header)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LISTS_DIR = ROOT / "lists"
SOURCES = ("ads.txt", "tracking.txt", "malware.txt")
OUTPUT = LISTS_DIR / "all.txt"

RULE_RE = re.compile(r"^\|\|([a-z0-9.-]+)\^$", re.IGNORECASE)
HEADER = """! Title: b255ea006 - All
! Description: Combined ads + tracking + malware starter lists
! Homepage: https://github.com/b255ea006/adguard-home-blocklists
! Expires: 7 days
!
"""


def rules_from(path: Path) -> list[str]:
    out: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if RULE_RE.match(line):
            out.append(line.lower())
    return out


def main() -> int:
    seen: set[str] = set()
    combined: list[str] = []

    for name in SOURCES:
        path = LISTS_DIR / name
        if not path.is_file():
            print(f"missing {name}", file=sys.stderr)
            return 1
        for rule in rules_from(path):
            if rule not in seen:
                seen.add(rule)
                combined.append(rule)

    OUTPUT.write_text(HEADER + "\n".join(combined) + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(combined)} rules)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
