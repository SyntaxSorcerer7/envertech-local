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

### 3. Changelog, Manifest, Commit und Tag erstellen

- Leite die Changelog-Einträge aus den tatsächlichen Änderungen ab (Schritt 1). Schreibe auf Deutsch.
- Formuliere eine prägnante deutsche Commit-Message im Format:
  ```
  Release v<VERSION>: <Kurzbeschreibung>

  - <Detailpunkt 1>
  - <Detailpunkt 2>
  - ...
  ```
- Zeige dem Benutzer die geplante Commit-Message und den Changelog-Inhalt zur Bestätigung – warte auf Freigabe bevor du weitermachst.
- Rufe dann das Script auf (in einem einzigen Befehl):

```bash
python3 .github/scripts/prepare_release.py \
    --version <VERSION> \
    --date <DATUM im Format YYYY-MM-DD> \
    --added "Feature A" "Feature B" \
    --changed "Änderung C" \
    --fixed "Bugfix D" \
    --commit-message "Release v<VERSION>: <Kurzbeschreibung>

- <Detailpunkt 1>
- <Detailpunkt 2>"
```

- Lasse `--added`, `--changed` oder `--fixed` weg, wenn es dazu keine Einträge gibt.
- Das Script aktualisiert automatisch: `CHANGELOG.md`, `manifest.json`, erstellt den Commit und setzt den annotierten Git-Tag.

### 4. Zusammenfassung

Zeige dem Benutzer eine Zusammenfassung:
- Neue Version
- Changelog-Eintrag
- Commit-Message
- Git-Tag
- Hinweis: Die GitHub Action erstellt nun automatisch das GitHub Release.

## Wichtige Regeln

- Das Script übernimmt alle Dateiänderungen (nur `CHANGELOG.md` und `manifest.json`) sowie Commit, Tag und Push – **keine manuellen Schritte** danach nötig.
- Führe **kein** `git push` aus – das erledigt `prepare_release.py` automatisch.
- Schreibe Changelog-Einträge und Commit-Messages auf **Deutsch**.
- Frage bei Unklarheiten **immer** nach, statt zu raten.
