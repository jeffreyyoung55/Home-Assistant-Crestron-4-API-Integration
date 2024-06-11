from homeassistant import config_entries
import requests

DOMAIN = "crestron_controller"

class CrestronConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Crestron Controller."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate and obtain the authkey
            try:
                auth_key = await self.hass.async_add_executor_job(
                    self._get_auth_key, user_input["base_url"], user_input["initial_token"]
                )
                user_input["auth_key"] = auth_key
                return self.async_create_entry(title="Crestron Controller", data=user_input)
            except Exception:
                errors["base"] = "auth"

        return self.async_show_form(
            step_id="user", data_schema=self._get_data_schema(), errors=errors
        )

    def _get_data_schema(self):
        from homeassistant.helpers import config_validation as cv
        import voluptuous as vol

        return vol.Schema({
            vol.Required("base_url"): cv.string,
            vol.Required("initial_token"): cv.string,
        })

    def _get_auth_key(self, base_url, initial_token):
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
