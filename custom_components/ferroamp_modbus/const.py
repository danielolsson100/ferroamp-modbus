"""Constants for the Ferroamp Modbus integration."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass

DOMAIN = "ferroamp_modbus"
DEFAULT_HOST = ""
DEFAULT_PORT = 502
DEFAULT_SCAN_INTERVAL = 30
FAST_SCAN_INTERVAL = 5

CONF_SCAN_INTERVAL = "scan_interval"
CONF_MIN_VALUE = "min_value"
CONF_MAX_VALUE = "max_value"

DEFAULT_MIN_VALUE = -12000.0
DEFAULT_MAX_VALUE = 12000.0

# Register types
REG_INPUT = "input"
REG_HOLDING = "holding"

# Data types
DTYPE_UINT16 = "uint16"
DTYPE_INT16 = "int16"
DTYPE_UINT32 = "uint32"
DTYPE_FLOAT32 = "float32"


@dataclass
class SensorDefinition:
    """Describes a Modbus sensor register."""

    key: str
    name: str
    address: int
    input_type: str  # REG_INPUT or REG_HOLDING
    data_type: str   # DTYPE_*
    unit: Optional[str] = None
    device_class: Optional[str] = None
    state_class: Optional[str] = None
    scan_interval: int = DEFAULT_SCAN_INTERVAL
    icon: Optional[str] = None
    as_int: bool = False


@dataclass
class BinarySensorDefinition:
    """Describes a Modbus binary sensor register."""

    key: str
    name: str
    address: int
    input_type: str = REG_INPUT
    scan_interval: int = FAST_SCAN_INTERVAL
    icon: Optional[str] = None


@dataclass
class NumberDefinition:
    """Describes a writable Modbus number entity."""

    key: str
    name: str
    read_address: int   # address of the *System Value* sensor to read state from
    write_address: int  # address to write the float32 value
    apply_address: int  # address to write [1] to apply the change
    unit: str
    device_class: Optional[str] = None
    min_value: float = DEFAULT_MIN_VALUE
    max_value: float = DEFAULT_MAX_VALUE
    step: float = 1.0
    scan_interval: int = FAST_SCAN_INTERVAL
    icon: Optional[str] = None
    as_int: bool = False


# ---------------------------------------------------------------------------
# Sensor register definitions
# ---------------------------------------------------------------------------

SENSOR_DEFINITIONS: list[SensorDefinition] = [
    # --- General / Firmware ---
    SensorDefinition(
        key="modbus_major_version_1",
        name="Modbus Major Version 1",
        address=1004,
        input_type=REG_INPUT,
        data_type=DTYPE_UINT16,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="modbus_major_version_2",
        name="Modbus Major Version 2",
        address=1008,
        input_type=REG_INPUT,
        data_type=DTYPE_UINT16,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    # --- Inverter ---
    SensorDefinition(
        key="inverter_status",
        name="Inverter Status",
        address=2000,
        input_type=REG_INPUT,
        data_type=DTYPE_UINT16,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.ENUM,
        icon="mdi:information-outline",
    ),
    SensorDefinition(
        key="grid_frequency",
        name="Grid Frequency",
        address=2016,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="Hz",
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="grid_voltage_l1",
        name="Grid Voltage L1",
        address=2032,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="V",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="grid_voltage_l2",
        name="Grid Voltage L2",
        address=2036,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="V",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="grid_voltage_l3",
        name="Grid Voltage L3",
        address=2040,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="V",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="energy_to_dc_nanogrid",
        name="Energy To DC-Nanogrid",
        address=2064,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorDefinition(
        key="energy_from_dc_nanogrid",
        name="Energy From DC-Nanogrid",
        address=2068,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorDefinition(
        key="inverter_active_power",
        name="Inverter Active Power",
        address=2100,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kW",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="inverter_reactive_power",
        name="Inverter Reactive Power",
        address=2104,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kvar",
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="inverter_apparent_power",
        name="Inverter Apparent Power",
        address=2108,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kVA",
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="inverter_active_current_l1",
        name="Inverter Active Current L1",
        address=2112,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="inverter_active_current_l2",
        name="Inverter Active Current L2",
        address=2116,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="inverter_active_current_l3",
        name="Inverter Active Current L3",
        address=2120,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="inverter_reactive_current_l1",
        name="Inverter Reactive Current L1",
        address=2124,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="inverter_reactive_current_l2",
        name="Inverter Reactive Current L2",
        address=2128,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="inverter_reactive_current_l3",
        name="Inverter Reactive Current L3",
        address=2132,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="inverter_rms_current_l1",
        name="Inverter RMS Current L1",
        address=2136,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="inverter_rms_current_l2",
        name="Inverter RMS Current L2",
        address=2140,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="inverter_rms_current_l3",
        name="Inverter RMS Current L3",
        address=2144,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    # --- Grid / Facility ---
    SensorDefinition(
        key="energy_exported_to_grid",
        name="Energy Exported To Grid",
        address=3064,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        as_int=True,
    ),
    SensorDefinition(
        key="energy_imported_from_grid",
        name="Energy Imported From Grid",
        address=3068,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        as_int=True,
    ),
    SensorDefinition(
        key="grid_active_power",
        name="Grid Active Power",
        address=3100,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kW",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="grid_reactive_power",
        name="Grid Reactive Power",
        address=3104,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kVAr",
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="grid_apparent_power",
        name="Grid Apparent Power",
        address=3108,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kVA",
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="grid_active_current_l1",
        name="Grid Active Current L1",
        address=3112,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="grid_active_current_l2",
        name="Grid Active Current L2",
        address=3116,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="grid_active_current_l3",
        name="Grid Active Current L3",
        address=3120,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="grid_reactive_current_l1",
        name="Grid Reactive Current L1",
        address=3124,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="grid_reactive_current_l2",
        name="Grid Reactive Current L2",
        address=3128,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="grid_reactive_current_l3",
        name="Grid Reactive Current L3",
        address=3132,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="grid_rms_current_l1",
        name="Grid RMS Current L1",
        address=3136,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="grid_rms_current_l2",
        name="Grid RMS Current L2",
        address=3140,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="grid_rms_current_l3",
        name="Grid RMS Current L3",
        address=3144,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="A",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    # --- PV / Solar ---
    SensorDefinition(
        key="num_idle_ssos",
        name="Number Of Idle SSOs",
        address=5000,
        input_type=REG_INPUT,
        data_type=DTYPE_UINT16,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-panel",
    ),
    SensorDefinition(
        key="num_running_ssos",
        name="Number Of Running SSOs",
        address=5002,
        input_type=REG_INPUT,
        data_type=DTYPE_UINT16,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-panel",
    ),
    SensorDefinition(
        key="num_faulty_ssos",
        name="Number Of Faulty SSOs",
        address=5004,
        input_type=REG_INPUT,
        data_type=DTYPE_UINT16,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-panel-large",
    ),
    SensorDefinition(
        key="energy_produced",
        name="Energy Produced",
        address=5064,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorDefinition(
        key="solar_power",
        name="Solar Power",
        address=5100,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kW",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    # --- Battery Control (Holding Registers) ---
    SensorDefinition(
        key="battery_mode",
        name="Battery Mode",
        address=6000,
        input_type=REG_HOLDING,
        data_type=DTYPE_UINT16,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-clock",
    ),
    SensorDefinition(
        key="battery_power_reference",
        name="Battery Power Reference",
        address=6064,
        input_type=REG_HOLDING,
        data_type=DTYPE_FLOAT32,
        unit="kW",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    # --- Battery Data (Input Registers) ---
    SensorDefinition(
        key="num_idle_batteries",
        name="Number Of Idle Batteries",
        address=6000,
        input_type=REG_INPUT,
        data_type=DTYPE_UINT16,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-off-outline",
    ),
    SensorDefinition(
        key="num_running_batteries",
        name="Number Of Running Batteries",
        address=6002,
        input_type=REG_INPUT,
        data_type=DTYPE_UINT16,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-charging",
    ),
    SensorDefinition(
        key="num_faulty_batteries",
        name="Number Of Faulty Batteries",
        address=6004,
        input_type=REG_INPUT,
        data_type=DTYPE_UINT16,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-alert",
    ),
    SensorDefinition(
        key="rated_capacity",
        name="Rated Capacity",
        address=6008,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kWh",
        device_class=SensorDeviceClass.ENERGY_STORAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="state_of_health",
        name="State Of Health",
        address=6012,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="%",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-heart",
    ),
    SensorDefinition(
        key="state_of_charge",
        name="State Of Charge",
        address=6016,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="%",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="energy_from_battery",
        name="Energy From Battery",
        address=6064,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorDefinition(
        key="energy_to_battery",
        name="Energy To Battery",
        address=6068,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorDefinition(
        key="battery_power",
        name="Battery Power",
        address=6100,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kW",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorDefinition(
        key="battery_mode_system_value",
        name="Battery Mode System Value",
        address=6104,
        input_type=REG_INPUT,
        data_type=DTYPE_UINT16,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-clock-outline",
    ),
    SensorDefinition(
        key="battery_power_reference_system_value",
        name="Battery Power Reference System Value",
        address=6106,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="kW",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    # --- Grid Limits (fast poll, 5s) ---
    SensorDefinition(
        key="import_threshold_system_value",
        name="Import Threshold System Value",
        address=8002,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="W",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        scan_interval=FAST_SCAN_INTERVAL,
    ),
    SensorDefinition(
        key="export_threshold_system_value",
        name="Export Threshold System Value",
        address=8012,
        input_type=REG_INPUT,
        data_type=DTYPE_FLOAT32,
        unit="W",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        scan_interval=FAST_SCAN_INTERVAL,
    ),
]

# ---------------------------------------------------------------------------
# Binary sensor register definitions
# ---------------------------------------------------------------------------

BINARY_SENSOR_DEFINITIONS: list[BinarySensorDefinition] = [
    BinarySensorDefinition(
        key="limit_import_active",
        name="Limit Import System Value",
        address=8000,
        input_type=REG_INPUT,
        scan_interval=FAST_SCAN_INTERVAL,
        icon="mdi:transmission-tower-import",
    ),
    BinarySensorDefinition(
        key="limit_export_active",
        name="Limit Export System Value",
        address=8010,
        input_type=REG_INPUT,
        scan_interval=FAST_SCAN_INTERVAL,
        icon="mdi:transmission-tower-export",
    ),
]

# ---------------------------------------------------------------------------
# Number (writable) entity definitions
# ---------------------------------------------------------------------------

NUMBER_DEFINITIONS: list[NumberDefinition] = [
    NumberDefinition(
        key="import_threshold",
        name="Import Threshold",
        read_address=8002,   # sensor.fmb_import_threshold_system_value
        write_address=8002,  # write float32 word-swapped
        apply_address=8006,  # write [1] to apply
        unit="W",
        device_class=SensorDeviceClass.POWER,
        min_value=-12000.0,
        max_value=12000.0,
        step=1.0,
        scan_interval=FAST_SCAN_INTERVAL,
        icon="mdi:transmission-tower-import",
        as_int=True,
    ),
    NumberDefinition(
        key="export_threshold",
        name="Export Threshold",
        read_address=8012,   # sensor.fmb_export_threshold_system_value
        write_address=8012,  # write float32 word-swapped
        apply_address=8016,  # write [1] to apply
        unit="W",
        device_class=SensorDeviceClass.POWER,
        min_value=-12000.0,
        max_value=12000.0,
        step=1.0,
        scan_interval=FAST_SCAN_INTERVAL,
        icon="mdi:transmission-tower-export",
        as_int=True,
    ),
]

# Convenience lookup by key
SENSOR_DEFINITIONS_BY_KEY: dict[str, SensorDefinition] = {
    s.key: s for s in SENSOR_DEFINITIONS
}
BINARY_SENSOR_DEFINITIONS_BY_KEY: dict[str, BinarySensorDefinition] = {
    b.key: b for b in BINARY_SENSOR_DEFINITIONS
}
NUMBER_DEFINITIONS_BY_KEY: dict[str, NumberDefinition] = {
    n.key: n for n in NUMBER_DEFINITIONS
}
