from typing import Any, Text, Dict, List

from rasa_sdk import Tracker
from rasa_sdk.forms import FormAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from api_modules.fetch import get_state_data, check_state, get_district_data, check_district, get_news_links

REQUESTED_SLOT = "requested_slot"

########################## State Form ##########################
class StateStatusForm(FormAction):
    '''
    A form to fetch details for a particular state.
    '''
    def name(self) -> Text:
        return "state_status_form"

    # Returns the type of intent
    @staticmethod
    def get_form_type(tracker):
        return tracker.active_form.get("trigger_message", {}).get("intent", {}).get("name") or tracker.latest_message.get("intent", {}).get("name")

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        '''
        Validated is if the state is entered with correct name
        '''
        form_type = StateStatusForm.get_form_type(tracker)
        if form_type == 'enter_state':
            return ['state', 'validated']

        return ['status', 'state', 'validated']

    def slot_mappings(self):
        '''
        Based on the users inputs from where to map
        '''
        return {
            'status': [
                    self.from_trigger_intent(intent="recovered+enter_state", value="recovered"),
                    self.from_trigger_intent(intent="active+enter_state", value="active"),
                    self.from_trigger_intent(intent="deaths+enter_state", value="deaths"), 
                    self.from_trigger_intent(intent="confirmed+enter_state", value="confirmed"),
                ],
            'state': self.from_entity(entity='state'),
            'validated': [
                    self.from_intent(intent="affirm", value=True),
                    self.from_intent(intent="deny", value=False)
                ]
            }

    def request_next_slot(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        '''
        Error handling to deactivate form incase of unknown entities
        '''
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):

                ## Condition of validated slot that triggers deactivation
                print(slot, tracker.get_slot("state"))
                if slot == "validated" and tracker.get_slot("state") == "Invalid":
                    dispatcher.utter_message(template='utter_fallback')
                    return self.deactivate()
                ## For all other slots, continue as usual
                return [SlotSet(REQUESTED_SLOT, slot)]
        return None
    
    def validate_state(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        '''
        Check if the state is entered with its correct values
        If value entered is correct then proceed with fetching status
        If value does not match then ask if it is the closest match
        '''
        state_status, validated = check_state(value)
        if state_status is None:
            return {'state': 'Invalid'}
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
        '''
        Prepares string based on information asked
        '''
        state_name = "India" if status["state"] == "Total" else status["state"]
        output = f'Here are the details for {state_name}\n'
        if intent == "active" or intent is None:
            output += f'There are currently {status["active"]} active cases\n'
        if intent == "confirmed" or intent is None:
            output += f'There are currently {status["confirmed"]} confirmed cases (delta change: {status["deltaconfirmed"]}).\n'
        if intent == "deaths" or intent is None:
            output += f'There are currently {status["deaths"]} reports of death (delta change: {status["deltadeaths"]}).\n'
        if intent == "recovered" or intent is None:
            output += f'There are currently {status["recovered"]} recovered cases (delta change: {status["deltarecovered"]}).\n'
        output += f'This data was last updated on {status["lastupdatedtime"]}\n'
        if status['statenotes'] != '':
            extra = status["statenotes"].replace("<br>", "").replace("- ", "")
            extra_arr = extra.splitlines(True)
            notes = ''
            # Hack to avoid points on date
            for e in extra_arr:
                if e[0] == '[':
                    notes += e
                elif len(e) > 1:
                    notes += '- ' + e 
            output += f'Extra Notes:\n{notes}\n'
        return output

########################## District Form ##########################

class DistrictStatusForm(FormAction):
    '''
    A form to fetch details for a particular district.
    '''
    def name(self) -> Text:
        return "district_status_form"

    # Returns the type of intent
    @staticmethod
    def get_form_type(tracker):
        return tracker.active_form.get("trigger_message", {}).get("intent", {}).get("name") or tracker.latest_message.get("intent", {}).get("name")

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        '''
        Validated is if the district is entered with correct name
        '''
        form_type = DistrictStatusForm.get_form_type(tracker)
        if form_type == 'enter_district':
            return ['district', 'validated']

        return ['status', 'district', 'validated']

    def slot_mappings(self):
        '''
        Based on the users inputs from where to map
        '''
        return {
            'status': [
                    self.from_trigger_intent(intent="recovered+enter_district", value="recovered"),
                    self.from_trigger_intent(intent="active+enter_district", value="active"),
                    self.from_trigger_intent(intent="deaths+enter_district", value="deaths"), 
                    self.from_trigger_intent(intent="confirmed+enter_district", value="confirmed"),
                ],
            'district': self.from_entity(entity='district'),
            'validated': [
                    self.from_intent(intent="affirm", value=True),
                    self.from_intent(intent="deny", value=False)
                ]
            }

    def request_next_slot(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        '''
        Error handling to deactivate form incase of unknown entities
        '''
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):

                ## Condition of validated slot that triggers deactivation
                print(slot, tracker.get_slot("district"))
                if slot == "validated" and tracker.get_slot("district") == "Invalid":
                    dispatcher.utter_message(template='utter_fallback')
                    return self.deactivate()
                ## For all other slots, continue as usual
                return [SlotSet(REQUESTED_SLOT, slot)]
        return None

    
    def validate_district(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        '''
        Check if the district is entered with its correct values
        If value entered is correct then proceed with fetching status
        If value does not match then ask if it is the closest match
        '''
        district_status, validated = check_district(value)
        if district_status is None:
            return {'district': 'Invalid'}
        if not validated:
            output = f"Did you mean {district_status}?"
            dispatcher.utter_message(output)
            return {'district': district_status, 'validated': None}
        else:
            return {'district': district_status, 'validated': True}

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
            district = tracker.get_slot('district')
            current_intent = tracker.get_slot('status')
            district_status = get_district_data(district)
            output = self.__prepare_message(district, district_status, current_intent)
            dispatcher.utter_message(text=output)
        else:
            dispatcher.utter_message(template='utter_apologies')

        return [SlotSet('district', None), SlotSet('validated', None), SlotSet('status', None)]
    
    def __prepare_message(self, district, status, intent=None):
        '''
        Prepares string based on information asked
        '''
        output = f'Here are the details for {district}\n'
        if intent == "active" or intent is None:
            output += f'There are currently {status["active"]} active cases\n'
        if intent == "confirmed" or intent is None:
            output += f'There are currently {status["confirmed"]} confirmed cases (delta change: {status["delta"]["confirmed"]}).\n'
        if intent == "deaths" or intent is None:
            output += f'There are currently {status["deceased"]} reports of death (delta change: {status["delta"]["deceased"]}).\n'
        if intent == "recovered" or intent is None:
            output += f'There are currently {status["recovered"]} recovered cases (delta change: {status["delta"]["recovered"]}).\n'
        if status['notes'] != '':
            output += f'Extra Notes:\n{status["notes"]}\n'
        return output



class PrecautionMessage(Action):
    '''
    Actions to take for precautions
    '''
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

class GetNews(Action):
    '''
    Actions to be taken for getting news links from WHO website
    '''
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

class DeathRate(Action):
    '''
    Actions to be taken for getting death rate in India
    '''
    def name(self) -> Text:
        return "action_get_death_rate_of_india"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        total = get_state_data('Total')
        output = f"The number of deaths in India are {total['deaths']}\n"
        output += f'This data was last updated on {total["lastupdatedtime"]}\n'
        dispatcher.utter_message(output)
        return []

class RecoveredRate(Action):
    '''
    Actions to be taken for getting recovered cases in India
    '''
    def name(self) -> Text:
        return "action_get_recovered_cases_of_india"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        total = get_state_data('Total')
        output = f"The  number of people recovered in India are {total['recovered']}\n"
        output += f'This data was last updated on {total["lastupdatedtime"]}\n'
        dispatcher.utter_message(output)
        return []

class ConfirmedCases(Action):
    '''
    Actions to be taken for getting confirmed cases in India
    '''
    def name(self) -> Text:
        return "action_get_confirmed_cases_of_india"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        total = get_state_data('Total')
        output = f"The  number of confirmed cases in India are {total['confirmed']}\n"
        output += f'This data was last updated on {total["lastupdatedtime"]}\n'
        dispatcher.utter_message(output)
        return []

class ActiveCases(Action):
    '''
    Actions to be taken for getting active cases in India
    '''
    def name(self) -> Text:
        return "action_get_active_cases_of_india"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        total = get_state_data('Total')
        output = f"The  number of active cases in India are {total['active']}\n"
        output += f'This data was last updated on {total["lastupdatedtime"]}\n'
        dispatcher.utter_message(output)
        return []