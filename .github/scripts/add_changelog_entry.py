#!/usr/bin/env python3
"""
Fügt einen neuen Eintrag in CHANGELOG.md ein.

Verwendung:
    python3 .github/scripts/add_changelog_entry.py \\
        --version 1.8.0 \\
        --date 2026-05-23 \\
        --added "Neues Feature A" "Neues Feature B" \\
        --changed "Änderung C" \\
        --fixed "Bugfix D"

Jeder --added/--changed/--fixed Wert wird als eigener Listenpunkt eingefügt.
Abschnitte ohne Einträge werden weggelassen.
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

CHANGELOG_PATH = Path(__file__).parents[2] / "CHANGELOG.md"

HEADER_MARKER = "# Changelog"
ENTRY_PATTERN = re.compile(r"^## \[", re.MULTILINE)


def build_entry(version: str, entry_date: str, added: list, changed: list, fixed: list) -> str:
    lines = [f"## [{version}] – {entry_date}", ""]
    for section, items in (("Hinzugefügt", added), ("Geändert", changed), ("Behoben", fixed)):
        if items:
            lines.append(f"### {section}")
            for item in items:
                lines.append(f"- {item}")
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Changelog-Eintrag hinzufügen")
    parser.add_argument("--version", required=True, help="Neue Version, z.B. 1.8.0")
    parser.add_argument("--date", default=str(date.today()), help="Datum YYYY-MM-DD (Standard: heute)")
    parser.add_argument("--added", nargs="*", default=[], metavar="TEXT", help="Einträge für 'Hinzugefügt'")
    parser.add_argument("--changed", nargs="*", default=[], metavar="TEXT", help="Einträge für 'Geändert'")
    parser.add_argument("--fixed", nargs="*", default=[], metavar="TEXT", help="Einträge für 'Behoben'")
    args = parser.parse_args()

    if not any([args.added, args.changed, args.fixed]):
        print("Fehler: Mindestens ein --added, --changed oder --fixed Eintrag erforderlich.", file=sys.stderr)
        sys.exit(1)

    if not CHANGELOG_PATH.exists():
        print(f"Fehler: {CHANGELOG_PATH} nicht gefunden.", file=sys.stderr)
        sys.exit(1)

    content = CHANGELOG_PATH.read_text(encoding="utf-8")

    # Check version not already present
    if f"## [{args.version}]" in content:
        print(f"Fehler: Version [{args.version}] existiert bereits im Changelog.", file=sys.stderr)
        sys.exit(1)

    new_entry = build_entry(args.version, args.date, args.added, args.changed, args.fixed)

    # Insert after the file header block (before the first ## [...] entry)
    match = ENTRY_PATTERN.search(content)
    if match:
        insert_pos = match.start()
        updated = content[:insert_pos] + new_entry + "\n" + content[insert_pos:]
    else:
        # No existing entries yet – append after header
        updated = content.rstrip() + "\n\n" + new_entry

    CHANGELOG_PATH.write_text(updated, encoding="utf-8")
    print(f"✓ Eintrag für [{args.version}] erfolgreich in {CHANGELOG_PATH.name} eingefügt.")
    print()
    print(new_entry)


if __name__ == "__main__":
    main()
