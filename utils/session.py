import streamlit as st
import openai
import string
import random


# Generate a 10 characters ID of pattern:
#   0     1     2     3     4     5     6     7     8     9
# [0-9] [0-9] [A-Z] [A-Z] [A-Z] [0-9] [0-9] [A-Z] [0-9] [A-Z]
def get_survey_id():
    survey_id = ''
    survey_id = survey_id + str(random.randint(0, 9))
    survey_id = survey_id + str(random.randint(0, 9))
    survey_id = survey_id + random.choice(string.ascii_letters)
    survey_id = survey_id + random.choice(string.ascii_letters)
    survey_id = survey_id + random.choice(string.ascii_letters)
    survey_id = survey_id + str(random.randint(0, 9))
    survey_id = survey_id + str(random.randint(0, 9))
    survey_id = survey_id + random.choice(string.ascii_letters)
    survey_id = survey_id + str(random.randint(0, 9))
    survey_id = survey_id + random.choice(string.ascii_letters)
    return survey_id


# Set up the state of this streamlit app session
def session_setup():
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    if 'response_count' not in st.session_state:
        st.session_state['response_count'] = 0

    if 'survey_id' not in st.session_state:
        st.session_state['survey_id'] = get_survey_id()

    if 'survey_finished' not in st.session_state:
        st.session_state['survey_finished'] = False

    if 'submitted_to_database' not in st.session_state:
        st.session_state['submitted_to_database'] = False

    if 'introduction' not in st.session_state:
        st.session_state['introduction'] = ''

    if 'next_page' not in st.session_state:
        st.session_state['next_page'] = False

    if 'system_instruction' not in st.session_state:
        st.session_state['system_instruction'] = """You finish your response within 512 tokens."""

    if 'submitted_input' not in st.session_state:
        st.session_state['submitted_input'] = False

    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = ""


# Save chat history
def modify_chat_history(user_input, response):
    st.session_state['chat_history'].append({
        'user_input': user_input,
        'response': response
    })