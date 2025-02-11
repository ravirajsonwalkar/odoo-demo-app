import os
import openai
import streamlit as st
from dotenv import load_dotenv

# -------------------------------------------
# CONFIGURATION & INITIALIZATION
# -------------------------------------------
# Load .env for local development and st.secrets for deployed environment
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API Key not set in your environment!")
    st.stop()

openai.api_key = openai_api_key
MODEL = "gpt-4o"  # Adjust the model as needed

# Define a system message that establishes context (this is kept in the background)
system_message = (
    "You are an expert assistant for Odoo post-implementation support. "
    "You have access to the full Odoo documentation and can help users with issues, configurations, best practices, and troubleshooting. "
    "Provide clear, step-by-step solutions based on the official documentation. "
    "If unsure, politely suggest checking with Odoo support or official forums."
)

# Initialize conversation history in session_state (this is not shown on the UI)
if "conversation" not in st.session_state:
    st.session_state.conversation = [{"role": "system", "content": system_message}]

# -------------------------------------------
# STREAMLIT LAYOUT
# -------------------------------------------
st.title("Odoo Post-Implementation Support Chatbot")
# (Optional) Remove any descriptive text if you want a minimal chat-like UI.
# st.markdown("This chatbot uses conversation context behind the scenes.")

# Create a form that clears input on submission.
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:", placeholder="Ask about Odoo support...")
    submitted = st.form_submit_button("Send")

# When the form is submitted and there is user input:
if submitted and user_input:
    # Append the user's message to the conversation history.
    st.session_state.conversation.append({"role": "user", "content": user_input})
    
    # Generate the assistant's response using the entire conversation as context.
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=st.session_state.conversation,
            stream=False
        )
        assistant_reply = response.choices[0].message.content
    except Exception as e:
        assistant_reply = f"Error: {e}"
    
    # Append the assistant's reply to the conversation history.
    st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})
    
    # Display only the latest assistant reply.
    st.markdown("**Assistant:**")
    st.markdown(assistant_reply)


