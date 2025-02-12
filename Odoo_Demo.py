import os
import openai
import streamlit as st
from dotenv import load_dotenv

# -------------------------------------------
# CONFIGURATION & INITIALIZATION
# -------------------------------------------
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API Key not set in your environment!")
    st.stop()

# gpt-4o-mini to save API costs
MODEL = "gpt-4o-mini"

openai.api_key = openai_api_key

# -------------------------------------------
# APP LAYOUT & INDUSTRY SELECTION
# -------------------------------------------
st.set_page_config(
    page_title="Odoo AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🚀 Odoo AI Support Chatbot")

# -------------------------------------------
# INDUSTRY SELECTION - Appears only once
# -------------------------------------------
if "selected_industry" not in st.session_state:
    st.session_state.selected_industry = None  # Initialize industry selection

if st.session_state.selected_industry is None:
    st.subheader("Select Your Industry to Get Started")
    
    industry_options = ["Retail", "Manufacturing", "Services", "IT", "Finance", "Healthcare", "Other"]
    
    # Unique key to avoid duplicate element errors
    selected_industry = st.selectbox(
        "What industry do you work in?", 
        industry_options, 
        key="industry_selection"
    )

    if st.button("Start Chat", key="start_chat_button"):
        st.session_state.selected_industry = selected_industry
        st.rerun()  # Updated from `st.experimental_rerun()`

else:
    # Show the selected industry at the top
    st.success(f"💼 Industry Selected: {st.session_state.selected_industry}")

    # -------------------------------------------
    # CHATBOT UI
    # -------------------------------------------
    system_message = (
        f"You are an AI assistant specializing in Odoo post-implementation support for the {st.session_state.selected_industry} industry. "
        "Provide tailored solutions, best practices, and troubleshooting guidance specific to this industry."
    )

    if "conversation" not in st.session_state:
        st.session_state.conversation = [{"role": "system", "content": system_message}]

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

    # Chat Input Form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message:", placeholder="Ask your Odoo-related question...")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        # Append the user's message to the conversation history
        st.session_state.conversation.append({"role": "user", "content": user_input})

        # Generate the assistant's response using OpenAI
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=st.session_state.conversation,
                stream=False
            )
            assistant_reply = response.choices[0].message.content
        except Exception as e:
            assistant_reply = f"Error: {e}"

        # Append the assistant's reply to the conversation history
        st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

    # Display Chat History
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in reversed(st.session_state.conversation[1:]):  # Skip system message
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'><strong>You:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f"<div class='assistant-bubble'><strong>Assistant:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Corrected Clear Conversation Button
    if st.button("Clear Conversation", key="clear_convo_button"):
        st.session_state.selected_industry = None  # Reset industry selection
        st.session_state.conversation = [{"role": "system", "content": system_message}]
        st.rerun()  # Updated from `st.experimental_rerun()`
