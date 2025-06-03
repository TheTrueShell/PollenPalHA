"""DataUpdateCoordinator for PollenPal."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class PollenPalDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the PollenPal API."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        api_url: str,
        location: str,
    ) -> None:
        """Initialize."""
        self.api_url = api_url.rstrip("/")
        self.location = location
        self.session = session

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            # Fetch current pollen data
            current_data = await self._fetch_current_data()
            
            # Fetch health advice
            advice_data = await self._fetch_advice_data()
            
            # Combine the data
            return {
                "current": current_data,
                "advice": advice_data,
                "location": current_data.get("location", self.location),
                "coordinates": current_data.get("coordinates", {}),
            }

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def _fetch_current_data(self) -> dict[str, Any]:
        """Fetch current pollen data."""
        url = f"{self.api_url}/pollen/{self.location}/current"
        
        try:
            async with self.session.get(url, timeout=10) as response:
                if response.status != 200:
                    raise UpdateFailed(f"API returned status {response.status}")
                
                data = await response.json()
                return data
                
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching current data: {err}") from err

    async def _fetch_advice_data(self) -> dict[str, Any]:
        """Fetch health advice data."""
        url = f"{self.api_url}/pollen/{self.location}/advice"
        
        try:
            async with self.session.get(url, timeout=10) as response:
                if response.status != 200:
                    # Advice endpoint might not be available, return empty data
                    _LOGGER.warning("Could not fetch advice data, status: %s", response.status)
                    return {"advice": [], "alert_level": "unknown"}
                
                data = await response.json()
                return data
                
        except aiohttp.ClientError as err:
            _LOGGER.warning("Error fetching advice data: %s", err)
            return {"advice": [], "alert_level": "unknown"} 