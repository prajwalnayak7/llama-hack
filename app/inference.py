
def get_response(user_input, role):
    if role == "Patient":
        return get_response_patient(user_input)
    elif role == "Doctor":
        return get_response_doctor(user_input)
    elif role == "Admin":
        return get_response_admin(user_input)
    else:
        return "I'm sorry, I don't understand your role. Please try again."

def get_response_admin(user_input):
    return "I'm here to assist you with administrative tasks. How can I help?"

def get_response_doctor(user_input):
    return "Welcome, Doctor. How can I assist you with patient care today?"

def get_response_patient(user_input):
    return "I'm here to assist you with your medical queries. How can I help?"
