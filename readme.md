**English** | [Deutsch](README.de.md)

# Envertech EVT Local – Home Assistant Integration

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1+-blue.svg)](https://www.home-assistant.io/)
[![Release downloads](https://img.shields.io/github/downloads/SyntaxSorcerer7/envertech-local/total?label=release%20downloads)](https://github.com/SyntaxSorcerer7/envertech-local/releases)

A local Home Assistant integration for **Envertech EVT2000SE** microinverters, connecting directly over the local TCP protocol without the cloud.

💡 [Suggest a feature](https://github.com/SyntaxSorcerer7/envertech-local/issues/new?template=feature_request.yml)
· [View feature requests](https://github.com/SyntaxSorcerer7/envertech-local/issues?q=is%3Aissue%20is%3Aopen%20label%3Aenhancement)
· [Report a bug](https://github.com/SyntaxSorcerer7/envertech-local/issues/new?template=bug_report.yml)

You need a GitHub account to create an issue. You can also support existing requests with 👍 or add your use case.

---

## Features

- **Fully local** – no cloud dependency or internet connection required
- **Live data** for all 4 microinverter channels (MI 0–3):
  - DC voltage (V)
  - AC power (W)
  - Total energy (kWh)
  - Temperature (°C)
  - AC voltage (V)
  - Frequency (Hz)
- **Aggregate values** across all channels (total power and energy)
- Set a **power limit** (600W–2000W in fixed steps)
- Read the **firmware version**
- **Persistent TCP connection** for maximum reliability
- **Config flow** – setup through the Home Assistant interface
- **Translations** – German and English

---

## Requirements

- Home Assistant 2024.1.0 or newer
- [HACS](https://hacs.xyz/) installed
- An Envertech EVT2000SE inverter on the local network
- The inverter's IP address and serial number

### Finding the serial number

The serial number is on the inverter's nameplate and must be **entered exactly as printed** (e.g. `3011156`).

You can also find it in the EnverView app or the Envertech portal.

---

## Installation

### Via HACS (recommended)

1. Open **HACS** → **Integrations** → menu (⋮) → **Custom repositories**
2. Enter the repository URL: `https://github.com/SyntaxSorcerer7/envertech-local`
3. Select the **Integration** category
4. Select **Add**, search for **Envertech EVT Local**, and select **Download**
5. **Restart** Home Assistant

### Manual

1. Copy the `custom_components/envertech_local/` folder into your Home Assistant `config/custom_components/` directory
2. **Restart** Home Assistant

---

## Configuration

### Via the UI (config flow)

1. Go to **Settings** → **Devices & services** → **Add integration**
2. Search for **Envertech EVT Local**
3. Enter the inverter's IP address
4. Enter the serial number exactly as printed on the nameplate
5. The integration automatically tests the connection

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| IP address | Local IP address of the inverter | `192.168.1.100` |
| Serial number | Serial number on the nameplate | `3011156` |

> **Tip:** Assign the inverter a fixed IP address in your router (DHCP reservation) so its address does not change.

---

## Entities

### Per microinverter channel (MI 0–3)

The integration creates **4 devices** (MI 0 to MI 3), each with:

| Sensor | Unit | Device class | Description |
|--------|------|--------------|-------------|
| DC voltage | V | `voltage` | Solar panel input voltage |
| AC power | W | `power` | Current power fed into the grid |
| Total energy | kWh | `energy` | Cumulative energy production |
| Temperature | °C | `temperature` | Internal MI temperature |
| AC voltage | V | `voltage` | Grid voltage |
| Frequency | Hz | `frequency` | Grid frequency |
| **Peak power today** | W | `power` | Highest AC power today, reset at midnight |

### Aggregate device

| Sensor | Unit | Description |
|--------|------|-------------|
| Total AC power | W | Sum of all 4 MI channels |
| Total energy | kWh | Sum of all 4 MI channels |
| **Total peak power today** | W | Highest total AC power today, reset at midnight |
| Firmware version | – | e.g. "164.125" (disabled by default) |

### Control

| Entity | Type | Description |
|--------|------|-------------|
| Power limit | `select` | Select a power level (600W–2000W) |

### Available power levels (EVT2000SE)

| Level |
|-------|
| 600W |
| 800W |
| 1200W |
| 1400W |
| 1440W |
| 1600W |
| 1640W |
| 1800W |
| 2000W |

---

## Dashboard

The integration includes a ready-made Lovelace dashboard at [`lovelace/dashboard.yaml`](lovelace/dashboard.yaml).

### Included cards

| Card | Description |
|------|-------------|
| **Energy flow** | Animated flow from each input through the inverter to the grid (Power Flow Card Plus) |
| **Live inputs** | Four-column grid showing current power per input (Mushroom Cards) |
| **Gauge** | Total power with color thresholds (0–2000W) |
| **Today / total** | Today's kWh, today's yield (€), total yield (€) |
| **24-hour power graph** | Power over the last 24 hours for all 4 inputs and the total (ApexCharts) |
| **Cumulative daily yield** | kWh accumulated from midnight to now, automatically reset daily (ApexCharts) |
| **7-day bar chart** | Daily production for the last 7 days with data labels (ApexCharts) |
| **Detail cards** | All readings per input (voltage, frequency, temperature, energy) |
| **Control** | Set the power limit |

### Required HACS custom cards

Install these once through HACS before using the dashboard:

| Card | HACS search |
|------|-------------|
| ApexCharts Card | `ApexCharts Card` |
| Mushroom | `Mushroom` |
| Power Flow Card Plus | `Power Flow Card Plus` |

### Importing the dashboard

1. In Home Assistant, go to **Settings** → **Dashboards** → **Add dashboard**
2. Enter a name (e.g. `Solar`) and the icon `mdi:solar-power-variant`
3. Open the dashboard → menu (⋮) → **Raw configuration editor**
4. Paste the contents of [`lovelace/dashboard.yaml`](lovelace/dashboard.yaml)
5. **Save**

### One-time setup

**Step 1 – Replace YOUR_SERIAL:**  
Replace every occurrence of `YOUR_SERIAL` with your serial number (lowercase). You can find the exact entity ID under Settings → Devices & services → Envertech → select the entity.

All other sensors (energy today, yield today) are **created automatically by the integration**; no manual helper is required.

---

## Automations & dashboards

### Example: Energy Dashboard

Sensors with `device_class: energy` and `state_class: total_increasing` are automatically compatible with the **Home Assistant Energy Dashboard**. Add the total energy sensor or the individual MI energy sensors there.

### Example: Power limit automation

```yaml
automation:
  - alias: "Limit inverter to 800W when grid consumption is high"
    trigger:
      - platform: numeric_state
        entity_id: sensor.stromzaehler_leistung
        above: 3000
        for:
          minutes: 5
    action:
      - service: select.select_option
        target:
          entity_id: select.envertech_a1b2c3d4_leistungsbegrenzung
        data:
          option: "800W"
```

### Example: Temperature warning

```yaml
automation:
  - alias: "Inverter overtemperature warning"
    trigger:
      - platform: numeric_state
        entity_id: sensor.envertech_input_port_1_temperatur
        above: 70
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Inverter warning"
          message: "MI 0 temperature: {{ states('sensor.envertech_input_port_1_temperatur') }}°C"
```

### Example: Lovelace dashboard card

```yaml
type: entities
title: Envertech EVT2000SE
entities:
  - entity: sensor.envertech_a1b2c3d4_ac_gesamtleistung
    name: Total power
  - entity: sensor.envertech_a1b2c3d4_gesamtenergie
    name: Total energy
  - entity: select.envertech_a1b2c3d4_leistungsbegrenzung
    name: Power limit
  - type: divider
  - entity: sensor.envertech_input_port_1_ac_leistung
    name: MI 0 power
  - entity: sensor.envertech_input_port_2_ac_leistung
    name: MI 1 power
  - entity: sensor.envertech_input_port_3_ac_leistung
    name: MI 2 power
  - entity: sensor.envertech_input_port_4_ac_leistung
    name: MI 3 power
```

The entity IDs above are examples; replace them with the IDs in your installation.

---

## Technical details

### Communication protocol

The integration communicates directly with the inverter over TCP port `14889`. The proprietary protocol was documented by reverse engineering the EnverView app (see [`research/wechselrichter-api.md`](research/wechselrichter-api.md)).

| Property | Value |
|----------|-------|
| Transport | TCP |
| Port | 14889 |
| TX encoding | ASCII-HEX |
| RX encoding | Binary |
| Polling interval | 120 seconds |
| Connection | Persistent (one TCP session) |

### Connection strategy

The integration maintains **one persistent TCP connection** to the inverter. This is necessary because frequent reconnections make the inverter unstable. It responds reliably over an existing connection, even after a long idle period.

### Retries & error handling

| Operation | Max retries | Delay | Timeout |
|-----------|-------------|-------|---------|
| Live Data (0x1077) | 3 | 3s | 3s |
| Power Limit Read (0x1041) | 5 | 5s | 10s |
| TCP Connect | 1 | – | 5s |

### Device architecture

The EVT2000SE contains 4 logical microinverters (MI 0–3) with consecutive UIDs. Each MI has its own solar panel input and provides independent readings. The integration creates a separate Home Assistant device with associated sensors for each MI.

---

## Troubleshooting

### "Cannot connect to inverter"

- Check that the inverter is switched on (is it currently producing power?)
- Check the IP address: `ping 192.168.1.100`
- Check whether port 14889 is reachable: `nc -zv 192.168.1.100 14889`
- Some inverters are only reachable during the day (no standby mode)
- Make sure no other application (e.g. the EnverView app) is connected at the same time

### "No response from inverter"

- The inverter sometimes takes several seconds to respond
- The integration retries automatically
- If problems persist, restart Home Assistant to reset the TCP connection

### Sensors show "Unavailable"

- Inverters often provide no data at night (no power = no network)
- Sensors should become available automatically after sunrise
- Check the Home Assistant logs: **Settings** → **System** → **Logs** → filter for "envertech"

### Incorrect serial number

- Enter the serial number **exactly as it appears on the nameplate**
- Example: if the nameplate shows `3011156`, enter exactly `3011156`

### Power limit does not work

- Reading the current limit is unreliable (~20% success rate)
- **Setting** the limit works reliably
- After setting it, the new value is immediately updated in the integration
- Only the defined levels are available (600, 800, 1200, 1400, 1440, 1600, 1640, 1800, 2000W)

---

## Development

### Project structure

```
custom_components/envertech_local/
├── __init__.py          # Integration setup & entry points
├── config_flow.py       # Configuration flow
├── const.py             # Constants
├── coordinator.py       # Data coordinator (polling)
├── manifest.json        # Integration manifest
├── protocol.py          # TCP protocol implementation
├── select.py            # Power limit select entity
├── sensor.py            # Sensor entities
├── strings.json         # Base UI strings
└── translations/
    ├── de.json           # German translation
    └── en.json           # English translation
```

### Architecture

```
┌─────────────────────────────────────────────┐
│                Home Assistant               │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ sensor.py │  │ select.py│  │config_flow│  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │              │             │        │
│  ┌────▼──────────────▼─────────────▼─────┐  │
│  │         coordinator.py                │  │
│  │    (DataUpdateCoordinator, 120s)      │  │
│  └────────────────┬──────────────────────┘  │
│                   │                         │
│  ┌────────────────▼──────────────────────┐  │
│  │          protocol.py                  │  │
│  │   (EnvertechConnection, TCP, async)   │  │
│  └────────────────┬──────────────────────┘  │
└───────────────────┼─────────────────────────┘
                    │ TCP :14889
          ┌─────────▼──────────┐
          │  EVT2000SE (LAN)   │
          │  MI 0 │ MI 1       │
          │  MI 2 │ MI 3       │
          └────────────────────┘
```

### Protocol reference

The complete protocol documentation is available in [`research/wechselrichter-api.md`](research/wechselrichter-api.md).

---

## Compatibility

| Device | Status |
|--------|--------|
| EVT2000SE | ✅ Fully supported |
| EVT800 | ⚠️ Should work (untested; watt codes may differ) |
| EVT1000 | ⚠️ Should work (untested) |
| EVT400 | ⚠️ Should work (untested; fewer MI channels) |
| Envertech monitor/gateway | ❌ Not supported (different communication flow) |

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the complete changelog.

---

## License

MIT License

---

## Acknowledgments

- Protocol analysis based on the decompiled EnverView app (v4.1.20)
- Live verification against an EVT2000SE (firmware 164.125)
- PCAP captures using PCAPdroid
