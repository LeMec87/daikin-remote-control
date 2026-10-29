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
        d = self.coordinator.data
        return CEILING if d["ceiling"] else VERTICAL.get(d["p05"])

    async def async_select_option(self, option: str) -> None:
        if option == CEILING:
            groups = {"e_3003": {"p_1D": "01"}}
        else:
            groups = {"e_3001": {"p_05": {v: k for k, v in VERTICAL.items()}[option]}}
            if self.coordinator.data["ceiling"]:  # End ceiling airflow first, otherwise the flap stays up
                groups["e_3003"] = {"p_1D": "00"}
        await self.coordinator.write(groups)


class HorizontalAirflow(DaikinRemoteEntity, SelectEntity):
    _attr_icon = "mdi:arrow-left-right"
    _attr_options = list(HORIZONTAL.values())

    @property
    def current_option(self) -> str | None:
        return HORIZONTAL.get(self.coordinator.data["p06"])

    async def async_select_option(self, option: str) -> None:
        value = {v: k for k, v in HORIZONTAL.items()}[option]
        await self.coordinator.write({"e_3001": {"p_06": value}})
