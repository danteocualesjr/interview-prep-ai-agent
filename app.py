import streamlit as st
import subprocess
import json

# Page config
st.set_page_config(
    page_title="Interview Prep AI",
    page_icon="💼",
    layout="wide"
)

# Initialize session states
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Title and description
st.title("Interview Prep AI 💼")

# Sidebar with options
st.sidebar.title("Interview Type")
interview_type = st.sidebar.selectbox(
    "Choose your interview preparation:",
    [
        "General Interview",
        "Behavioral Questions",
        "Technical Questions",
        "Leadership Questions",
        "Problem Solving",
        "Mock Interview"
    ]
)

# Different prompts based on interview type
prompts = {
    "General Interview": "I'll help you prepare for general interview questions. What would you like to know?",
    "Behavioral Questions": "I'll help you practice STAR method responses. What's your question?",
    "Technical Questions": "I'll help you with technical interview preparation. What's your area of focus?",
    "Leadership Questions": "I'll help you prepare leadership examples. What would you like to discuss?",
    "Problem Solving": "I'll present you with problem-solving scenarios. Ready to begin?",
    "Mock Interview": "I'll act as an interviewer. Ready to start the mock interview?"
}

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input section
user_input = st.chat_input(prompts[interview_type])

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Save user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Prepare context based on interview type
    context = f"You are an expert interview coach. Current mode: {interview_type}. "
    
    if interview_type == "Behavioral Questions":
        context += "Guide the user to structure their response using the STAR method (Situation, Task, Action, Result). "
    elif interview_type == "Technical Questions":
        context += "Provide detailed technical explanations and ask follow-up questions to deepen understanding. "
    elif interview_type == "Mock Interview":
        context += "Act as a professional interviewer, ask follow-up questions, and provide feedback. "
    
    # Prepare prompt
    prompt = f"{context}\n\nUser: {user_input}\nAssistant:"
    
    try:
        with st.chat_message("assistant"):
            with st.spinner('Thinking...'):
                # Use subprocess to call Ollama
                command = f'ollama run mistral "{prompt}"'
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    response = result.stdout
                    st.write(response)
                    # Save assistant response
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                else:
                    st.error(f"Error: {result.stderr}")
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Clear chat button
if st.sidebar.button('Clear Chat'):
    st.session_state.chat_history = []
    st.rerun()

# Display Ollama status in sidebar
try:
    result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
    if result.returncode == 0:
        st.sidebar.success("System Status: Ready")
    else:
        st.sidebar.error("System Status: Error")
except Exception as e:
    st.sidebar.error(f"System Status: Error - {str(e)}")