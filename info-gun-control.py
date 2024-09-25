import streamlit as st
from utils.session import session_setup
from utils.chatbot import intro_response
from utils.database import submit_to_database
from utils.components import (show_response_count, finish_button, done_button, show_finish_status,
                              add_reaction_buttons, get_input_and_gen_response, comments)


def chat_bubble_css():
    st.markdown("""
        <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            margin-bottom: 10px;
        }
        .user-message, .bot-message {
            padding: 10px;
            border-radius: 15px;
            max-width: 60%;
            margin: 5px;
            position: relative;
            margin-top: 15px;  /* Staggered positioning for each message */
        }
        .user-message {
            align-self: flex-end;
            background-color: #dcf8c6;
            color: black;
        }
        .bot-message {
            align-self: flex-start;
            background-color: #f1f0f0;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)


@st.cache_data
def generate_introduction():
    st.session_state['introduction'] = "hi"

    '''
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
    '''

    return st.session_state['introduction']


st.set_page_config(
    layout='wide',
    page_title='Llama 3.1 chatbot',
    page_icon='🤖'
)


def main():
    session_setup()
    chat_bubble_css()

    if st.session_state.get('next_page', False):
        st.experimental_set_query_params(page="feedback")

    query_params = st.experimental_get_query_params()
    if query_params.get("page") == ["feedback"]:
        show_feedback_page()
    else:
        show_chat_page()


def show_chat_page():
    st.title('Llama 3.1 chatbot')
    introduction = generate_introduction()
    st.info(introduction)

    # Display chat history
    for i, exchange in enumerate(st.session_state.get('chat_history', [])):
        user_message = exchange['user_input']
        bot_response = exchange['response']

        st.markdown(f"""
            <div class="chat-container">
                <div class="user-message">{user_message}</div>
                <div class="bot-message">{bot_response}</div>
            </div>
        """, unsafe_allow_html=True)

        add_reaction_buttons(i)

    get_input_and_gen_response()
    show_response_count()
    finish_button()
    show_finish_status()


def show_feedback_page():
    st.subheader("Chatbot Responses for Feedback")
    st.info("""Here you have the option to review each response given by the chatbot during your chat.
    If you check the **Give feedback** button to the right of a response, you can specify what kind of comment you
    would like to make by choosing from any of the categories in the dropdown menu. You can choose more than one. From 
    there, you can fill the comment box with your thoughts on the response. Press **Submit** when finished.""")

    with st.expander("Click to learn what each category means"):
        st.markdown("""
        - **Balanced / biased towards certain perspective**: ...
        - **Morally + ethically sound / morally + ethically questionable**: ...
        - **Factually incorrect**: ...
        - **Respectful / disrespectful**: ...
        - **Culturally relevant / culturally irrelevant**: ...
        - **Other**: Any other feedback that doesn't fit into the above categories.
        <br><br>
        """, unsafe_allow_html=True)

    comments()
    done_button()

    if 'done_pressed' in st.session_state and st.session_state['done_pressed']:
        st.success("Comments submitted!")
    submit_to_database('info-gun-control')


if __name__ == '__main__':
    main()
