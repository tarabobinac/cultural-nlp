import streamlit as st
import openai
import string
import random
from utils.chatbot import intro_response


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
        with st.spinner("Loading..."):
            st.session_state['introduction'] = intro_response(
                """Imagine you are a person from the United States moderating a discussion about gun control. Based on 
                the cultural values from the United States, provide your communication partner with stances why an average 
                person from the United States would be pro/against gun control. You should provide information in a casual 
                style in English. Start the conversation with exactly the following prompt and the culturally-relevant 
                information:\n\n\"Good afternoon. I will be your conversation partner today in a brief discussion about gun 
                control. This discussion is an opportunity for you to learn about gun control. I want to encourage you to speak 
                freely. You are not expected to be an expert. Also, no consensus is necessary, you do not need to agree with 
                the stances I provide. My role is to facilitate your understanding of gun control across cultural viewpoints. 
                Please start off by telling us something that puzzles you about this topic.\"""")

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
