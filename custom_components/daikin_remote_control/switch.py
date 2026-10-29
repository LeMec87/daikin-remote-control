"""Mold proof."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DaikinRemoteConfigEntry
from .const import MOLD_PROOF
from .entity import DaikinRemoteEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: DaikinRemoteConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities([MoldProof(entry.runtime_data, "mold_proof")])


class MoldProof(DaikinRemoteEntity, SwitchEntity):
    _attr_icon = "mdi:water-off"

    @property
    def is_on(self) -> bool:
        return self.coordinator.is_on(MOLD_PROOF)

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.coordinator.write({MOLD_PROOF: "01"})

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.coordinator.write({MOLD_PROOF: "00"})
