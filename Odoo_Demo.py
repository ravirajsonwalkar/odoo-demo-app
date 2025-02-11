import os
import openai
import streamlit as st
from dotenv import load_dotenv

# -------------------------------------------
# CONFIGURATION & INITIALIZATION
# -------------------------------------------
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API Key not set in your .env file!")
    st.stop()

openai.api_key = openai_api_key
MODEL = "gpt-4o"  # Adjust if needed

# System message for the assistant’s behavior.
system_message = (
    "You are an expert assistant for Odoo post-implementation support.\n"
    "You have access to the full Odoo documentation and can help users with issues, "
    "configurations, best practices, and troubleshooting.\n"
    "Provide clear, step-by-step solutions based on the official documentation.\n"
    "If unsure, politely suggest checking with Odoo support or official forums."
)

# Initialize session state for conversation history.
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_message}]

# -------------------------------------------
# STREAMLIT LAYOUT
# -------------------------------------------
st.title("Odoo Post-Implementation Support Chatbot")
st.markdown("Ask your questions about Odoo post-implementation support.")

# -------------------------------------------
# HELPER FUNCTION: Generate ChatGPT Response
# -------------------------------------------
def generate_response(user_message, stream_output=True):
    """
    Append the user's message to the conversation history and get the assistant's reply.
    Optionally stream the response.
    """
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    assistant_reply = ""
    
    if stream_output:
        # Use a placeholder for streaming tokens
        response_placeholder = st.empty()
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=st.session_state.messages,
                stream=True,  # enable streaming
            )
            for chunk in response:
                delta = chunk.choices[0].delta
                token = delta.get("content", "")
                assistant_reply += token
                response_placeholder.markdown(assistant_reply)
        except Exception as e:
            response_placeholder.error(f"Error: {e}")
    else:
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=st.session_state.messages,
            )
            assistant_reply = response.choices[0].message.content
            st.markdown(assistant_reply)
        except Exception as e:
            st.error(f"Error: {e}")
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

# -------------------------------------------
# USER INPUT
# -------------------------------------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:", placeholder="Ask about Odoo support...")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    generate_response(user_input, stream_output=True)
    # Conditionally call experimental_rerun if available.
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# -------------------------------------------
# DISPLAY CONVERSATION HISTORY
# -------------------------------------------
st.markdown("### Conversation")
for msg in st.session_state.messages[1:]:  # Skip the system message for display.
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Assistant:** {msg['content']}")

