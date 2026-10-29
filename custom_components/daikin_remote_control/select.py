"""Vertical and horizontal airflow direction in fixed positions."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DaikinRemoteConfigEntry
from .const import CEILING, HORIZONTAL, VERTICAL
from .entity import DaikinRemoteEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: DaikinRemoteConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    c = entry.runtime_data
    async_add_entities([VerticalAirflow(c, "vertical_position"), HorizontalAirflow(c, "horizontal_position")])


class VerticalAirflow(DaikinRemoteEntity, SelectEntity):
    _attr_icon = "mdi:arrow-up-down"
    _attr_options = [*VERTICAL.values(), CEILING]

    @property
    def current_option(self) -> str | None:
        return self.coordinator.vertical_option

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.set_vertical(option)


class HorizontalAirflow(DaikinRemoteEntity, SelectEntity):
    _attr_icon = "mdi:arrow-left-right"
    _attr_options = list(HORIZONTAL.values())

    @property
    def current_option(self) -> str | None:
        return self.coordinator.horizontal_option

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.set_horizontal(option)
