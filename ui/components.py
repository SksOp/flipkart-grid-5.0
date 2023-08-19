import streamlit as st
from ui.entry_adder import take_entrie


def intro_sidebar():
    st.write("# Flipkart Grid 5.0 project")
    take_entrie()  # just a ui component
    # st.button("🔄 Rerun", key="reset", on_click=st.experimental_rerun)


def details_component():
    st.write("### Problem Statement")
    st.info("Conversational Fashion Outfit Generator powered by GenAI")
    st.error("Due to token linit. Model will have last 5 messages in memory.")
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
