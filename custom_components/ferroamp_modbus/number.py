"""Number platform for Ferroamp Modbus (import/export threshold control)."""
from __future__ import annotations

import logging
import struct

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_MAX_VALUE,
    CONF_MIN_VALUE,
    DOMAIN,
    NUMBER_DEFINITIONS,
    NumberDefinition,
)
from .coordinator import FerroampModbusFastCoordinator
from .entity import FerroampModbusEntity

_LOGGER = logging.getLogger(__name__)

# Name of the HA built-in modbus hub defined in configuration.yaml
_MODBUS_HUB = DOMAIN
_MODBUS_SLAVE = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    fast_coordinator: FerroampModbusFastCoordinator = data["fast"]
    config = {**entry.data, **entry.options}

    async_add_entities(
        FerroampModbusNumber(fast_coordinator, entry.entry_id, defn, config)
        for defn in NUMBER_DEFINITIONS
    )


class FerroampModbusNumber(FerroampModbusEntity, NumberEntity):
    """A writable number entity backed by a Modbus float32 register.

    Reads its current value from the fast coordinator (which polls the
    *System Value* read-back register).  Writes use HA's built-in modbus
    service (the same hub used by the configuration.yaml templates) to
    avoid TCP connection conflicts with the device.
    """

    _attr_mode = NumberMode.BOX

    def __init__(
        self,
        coordinator: FerroampModbusFastCoordinator,
        entry_id: str,
        defn: NumberDefinition,
        config: dict[str, float | str | int],
    ) -> None:
        super().__init__(coordinator, entry_id, defn.key, defn.name)
        self._defn = defn
        self._attr_native_unit_of_measurement = defn.unit
        self._attr_device_class = defn.device_class
        self._attr_native_min_value = config.get(CONF_MIN_VALUE, defn.min_value)
        self._attr_native_max_value = config.get(CONF_MAX_VALUE, defn.max_value)
        self._attr_native_step = defn.step
        if defn.icon:
            self._attr_icon = defn.icon

    @property
    def native_value(self) -> float | None:
        """Return the current value read back from the device."""
        if self.coordinator.data is None:
            return None
        sensor_key = f"{self._defn.key}_system_value"
        raw = self.coordinator.data.get(sensor_key)
        if raw is None:
            return None
        if self._defn.as_int:
            return float(int(round(float(raw))))
        return round(float(raw), 1)

    async def async_set_native_value(self, value: float) -> None:
        """Write the new threshold to the device via HA's modbus service."""
        # Encode as big-endian float32, write word-swapped (CDAB order):
        # [ bytes_2_3, bytes_0_1 ] — matches Ferroamp register layout
        packed = struct.pack(">f", float(value))
        high_word = struct.unpack(">H", packed[2:4])[0]
        low_word = struct.unpack(">H", packed[0:2])[0]

        await self.hass.services.async_call(
            "modbus",
            "write_register",
            {
                "hub": _MODBUS_HUB,
                "address": self._defn.write_address,
                "slave": _MODBUS_SLAVE,
                "value": [high_word, low_word],
            },
            blocking=True,
        )
        await self.hass.services.async_call(
            "modbus",
            "write_register",
            {
                "hub": _MODBUS_HUB,
                "address": self._defn.apply_address,
                "slave": _MODBUS_SLAVE,
                "value": [1],
            },
            blocking=True,
        )
        await self.coordinator.async_request_refresh()
