#!/usr/bin/env python3
"""
Bereitet einen Release vor: Changelog-Eintrag, Manifest-Version, Commit und Tag.

Verwendung:
    python3 .github/scripts/prepare_release.py \\
        --version 1.8.0 \\
        --date 2026-05-23 \\
        --added "Neues Feature A" "Neues Feature B" \\
        --changed "Änderung C" \\
        --fixed "Bugfix D" \\
        --commit-message "Release v1.8.0: Kurzbeschreibung"

Mit --commit-message werden Manifest, Changelog, Commit und Tag automatisch
erstellt. Ohne --commit-message wird nur Changelog und Manifest aktualisiert.

Jeder --added/--changed/--fixed Wert wird als eigener Listenpunkt eingefügt.
Abschnitte ohne Einträge werden weggelassen.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"
MANIFEST_PATH = REPO_ROOT / "custom_components" / "envertech_local" / "manifest.json"

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


def update_manifest(version: str) -> None:
    """Aktualisiert die Version in manifest.json."""
    if not MANIFEST_PATH.exists():
        print(f"Fehler: {MANIFEST_PATH} nicht gefunden.", file=sys.stderr)
        sys.exit(1)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["version"] = version
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"✓ manifest.json auf Version {version} aktualisiert.")


def git_commit_and_tag(version: str, message: str) -> None:
    """Staged alle Änderungen, erstellt Commit, annotierten Tag und pusht alles."""
    subprocess.run(["git", "add", "-A"], cwd=REPO_ROOT, check=True)
    subprocess.run(["git", "commit", "-m", message], cwd=REPO_ROOT, check=True)
    tag = f"v{version}"
    subprocess.run(["git", "tag", "-a", tag, "-m", f"Release {tag}"], cwd=REPO_ROOT, check=True)
    print(f"✓ Commit erstellt und Tag {tag} gesetzt.")
    subprocess.run(["git", "push"], cwd=REPO_ROOT, check=True)
    subprocess.run(["git", "push", "--tags"], cwd=REPO_ROOT, check=True)
    print(f"✓ Branch und Tags nach origin gepusht.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Release vorbereiten: Changelog, Manifest, Commit und Tag")
    parser.add_argument("--version", required=True, help="Neue Version, z.B. 1.8.0")
    parser.add_argument("--date", default=str(date.today()), help="Datum YYYY-MM-DD (Standard: heute)")
    parser.add_argument("--added", nargs="*", default=[], metavar="TEXT", help="Einträge für 'Hinzugefügt'")
    parser.add_argument("--changed", nargs="*", default=[], metavar="TEXT", help="Einträge für 'Geändert'")
    parser.add_argument("--fixed", nargs="*", default=[], metavar="TEXT", help="Einträge für 'Behoben'")
    parser.add_argument("--commit-message", metavar="MSG", help="Commit-Message. Wenn angegeben, werden Commit und Tag automatisch erstellt.")
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

    # Update manifest
    update_manifest(args.version)

    # Commit + Tag + Push if message provided
    if args.commit_message:
        git_commit_and_tag(args.version, args.commit_message)
        print()
        print(f"✓ Release v{args.version} vollständig abgeschlossen und veröffentlicht.")


if __name__ == "__main__":
    main()
