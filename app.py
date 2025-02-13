import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key securely
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

# Streamlit UI
st.title("Secure Chatbot (Powered by Gemini)")
st.write("Ask me anything!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.text_input("You:")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call Gemini API
    response = model.generate_content(user_input)
    bot_response = response.text

    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # Store chat history in session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
