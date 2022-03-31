# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk.events import FollowupAction, SlotSet, UserUttered, EventType
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slot_events = []
        intent = {"intent": {"name": "activate_my_form", "confidence": 1.0}}
        utter_event = UserUttered("activate my form", intent)
        slot_events.append(utter_event)
        # slot_events.append(FollowupAction(name=""))
        # self.logger.info("SETTING SETTING ftux_trigger")
        # slot_events.append(SlotSet(key="my_form_trigger", value=True))
        dispatcher.utter_message(text="Hello World!")
        return slot_events


class ValidateSlots(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""

        return "validate_my_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        # always validate and extract without entities
        slot_to_simulate = SlotSet("my_slot", "FAKE ENTITY EXTRACTION")
        return [slot_to_simulate]