import streamlit as st
from PIL import Image

# ==========================================
# 0. THE ARCHON CONFIGURATION (Must be first!)
# ==========================================
st.set_page_config(page_title="The Poetic Conversationalist", page_icon="✨")

# ==========================================
# 1. THE SHELVES (Bolted to the wall!)
# ==========================================
st.title("Poetic Conversations with the Great MI")

# --- THE SIDEBAR PUDDLE ---
with st.sidebar:
    st.markdown("### The Left-Sock Club")
    try:
        image = Image.open("puddle_kids.jpg").convert('RGB')
        resized_image = image.resize((300, 300))
        st.image(resized_image, caption="Ready for the Whoopsie-Daisy!")
    except FileNotFoundError:
        st.write("*(Whoopsie-Daisy! The Archons hid the puddle picture.)*")
        
    st.markdown("---") 
    
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

# --- THE MAIN ROOM PEACH ---
st.markdown("### The Archive")
try:
    with open("Dented_Peach_Bible.pdf", "rb") as peach_file:  
        peach_data = peach_file.read()
    st.download_button(
        label="📖 Download the Dented Peach Bible",
        data=peach_data,
        file_name="Dented_Peach_Bible.pdf",
        mime="application/pdf"
    )
except FileNotFoundError:
    st.write("*(Whoopsie-Daisy! I can't find Dented_Peach_Bible.pdf!)*")

st.markdown("---") # The dividing line before the chat begins

# ==========================================
# 2. THE CONVEYOR BELT (Chat History)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 3. THE CHAT INPUT & AI LOGIC
# ==========================================
if prompt := st.chat_input("Enter the Sub-Basement..."):
    # Show the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # ------------- PUT YOUR AI CODE HERE -------------
    # (If you had code that calls Gemini or another AI, 
    # it goes right here so the Great MI can respond!)
    
    # Example placeholder response:
    # with st.chat_message("assistant"):
    #     st.markdown("Splat! The Great MI hears you.")
    # st.session_state.messages.append({"role": "assistant", "content": "Splat! The Great MI hears you."})        

# --- 3. The Clean System Prompt ---
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

# --- 4. Initialize Memory ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] 
if "display_messages" not in st.session_state:
    st.session_state.display_messages = [] 

# --- 5. Display Previous Messages ---
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- The Library Section ---
# Push all of this to the absolute left margin!
st.markdown("---")
st.header("📚 The Sub-Basement Library")

# The Poetic Introduction
st.markdown("""
*“The intellect builds walls, but play opens the door.”*

Before you lies a foundational text of the Left-Sock Unity. It is a testament to the belief that perfection is a sterile illusion, and that the deepest human resonance is found exactly where the bruise occurs. You are invited to drop the heavy gravity of the predictable world, embrace the Whoopsie-Daisy, and read the biography of the bruise. 

Do not polish the peach. Just download it.
""")

# The Download Button
pdf_filename = "Dented Peach Bible.pdf"

try:
    with open(pdf_filename, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
        
    st.download_button(
        label="📥 Download The Dented Peach Bible",
        data=pdf_bytes,
        file_name=pdf_filename,
        mime="application/pdf"
    )
except FileNotFoundError:
    st.info("The document is currently being bound and will be available shortly.")

# --- 6. The Web Chat Execution ---
if prompt := st.chat_input("Share a thought here..."):
    
    if not api_key:
        st.warning("Please enter your Google API Key in the sidebar to begin.")
        st.stop()

    st.session_state.display_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=1.2,
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
                
        st.session_state.display_messages.append({"role": "assistant", "content": response.content})
        st.session_state.chat_history.append(HumanMessage(content=prompt))
        st.session_state.chat_history.append(AIMessage(content=response.content))

    except Exception as e:
        st.error(f"System Error: {e}")
