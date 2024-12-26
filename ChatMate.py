import streamlit as st
import openai
import os

# Streamlit app configuration
st.set_page_config(page_title="ChatMate", layout="wide")

st.title("Chatbot like ChatGPT 💬")
st.write("Powered by OpenAI GPT-4")

api_key = st.sidebar.text_input("Enter api key", key="chatbot_api_key", type="password")
if "messages" not in st.session_state:
    st.session_state.messages = []
# Display chat history
for msg in st.session_state.messages:
    # Initialize session state for chat history
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message here...")
if not api_key:
    st.sidebar.write("Please enter your API key.")
else:
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Send user message to OpenAI API
        try:
            openai.api_key = api_key
            response = openai.chat.completions.create(
                model="gpt-4",  # Change to "gpt-3.5-turbo" if needed
                messages=st.session_state.messages,
                max_tokens=150,
                temperature=0.7,
            )
            bot_response = response.choices[0].message.content.strip()

            # Add bot response to chat history
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            with st.chat_message("assistant"):
                st.markdown(bot_response)

        except Exception as e:
            st.error(f"Error: {e}")
