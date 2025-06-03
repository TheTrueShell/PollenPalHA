"""Sensor platform for PollenPal integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_TYPES
from .coordinator import PollenPalDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PollenPal sensor based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for sensor_type in SENSOR_TYPES:
        entities.append(PollenPalSensor(coordinator, sensor_type, config_entry))

    async_add_entities(entities)


class PollenPalSensor(CoordinatorEntity, SensorEntity):
    """Representation of a PollenPal sensor."""

    def __init__(
        self,
        coordinator: PollenPalDataUpdateCoordinator,
        sensor_type: str,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._config_entry = config_entry
        self._attr_name = f"PollenPal {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_type}"
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit"]

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._config_entry.entry_id)},
            "name": f"PollenPal {self.coordinator.location}",
            "manufacturer": "PollenPal",
            "model": "Pollen Monitor",
            "sw_version": "1.0",
        }

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None

        current_data = self.coordinator.data.get("current", {})
        advice_data = self.coordinator.data.get("advice", {})
        current_day = current_data.get("current_day", {})

        if self._sensor_type == "grass_level":
            return current_day.get("grass", {}).get("level")
        elif self._sensor_type == "grass_count":
            return current_day.get("grass", {}).get("count")
        elif self._sensor_type == "trees_level":
            return current_day.get("trees", {}).get("level")
        elif self._sensor_type == "trees_count":
            return current_day.get("trees", {}).get("count")
        elif self._sensor_type == "weeds_level":
            return current_day.get("weeds", {}).get("level")
        elif self._sensor_type == "weeds_count":
            return current_day.get("weeds", {}).get("count")
        elif self._sensor_type == "alert_level":
            return advice_data.get("alert_level", "unknown")

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}

        current_data = self.coordinator.data.get("current", {})
        advice_data = self.coordinator.data.get("advice", {})
        current_day = current_data.get("current_day", {})
        
        attributes = {
            "location": self.coordinator.data.get("location"),
            "coordinates": self.coordinator.data.get("coordinates", {}),
            "day_name": current_day.get("day_name"),
            "day_number": current_day.get("day_number"),
        }

        # Add specific attributes based on sensor type
        if self._sensor_type.startswith("grass"):
            grass_data = current_day.get("grass", {})
            attributes.update({
                "grass_level": grass_data.get("level"),
                "grass_count": grass_data.get("count"),
                "grass_detail": grass_data.get("detail"),
            })
        elif self._sensor_type.startswith("trees"):
            trees_data = current_day.get("trees", {})
            attributes.update({
                "trees_level": trees_data.get("level"),
                "trees_count": trees_data.get("count"),
                "trees_detail": trees_data.get("detail"),
            })
        elif self._sensor_type.startswith("weeds"):
            weeds_data = current_day.get("weeds", {})
            attributes.update({
                "weeds_level": weeds_data.get("level"),
                "weeds_count": weeds_data.get("count"),
                "weeds_detail": weeds_data.get("detail"),
            })
        elif self._sensor_type == "alert_level":
            attributes.update({
                "advice": advice_data.get("advice", []),
                "high_levels": advice_data.get("high_levels", []),
                "moderate_levels": advice_data.get("moderate_levels", []),
            })

        return attributes

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success 