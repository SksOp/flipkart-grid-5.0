import streamlit as st
import os
def header():
    st.title("Fashion Outfit Generator GenAI")

def load_css():
    css =  "ui/style.css"
    with open(css) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        