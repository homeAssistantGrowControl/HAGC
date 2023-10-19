import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_entry_flow
from homeassistant.util import dt as dt_util

class GrowControlConfigFlow(config_entries.ConfigFlow, domain="grow_control"):
    async def async_step_user(self, user_input=None):
        errors = {}
        entities = self.hass.states.async_entity_ids()

        if user_input is not None:
            # Validate and store the user's input
            if not user_input["calendar_entity_id"]:
                errors["calendar_entity_id"] = "empty_calendar_entity_id"
            if not user_input["start_date"]:
                errors["start_date"] = "empty_start_date"
            if not user_input["end_date"]:
                errors["end_date"] = "empty_end_date"
            else:
                return self.async_create_entry(
                    title="Grow Control",
                    data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("calendar_entity_id", default=""): vol.In(entities),
                vol.Required("start_date", default=dt_util.now().isoformat()): str,
                vol.Required("end_date", default=dt_util.now().isoformat()): str,
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler()

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self):
        self.options = {}

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            # Process and save user input for options
            self.options.update(user_input)
            return self.async_create_entry(title="", data=self.options)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
        )