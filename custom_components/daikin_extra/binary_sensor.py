"""Streamer und Powerful: nur Anzeige, die Anlage nimmt dafür keine Befehle über WLAN an."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DaikinExtraEintrag
from .entity import DaikinExtraEntity


async def async_setup_entry(
    hass: HomeAssistant, eintrag: DaikinExtraEintrag, async_add_entities: AddEntitiesCallback
) -> None:
    c = eintrag.runtime_data
    async_add_entities([
        Anzeige(c, "streamer", "streamer", "mdi:creation"),
        Anzeige(c, "powerful", "powerful", "mdi:arm-flex"),
    ])


class Anzeige(DaikinExtraEntity, BinarySensorEntity):
    def __init__(self, coordinator, schluessel: str, feld: str, symbol: str) -> None:
        super().__init__(coordinator, schluessel)
        self._feld = feld
        self._attr_icon = symbol

    @property
    def is_on(self) -> bool:
        return self.coordinator.data[self._feld]
