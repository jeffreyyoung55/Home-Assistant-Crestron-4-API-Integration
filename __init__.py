import logging
import requests
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.core import HomeAssistant  # Update import to use HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "crestron_controller"
_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required("base_url"): cv.string,
                vol.Required("initial_token"): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Crestron Controller integration."""
    conf = config[DOMAIN]
    base_url = conf.get("base_url")
    initial_token = conf.get("initial_token")
    auth_key = await hass.async_add_executor_job(get_auth_key, base_url, initial_token)
    hass.data[DOMAIN] = {
        "base_url": base_url,
        "auth_key": auth_key,
    }
    return True

def get_auth_key(base_url, initial_token):
    """Obtain auth key from Crestron controller."""
    response = requests.get(f"{base_url}/cws/api/login", headers={
        "Crestron-RestAPI-AuthToken": initial_token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    if response.status_code == 200:
        return response.json().get("authkey")
    else:
        raise Exception("Failed to authenticate with Crestron controller.")
