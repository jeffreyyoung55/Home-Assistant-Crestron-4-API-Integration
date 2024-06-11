import logging
import requests
from homeassistant.components.cover import CoverEntity
from homeassistant.const import STATE_CLOSED, STATE_OPEN, STATE_UNKNOWN
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta

# Logger
_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Crestron cover platform."""
    crestron_data = hass.data["crestron_controller"]
    coordinator = CrestronCoverDataUpdateCoordinator(hass, crestron_data)
    devices = coordinator.data.get("shades", [])
    if not devices:
        _LOGGER.debug("No shades found")
    else:
        _LOGGER.debug("Shades found: %s", devices)
        add_entities(CrestronCover(coordinator, shade) for shade in devices)

class CrestronCoverDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Crestron cover data."""
    def __init__(self, hass, crestron_data):
        """Initialize."""
        self.base_url = crestron_data["base_url"]
        self.auth_key = crestron_data["auth_key"]
        super().__init__(
            hass,
            _LOGGER,
            name="Crestron Cover",
            update_interval=timedelta(seconds=30),
        )
        self.data = {}

    async def _async_update_data(self):
        """Fetch data from Crestron API."""
        try:
            response = requests.get(f"{self.base_url}/cws/api/shades", headers={"Crestron-RestAPI-AuthKey": self.auth_key})
            if response.status_code != 200:
                raise UpdateFailed(f"Error fetching data: {response.status_code}")
            return response.json()
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")

class CrestronCover(CoverEntity):
    """Representation of a Crestron cover."""

    def __init__(self, coordinator, shade):
        """Initialize the cover."""
        self.coordinator = coordinator
        self._shade = shade
        self._state = STATE_UNKNOWN

    @property
    def name(self):
        """Return the name of the cover."""
        return self._shade["name"]

    @property
    def is_closed(self):
        """Return true if cover is closed, else False."""
        return self._shade["position"] == 0

    @property
    def current_cover_position(self):
        """Return current position of cover. 0 is closed, 100 is fully open."""
        return int((self._shade["position"] / 65535) * 100)

    @property
    def state(self):
        """Return the state of the entity."""
        if self.is_closed:
            return STATE_CLOSED
        elif self.current_cover_position > 0:
            return STATE_OPEN
        return STATE_UNKNOWN

    def open_cover(self, **kwargs):
        """Open the cover."""
        self._set_cover_position(65535)

    def close_cover(self, **kwargs):
        """Close the cover."""
        self._set_cover_position(0)

    def set_cover_position(self, **kwargs):
        """Move the cover to a specific position."""
        position = kwargs.get("position", 100)
        position_value = int((position / 100) * 65535)
        self._set_cover_position(position_value)

    def _set_cover_position(self, position):
        """Set the cover to a specific position."""
        try:
            payload = {"shades": [{"id": self._shade["id"], "position": position}]}
            response = requests.post(f"{self.coordinator.base_url}/cws/api/shades/SetState", headers={"Crestron-RestAPI-AuthKey": self.coordinator.auth_key}, json=payload)
            if response.status_code == 200 and response.json().get("status") == "success":
                self._shade["position"] = position
                self.coordinator.async_request_refresh()
            else:
                _LOGGER.error(f"Failed to set cover position: {response.json()}")
        except Exception as err:
            _LOGGER.error(f"Error setting cover position: {err}")

    async def async_update(self):
        """Update the entity."""
        await self.coordinator.async_request_refresh()
        for shade in self.coordinator.data["shades"]:
            if shade["id"] == self._shade["id"]:
                self._shade = shade
                break
