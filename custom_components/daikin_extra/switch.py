"""Schimmelschutz."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DaikinExtraEintrag
from .entity import DaikinExtraEntity


async def async_setup_entry(
    hass: HomeAssistant, eintrag: DaikinExtraEintrag, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities([Schimmelschutz(eintrag.runtime_data, "mold_proof")])


class Schimmelschutz(DaikinExtraEntity, SwitchEntity):
    _attr_icon = "mdi:water-off"

    @property
    def is_on(self) -> bool:
        return self.coordinator.data["schimmel"]

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.coordinator.schreiben({"e_3003": {"p_4D": "01"}})

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.coordinator.schreiben({"e_3003": {"p_4D": "00"}})
