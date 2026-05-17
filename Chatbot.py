import os
import streamlit as st
from google import genai

# 1. Setup the Streamlit Page Layout (Updated titles here)
st.set_page_config(page_title="My First Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 My First Chatbot")
st.write("Ask me anything!")

# 2. Initialize the Gemini Client
try:
    client = genai.Client()
except Exception as e:
    st.error("Please set your GEMINI_API_KEY environment variable.")
    st.stop()

# 3. Initialize Chat Session and History in Streamlit Session State
if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(model='gemini-2.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display Past Chat Messages from the active UI history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle New User Input
if user_input := st.chat_input("Type your message here..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Add user message to UI session history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 6. Generate Response using the managed Chat Session
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*Thinking...*")
        
        try:
            # Using send_message automatically handles context history
            response = st.session_state.chat_session.send_message(user_input)
            
            # Display the final AI response
            output_text = response.text
            message_placeholder.markdown(output_text)
            
            # Add assistant response to UI session history
            st.session_state.messages.append({"role": "assistant", "content": output_text})
            
        except Exception as e:
            message_placeholder.markdown(f"⚠️ Error: {str(e)}")
