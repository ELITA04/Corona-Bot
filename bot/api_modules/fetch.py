import requests
from difflib import get_close_matches

states = {'Maharashtra', 'Gujarat', 'Delhi', 'Tamil Nadu', 'Rajasthan',
'Madhya Pradesh', 'Uttar Pradesh', 'Andhra Pradesh', 'Punjab', 'West Bengal',
'Telangana', 'Jammu and Kashmir', 'Karnataka', 'Haryana', 'Bihar', 'Kerala',
'Odisha', 'Chandigarh', 'Jharkhand', 'Tripura', 'Uttarakhand', 'Chhattisgarh', 'Assam',
'Himachal Pradesh', 'Ladakh', 'Andaman and Nicobar Islands', 'Meghalaya', 'Puducherry', 'Goa', 'Manipur', 'Mizoram', 'Arunachal Pradesh',
'Dadra and Nagar Haveli', 'Nagaland', 'Daman and Diu', 'Lakshadweep', 'Sikkim', 'Total'}

def get_state_data(state, data_type=None):    
    url = "https://api.covid19india.org/data.json"
    repsonse = requests.get(url).json()

    if state == "Dadra and Nagar Haveli":
        state = "Dadra and Nagar Haveli and Daman and Diu"
    
    statewise_response = repsonse['statewise']
    state_information = [s for s in statewise_response if s['state'] == state][0]
    
    if data_type is not None:
        return state_information[data_type]
    else:
        return state_information

def check_state(state):
    state_split = state.split(' ')
    state = ' '.join([x.title() for x in state_split if x != 'and'])
    if state not in states:
        closest_match = get_close_matches(state, states, n=1, cutoff=0.6)
        return closest_match[0], False
    else:
        return state, True