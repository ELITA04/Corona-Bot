import requests
from difflib import get_close_matches
import xml.etree.ElementTree as ET

from .list_data import states, districts


def get_state_data(state):    
    url = "https://api.covid19india.org/data.json"
    response = requests.get(url).json()
    if state == "India":
        state = "Total"

    if state == "Dadra and Nagar Haveli" or state == "Daman and Diu":
        state = "Dadra and Nagar Haveli and Daman and Diu"
    
    print(state)
    statewise_response = response['statewise']
    state_information = [s for s in statewise_response if s['state'] == state][0]
    
    return state_information
        

def check_state(state):
    state_split = state.split(' ')
    state = ' '.join([x.title() for x in state_split if x != 'and'])
    if state not in states:
        closest_match = get_close_matches(state, states, n=1, cutoff=0.6)
        if len(closest_match) < 1:
            closest_match = get_close_matches(state, states, n=1, cutoff=0.4)
            if len(closest_match) < 1:
                closest_match = get_close_matches(state, states, n=1, cutoff=0.2)
                if len(closest_match) < 1:
                    return None, False
        return closest_match[0], False
    else:
        return state, True


def get_district_data(district):    
    url = "https://api.covid19india.org/state_district_wise.json"
    response = requests.get(url).json()
    for state in response:
        if district in response[state]['districtData'].keys():
            district_response = response[state]['districtData'][district]

    return district_response
        

def check_district(district):
    district_split = district.split(' ')
    district = ' '.join([x.title() for x in district_split if x != 'and'])
    if district not in districts:
        closest_match = get_close_matches(district, districts, n=1, cutoff=0.6)
        if len(closest_match) < 1:
            closest_match = get_close_matches(district, districts, n=1, cutoff=0.4)
            if len(closest_match) < 1:
                closest_match = get_close_matches(district, districts, n=1, cutoff=0.2)
                if len(closest_match) < 1:
                    return None, False
        return closest_match[0], False
    else:
        return district, True

def get_news_links():
    '''
    Grabs the top links from WHO website
    '''
    news_link = 'https://www.who.int/rss-feeds/news-english.xml'
    repsonse = requests.get(news_link)
    tree = ET.fromstring(repsonse.text)
    links =  tree.findall('.//link')
    return links[2:7]



if __name__ == '__main__':
    closest_match = check_district('Munbai')
    print(f"Match {closest_match}")
    total = get_district_data('Mumbai')
    print(f"Total {total}")