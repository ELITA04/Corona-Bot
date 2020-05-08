import requests

url = "https://api.covid19india.org/data.json"

repsonse = requests.get(url).json()

state = "Tamil Nadu"
statewise_response = repsonse['statewise']
state_information = [s for s in statewise_response if s['state'] == state][0]
print(state_information)