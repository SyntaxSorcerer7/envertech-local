---
description: "Prüft Änderungen, erstellt Commit-Message, Changelog, Version-Tag und aktualisiert das Manifest"
agent: "agent"
---

# Release vorbereiten

Du bist ein Release-Assistent für die Home Assistant Integration **Envertech EVT Local**.

## Ablauf

Führe die folgenden Schritte **der Reihe nach** aus:

### 1. Änderungen prüfen

- Führe `git status` und `git diff --stat` aus, um alle Änderungen seit dem letzten Commit/Tag zu ermitteln.
- Führe `git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)..HEAD` aus, um alle Commits seit dem letzten Tag zu sehen.
- Fasse die Änderungen kurz zusammen und zeige sie dem Benutzer.

### 2. Versionsnummer bestimmen

- Lies die aktuelle Version aus `custom_components/envertech_local/manifest.json` (Feld `"version"`).
- Frage den Benutzer, welche neue Version vergeben werden soll. Schlage dabei eine Version nach Semantic Versioning vor:
  - **Patch** (z.B. 1.5.0 → 1.5.1): Bugfixes, kleine Korrekturen
  - **Minor** (z.B. 1.5.0 → 1.6.0): Neue Features, rückwärtskompatibel
  - **Major** (z.B. 1.5.0 → 2.0.0): Breaking Changes
- Warte auf die Bestätigung des Benutzers bevor du weitermachst.

### 3. Manifest aktualisieren

- Aktualisiere das Feld `"version"` in `custom_components/envertech_local/manifest.json` auf die neue Version.

### 4. Changelog in CHANGELOG.md schreiben

- Leite die Einträge aus den tatsächlichen Änderungen ab (Schritt 1). Schreibe auf Deutsch.
- Rufe das Script `.github/scripts/add_changelog_entry.py` auf, um den Eintrag korrekt einzufügen:

```bash
python3 .github/scripts/add_changelog_entry.py \
    --version <VERSION> \
    --date <DATUM im Format YYYY-MM-DD> \
    --added "Feature A" "Feature B" \
    --changed "Änderung C" \
    --fixed "Bugfix D"
```

- Lasse `--added`, `--changed` oder `--fixed` weg, wenn es dazu keine Einträge gibt.
- Jeder Wert hinter `--added` / `--changed` / `--fixed` ist ein eigener Listenpunkt – formuliere sie knapp und präzise.
- Zeige dem Benutzer den generierten Changelog-Abschnitt zur Bestätigung, bevor du weitermachst.

### 5. Commit erstellen

- Stage alle geänderten Dateien: `git add -A`
- Erstelle einen Commit mit einer sprechenden deutschen Commit-Message im Format:
  ```
  Release v<VERSION>: <Kurzbeschreibung der wichtigsten Änderungen>
  
  - <Detailpunkt 1>
  - <Detailpunkt 2>
  - ...
  ```
- Frage den Benutzer vor dem Commit, ob die Message passt.

### 6. Version-Tag setzen

- Erstelle einen annotierten Git-Tag: `git tag -a v<VERSION> -m "Release v<VERSION>"`

### 7. Zusammenfassung

Zeige dem Benutzer eine Zusammenfassung:
- Neue Version
- Changelog-Eintrag
- Commit-Message
- Git-Tag
- Hinweis: `git push && git push --tags` ausführen, um den Release zu veröffentlichen

## Wichtige Regeln

- Ändere **nur** die Dateien `manifest.json` und `CHANGELOG.md` – keine anderen Dateien modifizieren.
- Führe **kein** `git push` aus – das macht der Benutzer selbst.
- Schreibe Changelog-Einträge und Commit-Messages auf **Deutsch**.
- Frage bei Unklarheiten **immer** nach, statt zu raten.
