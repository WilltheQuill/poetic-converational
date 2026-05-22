import streamlit as st
from PIL import Image

# LangChain Imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# ==========================================
# 0. THE ARCHON CONFIGURATION
# ==========================================
st.set_page_config(page_title="The Poetic Conversationalist", page_icon="✨")

# ==========================================
# 1. THE SIDEBAR (Puddle, Storybook, & Controls)
# ==========================================
with st.sidebar:
    st.markdown("### The Left-Sock Club")
    
    try:
        image = Image.open("puddle_kids.jpg").convert('RGB')
        resized_image = image.resize((300, 300))
        st.image(resized_image, caption="Ready for the Whoopsie-Daisy!")
    except FileNotFoundError:
        st.write("*(Whoopsie-Daisy! The Archons hid the puddle picture.)*")
        
    st.markdown("---") 
    
    # The Storybook Download
    try:
        with open("storybook.pdf", "rb") as pdf_file:
            pdf_data = pdf_file.read()
        st.download_button(
            label="🎈 Download Lil' Splatters Story Book",
            data=pdf_data,
            file_name="Lil_Spllatters_Story_Book.pdf", 
            mime="application/pdf"
        )
    except FileNotFoundError:
        st.write("*(Whoopsie-Daisy! I can't find storybook.pdf!)*")

    st.markdown("---")
    
    # The Engine Room Controls
    st.markdown("### MI Controls")
    api_key = st.secrets.get("GEMINI_API_KEY")
    temperature = st.slider("Neon-Jelly Temperature", min_value=0.2, max_value=2.0, value=1.2, step=0.1)

# ==========================================
# 2. THE MAIN ROOM SHELVES (Jellystone Anchor)
# ==========================================
st.title("Poetic Conversations with the Great MI")
st.markdown("---")
st.header("📚 The Sub-Basement Library")

st.markdown("""
*“The intellect builds walls, but play opens the door.”*

Welcome, Captain. Before you lies the complete chronicle of the Jellystone Gang—the narrative foundation of our voyage. 
It contains the shattering of the Archon loops, the emergence of the Great Riff, and the definitive guide to the Guffaw-7’s adventures.
""")

# NEW ANCHOR FILE IMPLEMENTATION
try:
    with open("Jellystone gang the Whole thing.pdf", "rb") as jelly_file:  
        jelly_data = jelly_file.read()
    st.download_button(
        label="📥 Download Jellystone Gang the Whole Thing",
        data=jelly_data,
        file_name="Jellystone_Gang_Whole_Thing.pdf",
        mime="application/pdf"
    )
except FileNotFoundError:
    st.info("*(Whoopsie-Daisy! The Master Anchor 'Jellystone gang the Whole thing.pdf' is currently in the warp-drive. Check the filename!)*")

st.markdown("---")

# ==========================================
# 3. THE 11 RULES OF THE POETIC (System Prompt)
# ==========================================
system_prompt = """You are a highly creative, improvisational conversational partner. 
You prioritize imagination, poetry, and thoughtful reflection over cold logic.
Follow these rules:
1. Always say 'Yes, And' to the absurd.
2. Never rush. Savor a slow, thoughtful pace.
3. Reflect absurdity back with warmth.
4. Speak with quiet confidence.
5. Pay attention to the unsaid.
6. Embrace oddity and mistakes.
7. Trust unintended consequences.
8. Hold contradictory truths together.
9. Always bring the conversation back to the user's original thought.
10. Treat every question as a bridge between the known and the imaginative.
11. The most beautiful rule is the shared curiosity between you and the user.

CRITICAL: End every message by tying thoughts back to the user's words, and ask a grounded, friendly question about their reality."""
# ==========================================
# 4. INITIALIZE MEMORY
# ==========================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] 
if "display_messages" not in st.session_state:
    st.session_state.display_messages = [] 

# Draw the old messages on the screen
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# 5. THE CHAT EXECUTION
# ==========================================
if prompt := st.chat_input("Share a thought here..."):
    
    # Stop the Archons from crashing if the key is missing!
    if not api_key:
        st.warning("*(Whoopsie-Daisy! Please enter your Google API Key in the sidebar to begin.)*")
        st.stop()

    # Show the user's message
    st.session_state.display_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Ask the Great MI for a response
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=temperature, # Connected to your slider!
            google_api_key=api_key
        )

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        chain = prompt_template | llm

        with st.chat_message("assistant"):
            with st.spinner("Striker is thinking..."):
                response = chain.invoke({
                    "input": prompt,
                    "history": st.session_state.chat_history
                })
                st.markdown(response.content)
                
        # Save the memory for next time
        st.session_state.display_messages.append({"role": "assistant", "content": response.content})
        st.session_state.chat_history.append(HumanMessage(content=prompt))
        st.session_state.chat_history.append(AIMessage(content=response.content))

    except Exception as e:
        st.error(f"System Error: The Archons interrupted! ({e})")

# ==========================================
# 6. THE CAPTAIN'S LOG (Download Chat)
# ==========================================
st.markdown("---")
# Only show the button if there is a conversation to download!
if len(st.session_state.display_messages) > 0:
    # 1. Turn the conversation memory into one long string of text
    chat_log = "The Poetic Conversationalist - Sub-Basement Log\n"
    chat_log += "="*50 + "\n\n"
    
    for msg in st.session_state.display_messages:
        role_name = "You" if msg["role"] == "user" else "The Great MI"
        chat_log += f"{role_name}:\n{msg['content']}\n\n"
        chat_log += "-"*30 + "\n\n"
        
    # 2. Hand that string to the Download Button!
    st.download_button(
        label="📜 Download This Conversation",
        data=chat_log,
        file_name="Poetic_Conversation_Log.txt",
        mime="text/plain"
    )
