import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Streamlit app title
st.title("Simple Chat")

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Streamed response emulator
    def response_generator(prompt):
        response = get_gemini_response(prompt)
        response_text = ""
        for chunk in response:
            response_text += chunk.text
            yield chunk.text
        return response_text

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response_text = "".join(response_generator(prompt))
        st.markdown(response_text)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
