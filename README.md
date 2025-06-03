# PollenPal Home Assistant Integration 🌾

A custom Home Assistant integration for the PollenPal API that provides real-time UK pollen data and forecasts directly in your Home Assistant dashboard.

## Features

- 🌍 **Real-time pollen monitoring** for any UK location
- 📊 **Multiple sensor types** for grass, tree, and weed pollen
- 🚨 **Alert level monitoring** with health advice
- 📍 **Flexible location support** (cities and postcodes)
- 🔧 **Dynamic API URL** support for self-hosted instances
- 🏠 **Native Home Assistant integration** with proper device grouping

## Sensors Provided

The integration creates the following sensors for your configured location:

- **Grass Pollen Level** - Current grass pollen level (Low/Moderate/High/Very High)
- **Grass Pollen Count** - Numerical grass pollen count
- **Tree Pollen Level** - Current tree pollen level
- **Tree Pollen Count** - Numerical tree pollen count
- **Weed Pollen Level** - Current weed pollen level
- **Weed Pollen Count** - Numerical weed pollen count
- **Pollen Alert Level** - Overall alert level with health advice

Each sensor includes detailed attributes with additional information such as:
- Location coordinates
- Detailed pollen breakdowns by species
- Health advice recommendations
- Current day information

## Installation

### Method 1: Manual Installation

1. Download or clone this repository
2. Copy the `custom_components/pollenpal` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant
4. Go to **Settings** → **Devices & Services** → **Add Integration**
5. Search for "PollenPal" and click to add it

### Method 2: HACS (Home Assistant Community Store)

*Note: This integration is not yet available in HACS. Use manual installation for now.*

## Configuration

1. **Add Integration**: Go to Settings → Devices & Services → Add Integration
2. **Search**: Look for "PollenPal" in the integration list
3. **Configure**:
   - **API URL**: Enter your PollenPal API URL (default: `http://localhost:3000`)
   - **Location**: Enter a UK city name or postcode (e.g., "London" or "SW1A 1AA")
4. **Submit**: Click submit to validate and create the integration

### Configuration Options

| Field | Description | Example |
|-------|-------------|---------|
| API URL | URL of your PollenPal API instance | `http://localhost:3000` |
| Location | UK city or postcode to monitor | `London` or `M1 1AA` |

## Usage Examples

### Automation Example

Create an automation to notify when pollen levels are high:

```yaml
automation:
  - alias: "High Pollen Alert"
    trigger:
      - platform: state
        entity_id: sensor.pollenpal_pollen_alert_level
        to: "high"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "High Pollen Alert!"
          message: "Pollen levels are high in {{ state_attr('sensor.pollenpal_grass_pollen_level', 'location') }}. Consider staying indoors."
```

### Lovelace Card Example

Display pollen information on your dashboard:

```yaml
type: entities
title: Pollen Levels
entities:
  - entity: sensor.pollenpal_grass_pollen_level
    name: Grass Pollen
  - entity: sensor.pollenpal_tree_pollen_level
    name: Tree Pollen
  - entity: sensor.pollenpal_weed_pollen_level
    name: Weed Pollen
  - entity: sensor.pollenpal_pollen_alert_level
    name: Alert Level
```

### Template Sensor Example

Create a template sensor for combined pollen information:

```yaml
template:
  - sensor:
      - name: "Pollen Summary"
        state: >
          {% set grass = states('sensor.pollenpal_grass_pollen_level') %}
          {% set trees = states('sensor.pollenpal_tree_pollen_level') %}
          {% set weeds = states('sensor.pollenpal_weed_pollen_level') %}
          Grass: {{ grass }}, Trees: {{ trees }}, Weeds: {{ weeds }}
        attributes:
          location: "{{ state_attr('sensor.pollenpal_grass_pollen_level', 'location') }}"
          advice: "{{ state_attr('sensor.pollenpal_pollen_alert_level', 'advice') }}"
```

## API Requirements

This integration requires a running PollenPal API instance. You can:

1. **Self-host**: Follow the [PollenPal API documentation](https://github.com/TheTrueShell/PollenPal) to set up your own instance
2. **Use existing instance**: Point to an existing PollenPal API deployment

### Supported API Endpoints

The integration uses these PollenPal API endpoints:
- `/pollen/{location}/current` - Current pollen data
- `/pollen/{location}/advice` - Health advice (optional)

## Troubleshooting

### Common Issues

**Integration not appearing**
- Ensure the `custom_components/pollenpal` folder is in the correct location
- Restart Home Assistant after installation
- Check the Home Assistant logs for any error messages

**Cannot connect to API**
- Verify the API URL is correct and accessible from Home Assistant
- Check that the PollenPal API is running and responding
- Ensure there are no firewall issues blocking the connection

**Location not found**
- Verify the location name or postcode is correct
- Try alternative spellings or nearby locations
- Check the PollenPal API directly to confirm location support

### Debug Logging

Enable debug logging by adding this to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.pollenpal: debug
```

## Data Update Frequency

The integration updates pollen data every hour (3600 seconds) by default. This frequency is appropriate for pollen data which doesn't change rapidly throughout the day.

## Privacy and Data

- This integration only communicates with your specified PollenPal API instance
- No data is sent to third parties
- Location data is only used to fetch relevant pollen information
- All communication follows Home Assistant's standard security practices

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
- Check the [troubleshooting section](#troubleshooting) above
- Review Home Assistant logs for error messages
- Open an issue on the repository with detailed information

## License

This project is open source. Please check the license file for details.

---

**Note**: This integration requires the PollenPal API to be running and accessible. Make sure to set up the API first before configuring this integration. 