## start conversation
* start
    - utter_aboutus
    - utter_help
* other
	- utter_fallback

## ask for overall corona details
* greet
    - utter_greet
* enter_state
    - state_status_form
    - form{"name": "state_status_form"}
    - form{"name": null}
* thanks
    - utter_welcome_and_safety_instructions

## Wrong entry positive end happy
* greet
    - utter_greet
* enter_state{"state": "gao"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Goa"}
    - slot{"validated": null}
    - slot{"requested_slot": "validated"}
* affirm
    - utter_did_that_help
* affirm
    - utter_happy_to_help

## Wrong entry positive end sad
* greet
    - utter_greet
* enter_state{"state": "gao"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Goa"}
    - slot{"validated": null}
    - slot{"requested_slot": "validated"}
* affirm
    - utter_did_that_help
* deny
    - utter_will_do_better

## Correct entry positive end happy
* greet
    - utter_greet
* enter_state{"state": "maharashtra"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Maharashtra"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_did_that_help
* affirm
    - utter_happy_to_help

## Correct entry positive end sad
* greet
    - utter_greet
* enter_state{"state": "maharashtra"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Maharashtra"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_did_that_help
* deny
    - utter_will_do_better

## Wrong then right then say thanks end happy
* greet
    - utter_greet
* enter_state{"state": "naggland"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Nagaland"}
    - slot{"validated": null}
    - slot{"requested_slot": "validated"}
* form: deny
    - form: state_status_form
    - slot{"validated": false}
    - slot{"state": null}
    - slot{"validated": null}
    - form{"name": null}
    - slot{"requested_slot": null}
* enter_state{"state": "nagaland"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Nagaland"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_did_that_help
* affirm
    - utter_happy_to_help

## Wrong then right then say thanks end sad
* greet
    - utter_greet
* enter_state{"state": "naggland"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Nagaland"}
    - slot{"validated": null}
    - slot{"requested_slot": "validated"}
* form: deny
    - form: state_status_form
    - slot{"validated": false}
    - slot{"state": null}
    - slot{"validated": null}
    - form{"name": null}
    - slot{"requested_slot": null}
* enter_state{"state": "nagaland"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Nagaland"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_did_that_help
* deny
    - utter_will_do_better

## provide precautionary measures affirm
* greet
    - utter_greet
* ask_precautions
    - action_provide_precautions
    - utter_did_that_help
* affirm
    - utter_happy_to_help

## provide precautionary measures deny
* greet
    - utter_greet
* ask_precautions
    - action_provide_precautions
    - utter_did_that_help
* deny
    - utter_will_do_better

## todays news updates
* greet
    - utter_greet
* ask_news
    - action_news_updates
* thanks
    - utter_welcome_and_safety_instructions

## ask news update
* greet
    - utter_greet
* ask_news
    - action_news_updates

## ask india death rate
* greet
    - utter_greet
* deaths
    - action_get_death_rate_of_india
* thanks
    - utter_welcome_and_safety_instructions

## ask india confirmed cases
* greet
    - utter_greet
* confirmed
    - action_get_confirmed_cases_of_india
* thanks
    - utter_welcome_and_safety_instructions

## ask india recovered cases
* greet
    - utter_greet
* recovered
    - action_get_recovered_cases_of_india
* thanks
    - utter_welcome_and_safety_instructions

## ask india active cases
* greet
    - utter_greet
* active
    - action_get_active_cases_of_india
* thanks
    - utter_welcome_and_safety_instructions

## interactive story enter state 1
* enter_state
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"requested_slot": "state"}

## interactive story enter state affirm 1
* enter_state{"state": "assam"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Assam"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - slot{"status": null}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_did_that_help
* affirm
    - utter_happy_to_help
* recovered+enter_state{"state": "assam"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"status": "recovered"}
    - slot{"state": "Assam"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - slot{"status": null}
    - form{"name": null}
    - slot{"requested_slot": null}

## interactive_story_enter_state_multiple_1
* deaths+enter_state{"state": "assam"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"status": "deaths"}
    - slot{"state": "Assam"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - slot{"status": null}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_did_that_help
* affirm
    - utter_happy_to_help
* enter_state{"state": "assam"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Assam"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - slot{"status": null}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_did_that_help
* affirm
    - utter_happy_to_help

## interactive_story_deaths_and_enter_state_1
* greet
    - utter_greet
* deaths
    - action_get_death_rate_of_india
* enter_state{"state": "madhya pradesh"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Madhya Pradesh"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - slot{"status": null}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_did_that_help

## interactive_story_large_story_1
* greet
    - utter_greet
* enter_state{"state": "sikkim"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Sikkim"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - slot{"status": null}
    - form{"name": null}
    - slot{"requested_slot": null}
* enter_state{"state": "arunachal pradesh"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Arunachal Pradesh"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - slot{"status": null}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_did_that_help
* confirmed+enter_state{"state": "arunachal pradesh"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Arunachal Pradesh"}
    - slot{"validated": true}
    - slot{"requested_slot": "status"}
* form: enter_state{"state": "puducherry"}
    - form: state_status_form
    - slot{"state": "Puducherry"}
    - slot{"validated": true}
    - slot{"requested_slot": "status"}
    - utter_welcome_and_safety_instructions

## interactive_story_enter_state_2
* enter_state{"state": "india"}
    - state_status_form

## interactive_story_ask_news_1
* ask_news

## interactive_story_enter_state_3
* enter_state{"state": "india"}
    - state_status_form

## interactive_story_enter_state_4
* enter_state{"state": "india"}
    - state_status_form
    - utter_did_that_help

## interactive_story_stop_1
* stop

## interactive_story_large_story_2
* enter_state{"state": "india"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "India"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - slot{"status": null}
    - form{"name": null}
    - slot{"requested_slot": null}
* active{"state": "india"}
    - action_get_active_cases_of_india
* enter_state{"state": "tamil nadu"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"state": "Tamil Nadu"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - slot{"status": null}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_did_that_help
* recovered+enter_state{"state": "tamil nadu"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"status": "recovered"}
    - slot{"state": "Tamil Nadu"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - slot{"status": null}
    - form{"name": null}
    - slot{"requested_slot": null}

## interactive_story_multiple_2
* recovered+enter_state{"state": "tamil nadu"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"status": "recovered"}
    - slot{"state": "Tamil Nadu"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - slot{"status": null}
    - form{"name": null}
    - slot{"requested_slot": null}
* enter_state{"state": "rajasthan"}
    - utter_did_that_help
* thanks
    - utter_welcome_and_safety_instructions
* recovered+enter_state{"state": "uttar pradesh"}
    - state_status_form
    - form{"name": "state_status_form"}
    - slot{"status": "recovered"}
    - slot{"state": "Uttar Pradesh"}
    - slot{"validated": true}
    - slot{"state": null}
    - slot{"validated": null}
    - slot{"status": null}
    - form{"name": null}
    - slot{"requested_slot": null}

## Long Story

* greet
    - utter_greet
* help_me
    - utter_help
* enter_state{"state":"india"}
    - state_status_form
    - form{"name":"state_status_form"}
    - slot{"state":"India"}
    - slot{"validated":true}
    - slot{"state":null}
    - slot{"validated":null}
    - slot{"status":null}
    - form{"name":null}
    - slot{"requested_slot":null}
* help_me
    - utter_help
* deaths
    - action_get_death_rate_of_india
    - utter_did_that_help
* deny
    - utter_will_do_better
* active+enter_state{"state":"Kerala"}
    - state_status_form
    - utter_did_that_help
* thanks
    - utter_welcome_and_safety_instructions

## Issue with deaths

* deaths
    - action_get_death_rate_of_india
    - utter_did_that_help

## Recovered and Deaths

* recovered
    - action_get_recovered_cases_of_india
* deaths
    - action_get_death_rate_of_india
    - utter_did_that_help

## Start Conversation 2

* start
    - utter_aboutus
    - utter_help
