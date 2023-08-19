
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory

msgs = StreamlitChatMessageHistory()
"""
A streamlit session based memory
"""

memory = ConversationBufferWindowMemory(
    return_messages=True,
    k=5,
    memory_key="history",
    chat_memory=msgs
)
