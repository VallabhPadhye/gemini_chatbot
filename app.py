import streamlit as st
import google.generativeai as genai

# Configure Gemini API
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

# Initialize session state
if "chats" not in st.session_state:
    st.session_state.chats = {"Default": []}  # Stores multiple chat sessions
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Default"  # Active chat session
if "pinned_chat" not in st.session_state:
    st.session_state.pinned_chat = "Default"  # Pinned chat
if "messages" not in st.session_state:
    st.session_state.messages = st.session_state.chats["Default"]

# Sidebar for chat history and pinning
with st.sidebar:
    st.title("Chat History")
    
    # Display available chat sessions
    for chat_name in st.session_state.chats.keys():
        if st.button(chat_name, key=f"chat_{chat_name}"):
            st.session_state.current_chat = chat_name
            st.session_state.messages = st.session_state.chats[chat_name]
            st.rerun()

    # New Chat button
    if st.button("➕ New Chat"):
        new_chat_name = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[new_chat_name] = []
        st.session_state.current_chat = new_chat_name
        st.session_state.messages = []
        st.rerun()

    # Pin current chat
    if st.button("📌 Pin This Chat"):
        st.session_state.pinned_chat = st.session_state.current_chat

# Set pinned chat as default on reload
if st.session_state.current_chat not in st.session_state.chats:
    st.session_state.current_chat = st.session_state.pinned_chat
    st.session_state.messages = st.session_state.chats[st.session_state.pinned_chat]

# Display chat history
st.title("Secure Chatbot (Powered by Gemini)")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input section with adaptive width
col1, col2 = st.columns([8, 2])
with col1:
    user_input = st.text_area(
        "Type your message:",
        height=80,
        key="chat_input"
    )
with col2:
    send = st.button("Send", use_container_width=True)

# Process input when "Send" button is clicked
if send and user_input.strip():
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from Gemini API
    response = model.generate_content(user_input)
    bot_response = response.text

    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # Save chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.session_state.chats[st.session_state.current_chat] = st.session_state.messages

    # Clear input field after sending
    st.session_state.chat_input = st.empty()  # Clears text area properly
    st.rerun()  # Refresh UI
