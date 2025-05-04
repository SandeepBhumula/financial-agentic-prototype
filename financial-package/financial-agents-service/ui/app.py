import streamlit as st
import time
import os
from core.orchestrator import app as orchestrator_app

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Financial Agent Chat", layout="wide")
st.title("Financial Services Agent Chat")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello! How can I help you with your financial card services today?"})

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Handle User Input ---
if prompt := st.chat_input("Ask about financial products or card actions..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

    # Simulate thinking indicator
    with st.spinner("Thinking..."):
        # Invoke the orchestrator agent
        inputs = {"user_query": prompt}
        result = orchestrator_app.invoke(inputs)
        assistant_response = result.get('final_response', "Sorry, I could not process your request.")

    # Simulate streaming effect for demonstration
    for chunk in assistant_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        message_placeholder.markdown(full_response + "▌") # Display intermediate response
    message_placeholder.markdown(full_response) # Display final response

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response}) 