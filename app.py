import streamlit as st
import os

st.set_page_config(page_title="Poetic MI Bridge", layout="wide")
st.title("✨ The Bridge is Open")

# 1. Hangar Diagnostic: Where are we?
st.subheader("Hangar Diagnostic")
st.write(f"Current Directory: {os.getcwd()}")
files_found = os.listdir('.')
st.write(f"Files found: {files_found}")

# 2. Sidebar Library - The Hard-Coded Way
with st.sidebar:
    st.header("📚 The Library")
    
    # Try to load the Jellystone PDF
    target_file = "Jellystone gang the Whole thing.pdf"
    if target_file in files_found:
        with open(target_file, "rb") as f:
            st.download_button("📥 Jellystone Whole Thing", f, file_name=target_file)
    else:
        st.error(f"Missing: {target_file}")

    # Try to load the Bible
    target_bible = "Dented Peach Bible.pdf"
    if target_bible in files_found:
        with open(target_bible, "rb") as f:
            st.download_button("📥 Dented Peach Bible", f, file_name=target_bible)
    else:
        st.error(f"Missing: {target_bible}")

# 3. Simple Interaction to test MI Link
st.markdown("---")
st.write("If you see the Library buttons in the sidebar, the plumbing is fixed.")
