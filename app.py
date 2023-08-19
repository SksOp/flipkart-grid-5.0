
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import AgentExecutor
from utils.model import agent, tools
from utils.memory import memory, msgs
# from utils.streamlit_config import config
from ui.style import header, load_css
from ui.entry_adder import take_entrie
from utils.callbacks import add_image_links_to_assistant_response

# set_config = config
st.set_page_config(
    page_title="Fashion Outfit Generator GenAI",
    initial_sidebar_state="expanded",
    page_icon="👗",
)

# add a title and load css
header()
load_css()

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


def tab1(st):

    st.caption(
        "This is a demo of a chatbot that can help you find your next outfit.")
    st.caption("Model have only last 5 chat messages in memory.")
    for msg in msgs.messages:
        icon_type = "assistant" if msg.type == "ai" else "👤"
        content = add_image_links_to_assistant_response(
            msg.content) if msg.type == "ai" else msg.content
        st.chat_message(icon_type).write(msg.content)

    if prompt := st.chat_input():
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            response = agent_executor.run(prompt, callbacks=[st_callback])
            st.write(add_image_links_to_assistant_response(response))


def sidebar():
    st.write("Flipkart Grid 5.0 project")
    st.header("Problem Statement")
    st.info("Conversational Fashion Outfit Generator powered by GenAI")
    st.error("Due to token linit. Model will have last 5 messages in memory.")
    # st.button("🔄 Rerun", key="reset", on_click=st.experimental_rerun)
    take_entrie()
    st.button("🚫 Clear Memory", key="clear_memory", on_click=clear)
    st.header("Details")
    st.markdown("✔️ Based on Current Trends")
    st.markdown("✔️ Conversational AI")
    st.markdown("## How we are getting Current trends?")
    st.markdown("""
        We employ a sophisticated approach to identify and analyze the latest fashion trends. The process involves the following steps:

        1. **Data Collection**: We start by gathering fashion images from reputable sources like *Pinterest* and *Vogue* through web scraping.

        2. **Object Detection**: We use YOLOv8, a state-of-the-art object detection algorithm, to create bounding boxes around clothing items in the images.

        3. **Item Extraction**: The clothing items are then extracted from the images for further analysis.

        4. **Similarity Scoring**: We employ cosine similarity to find products in our database that resemble the extracted items. Each product is assigned a logarithmic score based on its similarity to the trend.

        5. **Periodic Updates**: This entire process is carried out periodically (once per month) to keep our trend insights up-to-date.
            
""")

    st.markdown("## How we are getting Conversational AI?")
    st.markdown("""
    - We are using GPT-3.5 model to generate responses. We are using [Langchain](https://python.langchain.com/) to create a conversational Agent.
    - We are storing the last 5 messages in memory and using them to generate responses.
""")

    st.markdown("""
    ## Tech Stack used:
    - [Streamlit](https://streamlit.io/)
    - [Langchain](https://python.langchain.com/)
    - [GPT-3.5](https://openai.com/blog/openai-api/)
    - [YoloV8](https://ultralytics.com/yolov8)                    
    """)


def main():
    c = st.container()
    tab1(c)
    with st.sidebar:
        sidebar()


if __name__ == "__main__":
    main()
