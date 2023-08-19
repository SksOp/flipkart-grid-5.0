import streamlit as st
from utils.model import agent,tools,memory,msgs
import pandas as pd



def take_entrie():
    st.divider()
    st.header("Custom purchase History")
    col1, col2 = st.columns(2)
    with col1:
        product = st.text_input("Enter the product name")

    with col2:
        price = st.text_input("Enter the price")

    session_state = get_session_state()
    col1, col2 = st.columns(2)   
    
    with col1:
        if st.button("➕ Add", key="add_entry"):
            try:    
                if product!="" and (price!="" and type(int(price))==int):
                    add_entry(session_state, product, int(price))
                
                   
                else:
                    st.write('<span style="color:red;">You are leaving space blank or enter the wrong price</span>', unsafe_allow_html=True)
            except:
                st.write('<span style="color:red;">Please enter the price as an integer</span>', unsafe_allow_html=True)
    with col2:
        if st.button("❌ Clear", key="clear"):
            session_state.entries = []
    display_entries(session_state)


    

    
    # Display the table of key-value pairs
    

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
    df = pd.DataFrame(session_state.entries, columns=["product_name", "price"])
    df.columns = ["Product Name", "Price"]
    id = len(df)
    # print([i+1 for i in range(id)])
    ind = [i+1 for i in range(id)]
    df.index=ind
    # Display the DataFrame using st.dataframe
    if not df.empty:
        st.dataframe(df)
    product = st.empty()
    price = st.empty()
