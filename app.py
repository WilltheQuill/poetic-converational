https://github.com/WilltheQuill/poetic-converational/blob/main/app.py# ==========================================
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
