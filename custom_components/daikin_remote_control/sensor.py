"""Indoor temperature, indoor humidity and outdoor temperature."""

from __future__ import annotations

from collections.abc import Callable

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DaikinRemoteConfigEntry
from .const import INDOOR_HUMIDITY, INDOOR_TEMP, OUTDOOR_TEMP
from .coordinator import DaikinRemoteCoordinator
from .entity import DaikinRemoteEntity


def signed_byte(raw: str) -> int:
    """Indoor temperature: one signed byte in whole degrees."""
    return int.from_bytes(bytes.fromhex(raw[:2]), "big", signed=True)


def signed_le_half(raw: str) -> float:
    """Outdoor temperature: signed little-endian value in half degrees."""
    return int.from_bytes(bytes.fromhex(raw), "little", signed=True) / 2


async def async_setup_entry(
    hass: HomeAssistant, entry: DaikinRemoteConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    c = entry.runtime_data
    async_add_entities([
        Measurement(c, "indoor_temperature", INDOOR_TEMP, signed_byte,
                    SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
        Measurement(c, "indoor_humidity", INDOOR_HUMIDITY, lambda raw: int(raw, 16),
                    SensorDeviceClass.HUMIDITY, PERCENTAGE),
        Measurement(c, "outdoor_temperature", OUTDOOR_TEMP, signed_le_half,
                    SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
    ])


class Measurement(DaikinRemoteEntity, SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: DaikinRemoteCoordinator,
        key: str,
        path: str,
        decode: Callable[[str], float],
        device_class: SensorDeviceClass,
        unit: str,
    ) -> None:
        super().__init__(coordinator, key)
        self._path = path
        self._decode = decode
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self) -> float | None:
        raw = self.coordinator.data.get(self._path)
        return self._decode(raw) if raw else None
