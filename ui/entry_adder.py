import streamlit as st
import pandas as pd


def initiate_session():
    if not hasattr(st.session_state, 'entries'):
        st.session_state.entries = []
    return st.session_state


def add_entry(session_state, key, value):
    entry = {"product_name": key, "price": value}
    session_state.entries.append(entry)


def display_entries(session_state):
    initiate_session()
    df = pd.DataFrame(session_state.entries, columns=["product_name", "price"])
    df.columns = ["Product Name", "Price"]
    id = len(df)
    # print([i+1 for i in range(id)])
    ind = [i+1 for i in range(id)]
    df.index = ind
    if not df.empty:
        st.dataframe(df)
    product = st.empty()
    price = st.empty()


def take_entrie():
    st.divider()
    st.header("Custom purchase History")
    col1, col2 = st.columns(2)
    with col1:
        product = st.text_input("Enter the product name")

    with col2:
        price = st.text_input("Enter the price")

    session_state = initiate_session()
    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Add", key="add_entry"):
            try:
                if product != "" and (price != "" and type(int(price)) == int):
                    add_entry(session_state, product, int(price))

                else:
                    st.write(
                        '<span style="color:red;">You are leaving space blank or enter the wrong price</span>', unsafe_allow_html=True)
            except:
                st.write(
                    '<span style="color:red;">Please enter the price as an integer</span>', unsafe_allow_html=True)
    with col2:
        if st.button("❌ Clear", key="clear"):
            session_state.entries = []
    display_entries(session_state)
