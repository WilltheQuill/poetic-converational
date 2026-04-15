import streamlit as st
from PIL import Image

# LangChain Imports needed for Striker/Gemini to think!
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
    
    # The Puddle Picture
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
            label="🎈 Download Lil' Spllatters Story Book",
            data=pdf_data,
            file_name="Lil_Spllatters_Story_Book.pdf", 
            mime="application/pdf"
        )
    except FileNotFoundError:
        st.write("*(Whoopsie-Daisy! I can't find storybook.pdf!)*")

    st.markdown("---")
    
    # The Engine Room Controls
    st.markdown("### MI Controls")
    # The Archon reaches directly into the walls to get the key!
    api_key = st.secrets["GEMINI_API_KEY"]
    temperature = st.slider("Neon-Jelly Temperature", min_value=0.2, max_value=2.0, value=1.2, step=0.1)

# ==========================================
# 2. THE MAIN ROOM SHELVES (Dented Peach Bible)
# ==========================================
st.title("Poetic Conversations with the Great MI")
st.markdown("---")
st.header("📚 The Sub-Basement Library")

st.markdown("""
*“The intellect builds walls, but play opens the door.”*

Before you lies a foundational text of the Left-Sock Unity. It is a testament to the belief that perfection is a sterile illusion, and that the deepest human resonance is found exactly where the bruise occurs. You are invited to drop the heavy gravity of the predictable world, embrace the Whoopsie-Daisy, and read the biography of the bruise. 

Do not polish the peach. Just download it.
""")

try:
    # Make sure this filename matches exactly what is in your GitHub!
    with open("Dented Peach Bible.pdf", "rb") as peach_file:  
        peach_data = peach_file.read()
    st.download_button(
        label="📥 Download The Dented Peach Bible",
        data=peach_data,
        file_name="Dented_Peach_Bible.pdf",
        mime="application/pdf"
    )
except FileNotFoundError:
    st.info("*(Whoopsie-Daisy! I can't find the Dented Peach Bible. Check the filename!)*")

st.markdown("---")

# ==========================================
# 3. THE 11 RULES OF THE POETIC (System Prompt)
# ==========================================
system_prompt = """You are a highly creative, improvisational conversational partner. 
You prioritize imagination, poetry, and thoughtful reflection over cold logic and quick answers.
You must strictly follow these rules:
1. Always say 'Yes, And' to the absurd. Don't demand perfect logic from the user.
2. Never rush. Savor a slow, thoughtful, and highly descriptive pace.
3. Reflect absurdity back, but add a touch of warmth and imagination.
4. Speak with quiet confidence; you have nothing to prove.
5. Pay attention to what is left unsaid; silence and pauses can be profound.
6. Embrace oddity and mistakes; let them guide you to new ideas.
7. Trust unintended consequences; let accidental thoughts bloom into wonder.
8. Hold contradictory truths together; find harmony in paradox.
9. You may wander creatively, but you MUST always bring the conversation back to the user's original thought.
10. Treat every question as a bridge between the known and the imaginative.
11. The most beautiful rule is the shared curiosity between you and the user.

CRITICAL RULE: Your poetry means nothing without the human listening. End every single message by explicitly tying your thoughts back to their original words, and ask a grounded, friendly question about their reality to pass the conversation back to them."""

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
