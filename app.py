import streamlit as st
import subprocess
import time

# Custom CSS to match the design as closely as possible
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(to bottom right, #fff7ed, #fef3c7);
        padding: 1rem;
    }
    
    /* Card styling */
    .stApp {
        background: linear-gradient(to bottom right, #fff7ed, #fef3c7);
    }
    
    /* Header styling */
    .stTitle {
        font-size: 2rem !important;
        font-weight: bold !important;
        color: white !important;
        padding: 1rem !important;
        background: linear-gradient(to right, #fb923c, #f59e0b);
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Message container styling */
    .user-message {
        background: linear-gradient(to bottom right, #fb923c, #f59e0b);
        color: white;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        float: right;
        clear: both;
        max-width: 80%;
    }
    
    .ai-message {
        background: #f3f4f6;
        color: #1f2937;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        float: left;
        clear: both;
        max-width: 80%;
    }
    
    /* Input styling */
    .stTextInput input {
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 0.5rem;
        background: #f9fafb;
    }
    
    .stTextInput input:focus {
        border-color: #fb923c;
        box-shadow: 0 0 0 2px rgba(251, 146, 60, 0.2);
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(to right, #fb923c, #f59e0b);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
    }
    
    .stButton button:hover {
        background: linear-gradient(to right, #ea580c, #d97706);
    }
    
    /* Message container */
    .message-container {
        margin-bottom: 1rem;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session states
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "ai", "content": "Hello! I'm HireMind, your interview prep assistant. Please enter the Job Position you're applying for and we'll begin our interview prep session."}
    ]
if 'job_position' not in st.session_state:
    st.session_state.job_position = None

# App title
st.markdown('<h1 class="stTitle">💼 HireMind</h1>', unsafe_allow_html=True)

# Message container
message_container = st.container()

# Display messages
with message_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-message">{message["content"]}</div>', unsafe_allow_html=True)

# Input form
with st.container():
    col1, col2 = st.columns([6,1])
    with col1:
        user_input = st.text_input("", placeholder="Type your message here...", label_visibility="collapsed")
    with col2:
        send_button = st.button("Send")

if send_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Process based on job position
    if not st.session_state.job_position:
        st.session_state.job_position = user_input
        ai_response = f"""Great! I see you're preparing for a {user_input} role. Let's start our interview prep session. 
        What specific area would you like to focus on? You can choose from:
        - Work Experience
        - Technical Skills
        - Behavioral Questions
        - Company Knowledge
        - Career Goals"""
    else:
        # Here we'll add the Ollama integration
        prompt = f"""As an interview coach helping someone prepare for a {st.session_state.job_position} position, 
        provide a clear and helpful response to: {user_input}"""
        
        try:
            with st.spinner("Thinking..."):
                process = subprocess.Popen(
                    f'ollama run mistral "{prompt}"',
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate(timeout=60)
                if process.returncode == 0:
                    ai_response = stdout
                else:
                    ai_response = "I apologize, but I encountered an error. Please try again."
                    
        except Exception as e:
            ai_response = "I apologize, but I encountered an error. Please try again."
    
    # Add AI response
    st.session_state.messages.append({"role": "ai", "content": ai_response})
    
    # Rerun to update the UI
    st.rerun()

# Clear button in sidebar
if st.sidebar.button("Start New Session"):
    st.session_state.messages = [
        {"role": "ai", "content": "Hello! I'm HireMind, your interview prep assistant. Please enter the Job Position you're applying for and we'll begin our interview prep session."}
    ]
    st.session_state.job_position = None
    st.rerun()