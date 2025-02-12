import os
import openai
import streamlit as st
from dotenv import load_dotenv
import time

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
    st.session_state.selected_industry = None

if st.session_state.selected_industry is None:
    st.subheader("🔍 Select Your Industry to Get Started")

    industry_options = {
        "Retail": "🛒 Sales & inventory automation",
        "Manufacturing": "🏭 Production & supply chain management",
        "Services": "💼 Project management & invoicing",
        "IT": "💻 Odoo development & deployment",
        "Finance": "💰 Accounting & invoicing",
        "Healthcare": "🏥 Patient & appointment management",
        "Other": "🌍 General Odoo assistance"
    }

    selected_industry = st.selectbox(
        "What industry do you work in?", 
        list(industry_options.keys()), 
        format_func=lambda x: f"{x} - {industry_options[x]}",
        key="industry_selection"
    )

    if st.button("🚀 Start Chat", key="start_chat_button"):
        st.session_state.selected_industry = selected_industry
        st.rerun()

else:
    st.success(f"💼 Industry Selected: {st.session_state.selected_industry}")

    # -------------------------------------------
    # CHATBOT UI - Odoo Support & Feature Guide
    # -------------------------------------------
    system_message = (
        f"You are an AI Odoo Assistant for {st.session_state.selected_industry}. "
        "Your job is to help users find solutions from Odoo user guides, guide them to Odoo features, "
        "assist with configurations, and provide general support for both new and existing Odoo users."
    )

    if "conversation" not in st.session_state:
        st.session_state.conversation = [
            {"role": "system", "content": system_message},
            {"role": "assistant", "content": "👋 Hi! I'm your Odoo AI Assistant. How can I help you today?"}
        ]

    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding: 10px;
            background-color: #2c2c2c;
            border-radius: 8px;
        }

        .user-bubble {
            background-color: #A5DC86;
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
            text-align: right;
            font-size: 1rem;
            color: black;
            font-weight: bold;
        }

        .assistant-bubble {
            background-color: #ffffff;
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
            text-align: left;
            font-size: 1rem;
            color: black;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Chat Input Form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message:", placeholder="Ask about Odoo configurations, features, or guides...")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        st.session_state.conversation.append({"role": "user", "content": user_input})

        # Simulating response delay for better UX
        with st.spinner("🤖 Fetching the best solution for you..."):
            time.sleep(1.5)

            try:
                # Customize bot responses for Odoo configurations & features
                response = openai.ChatCompletion.create(
                    model=MODEL,
                    messages=st.session_state.conversation,
                    stream=False
                )
                assistant_reply = response.choices[0].message.content

                # If user asks about a module, guide them
                feature_map = {
                    "inventory": "📦 To manage inventory, go to **Odoo > Inventory**. Here you can track stock levels, shipments, and suppliers.",
                    "sales": "💰 To manage sales, navigate to **Odoo > Sales**. You can create quotations, manage orders, and set pricing strategies.",
                    "accounting": "📊 To manage accounting, visit **Odoo > Accounting**. It handles invoicing, reports, and bank reconciliation.",
                    "manufacturing": "🏭 For manufacturing setups, go to **Odoo > Manufacturing**. This module manages work orders, BoMs, and production planning.",
                    "crm": "📇 To track leads and customers, check **Odoo > CRM** for pipeline management and communication tracking."
                }

                for keyword, feature in feature_map.items():
                    if keyword in user_input.lower():
                        assistant_reply += f"\n\n**📌 Quick Guide:** {feature}"

            except Exception as e:
                assistant_reply = f"⚠️ Error: {e}"

        st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

    # Display Chat History
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in reversed(st.session_state.conversation[1:]):  # Skip system message
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'><strong>You:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f"<div class='assistant-bubble'><strong>Assistant:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Clear Conversation Button
    if st.button("🗑️ Clear Conversation", key="clear_convo_button"):
        st.session_state.selected_industry = None  # Reset industry selection
        st.session_state.conversation = [
            {"role": "system", "content": system_message},
            {"role": "assistant", "content": "👋 Hi! I'm your Odoo AI Assistant. How can I help you today?"}
        ]
        st.rerun()
