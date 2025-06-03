"""Constants for the PollenPal integration."""

DOMAIN = "pollenpal"

# Default values
DEFAULT_SCAN_INTERVAL = 3600  # 1 hour in seconds
DEFAULT_API_URL = "http://localhost:3000"

# Configuration keys
CONF_API_URL = "api_url"
CONF_LOCATION = "location"

# Sensor types
SENSOR_TYPES = {
    "grass_level": {
        "name": "Grass Pollen Level",
        "icon": "mdi:grass",
        "unit": None,
    },
    "grass_count": {
        "name": "Grass Pollen Count",
        "icon": "mdi:grass",
        "unit": None,
    },
    "trees_level": {
        "name": "Tree Pollen Level",
        "icon": "mdi:tree",
        "unit": None,
    },
    "trees_count": {
        "name": "Tree Pollen Count",
        "icon": "mdi:tree",
        "unit": None,
    },
    "weeds_level": {
        "name": "Weed Pollen Level",
        "icon": "mdi:flower",
        "unit": None,
    },
    "weeds_count": {
        "name": "Weed Pollen Count",
        "icon": "mdi:flower",
        "unit": None,
    },
    "alert_level": {
        "name": "Pollen Alert Level",
        "icon": "mdi:alert-circle",
        "unit": None,
    },
}

# Pollen levels
POLLEN_LEVELS = ["Low", "Moderate", "High", "Very High"] 