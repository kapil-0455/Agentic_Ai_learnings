import uuid

import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph_database_integration import chatbot, retrive_threads

# <_--------------------------------generating new Thread id ----------->


def generate_new_thread_id():
    thread_id = uuid.uuid4()
    return thread_id


def reset_chat():
    thread_id = generate_new_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_thread"]:
        st.session_state["chat_thread"].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])

# <----------------------------------Session Setup --------------------->
# session state ekk dict hae jismae message history ekk key hae -> []
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# making own thread id
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_new_thread_id()

# make a new list store threads
if "chat_thread" not in st.session_state:
    st.session_state["chat_thread"] = list(retrive_threads()) # yahan sbhi threads repfresh honaee kae baad bhi dikhenghi

add_thread(st.session_state["thread_id"])


# <---------------------------Making side bar ----------------------->
st.sidebar.title("Langgraph Chat bot")

if st.sidebar.button("New Chat"):
    reset_chat()


st.sidebar.header("My conversations")

for thread_id in st.session_state["chat_thread"][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"] = thread_id

        message = load_conversation(thread_id)

        temp_messages = []
        for msg in message:
            if isinstance(msg, HumanMessage):
                role = "user"
            else:
                role = "assistant"

            temp_messages.append({'role': role, "content": msg.content})
        
        st.session_state['message_history'] = temp_messages


# <------------------------ Chat UI ------------------------->
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Type your chat")


if user_input:
    # add message to message history
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    
    # st session
    # not refresh after every ewxwcution
    CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]},
            "metadata" : {"thread_id": st.session_state["thread_id"]},
            "run_name" : "chatbot_tunrn"
    }

    with st.chat_message("assistant"):
        # genertaor expression ()iskae andar use hua
        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            )
        )

    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )
