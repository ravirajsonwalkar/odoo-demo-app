import os
import openai
import streamlit as st
from dotenv import load_dotenv

# -------------------------------------------
# CONFIGURATION & INITIALIZATION
# -------------------------------------------
# Load local .env (useful for local development) and/or use Streamlit secrets
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API Key not set in your environment!")
    st.stop()

openai.api_key = openai_api_key
MODEL = "gpt-4o"  # Adjust as needed

# System message: instructs the assistant about its role.
system_message = (
    "You are an expert assistant for Odoo post-implementation support. "
    "You have access to the full Odoo documentation and can help users with issues, configurations, best practices, and troubleshooting. "
    "Provide clear, step-by-step solutions based on the official documentation. "
    "If unsure, politely suggest checking with Odoo support or official forums."
)

# -------------------------------------------
# SESSION STATE SETUP
# -------------------------------------------
# Initialize conversation history only once.
if "conversation" not in st.session_state:
    st.session_state.conversation = [{"role": "system", "content": system_message}]

# -------------------------------------------
# STREAMLIT LAYOUT
# -------------------------------------------
st.title("Odoo Post-Implementation Support Chatbot")
st.markdown("This chatbot retains conversation history so that it can understand context from previous messages.")

# -------------------------------------------
# HELPER FUNCTION: Generate ChatGPT Response
# -------------------------------------------
def generate_response(user_message):
    # Append user's new message to the conversation history.
    st.session_state.conversation.append({"role": "user", "content": user_message})
    
    # Generate a response using the entire conversation history.
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=st.session_state.conversation,
            stream=False,  # Change to True if you want streaming (and update the UI accordingly)
        )
        assistant_reply = response.choices[0].message.content
    except Exception as e:
        assistant_reply = f"Error: {e}"
    
    # Append assistant's reply to the conversation history.
    st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

# -------------------------------------------
# USER INPUT SECTION
# -------------------------------------------
# You can use a form or simple text input with a button.
user_input = st.text_input("Your message:", placeholder="Type your question here...")

# When the user clicks the "Send" button, process the input.
if st.button("Send") and user_input:
    generate_response(user_input)
    # Optionally clear the text input by re-running the script:
    st.experimental_rerun()

# -------------------------------------------
# DISPLAY CONVERSATION HISTORY
# -------------------------------------------
st.markdown("### Conversation History")
for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Assistant:** {msg['content']}")

