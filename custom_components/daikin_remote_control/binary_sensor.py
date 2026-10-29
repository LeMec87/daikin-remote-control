"""Streamer and Powerful: display only, the unit does not accept these commands over Wi-Fi."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DaikinRemoteConfigEntry
from .coordinator import DaikinRemoteCoordinator
from .entity import DaikinRemoteEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: DaikinRemoteConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    c = entry.runtime_data
    async_add_entities([
        StatusSensor(c, "streamer", "mdi:creation"),
        StatusSensor(c, "powerful", "mdi:arm-flex"),
    ])


class StatusSensor(DaikinRemoteEntity, BinarySensorEntity):
    def __init__(self, coordinator: DaikinRemoteCoordinator, key: str, icon: str) -> None:
        super().__init__(coordinator, key)
        self._key = key
        self._attr_icon = icon

    @property
    def is_on(self) -> bool:
        return self.coordinator.data[self._key]
