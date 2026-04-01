"""Config flow for Ferroamp Modbus integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, OptionsFlow
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import callback

from .const import (
    CONF_MAX_VALUE,
    CONF_MIN_VALUE,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DOMAIN,
    DEFAULT_MAX_VALUE,
    DEFAULT_MIN_VALUE,
)
from .hub import FerroampModbusHub

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): vol.Coerce(int),
        vol.Required(CONF_MIN_VALUE, default=DEFAULT_MIN_VALUE): vol.Coerce(float),
        vol.Required(CONF_MAX_VALUE, default=DEFAULT_MAX_VALUE): vol.Coerce(float),
    }
)


class FerroampModbusConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ferroamp Modbus."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> dict:
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]

            hub = FerroampModbusHub(self.hass, host, port)
            try:
                await hub.async_validate_modbus_protocol()
                await hub.async_close()
                await self.async_set_unique_id(f"{host}:{port}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"Ferroamp {host}:{port}",
                    data=user_input,
                )
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:  # noqa: BLE001
                _LOGGER.exception("Unexpected error during Ferroamp Modbus setup")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry) -> FerroampModbusOptionsFlow:
        return FerroampModbusOptionsFlow()


class FerroampModbusOptionsFlow(OptionsFlow):
    """Handle options for Ferroamp Modbus (host/port can be changed)."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> dict:
        errors: dict[str, str] = {}
        current = {**self.config_entry.data, **self.config_entry.options}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]

            hub = FerroampModbusHub(self.hass, host, port)
            try:
                await hub.async_validate_modbus_protocol()
                await hub.async_close()
                return self.async_create_entry(title="", data=user_input)
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:  # noqa: BLE001
                _LOGGER.exception("Unexpected error during options update")
                errors["base"] = "unknown"

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=current.get(CONF_HOST, DEFAULT_HOST)): str,
                vol.Required(CONF_PORT, default=current.get(CONF_PORT, DEFAULT_PORT)): vol.Coerce(int),
                vol.Required(CONF_MIN_VALUE, default=current.get(CONF_MIN_VALUE, DEFAULT_MIN_VALUE)):
                    vol.Coerce(float),
                vol.Required(CONF_MAX_VALUE, default=current.get(CONF_MAX_VALUE, DEFAULT_MAX_VALUE)):
                    vol.Coerce(float),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)
