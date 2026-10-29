"""Vertical and horizontal airflow direction in fixed positions."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DaikinRemoteConfigEntry
from .const import CEILING, CEILING_AIRFLOW, HORIZONTAL, VERTICAL
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
        c = self.coordinator
        return CEILING if c.ceiling else VERTICAL.get(c.value("vertical") or "")

    async def async_select_option(self, option: str) -> None:
        c = self.coordinator
        if option == CEILING:
            changes = {CEILING_AIRFLOW: "01"}
        else:
            changes = {c.point("vertical"): {v: k for k, v in VERTICAL.items()}[option]}
            if c.ceiling:  # End ceiling airflow first, otherwise the flap stays up
                changes[CEILING_AIRFLOW] = "00"
        await c.write(changes)


class HorizontalAirflow(DaikinRemoteEntity, SelectEntity):
    _attr_icon = "mdi:arrow-left-right"
    _attr_options = list(HORIZONTAL.values())

    @property
    def current_option(self) -> str | None:
        return HORIZONTAL.get(self.coordinator.value("horizontal") or "")

    async def async_select_option(self, option: str) -> None:
        c = self.coordinator
        await c.write({c.point("horizontal"): {v: k for k, v in HORIZONTAL.items()}[option]})
