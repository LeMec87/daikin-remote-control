"""Polls the unit so that changes made with the remote show up in Home Assistant."""

from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import DaikinDsiot, DaikinError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class DaikinRemoteCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, api: DaikinDsiot, interval: int) -> None:
        super().__init__(
            hass, _LOGGER, config_entry=entry, name=DOMAIN, update_interval=timedelta(seconds=interval)
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self.api.read()
        except DaikinError as err:
            raise UpdateFailed(str(err)) from err

    async def write(self, groups: dict[str, dict[str, str]]) -> None:
        try:
            await self.api.write(groups)
        except DaikinError as err:
            raise HomeAssistantError(str(err)) from err
        # The unit applies new values with a short delay
        await asyncio.sleep(2)
        await self.async_request_refresh()
