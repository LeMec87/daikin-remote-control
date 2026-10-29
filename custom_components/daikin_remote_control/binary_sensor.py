"""Streamer and Powerful: display only, the unit does not accept these commands over Wi-Fi."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DaikinRemoteConfigEntry
from .const import POWERFUL, STREAMER
from .coordinator import DaikinRemoteCoordinator
from .entity import DaikinRemoteEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: DaikinRemoteConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    c = entry.runtime_data
    async_add_entities([
        StatusSensor(c, "streamer", STREAMER, "mdi:creation"),
        StatusSensor(c, "powerful", POWERFUL, "mdi:arm-flex"),
    ])


class StatusSensor(DaikinRemoteEntity, BinarySensorEntity):
    def __init__(self, coordinator: DaikinRemoteCoordinator, key: str, path: str, icon: str) -> None:
        super().__init__(coordinator, key)
        self._path = path
        self._attr_icon = icon

    @property
    def is_on(self) -> bool:
        return self.coordinator.is_on(self._path)
