"""Config flow for Envertech EVT Local integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_HOST
from homeassistant.core import callback

from .const import (
    CONF_MAX_POWER_PREFIX,
    CONF_PRICE_PER_KWH,
    CONF_SERIAL,
    DEFAULT_MAX_POWER,
    DEFAULT_PRICE_PER_KWH,
    DOMAIN,
)
from .coordinator import EnvertechCoordinator
from .protocol import EnvertechConnection

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_SERIAL): str,
    }
)


class EnvertechLocalConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Envertech EVT Local."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: Any) -> OptionsFlow:
        """Return the options flow."""
        return EnvertechOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            serial_str = user_input[CONF_SERIAL].strip()

            # Parse serial as hex (entered exactly as printed on the device label)
            try:
                serial = int(serial_str, 16)
            except ValueError:
                errors[CONF_SERIAL] = "invalid_serial"

            if not errors:
                # Test connection
                conn = EnvertechConnection(host, serial)
                try:
                    await conn.get_live_data()
                    await conn.disconnect()
                except (ConnectionError, OSError):
                    errors["base"] = "cannot_connect"
                else:
                    await self.async_set_unique_id(f"{serial:08X}")
                    self._abort_if_unique_id_configured()

                    return self.async_create_entry(
                        title=f"Envertech {serial:08X}",
                        data={
                            CONF_HOST: host,
                            CONF_SERIAL: serial,
                        },
                    )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )


class EnvertechOptionsFlow(OptionsFlow):
    """Handle options for Envertech EVT Local."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        current_price = self.config_entry.options.get(
            CONF_PRICE_PER_KWH, DEFAULT_PRICE_PER_KWH
        )

        schema_fields: dict[Any, Any] = {
            vol.Required(CONF_PRICE_PER_KWH, default=current_price): vol.All(
                vol.Coerce(float), vol.Range(min=0)
            ),
        }

        # Add per-channel max power fields
        coordinator: EnvertechCoordinator = self.config_entry.runtime_data
        if coordinator.data and coordinator.data.channels:
            for idx in range(len(coordinator.data.channels)):
                key = f"{CONF_MAX_POWER_PREFIX}{idx}"
                current_max = self.config_entry.options.get(key, DEFAULT_MAX_POWER)
                schema_fields[
                    vol.Required(key, default=current_max)
                ] = vol.All(vol.Coerce(int), vol.Range(min=1))

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema_fields),
        )
