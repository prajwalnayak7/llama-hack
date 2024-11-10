import streamlit as st
import pandas as pd
from together import Together
# Define the questions to generate responses for

client = Together(api_key ="5e44022a52ba3e082d1ffb1932d14e3e259d91dfde97a3d0ae28d7a7c8863a0c")

questions = [
    "What is the patient's name?",
    "What is the patient's age?",
    "What is the patient's condition?",
    "What symptoms is the patient experiencing?",
    "What precautions did the doctor advise?",
    "What drug did the doctor prescribe?"
]

# Function to process conversation and generate responses
def generate_responses(conversation_text):
    results = []
    
    # Loop over each question
    for question in questions:
        # Define the context with the conversation and the current question
        context = [
            {"role": "assistant", "content": "Answer the following question based on the patient-doctor conversation provided."},
            {"role": "system", "content": conversation_text},
            {"role": "user", "content": question}
        ]
        
        # Call the model API for each question (replace with actual client code as needed)
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct-Turbo",  # Replace with the actual model identifier
            messages=context,
            max_tokens=150,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stop=["<|eot_id|>", "<|eom_id|>"],
            stream=False
        )
        
        # Extract the response content
        answer = response.choices[0].message.content
        
        # Append the question and answer to the results
        results.append({
            "Question": question,
            "Answer": answer
        })
    
    return pd.DataFrame(results)  # Return the results as a DataFrame for easy display in Streamlit

# Streamlit app layout
st.title("Healthcare Conversation Analyzer")

# Text input for the user to paste a conversation
conversation_text = st.text_area("Enter the conversation text here:", height=300)

# Button to generate responses
if st.button("Generate Responses"):
    if conversation_text.strip():
        # Generate responses
        response_df = generate_responses(conversation_text)
        
        # Display the results
        st.write("Generated Responses:")
        st.dataframe(response_df)
    else:
        st.warning("Please enter a conversation to analyze.")
