"""Polls the unit so that changes made with the remote show up in Home Assistant."""

from __future__ import annotations

import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import DaikinDsiot, DaikinError
from .const import CEILING_AIRFLOW, DOMAIN, MODE, MODE_COOL, MODE_POINTS, POWER

_LOGGER = logging.getLogger(__name__)


class DaikinRemoteCoordinator(DataUpdateCoordinator[dict[str, str]]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, api: DaikinDsiot, interval: int) -> None:
        super().__init__(
            hass, _LOGGER, config_entry=entry, name=DOMAIN, update_interval=timedelta(seconds=interval)
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, str]:
        try:
            return await self.api.read()
        except DaikinError as err:
            raise UpdateFailed(str(err)) from err

    @property
    def power(self) -> bool:
        return self.data.get(POWER) == "01"

    @property
    def mode(self) -> str | None:
        return self.data.get(MODE)

    @property
    def ceiling(self) -> bool:
        return self.data.get(CEILING_AIRFLOW) == "01"

    def point(self, kind: str) -> str | None:
        """Data point of the current mode for "temperature", "fan", "vertical" or "horizontal"."""
        return MODE_POINTS.get(self.mode or "", MODE_POINTS[MODE_COOL])[kind]

    def value(self, kind: str) -> str | None:
        point = self.point(kind)
        return self.data.get(point) if point else None

    def is_on(self, path: str) -> bool:
        return self.data.get(path) == "01"

    async def write(self, changes: dict[str, str]) -> None:
        try:
            await self.api.write(changes)
        except DaikinError as err:
            raise HomeAssistantError(str(err)) from err
        # The unit applies new values with a short delay
        await asyncio.sleep(2)
        await self.async_request_refresh()
