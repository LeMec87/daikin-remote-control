"""Daikin Extra: Funktionen der Fernbedienung, die die Daikin-Integration nicht kann."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_SCAN_INTERVAL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import DaikinDsiot
from .const import STANDARD_TAKT
from .coordinator import DaikinExtraCoordinator

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SELECT, Platform.SWITCH]

type DaikinExtraEintrag = ConfigEntry[DaikinExtraCoordinator]


async def async_setup_entry(hass: HomeAssistant, eintrag: DaikinExtraEintrag) -> bool:
    api = DaikinDsiot(async_get_clientsession(hass), eintrag.data[CONF_HOST])
    takt = eintrag.options.get(CONF_SCAN_INTERVAL, STANDARD_TAKT)
    coordinator = DaikinExtraCoordinator(hass, eintrag, api, takt)
    await coordinator.async_config_entry_first_refresh()
    eintrag.runtime_data = coordinator
    eintrag.async_on_unload(eintrag.add_update_listener(_optionen_geaendert))
    await hass.config_entries.async_forward_entry_setups(eintrag, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, eintrag: DaikinExtraEintrag) -> bool:
    return await hass.config_entries.async_unload_platforms(eintrag, PLATFORMS)


async def _optionen_geaendert(hass: HomeAssistant, eintrag: DaikinExtraEintrag) -> None:
    await hass.config_entries.async_reload(eintrag.entry_id)
