import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph_backend import chatbot

# st session 
# not refresh after every ewxwcution 
CONFIG = {'configurable' : {'thread_id' : 'thread-1'}}

# session state ekk dict hae jismae message history ekk key hae -> []
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type your chat')

if user_input:
    # add message to message history 
    st.session_state['message_history'].append({'role' : 'user' , 'content' : user_input })
    with st.chat_message('user'):
        st.text(user_input)


    with st.chat_message('assistant'):
    # genertaor expression ()iskae andar use hua 
        ai_message = st.write_stream(
            message_chunk.content for message_chunk , metadata in chatbot.stream(
                {'messages' : [HumanMessage(content=user_input)]},
                config = {'configurable' : {'thread_id' : 'thread-1'}},
                stream_mode = 'messages'
            )
        )

    st.session_state['message_history'].append({'role' : 'assistant' , 'content' : ai_message })
    
