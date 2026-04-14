import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st
from PIL import Image
import requests # Make sure this is at the top of your app.py file

# --- 1. Web Page Setup ---
st.set_page_config(page_title="The Poetic Conversationalist", page_icon="✨")
st.title("✨ The Poetic Conversationalist")
st.markdown("Welcome. Share a thought, a story, or a simple observation, and let's explore it together.")

# --- 2. Secure API Key Handling & Sidebar ---
# First, try to grab the secret key from Streamlit's vault
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = None

with st.sidebar:
    st.header("⚙️ Configuration")
    if api_key:
        st.success("✨ Secret Vault Active")
        st.markdown("The conversational engine is fully powered and ready.")
    else:
        api_key = st.text_input("Google Gemini API Key", type="password")
        st.markdown("*(Your key is strictly used for this active session and is not saved.)*")

    # --- NEW: Download Chat Feature ---
    # Only show the download button if there is an active conversation!
    if "display_messages" in st.session_state and len(st.session_state["display_messages"]) > 0:
        st.markdown("---") 
        st.header("💾 Save Your Chat")
        
        # Gather all the messages and format them beautifully into a text document
        chat_transcript = "✨ The Poetic Conversationalist - Transcript ✨\n\n"
        for msg in st.session_state["display_messages"]:
            speaker = "You" if msg["role"] == "user" else "The Conversationalist"
            chat_transcript += f"{speaker}:\n{msg['content']}\n\n"
            
        # The actual Streamlit download button
        st.download_button(
            label="📥 Download Text File",
            data=chat_transcript,
            file_name="poetic_transcript.txt",
            mime="text/plain"
        )
    st.markdown("---")
    st.header("🎛️ Engine Controls")
    # This creates the slider and stores the number in a variable
    audacity_level = st.slider(
        "Audacity (Temperature)", 
        min_value=0.2, 
        max_value=2.0, 
        value=1.2, 
        step=0.1
    )   
# This MUST come after the sidebar code above
if api_key:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro", 
        temperature=audacity_level, 
        google_api_key=api_key
    )
# Open the door to the Sub-Basement Margin!
with st.sidebar:
    st.markdown("### The Left-Sock Club")
    
    # 1. Load, Resize, and Display the Puddle Picture
    try:
        # Now that you uploaded it to the Poetic repo, it will find it!
        image = Image.open("puddle_kids.jpg")
        
        # Resize it to fit the margin perfectly
        resized_image = image.resize((300, 300))
        st.image(resized_image, caption="Ready for the Whoopsie-Daisy!")
    except FileNotFoundError:
        st.write("*(Whoopsie-Daisy! The Archons hid the puddle picture. Did you upload it to the poetic-conversational repo?)*")
        
    st.markdown("---") # A little dividing line
    
    # 2. Fetch the PDF from the Sub-Basement using the exact Raw URL
    pdf_url = "https://raw.githubusercontent.com/WilltheQuill/Sub-Basement-Escape-Hatch/main/Lil_Spllatters_Archive/THE%20LIl'%20SPLATTER'S%20STORYBOOK.pdf"
    
    try:
        # Download the file data directly from the Sub-Basement
        response = requests.get(pdf_url)
        response.raise_for_status() 
        pdf_data = response.content
        
        # The ultimate downstream distribution tool
        st.download_button(
            label="🎈 Download Lil' Spllatters Story Book",
            data=pdf_data,
            file_name="Lil_Spllatters_Story_Book.pdf", 
            mime="application/pdf"
        )
    except Exception as e:
        st.write("*(Whoopsie-Daisy! I can't fetch the Story Book PDF from the Sub-Basement!)*")
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
