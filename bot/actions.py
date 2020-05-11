from typing import Any, Text, Dict, List

from rasa_sdk import Tracker
from rasa_sdk.forms import FormAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from api_modules.fetch import get_state_data, check_state, get_news_links


########################## State Form ##########################
class StateStatusForm(FormAction):
    def name(self) -> Text:
        return "state_status_form"

    # Returns the type of intent
    @staticmethod
    def get_form_type(tracker):
        return tracker.active_form.get("trigger_message", {}).get("intent", {}).get("name") or tracker.latest_message.get("intent", {}).get("name")

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        # Validated is if the state is entered with correct name
        form_type = StateStatusForm.get_form_type(tracker)
        if form_type == 'enter_state':
            return ['state', 'validated']

        return ['status', 'state', 'validated']

    def slot_mappings(self):
        # Based on the users inputs from where to map
        return {
            'status': [
                    self.from_trigger_intent(intent="recovered", value="recovered"),
                    self.from_trigger_intent(intent="recovered+enter_state", value="recovered"),
                    self.from_trigger_intent(intent="active", value="active"),
                    self.from_trigger_intent(intent="active+enter_state", value="active"),
                    self.from_trigger_intent(intent="deaths", value="deaths"),
                    self.from_trigger_intent(intent="deaths+enter_state", value="deaths"), 
                    self.from_intent(intent="confirmed", value="confirmed"),
                    self.from_intent(intent="confirmed+enter_state", value="confirmed"),
                ],
            'state': self.from_entity(entity='state'),
            'validated': [
                    self.from_intent(intent="affirm", value=True),
                    self.from_intent(intent="deny", value=False)
                ]
            }

    def validate_state(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        # Check if the state is entered with its correct values
        # If value entered is correct then proceed with fetching status
        # If value does not match then ask if it is the closest match
        state_status, validated = check_state(value)
        if not validated:
            output = f"Did you mean {state_status}?"
            dispatcher.utter_message(output)
            return {'state': state_status, 'validated': None}
        else:
            return {'state': state_status, 'validated': True}

    def validate_validated(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        # Set the validated value so that the form can proceed
        if not value:
            return {"validated": value}
        return {"validated": value}

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Run the form to output details to user
        validated = tracker.get_slot('validated')
        if validated:
            dispatcher.utter_message(template='utter_finding_info')
            state = tracker.get_slot('state')
            current_intent = tracker.get_slot('status')
            state_status = get_state_data(state)
            output = self.__prepare_message(state_status, current_intent)
            dispatcher.utter_message(text=output)
        else:
            dispatcher.utter_message(template='utter_apologies')

        return [SlotSet('state', None), SlotSet('validated', None), SlotSet('status', None)]
    
    def __prepare_message(self, status, intent=None):
        # Prepare details based on information
        output = f'Here are the details for {status["state"]}\n'
        if intent == "active" or intent is None:
            output += f'There are currently {status["active"]} active cases\n'
        if intent == "confirmed" or intent is None:
            output += f'There are currently {status["confirmed"]} confirmed cases\n'
        if intent == "deaths" or intent is None:
            output += f'There are currently {status["deaths"]} reports of death\n'
        if intent == "recovered" or intent is None:
            output += f'There are currently {status["recovered"]} recovered cases\n'
        output += f'This data was last updated on {status["lastupdatedtime"]}\n'
        if status['statenotes'] != '':
            output += f'Extra Notes: {status["statenotes"]}\n'
        return output

########################## Precaution Action ##########################
class PrecautionMessage(Action):
    def name(self) -> Text:
        return "action_provide_precautions"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        output = ''
        output = '1. STAY at home\n'
        output += '2. KEEP a safe distance\n'
        output += '3. WASH your hands often\n'
        output += '4. COVER your mouth while coughing\n'
        output += '5. SICK? Call the helpline'
        dispatcher.utter_message(output)

        return []

########################## News Action ##########################
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
