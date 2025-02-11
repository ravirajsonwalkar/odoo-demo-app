import os
import openai
import streamlit as st
from dotenv import load_dotenv

# -------------------------------------------
# CONFIGURATION & INITIALIZATION
# -------------------------------------------
# Load local .env for development and/or st.secrets for deployed environment.
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API Key not set in your environment!")
    st.stop()

openai.api_key = openai_api_key
MODEL = "gpt-4o"  # Adjust the model if needed

# Define a system message that sets the context for the assistant (kept in the background)
system_message = (
    "You are an expert assistant for Odoo post-implementation support. "
    "You have access to the full Odoo documentation and can help users with issues, configurations, best practices, and troubleshooting. "
    "Provide clear, step-by-step solutions based on the official documentation. "
    "If unsure, politely suggest checking with Odoo support or official forums."
)

# Initialize the conversation history in session state if it doesn't exist yet.
if "conversation" not in st.session_state:
    st.session_state.conversation = [{"role": "system", "content": system_message}]

# -------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------
st.set_page_config(
    page_title="Odoo Support Chatbot",
    page_icon=":robot:",
    layout="centered"
)
st.title("Odoo Support Chatbot")

# -------------------------------------------
# CUSTOM CSS FOR CHAT UI
# -------------------------------------------
st.markdown("""
    <style>
    /* Hide default Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Chat container styling */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 10px;
        background-color: #2c2c2c; /* Dark background for contrast */
        border-radius: 8px;
    }
    /* User chat bubble styling */
    .user-bubble {
        background-color: #A5DC86; /* Light green */
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
        text-align: right;
        font-size: 1rem;
        color: black;
        font-weight: bold;
    }
    /* Assistant chat bubble styling */
    .assistant-bubble {
        background-color: #ffffff; /* White background */
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
        text-align: left;
        font-size: 1rem;
        color: black; /* Make text fully visible */
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------
# CHAT INPUT FORM
# -------------------------------------------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:", placeholder="Ask your question here...")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Append the user's message to the conversation history.
    st.session_state.conversation.append({"role": "user", "content": user_input})
    
    # Generate the assistant's response using the full conversation history.
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

# -------------------------------------------
# DISPLAY THE FULL CONVERSATION HISTORY
# -------------------------------------------
# We skip the first message (the system message) to show only user and assistant exchanges.
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.conversation[1:]:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'><strong>You:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"<div class='assistant-bubble'><strong>Assistant:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------
# CLEAR CONVERSATION BUTTON
# -------------------------------------------
if st.button("Clear Conversation"):
    st.session_state.conversation = [{"role": "system", "content": system_message}]
    st.experimental_rerun()


