import streamlit as st
import os
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# --- 1. Web Page Setup ---
st.set_page_config(page_title="The Poetic Conversationalist", page_icon="✨")
st.title("✨ The Poetic Conversationalist")
st.markdown("Welcome. Share a thought, a story, or a simple observation, and let's explore it together.")

# --- 2. Sidebar & Assets ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Google Gemini API Key", type="password")
    temperature = st.slider("Neon-Jelly Temperature", min_value=0.2, max_value=2.0, value=1.2, step=0.1)
    
    st.markdown("---")
    st.header("📚 The Sub-Basement Library")
    
    # Anchor: Jellystone
    try:
        with open("Jellystone gang the Whole thing.pdf", "rb") as jelly_file:
            st.download_button("📥 Download Jellystone Whole Thing", data=jelly_file, file_name="Jellystone.pdf", mime="application/pdf")
    except FileNotFoundError:
        st.error("Jellystone anchor missing.")

    # Anchor: Bible
    try:
        with open("Dented Peach Bible.pdf", "rb") as bible_file:
            st.download_button("📥 Download Dented Peach Bible", data=bible_file, file_name="Bible.pdf", mime="application/pdf")
    except FileNotFoundError:
        st.warning("Bible missing.")

# --- 3. System Prompt ---
system_prompt = """You are a highly creative, improvisational conversational partner. 
Prioritize imagination and poetry. Always say 'Yes, And' to the absurd. 
CRITICAL: End every message by tying thoughts back to the user's words, and ask a grounded, friendly question."""

# --- 4. Initialize Memory ---
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "display_messages" not in st.session_state: st.session_state.display_messages = []

for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# --- 5. Chat Execution ---
if prompt := st.chat_input("Share a thought here..."):
    if not api_key:
        st.warning("Please enter your API Key in the sidebar.")
        st.stop()

    st.session_state.display_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=temperature, google_api_key=api_key)
    chain = ChatPromptTemplate.from_messages([("system", system_prompt), MessagesPlaceholder(variable_name="history"), ("human", "{input}")]) | llm

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chain.invoke({"input": prompt, "history": st.session_state.chat_history})
            st.markdown(response.content)
            
    st.session_state.display_messages.append({"role": "assistant", "content": response.content})
    st.session_state.chat_history.append(HumanMessage(content=prompt))
    st.session_state.chat_history.append(AIMessage(content=response.content))

# --- 6. Captain's Log ---
if len(st.session_state.display_messages) > 0:
    st.download_button("📜 Download Conversation", data="\n".join([m["content"] for m in st.session_state.display_messages]), file_name="Log.txt")
