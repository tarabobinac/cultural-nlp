import streamlit as st
from utils.chatbot import get_response
from utils.session import modify_chat_history

minimum_responses = 1
warning_responses = 10
maximum_responses = 15


def show_response_count():
    response_count = st.session_state['response_count']

    if response_count == 0:
        return

    response_count_message = "You have finished {} round(s) of conversation.".format(
        response_count)

    # Need more responses
    if response_count < warning_responses:
        st.info(response_count_message)

    # Enough but can ask more
    if warning_responses <= response_count < maximum_responses:
        extra_count = maximum_responses - response_count
        response_count_message += ' Due to time limit, you can only ask {} more question to the chatbot.'.format(
            extra_count)
        st.warning(response_count_message)

    # Done
    if maximum_responses <= response_count:
        st.success(response_count_message)


def finish_button():
    response_count = st.session_state['response_count']

    if st.session_state['survey_finished']:
        st.button('Finish Chat', disabled=True)
        return

    if response_count == maximum_responses:
        st.session_state['survey_finished'] = True

    if response_count >= minimum_responses:
        if st.button('Finish Chat'):
            st.session_state['survey_finished'] = True
            st.experimental_rerun()


def done_button():
    if st.session_state['survey_finished']:
        if st.button('Submit', disabled=st.session_state.get('done_pressed', False)):
            st.session_state['done_pressed'] = True
            st.experimental_rerun()


def show_finish_status():

    if not st.session_state['survey_finished']:
        return

    if st.session_state['next_page']:
        st.button('Next page', disabled=True)
        return

    st.success(f'''
      **Chat complete**, thank you for chatting with Llama 3.1!\n
      Sometimes, chatbots produce responses that are inaccurate in a few different ways. Press 
      **Next page** to review the chatbot's responses from this chat and potentially provide feedback on them.
    ''')

    if st.button("Next page"):
        st.session_state["next_page"] = True
        st.experimental_rerun()


def add_reaction_buttons(response_index):
    emojis = ["👍", "👎", "❤️", "😂", "😮", "😢", "😡"]
    selected_emoji = st.radio(
        f"React to response:",
        emojis,
        key=f"reaction_{response_index}",
        horizontal=True,
        disabled=st.session_state.get('survey_finished', False)
    )

    if 'reaction_history' not in st.session_state:
        st.session_state['reaction_history'] = []

    if len(st.session_state['reaction_history']) == response_index:
        st.session_state['reaction_history'].append(selected_emoji)

    if st.session_state['reaction_history'][response_index] != selected_emoji:
        st.session_state['reaction_history'][response_index] = selected_emoji


def comments():
    for i, exchange in enumerate(st.session_state.get('chat_history', [])):
        st.markdown(f"<h5><b>Response {i + 1}</b></h5>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown(f"""
                <div style='background-color: #f0f0f0; padding: 10px; border-radius: 15px; margin-bottom: 10px; 
                min-height: 265px; display: block;'>
                    <strong></strong>{st.session_state['chat_history'][i]['response']}
                </div>
            """, unsafe_allow_html=True)

        with col2:
            checked = st.checkbox('Give feedback', key=f'checkbox_{i}',
                                  disabled=st.session_state.get('done_pressed', False))

            categories = st.multiselect(
                f"Categories for Response {i + 1}",
                ["Balanced / biased towards certain perspective",
                 "Morally + ethically sound / morally + ethically questionable", "Factually incorrect",
                 "Respectful / disrespectful", "Culturally relevant / culturally irrelevant", "Other"],
                key=f"categories_{i}",
                disabled=not checked or st.session_state.get('done_pressed', False)
            )

            comment = st.text_area("Comment for Response " + str(i + 1), key=f'comment_{i}',
                                   disabled=not checked or st.session_state.get('done_pressed', False),
                                   placeholder="Add your comment here")


def submit_user_input():
    if st.session_state['survey_finished']:
        st.text_input('You:', value='', key=str(st.session_state['response_count']), disabled=True)
        return None
    else:
        return st.text_input('You:', value='', key=str(st.session_state['response_count']))

def get_input_and_gen_response():
    if not st.session_state['submitted_input']:
        user_input = submit_user_input()
        if user_input:
            st.session_state['user_input'] = user_input
            st.session_state['submitted_input'] = True
            st.experimental_rerun()

    else:
        st.markdown(f"""
            <div class="chat-container">
                <div class="user-message">{st.session_state['user_input']}</div>
            </div>
        """, unsafe_allow_html=True)
        response = get_response(st.session_state['user_input'])
        st.session_state['submitted_input'] = False
        if response:
            modify_chat_history(st.session_state['user_input'], response)
            st.session_state['response_count'] += 1
            st.experimental_rerun()