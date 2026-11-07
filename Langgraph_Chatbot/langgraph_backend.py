from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

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
