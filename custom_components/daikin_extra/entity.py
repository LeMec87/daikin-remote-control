from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import DaikinExtraCoordinator


class DaikinExtraEntity(CoordinatorEntity[DaikinExtraCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator: DaikinExtraCoordinator, schluessel: str) -> None:
        super().__init__(coordinator)
        eintrag = coordinator.config_entry
        self._attr_translation_key = schluessel
        self._attr_unique_id = f"{eintrag.entry_id}_{schluessel}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, eintrag.entry_id)},
            name=eintrag.title,
            manufacturer="Daikin",
            model="dsiot-WLAN-Adapter",
            configuration_url=f"http://{eintrag.data['host']}",
        )
