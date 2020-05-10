from typing import Any, Text, Dict, List

from rasa_sdk import Tracker
from rasa_sdk.forms import FormAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from api_modules.fetch import get_state_data, check_state, get_news_links

class StateForm(FormAction):

    def name(self) -> Text:
        return "state_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ['state', 'validated']

    def slot_mappings(self):
        return {'state': self.from_entity(entity='state'),
                'validated': [self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False)]
            }

    def validate_state(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        print("Validate state", value)
        state_status, validated = check_state(value)
        if not validated:
            output = f"Did you mean {state_status}?"
            dispatcher.utter_message(output)
            return {'state': state_status, 'validated': None}
        else:
            return {'state': state_status, 'validated': True}

    def validate_validated(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        print("Validate validated", value)
        if not value:
            return {"validated": value}
        return {"validated": value}

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        validated = tracker.get_slot('validated')
        if validated:
            dispatcher.utter_message(template='utter_finding_info')
            state = tracker.get_slot('state')
            state_status = get_state_data(state)
            output = self.__prepare_message(state_status)
            dispatcher.utter_message(text=output)
        else:
            dispatcher.utter_message(template='utter_apologies')

        return [SlotSet('state', None), SlotSet('validated', None)]

    def __prepare_message(self, status):
        output = f'Here are the details for {status["state"]}\n'
        output += f'There are currently {status["active"]} active cases\n'
        output += f'There are currently {status["confirmed"]} confirmed cases\n'
        output += f'There are currently {status["deaths"]} reports of death\n'
        output += f'This data was last updated on {status["lastupdatedtime"]}\n'
        if status['statenotes'] != '':
            output += f'Extra Notes: {status["statenotes"]}\n'
        return output

    class PrecautionMessage(Action):
        def name(self) -> Text:
            return "action_provide_precautions"

        def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            output = ""
            output = '1. STAY at home\n'
            output += '2. KEEP a safe distance\n'
            output += '3. WASH your hands often\n'
            output += '4. COVER your mouth while coughing\n'
            output += '5. SICK? call the helpline'
            dispatcher.utter_message(output)

            return []

    class GetNews(Action):
        def name(self) -> Text:
            return "action_news_updates"

        def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            links = get_news_links()
            output = ''
            output += 'Here are a list of WHO links with the latest updates\n'
            for link in links:
                output += link.text + '\n'
            dispatcher.utter_message(output)
            return []
