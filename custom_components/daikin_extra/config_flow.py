from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_SCAN_INTERVAL
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import DaikinDsiot, DaikinFehler
from .const import DOMAIN, STANDARD_TAKT


class DaikinExtraConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        fehler: dict[str, str] = {}
        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            await self.async_set_unique_id(host)
            self._abort_if_unique_id_configured()
            try:
                await DaikinDsiot(async_get_clientsession(self.hass), host).lesen()
            except DaikinFehler:
                fehler["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title=user_input[CONF_NAME], data={CONF_HOST: host})
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_NAME, default="Daikin"): str,
                }
            ),
            errors=fehler,
        )

    @staticmethod
    @callback
    def async_get_options_flow(eintrag: ConfigEntry) -> OptionsFlow:
        return DaikinExtraOptionsFlow()


class DaikinExtraOptionsFlow(OptionsFlow):
    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(data=user_input)
        takt = self.config_entry.options.get(CONF_SCAN_INTERVAL, STANDARD_TAKT)
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {vol.Required(CONF_SCAN_INTERVAL, default=takt): vol.All(int, vol.Range(min=5, max=300))}
            ),
        )
