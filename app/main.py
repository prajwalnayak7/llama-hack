import streamlit as st
from datetime import datetime

# Page Configurations
st.set_page_config(page_title="MediAssist", page_icon="💊", layout="centered")
st.markdown(
    """
    <style>
    /* Background and Font Styles */
    .main {
        background-color: #ffffff;
        color: #222222;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Title and Subtitle */
    .title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #ff6f61;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px #f0f0f0;
    }
    .subtitle {
        font-size: 1.3rem;
        color: #ff9f80;
        text-align: center;
        margin-bottom: 2.5rem;
        font-style: italic;
    }

    /* Message Bubbles */
    .user-message, .bot-message {
        padding: 15px 20px;
        border-radius: 18px;
        margin: 8px 0;
        max-width: 75%;
        line-height: 1.8;
        box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s;
    }
    .user-message {
        background-color: #ff9f80;
        color: #ffffff;
        align-self: flex-end;
        text-align: right;
    }
    .bot-message {
        background-color: #f0f5f9;
        color: #333333;
        align-self: flex-start;
        text-align: left;
    }

    /* Custom Button Style */
    .stButton button {
        background-color: #ff6f61;
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: bold;
        padding: 10px 25px;
        box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s, transform 0.3s;
    }
    .stButton button:hover {
        background-color: #ff4d4d;
        transform: translateY(-2px);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display Title and Subtitle
st.markdown('<div class="title">⚕️ MediAssist</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your Personal Medical Companion</div>', unsafe_allow_html=True)

# Define function to get a hardcoded response (simulate bot's response)
def get_response(user_input):
    # Static response for testing
    return "I'm here to assist you. How can I help?"

# Initialize session state to hold the conversation history
if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []

# Input for user to enter their message
user_input = st.text_input("You:", placeholder="Type your message here...", key="input_text")

# Display conversation when user submits a message
if st.button("Send") and user_input:
    # Get bot's response
    bot_response = get_response(user_input)
    
    # Append user input and bot response to the conversation history
    st.session_state["conversation_history"].append({"role": "user", "message": user_input})
    st.session_state["conversation_history"].append({"role": "assistant", "message": bot_response})

    # Clear input box after sending
    user_input = ""

# Display conversation history with enhanced styling
for entry in st.session_state["conversation_history"]:
    if entry["role"] == "user":
        st.markdown(f'<div class="user-message">{entry["message"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{entry["message"]}</div>', unsafe_allow_html=True)

