import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Configure Gemini API
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

# Initialize session state
def init_session_state():
    defaults = {
        "chats": {"Default": []},
        "current_chat": "Default",
        "pinned_chat": "Default",
        "messages": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    st.session_state.messages = st.session_state.chats[st.session_state.current_chat]

init_session_state()

# Sidebar for chat history
with st.sidebar:
    st.title("Chat History")

    # Display pinned chat first
    if st.session_state.pinned_chat in st.session_state.chats:
        if st.button(f"📌 {st.session_state.pinned_chat}", key="pinned_chat"):
            st.session_state.current_chat = st.session_state.pinned_chat
            st.session_state.messages = st.session_state.chats[st.session_state.pinned_chat]
            st.rerun()

    # Display other chats
    for chat_name in st.session_state.chats.keys():
        if chat_name != st.session_state.pinned_chat:
            if st.button(chat_name, key=f"chat_{chat_name}"):
                st.session_state.current_chat = chat_name
                st.session_state.messages = st.session_state.chats[chat_name]
                st.rerun()

    # Add new chat button
    if st.button("➕ New Chat"):
        new_chat_name = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[new_chat_name] = []
        st.session_state.current_chat = new_chat_name
        st.session_state.messages = []
        st.rerun()

# Set pinned chat as default on reload
if st.session_state.current_chat not in st.session_state.chats:
    st.session_state.current_chat = st.session_state.pinned_chat
    st.session_state.messages = st.session_state.chats[st.session_state.pinned_chat]

# Display chat history
st.title("Secure Chatbot (Powered by Gemini)")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(message.get("timestamp", ""))

# Chat input section
user_input = st.text_area(
    "Type your message:",
    height=80,
    key="chat_input",
    value="",
    placeholder="Ask me anything...",
)
send = st.button("Send", use_container_width=True)

# Handle user input
def handle_message():
    if user_input.strip():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get response from Gemini API
        try:
            response = model.generate_content(user_input)
            bot_response = response.candidates[0].content.parts[0].text
        except genai.errors.APIError as e:
            bot_response = f"⚠️ API Error: {str(e)}"
        except Exception as e:
            bot_response = f"⚠️ Unexpected Error: {str(e)}"

        with st.chat_message("assistant"):
            st.markdown(bot_response)

        # Save chat history
        st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": timestamp})
        st.session_state.messages.append({"role": "assistant", "content": bot_response, "timestamp": timestamp})
        st.session_state.chats[st.session_state.current_chat] = st.session_state.messages

        # Clear input
        st.session_state.chat_input = ""
        st.rerun()

# Call function only when send button is clicked
if send:
    handle_message()