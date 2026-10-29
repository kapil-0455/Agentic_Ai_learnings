from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model = "openai/gpt-oss-120b")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage] , add_messages]

def chat_node(state : ChatState):
    message = state['messages']

    response = llm.invoke(message)
    return {'messages' : [response]}

checkpointer = InMemorySaver()

graph = StateGraph(ChatState)

graph.add_node('chat_node' , chat_node)
graph.add_edge(START , 'chat_node')
graph.add_edge('chat_node' , END)

chatbot = graph.compile(checkpointer = checkpointer)
