"""Daikin Remote Control: standalone control of Daikin air conditioners with a dsiot Wi-Fi adapter."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_SCAN_INTERVAL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import DaikinDsiot
from .const import DEFAULT_SCAN_INTERVAL
from .coordinator import DaikinRemoteCoordinator

PLATFORMS = [Platform.BINARY_SENSOR, Platform.CLIMATE, Platform.SELECT, Platform.SENSOR, Platform.SWITCH]

type DaikinRemoteConfigEntry = ConfigEntry[DaikinRemoteCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: DaikinRemoteConfigEntry) -> bool:
    api = DaikinDsiot(async_get_clientsession(hass), entry.data[CONF_HOST])
    interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    coordinator = DaikinRemoteCoordinator(hass, entry, api, interval)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    entry.async_on_unload(entry.add_update_listener(_options_updated))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: DaikinRemoteConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _options_updated(hass: HomeAssistant, entry: DaikinRemoteConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)
