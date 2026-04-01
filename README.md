# Ferroamp Modbus — Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/danielolsson100/ferroamp-modbus.svg)](https://github.com/danielolsson100/ferroamp-modbus/releases)
[![License](https://img.shields.io/github/license/danielolsson100/ferroamp-modbus.svg)](LICENSE)

A Home Assistant custom integration for the **Ferroamp Energy Hub** using Modbus TCP. Provides real-time monitoring of solar production, battery state, grid power, and control of battery mode and grid import/export limits.

> **Prerequisite:** Modbus TCP must be enabled on your Ferroamp Energy Hub. If it is not, contact [Ferroamp support](https://ferroamp.com/contact/) to have it activated.

---

## Features

- **Sensors** — solar power, battery state of charge, grid power, inverter data, energy totals, and more
- **Binary sensors** — import/export limit active states
- **Number controls** — set grid import and export thresholds (W)
- **Two poll intervals** — fast (5 s) for control registers, standard (30 s) for all others
- **Config flow** — set up entirely from the Home Assistant UI, no YAML required

---

## Installation

### Via HACS (recommended)

1. Open **HACS** in Home Assistant
2. Go to **Integrations** → click the three-dot menu → **Custom repositories**
3. Add `danielolsson100/ferroamp-modbus` with category **Integration**
4. Search for **Ferroamp Modbus** and click **Download**
5. Restart Home Assistant

### Manual

1. Copy the `custom_components/ferroamp_modbus/` folder into your HA `config/custom_components/` directory
2. Restart Home Assistant

---

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Ferroamp Modbus**
3. Enter the **IP address** and **port** (default: `502`) of your Ferroamp Energy Hub
4. Click **Submit**

---

## Entities

### Sensors

| Entity | Unit | Description |
|--------|------|-------------|
| Solar Power | kW | Total DC solar input power |
| Energy Produced | kWh | Lifetime solar energy produced |
| Battery Power | kW | Battery charge (+) / discharge (−) power |
| State of Charge | % | Battery state of charge |
| State of Health | % | Battery state of health |
| Rated Capacity | kWh | Battery rated energy capacity |
| Grid Active Power | kW | Grid import (+) / export (−) power |
| Inverter Active Power | kW | Inverter AC output power |
| Grid Voltage L1/L2/L3 | V | Per-phase grid voltage |
| Grid Frequency | Hz | Grid frequency |
| Energy Imported From Grid | kWh | Lifetime grid import energy |
| Energy Exported To Grid | kWh | Lifetime grid export energy |
| Energy From Battery | kWh | Lifetime energy discharged from battery |
| Energy To Battery | kWh | Lifetime energy charged to battery |
| Battery Mode System Value | — | Active battery operating mode |
| Battery Power Reference | kW | Active battery power setpoint |
| Import Threshold System Value | W | Active grid import limit |
| Export Threshold System Value | W | Active grid export limit |
| Running / Idle / Faulty Batteries | — | Battery unit status counts |
| Running / Idle / Faulty SSOs | — | Solar string optimizer status counts |

### Binary Sensors

| Entity | Description |
|--------|-------------|
| Limit Import Active | Whether a grid import limit is currently enforced |
| Limit Export Active | Whether a grid export limit is currently enforced |

### Number Controls

| Entity | Unit | Range | Description |
|--------|------|-------|-------------|
| Import Threshold | W | −12 000 to 12 000 | Set the grid import power limit |
| Export Threshold | W | −12 000 to 12 000 | Set the grid export power limit |

---

## Requirements

- Home Assistant 2024.1 or newer
- Ferroamp Energy Hub with **Modbus TCP enabled**
- Network access from HA to the Energy Hub on TCP port 502

---

## Contributing

Issues and pull requests are welcome at [github.com/danielolsson100/ferroamp-modbus](https://github.com/danielolsson100/ferroamp-modbus/issues).
