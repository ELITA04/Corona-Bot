from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from api_modules.fetch import get_state_data

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_give_location_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        state = tracker.get_slot('state')
        location_status = get_state_data(state)
        print(location_status)
        dispatcher.utter_message(text="Hello")

        return []
