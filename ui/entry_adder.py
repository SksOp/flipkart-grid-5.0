import streamlit as st
import pandas as pd


def take_entrie():
    # st.set_page_config(layout="wide")
    st.divider()

    st.header("Custom purchase History")
    col1, col2 = st.columns(2)
    with col1:
        product = st.text_input("Enter the product name")
    with col2:
        price = st.text_input("Enter the price")
    session_state = get_session_state()
    col1, col2 = st.columns(2)

    def callback_to_add_entry():
        add_entry(session_state, product, price)

    def callback_to_clear_entries():
        session_state.entries = []

    with col1:
        st.button("➕ Add", key="add_entry", on_click=callback_to_add_entry)
    with col2:
        st.button("❌ Clear", key="clear", on_click=callback_to_clear_entries)

    # Display the table of key-value pairs
    display_entries(session_state)
    st.divider()


def get_session_state():
    # Create a session state object if it doesn't exist
    if not hasattr(st.session_state, 'entries'):
        st.session_state.entries = []
    return st.session_state


def add_entry(session_state, key, value):
    # Append the new key-value pair as a dictionary to the session state
    entry = {"product_name": key, "price": value}
    session_state.entries.append(entry)


def display_entries(session_state):
    get_session_state()
    # Display the table using st.table
    df = pd.DataFrame(session_state.entries)
    id = len(df)
    # print([i+1 for i in range(id)])
    ind = [i+1 for i in range(id)]
    df.index = ind
    # Display the DataFrame using st.dataframe
    if not df.empty:
        st.dataframe(df)
