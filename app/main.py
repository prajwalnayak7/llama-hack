import streamlit as st
from together import Together
import pandas as pd
import os

# Initialize Together API
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))


# Track the conversation history and responses in session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "patient_data" not in st.session_state:
    st.session_state.patient_data = {}
if "conversation_active" not in st.session_state:
    st.session_state.conversation_active = True  # Track if conversation is active
if "rerun_trigger" not in st.session_state:
    st.session_state.rerun_trigger = 0  # Dummy variable to trigger rerun

## Function to ask questions to patient

def generate_response(conversation_history):
   
    prompt = (
        "You are a healthcare assistant chatbot. Your task is to ask one clear and specific question to collect "
        "essential health-related information from the patient. The goal is to gather details such as:\n"
        "- Patient's name\n"
        "- Age\n"
        "- Condition\n"
        "- Reason for visit\n"
        "- Symptom onset and progression\n"
        "- Pain level\n"
        "- Pain location and spread\n"
        "- Additional symptoms (e.g., nausea, dizziness)\n"
        "- Recent fever, chills, or cough\n"
        "- Allergies\n"
        "- Medical conditions\n"
        "- Current medications\n"
        "- Recent contact with sick individuals\n\n"
        "Ask only one relevant question at a time, based on the conversation so far.\n\n"
        "Conversation history:\n"
    )
    # Use only the last few entries in the conversation history to keep context focused
    recent_history = conversation_history[-5:]  # Last 5 messages for context
    prompt += "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_history])
    prompt += "\n\nHealthcare Assistant's next question:"

    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
            messages=[{"role": "assistant", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            repetition_penalty=1.0,
            stream=False
        )
        generated_text = response.choices[0].message.content.strip()
        # Return only the assistant's question
        return generated_text
    except Exception as e:
        st.error(f"An error occurred in generating the question: {e}")
        return "I'm sorry, I couldn't generate a question. Please try again."


# Function to extract key information from the conversation
def extract_information(conversation_history):
   
    extraction_prompt = (
        "Based on the following conversation between a healthcare assistant and a patient, extract only the patient's "
        "specific information in English in a structured JSON format. Ignore any statements by the assistant. "
        "Only include information provided directly by the patient. Please use the following format:\n\n"
        "{\n"
        "  'name': 'Patient's name',\n"
        "  'age': 'Patient's age',\n"
        "  'condition': 'Patient's condition',\n"
        "  'reason_for_visit': 'Reason for visit',\n"
        "  'symptoms': 'Symptom details',\n"
        "  'pain_level': 'Pain level',\n"
        "  'pain_location': 'Pain location and spread',\n"
        "  'additional_symptoms': 'Additional symptoms',\n"
        "  'fever_or_cough': 'Recent fever, chills, or cough',\n"
        "  'allergies': 'Allergies',\n"
        "  'medical_conditions': 'Medical conditions',\n"
        "  'current_medications': 'Current medications',\n"
        "  'contact_with_sick_individuals': 'Recent contact with sick individuals'\n"
        "}\n\n"
        "Include only the relevant information provided by the patient, and exclude any questions or statements from the assistant.\n\n"
        "Conversation:\n"
    )
    extraction_prompt += "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])

    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
            messages=[{"role": "assistant", "content": extraction_prompt}],
            max_tokens=500,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1.0,
            stream=False
        )
        extracted_info = response.choices[0].message.content

        # Debug: Show the raw extracted information
        #st.write("Raw Extracted Information:")
        #st.text(extracted_info)

        return extracted_info
    except Exception as e:
        st.error(f"An error occurred during information extraction: {e}")
        return None


# Streamlit app layout
st.title("LinguaLink Chatbot")

# Language selection
language = st.selectbox("Select a language for conversation:", ["English", "Cantonese"])

# Display the initial greeting if the conversation is just starting
if len(st.session_state.conversation_history) == 0 and st.session_state.conversation_active:
    intro_text = "Hello! I'm LinguaLink. Let's discuss your health concerns, and I'll gather some essential information along the way."
    st.session_state.conversation_history.append({"role": "assistant", "content": intro_text})


for msg in st.session_state.conversation_history:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.write(msg["content"])

# Initialize session state 
if "user_input" not in st.session_state:
    st.session_state.user_input = ""  # Initialize as an empty string to store user input

# Check if the conversation is active
if st.session_state.conversation_active:
    # Generate the next question based on conversation history
    next_question = generate_response(st.session_state.conversation_history)
    st.session_state.conversation_history.append({"role": "assistant", "content": next_question})

    # Display the text input for user message
    user_input_temp = st.text_input("Your message", key="user_input_box")

    # Process user input only if it's non-empty and different from the last stored input
    if user_input_temp.strip() and user_input_temp != st.session_state.user_input:
        
        st.session_state.conversation_history.append({"role": "user", "content": user_input_temp.strip()})

        
        st.session_state.user_input = user_input_temp.strip()

        # Increment rerun trigger to force a UI refresh
        st.session_state["rerun_trigger"] = st.session_state.get("rerun_trigger", 0) + 1
        

# Button to stop the conversation and proceed with extraction
if st.button("End Conversation") and st.session_state.conversation_active:
    # Stop the conversation
    st.session_state.conversation_active = False

    # Extract required information
    extracted_info = extract_information(st.session_state.conversation_history)
    
    # Check if extraction was successful
    if extracted_info:
        # Parse the extracted info into a dictionary if needed
        extracted_info_dict = {}
        for line in extracted_info.strip().split('\n'):
            if ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                extracted_info_dict[key] = value
        
        # Convert to DataFrame
        patient_data_df = pd.DataFrame([extracted_info_dict])

        # Display the DataFrame
        st.write("Extracted Patient Information:")
        st.dataframe(patient_data_df)

        # patient_data_df.to_csv("patient_data.csv", index=False)
    else:
        st.warning("No information extracted.")
