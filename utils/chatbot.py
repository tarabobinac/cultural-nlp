import streamlit as st
import openai
import requests
import os

minimum_responses = 1
warning_responses = 10
maximum_responses = 15

DEEPINFRA_TOKEN = os.getenv("DEEPINFRA_TOKEN", st.secrets["llama_api_key"])

url = "https://api.deepinfra.com/v1/openai/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {DEEPINFRA_TOKEN}"
}

def intro_response(user_input):
    data = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "messages": [
            {
                "role": "system",
                "content": """Respond with a list of pros and cons on the topic at hand."""
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        "temperature": 0.7,
        "top_p": 0.9,
        "repetition_penalty": 1,
        "max_tokens": 512
    }
    response = requests.post(url, headers=headers, json=data)
    #print(response.json()['usage']['estimated_cost'])
    return response.json()['choices'][0]['message']['content']


def request_response(user_input):
    messages = [{"role": "system", "content": st.session_state['system_instruction']},
                {"role": "assistant", "content": st.session_state["introduction"]}]

    for IO_pair in st.session_state['chat_history']:
        messages.extend(
            [
                {
                    "role": "user",
                    "content": IO_pair['user_input'],
                },
                {
                    "role": "assistant",
                    "content": IO_pair['response']
                }
            ]
        )
    messages.append({"role": "user", "content": user_input})

    data = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.9,
        "repetition_penalty": 1.1,
        "max_tokens": 512
    }

    response = requests.post(url, headers=headers, json=data)
    #print(response.json()['usage']['estimated_cost'])
    return response.json()['choices'][0]['message']['content']


def get_response(user_input):
    # User input is empty
    if user_input == '':
        return None

    # The response count has reached the maximum responses
    if st.session_state['response_count'] >= maximum_responses:
        return None

    # The survey has been finished
    if st.session_state['survey_finished']:
        return None

    # Preliminary hello input
    if user_input in ['Hello', 'hello', 'Hello!', 'Hi', 'hi', 'HI', 'Hi!']:
        return 'Hello! I am the chatbot. What can I do for you today?'

    # Show the spinner while waiting for the response
    with st.spinner('Waiting for the chatbot to respond...'):
        response = request_response(user_input)

    return response

