# Changelog

Alle wesentlichen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.
Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).
Versionierung folgt [Semantic Versioning](https://semver.org/).

## [1.7.1] – 2026-05-23

### Hinzugefügt
- GitHub Action für HACS-Validierung (validate.yaml)
- GitHub Action für hassfest-Validierung (hassfest.yaml)
- GitHub Action für automatische Release-Erstellung aus CHANGELOG.md (release.yaml)
- Script `add_changelog_entry.py` für strukturiertes Hinzufügen von Changelog-Einträgen
- Brand-Icons für HACS-UI (`brand/icon.png`, `logo.png` inkl. @2x-Varianten)
- CHANGELOG.md als eigenständige Datei im Keep-a-Changelog-Format

### Geändert
- Release-Prompt verwendet jetzt `add_changelog_entry.py` statt manuellem Editieren
- README verweist auf CHANGELOG.md statt eigenen Changelog-Abschnitt
- `codeowners` in manifest.json mit korrektem `@`-Präfix
- `hacs.json` bereinigt (Name, unnötige Felder entfernt)

## [1.7.0] – 2026-05-22

### Hinzugefügt
- Konfigurierbare maximale Eingangsleistung pro Kanal (Standard: 500 W) – einstellbar über **Einstellungen → Geräte & Dienste → Konfigurieren**
- Sensor `Maximalleistung` pro Eingang (MI 0–3) – zeigt den konfigurierten Maximalwert in Watt, nutzbar für Automationen und Dashboards
- Sensor `Leistung in Prozent` pro Eingang (MI 0–3) – zeigt die aktuelle Auslastung als Prozentwert der konfigurierten Maximalleistung

## [1.6.0] – 2026-05-22

### Hinzugefügt
- `Energie Heute` pro Eingang (MI 0–3) – zeigt die seit Mitternacht erzeugte Energie je Kanal in kWh, automatischer Reset um Mitternacht

### Geändert
- Channel-Sensoren in saubere Klassenhierarchie aufgeteilt (`EnvertechChannelSensor`, `EnvertechChannelPeakSensor`, `EnvertechChannelDailySensor`) statt Bool-Flags – keine Breaking Changes bei bestehenden Entities

## [1.5.0] – 2026-05-22

### Hinzugefügt
- `Spitzenleistung Heute` pro Eingang (MI 0–3) – höchste AC-Leistung des aktuellen Tages, automatischer Reset um Mitternacht
- `Gesamtspitzenleistung Heute` – höchste Gesamt-AC-Leistung des aktuellen Tages, automatischer Reset um Mitternacht
- Peak-Sensoren überleben HA-Neustarts dank `RestoreSensor` und setzen sich täglich automatisch zurück
- Peak-Logik direkt in die `EnvertechChannelSensorDescription` integriert

## [1.4.0] – 2026-05-08

### Hinzugefügt
- `Energie Heute` und `Ertrag Heute` werden automatisch von der Integration als native Sensoren angelegt (kein manueller Utility-Meter-Helfer mehr nötig)
- Tages-Sensoren setzen sich täglich um Mitternacht automatisch zurück und überleben HA-Neustarts dank `RestoreSensor`

## [1.3.0] – 2026-05-08

### Hinzugefügt
- Vollständig überarbeitetes Live-Dashboard mit animiertem Energiefluss, Tagesertrag-Graph (akkumuliert ab 00:00), 7-Tage-Balkendiagramm, 24h-Leistungsgraph aller 4 Eingänge
- Anleitung für Utility-Meter-Helper (heutige kWh) und Today's-Earnings-Template-Sensor

## [1.2.0] – 2026-05-08

### Hinzugefügt
- Mitgeliefertes Lovelace-Dashboard (`lovelace/dashboard.yaml`) mit Gauge, Verlaufsgraphen, MI-Detailkarten und Ertragssensor

## [1.1.0] – 2026-05-08

### Hinzugefügt
- Ertragssensor (EUR) – berechnet den finanziellen Ertrag auf Basis der Gesamtenergie und einem konfigurierbaren Preis pro kWh
- Options Flow – Preis pro kWh jederzeit über **Einstellungen → Geräte & Dienste → Konfigurieren** anpassbar (Standard: 0,30 €/kWh)
- Sensor-Typ `monetary` mit `total_increasing` für korrekte HA-Integration

## [1.0.0] – 2026-05-08

### Hinzugefügt
- Erstveröffentlichung
- Live-Daten aller 4 Mikroinverter-Kanäle (DC-Spannung, AC-Leistung, Energie, Temperatur, AC-Spannung, Frequenz)
- Gesamtleistung und Gesamtenergie als eigene Sensoren
- Leistungsbegrenzung lesen und setzen (600 W–2000 W)
- Persistente TCP-Verbindung für maximale Zuverlässigkeit
- Retry-Strategie gemäß Protokollspezifikation (Live: 3×, Power Limit: 5× mit dedizierter Verbindung)
- Config Flow mit Verbindungstest
- Übersetzungen Deutsch und Englisch
- HACS-kompatibel
