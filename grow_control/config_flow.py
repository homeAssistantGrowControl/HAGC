import voluptuous as vol
from datetime import timedelta
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_entry_flow
from homeassistant.util import dt as dt_util
from homeassistant.const import SERVICE_TURN_ON

class GrowControlConfigFlow(config_entries.ConfigFlow, domain="grow_control"):
    async def async_step_user(self, user_input=None):
        errors = {}
        entities = self.hass.states.async_entity_ids("calendar")

        if user_input is not None:
            # Validate and store the user's input
            if not user_input["calendar_entity_id"]:
                errors["calendar_entity_id"] = "empty_calendar_entity_id"
            if not user_input["start_date"]:
                errors["start_date"] = "empty_start_date"
            if not user_input["end_date"]:
                errors["end_date"] = "empty_end_date"
            else:
                # Create events based on user input
                await self.create_calendar_events(user_input)
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

    async def create_calendar_events(self, user_input):
        # Create events in the selected calendar entity
        calendar_entity_id = user_input["calendar_entity_id"]
        start_date: datetime | None = dt_util.parse_datetime(user_input["start_date"])
        end_date = dt_util.parse_datetime(user_input["end_date"])

        # Create events from start_date to end_date
        while start_date <= end_date:
            await self.hass.services.async_call(
                "calendar",
                "event",
                {
                    "calendar_id": calendar_entity_id,
                    "title": "Your Event Title",
                    "start": start_date.isoformat(),
                    "end": (start_date + timedelta(days=1)).isoformat(),
                },
                blocking=True
            )
            start_date += timedelta(days=1)

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
