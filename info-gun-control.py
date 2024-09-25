import streamlit as st
from utils.session import session_setup
from utils.chatbot import intro_response
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
    introduction = st.session_state['introduction']
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


if __name__ == '__main__':
    main()
