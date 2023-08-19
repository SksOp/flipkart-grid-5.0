
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import AgentExecutor
from utils.chat_model import agent
from utils.memory import memory, msgs
from utils.tools import tools
from utils.callbacks import add_image_links_to_assistant_response
from ui.components import sidebar, header


# set_config = config
st.set_page_config(
    page_title="Fashion Outfit Generator GenAI",
    initial_sidebar_state="expanded",
    page_icon="👗",
)


# add a AI message if there are no messages
if len(msgs.messages) == 0:
    msgs.add_ai_message(
        "How I am you fashion assistant 👋. I can help you find your next outfit.👗 ")


# function to clear memory
def clear():
    memory.clear()


# create an agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,
    # callbacks=[]
)
st_callback = StreamlitCallbackHandler(st.container())


def chatBot():

    st.info(
        "To add demo product to your purchase history use sidebar on left side.")
    st.caption("Model have only last 5 chat messages in memory.")
    for msg in msgs.messages:
        icon_type = "assistant" if msg.type == "ai" else "👤"
        content = add_image_links_to_assistant_response(
            msg.content) if msg.type == "ai" else msg.content
        st.chat_message(icon_type).write(content, unsafe_allow_html=True)

    if prompt := st.chat_input():
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            response = agent_executor.run(prompt, callbacks=[st_callback])
            st.write(add_image_links_to_assistant_response(
                response), unsafe_allow_html=True)


def main():
    header()
    chatBot()
    sidebar(clear=clear)


if __name__ == "__main__":
    main()
