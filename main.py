import os
import streamlit as st
import google.generativeai as gen_ai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="ChatBot",
    page_icon=":brain:",
    layout="centered",
)

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    st.error("API Key is missing. Check your .env file.")
else:
    gen_ai.configure(api_key=API_KEY)

    # Use a valid model from list_models()
    try:
        model = gen_ai.GenerativeModel("learnlm-2.0-flash-experimental")  # Change this based on list_models()
    except Exception as e:
        st.error(f"Error loading model: {e}")

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    st.title("🤖Leader - Bot")

    for message in st.session_state.chat_session.history:
        with st.chat_message(message.role):
            st.markdown(message.parts[0].text)

    user_prompt = st.chat_input("Ask Gemini...")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        try:
            gemini_response = st.session_state.chat_session.send_message(user_prompt)
            if gemini_response and hasattr(gemini_response, "text"):
                with st.chat_message("assistant"):
                    st.markdown(gemini_response.text)
            else:
                st.error("No valid response received.")
        except Exception as e:
            st.error(f"Error in API response: {e}")


