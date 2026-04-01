"""Sensor platform for Ferroamp Modbus."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    FAST_SCAN_INTERVAL,
    SENSOR_DEFINITIONS,
    SensorDefinition,
)
from .coordinator import FerroampModbusCoordinator, FerroampModbusFastCoordinator
from .entity import FerroampModbusEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinators = hass.data[DOMAIN][entry.entry_id]
    coordinator: FerroampModbusCoordinator = coordinators["standard"]
    fast_coordinator: FerroampModbusFastCoordinator = coordinators["fast"]

    entities: list[FerroampModbusSensor] = []
    for defn in SENSOR_DEFINITIONS:
        coord = fast_coordinator if defn.scan_interval == FAST_SCAN_INTERVAL else coordinator
        entities.append(FerroampModbusSensor(coord, entry.entry_id, defn))

    async_add_entities(entities)


class FerroampModbusSensor(FerroampModbusEntity, SensorEntity):
    """A single Ferroamp Modbus sensor."""

    def __init__(
        self,
        coordinator: FerroampModbusCoordinator | FerroampModbusFastCoordinator,
        entry_id: str,
        defn: SensorDefinition,
    ) -> None:
        super().__init__(coordinator, entry_id, defn.key, defn.name)
        self._defn = defn
        self._attr_native_unit_of_measurement = defn.unit
        self._attr_device_class = defn.device_class
        self._attr_state_class = defn.state_class
        if defn.icon:
            self._attr_icon = defn.icon

    @property
    def native_value(self) -> int | float | None:
        if self.coordinator.data is None:
            return None
        raw = self.coordinator.data.get(self._defn.key)
        if raw is None:
            return None
        if self._defn.as_int:
            return int(round(float(raw)))
        # Round floats to 3 decimal places for clean display
        if isinstance(raw, float):
            return round(raw, 3)
        return raw
