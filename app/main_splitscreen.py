import streamlit as st
from datetime import datetime
import speech_recognition as sr
from io import StringIO
from pdfminer.high_level import extract_text

# Page Configurations
st.set_page_config(page_title="MediAssist", page_icon="💊", layout="wide")
st.markdown(
    """
    <style>
    /* Base styles */
    .main {
        background-color: #ffffff;
        color: #222222;
        font-family: 'Poppins', sans-serif;
    }
    
    .title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ff6f61;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px #f0f0f0;
    }
    
    .subtitle {
        font-size: 1rem;
        color: #ff9f80;
        text-align: center;
        margin-bottom: 1rem;
        font-style: italic;
    }

    /* Split screen layout */
    .split-container {
        display: flex;
        gap: 20px;
        height: calc(100vh - 200px);
        margin: -1rem;
    }

    .chat-column {
        flex: 1;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        background: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem;
        position: relative;
    }

    .chat-header {
        padding: 16px;
        border-bottom: 1px solid #e5e7eb;
        background: #f8fafc;
        border-radius: 12px 12px 0 0;
    }

    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
    }

    /* Message styles */
    .message {
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 80%;
        line-height: 1.5;
    }

    .patient-message {
        background-color: #ff9f80;
        color: white;
        margin-left: auto;
        margin-right: 16px;
    }

    .doctor-message {
        background-color: #f0f5f9;
        color: #333333;
        margin-right: auto;
        margin-left: 16px;
    }

    /* Input container styles */
    .chat-input-container {
        padding: 16px;
        border-top: 1px solid #e5e7eb;
        background: white;
        border-radius: 0 0 12px 12px;
    }

    .input-container {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        display: flex;
        align-items: flex-end;
        padding: 8px 12px;
        gap: 8px;
    }

    .input-textarea {
        flex-grow: 1;
        border: none;
        resize: none;
        padding: 8px 0;
        min-height: 24px;
        max-height: 120px;
        outline: none;
        font-size: 14px;
        line-height: 1.5;
    }

    /* Action buttons */
    .action-buttons {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .icon-button {
        background: none;
        border: none;
        padding: 6px;
        color: #6b7280;
        cursor: pointer;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
    }

    .icon-button:hover {
        background-color: #f3f4f6;
        color: #374151;
    }

    .send-button {
        background-color: #ff6f61;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .send-button:hover {
        background-color: #ff4d4d;
    }

    /* Hide Streamlit components */
    .stButton, .stFileUploader {
        display: none;
    }

    .upload-input {
        display: none;
    }

    /* User info styles */
    .user-info {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .user-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #e5e7eb;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }

    .user-name {
        font-weight: 600;
        color: #374151;
    }

    .user-status {
        font-size: 12px;
        color: #6b7280;
    }

    /* Data display section */
    .data-section {
        padding: 16px;
        background: #f8fafc;
        border-radius: 8px;
        margin: 16px;
    }

    .data-title {
        font-weight: 600;
        color: #374151;
        margin-bottom: 8px;
    }

    .data-item {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #e5e7eb;
    }

    .data-label {
        color: #6b7280;
    }

    .data-value {
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session states
if "patient_history" not in st.session_state:
    st.session_state["patient_history"] = []
if "doctor_history" not in st.session_state:
    st.session_state["doctor_history"] = []
if "is_recording" not in st.session_state:
    st.session_state["is_recording"] = False

# Sample patient data
patient_data = {
    "name": "John Doe",
    "age": 45,
    "blood_type": "A+",
    "last_visit": "2024-03-15",
    "conditions": ["Hypertension", "Type 2 Diabetes"],
    "medications": ["Lisinopril", "Metformin"]
}

# Display split screen layout
st.markdown('<div class="title">⚕️ MediAssist</div>', unsafe_allow_html=True)

# Create two columns for split screen
col1, col2 = st.columns(2)


with col1:
    st.markdown(
        """
        <div class="chat-column">
            <div class="chat-header">
                <div class="user-info">
                    <div class="user-avatar">👤</div>
                    <div>
                        <div class="user-name">Patient Portal</div>
                        <div class="user-status">John Doe</div>
                    </div>
                </div>
            </div>
            <div class="chat-messages" id="patient-messages">
                <!-- Patient messages will be displayed here -->
            </div>
            <div class="chat-input-container">
                <div class="input-container">
                    <textarea 
                        class="input-textarea"
                        placeholder="Type your message..."
                        rows="1"
                    ></textarea>
                    <div class="action-buttons">
                        <label class="icon-button" title="Upload file">
                            📎
                            <input type="file" class="upload-input" accept=".txt,.pdf,.docx,xlsx" />
                        </label>
                        <button class="icon-button" title="Voice input">
                            🎤
                        </button>
                        <button class="send-button" id="patient-send-button">
                            Send
                        </button>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    def get_response(user_input):
        # Static response for testing
        return "I'm here to assist you. How can I help?"
    # Display conversation when user submits a message
    if st.button("patient-send-button") and user_input:
        # Get bot's response
        bot_response = get_response(user_input)
        # Append user input and bot response to the conversation history
        st.session_state["patient_history"].append({"role": "user", "message": user_input})
        st.session_state["patient_history"].append({"role": "assistant", "message": bot_response})
        # Clear input box after sending
        user_input = ""
    # Display conversation history with enhanced styling
    for entry in st.session_state["patient_history"]:
        if entry["role"] == "user":
            st.markdown(f'<div class="user-message">{entry["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{entry["message"]}</div>', unsafe_allow_html=True)
    # Add JavaScript for textarea auto-resize
    st.markdown(
        """
        <script>
        const textareas = document.querySelectorAll('.input-textarea');
        textareas.forEach(textarea => {
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = this.scrollHeight + 'px';
            });
        });
        </script>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="chat-column">
            <div class="chat-header">
                <div class="user-info">
                    <div class="user-avatar">👨‍⚕️</div>
                    <div>
                        <div class="user-name">Doctor Portal</div>
                        <div class="user-status">Dr. Sarah Johnson</div>
                    </div>
                </div>
            </div>
            <div class="chat-messages" id="doctor-messages">
                <!-- Doctor messages will be displayed here -->
            </div>
            <div class="chat-input-container">
                <div class="input-container">
                    <textarea 
                        class="input-textarea"
                        placeholder="Type your medical advice..."
                        rows="1"
                    ></textarea>
                    <div class="action-buttons">
                        <label class="icon-button" title="Upload file">
                            📎
                            <input type="file" class="upload-input" accept=".txt,.pdf,.docx,xlsx" />
                        </label>
                        <button class="icon-button" title="Voice input">
                            🎤
                        </button>
                        <button class="send-button">
                            Send
                        </button>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

