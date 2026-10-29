"""Liest die Anlage regelmäßig, damit Änderungen über die Fernbedienung ankommen."""

from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import DaikinDsiot, DaikinFehler
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class DaikinExtraCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, eintrag: ConfigEntry, api: DaikinDsiot, takt: int) -> None:
        super().__init__(
            hass, _LOGGER, config_entry=eintrag, name=DOMAIN, update_interval=timedelta(seconds=takt)
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self.api.lesen()
        except DaikinFehler as err:
            raise UpdateFailed(str(err)) from err

    async def schreiben(self, gruppen: dict[str, dict[str, str]]) -> None:
        try:
            await self.api.schreiben(gruppen)
        except DaikinFehler as err:
            raise HomeAssistantError(str(err)) from err
        # Die Anlage übernimmt Werte mit kurzer Verzögerung
        await asyncio.sleep(2)
        await self.async_request_refresh()
