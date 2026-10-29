"""Power, mode, target temperature, fan speed and swing."""

from __future__ import annotations

from typing import Any

from homeassistant.components.climate import (
    ATTR_HVAC_MODE,
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DaikinRemoteConfigEntry
from .const import (
    CEILING,
    COOL_MAX_TEMP,
    COOL_MIN_TEMP,
    DOMAIN,
    FAN_SPEEDS,
    HORIZONTAL,
    INDOOR_HUMIDITY,
    INDOOR_TEMP,
    MODE,
    MODE_COOL,
    MODE_DRY,
    MODE_FAN,
    MOLD_PROOF,
    POWER,
    POWERFUL,
    STREAMER,
    VERTICAL,
)
from .entity import DaikinRemoteEntity
from .sensor import signed_byte

HVAC_MODES = {MODE_COOL: HVACMode.COOL, MODE_DRY: HVACMode.DRY, MODE_FAN: HVACMode.FAN_ONLY}


async def async_setup_entry(
    hass: HomeAssistant, entry: DaikinRemoteConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities([DaikinClimate(entry.runtime_data, "climate")])


class DaikinClimate(DaikinRemoteEntity, ClimateEntity):
    """Swing mode holds the vertical flap position, horizontal swing mode the louvre position,
    so that every airflow setting of the remote is available in the climate dialog."""

    _attr_name = None
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_target_temperature_step = 0.5
    _attr_min_temp = COOL_MIN_TEMP
    _attr_max_temp = COOL_MAX_TEMP
    _attr_hvac_modes = [HVACMode.OFF, *HVAC_MODES.values()]
    _attr_fan_modes = list(FAN_SPEEDS.values())
    _attr_swing_modes = [*VERTICAL.values(), CEILING]
    _attr_swing_horizontal_modes = list(HORIZONTAL.values())
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.FAN_MODE
        | ClimateEntityFeature.SWING_MODE
        | ClimateEntityFeature.SWING_HORIZONTAL_MODE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )

    @property
    def hvac_mode(self) -> HVACMode | None:
        c = self.coordinator
        return HVAC_MODES.get(c.mode or "") if c.power else HVACMode.OFF

    @property
    def current_temperature(self) -> float | None:
        raw = self.coordinator.data.get(INDOOR_TEMP)
        return signed_byte(raw) if raw else None

    @property
    def current_humidity(self) -> float | None:
        raw = self.coordinator.data.get(INDOOR_HUMIDITY)
        return int(raw, 16) if raw else None

    @property
    def target_temperature(self) -> float | None:
        raw = self.coordinator.value("temperature")
        return int(raw[:2], 16) / 2 if raw else None

    @property
    def fan_mode(self) -> str | None:
        return FAN_SPEEDS.get(self.coordinator.value("fan") or "")

    @property
    def swing_mode(self) -> str | None:
        return self.coordinator.vertical_option

    @property
    def swing_horizontal_mode(self) -> str | None:
        return self.coordinator.horizontal_option

    @property
    def extra_state_attributes(self) -> dict[str, bool]:
        c = self.coordinator
        return {
            "mold_proof": c.is_on(MOLD_PROOF),
            "streamer": c.is_on(STREAMER),
            "powerful": c.is_on(POWERFUL),
        }

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        if hvac_mode == HVACMode.OFF:
            await self.coordinator.write({POWER: "00"})
            return
        mode = {v: k for k, v in HVAC_MODES.items()}[hvac_mode]
        await self.coordinator.write({POWER: "01", MODE: mode})

    async def async_turn_on(self) -> None:
        await self.coordinator.write({POWER: "01"})

    async def async_turn_off(self) -> None:
        await self.coordinator.write({POWER: "00"})

    async def async_set_temperature(self, **kwargs: Any) -> None:
        changes: dict[str, str] = {}
        if (hvac_mode := kwargs.get(ATTR_HVAC_MODE)) is not None and hvac_mode != self.hvac_mode:
            if hvac_mode == HVACMode.OFF:
                changes[POWER] = "00"
            else:
                changes |= {POWER: "01", MODE: {v: k for k, v in HVAC_MODES.items()}[hvac_mode]}
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is not None:
            if changes.get(MODE, self.coordinator.mode) != MODE_COOL:
                raise ServiceValidationError(
                    translation_domain=DOMAIN, translation_key="no_target_temperature"
                )
            changes["e_1002/e_3001/p_02"] = format(int(round(temperature * 2)), "02X")
        if changes:
            await self.coordinator.write(changes)

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        point = self.coordinator.point("fan")
        if point is None:
            raise ServiceValidationError(translation_domain=DOMAIN, translation_key="no_fan_speed")
        await self.coordinator.write({point: {v: k for k, v in FAN_SPEEDS.items()}[fan_mode]})

    async def async_set_swing_mode(self, swing_mode: str) -> None:
        await self.coordinator.set_vertical(swing_mode)

    async def async_set_swing_horizontal_mode(self, swing_horizontal_mode: str) -> None:
        await self.coordinator.set_horizontal(swing_horizontal_mode)
