"""Luftrichtung oben/unten und links/rechts in festen Positionen."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DaikinExtraEintrag
from .const import DECKE, LINKS_RECHTS, OBEN_UNTEN
from .entity import DaikinExtraEntity


async def async_setup_entry(
    hass: HomeAssistant, eintrag: DaikinExtraEintrag, async_add_entities: AddEntitiesCallback
) -> None:
    c = eintrag.runtime_data
    async_add_entities([LuftObenUnten(c, "vertical_position"), LuftLinksRechts(c, "horizontal_position")])


class LuftObenUnten(DaikinExtraEntity, SelectEntity):
    _attr_icon = "mdi:arrow-up-down"
    _attr_options = [*OBEN_UNTEN.values(), DECKE]

    @property
    def current_option(self) -> str | None:
        d = self.coordinator.data
        return DECKE if d["decke"] else OBEN_UNTEN.get(d["p05"])

    async def async_select_option(self, option: str) -> None:
        if option == DECKE:
            gruppen = {"e_3003": {"p_1D": "01"}}
        else:
            gruppen = {"e_3001": {"p_05": {v: k for k, v in OBEN_UNTEN.items()}[option]}}
            if self.coordinator.data["decke"]:  # Luft zur Decke zuerst beenden, sonst bleibt die Klappe oben
                gruppen["e_3003"] = {"p_1D": "00"}
        await self.coordinator.schreiben(gruppen)


class LuftLinksRechts(DaikinExtraEntity, SelectEntity):
    _attr_icon = "mdi:arrow-left-right"
    _attr_options = list(LINKS_RECHTS.values())

    @property
    def current_option(self) -> str | None:
        return LINKS_RECHTS.get(self.coordinator.data["p06"])

    async def async_select_option(self, option: str) -> None:
        wert = {v: k for k, v in LINKS_RECHTS.items()}[option]
        await self.coordinator.schreiben({"e_3001": {"p_06": wert}})
