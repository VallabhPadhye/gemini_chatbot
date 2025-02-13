import streamlit as st
import google.generativeai as genai

# Configure Gemini API
api_key = st.secrets["GEMINI_API_KEY"]
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

# Add chat input at the bottom with "Send" button
with st.container():
    user_input = st.text_area("Type your message:", key="chat_input", height=100)

    col1, col2 = st.columns([8, 2])
    with col1:
        st.write("")  # Empty space for layout
    with col2:
        send = st.button("Send")

# Process input when the "Send" button is clicked
if send and user_input.strip():
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call Gemini API
    response = model.generate_content(user_input)
    bot_response = response.text

    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # Store chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Clear input after sending
    st.session_state.chat_input = ""
