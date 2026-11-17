"""The Envertech EVT Local integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MAJOR_VERSION, MINOR_VERSION, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN, MANUFACTURER, MODEL
from .coordinator import EnvertechCoordinator

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR, Platform.SELECT]

EnvertechConfigEntry = ConfigEntry[EnvertechCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: EnvertechConfigEntry) -> bool:
    """Set up Envertech EVT Local from a config entry."""
    coordinator = EnvertechCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    if (MAJOR_VERSION, MINOR_VERSION) >= (2026, 8):
        # The inputs need the inverter's registry ID before any platform loads.
        inverter = dr.async_get(hass).async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, coordinator.serial_hex)},
            name=f"Envertech {coordinator.serial_hex}",
            manufacturer=MANUFACTURER,
            model=MODEL,
        )
        coordinator.inverter_device_id = inverter.id

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: EnvertechConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        coordinator: EnvertechCoordinator = entry.runtime_data
        await coordinator.async_shutdown()
    return unload_ok
