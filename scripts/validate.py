#!/usr/bin/env python3
"""Validate AdGuard-style blocklist files in lists/."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LISTS_DIR = ROOT / "lists"
SOURCE_LISTS = ("ads.txt", "tracking.txt", "malware.txt")
ALL_LIST = "all.txt"

# AdGuard network rule for a domain: ||example.com^
RULE_RE = re.compile(r"^\|\|([a-z0-9.-]+)\^$", re.IGNORECASE)
COMMENT_OR_EMPTY = re.compile(r"^\s*(?:!.*)?$")


def iter_rules(path: Path) -> list[tuple[int, str]]:
    rules: list[tuple[int, str]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if COMMENT_OR_EMPTY.match(line):
            continue
        if not RULE_RE.match(line):
            raise SystemExit(f"{path.relative_to(ROOT)}:{lineno}: invalid rule: {raw!r}")
        rules.append((lineno, line.lower()))
    return rules


def check_file(path: Path) -> list[str]:
    rules = iter_rules(path)
    if not rules:
        raise SystemExit(f"{path.relative_to(ROOT)}: no rules found")

    seen: dict[str, int] = {}
    dupes: list[str] = []
    for lineno, rule in rules:
        if rule in seen:
            dupes.append(
                f"{path.relative_to(ROOT)}:{lineno}: duplicate of line {seen[rule]}: {rule}"
            )
        else:
            seen[rule] = lineno
    return dupes


def main() -> int:
    errors: list[str] = []
    source_rules: dict[str, str] = {}

    for name in SOURCE_LISTS:
        path = LISTS_DIR / name
        if not path.is_file():
            errors.append(f"missing source list: {name}")
            continue
        errors.extend(check_file(path))
        for _, rule in iter_rules(path):
            if rule in source_rules and source_rules[rule] != name:
                errors.append(
                    f"cross-list duplicate: {rule} in {source_rules[rule]} and {name}"
                )
            else:
                source_rules[rule] = name

    all_path = LISTS_DIR / ALL_LIST
    if not all_path.is_file():
        errors.append(f"missing {ALL_LIST}")
    else:
        errors.extend(check_file(all_path))
        all_rules = {rule for _, rule in iter_rules(all_path)}
        missing = sorted(set(source_rules) - all_rules)
        extra = sorted(all_rules - set(source_rules))
        if missing:
            errors.append(f"{ALL_LIST} missing {len(missing)} rule(s); run scripts/build_all.py")
            errors.extend(f"  missing: {r}" for r in missing[:20])
        if extra:
            errors.append(f"{ALL_LIST} has {len(extra)} unexpected rule(s); run scripts/build_all.py")
            errors.extend(f"  extra: {r}" for r in extra[:20])

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(
        f"OK: {len(SOURCE_LISTS)} source lists, "
        f"{len(source_rules)} unique rules, {ALL_LIST} in sync"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
