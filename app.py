import streamlit as st
import os

st.title("IS THIS THE RIGHT FILE?")
st.write(f"I am running from: {os.getcwd()}")
st.write(f"I see these files: {os.listdir('.')}")
