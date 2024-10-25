import streamlit as st
import subprocess
import time

# Page config
st.set_page_config(
    page_title="HireMind - AI Interview Prep",
    page_icon="💼",
    layout="wide"
)

# Initialize session state for job position
if 'job_position' not in st.session_state:
    st.session_state.job_position = None
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False

st.title("HireMind 💼")

# Initial job position input if not already provided
if not st.session_state.job_position:
    st.markdown("### Hello! I'm HireMind, your interview prep assistant.")
    st.markdown("Please enter the Job Position you're applying for and we'll begin our interview prep session.")
    
    job_position = st.text_input("Job Position:")
    
    if st.button("Start Interview Prep"):
        if job_position:
            st.session_state.job_position = job_position
            st.session_state.interview_started = True
            st.rerun()
        else:
            st.warning("Please enter a job position to continue.")

# Interview prep session
elif st.session_state.interview_started:
    st.markdown(f"### Preparing you for: {st.session_state.job_position}")
    
    # User input for questions
    question = st.text_input("Ask me anything about the interview process, or type 'generate questions' for sample questions:")
    
    if st.button("Submit"):
        if question:
            st.write("Your input:", question)
            
            # Prepare context based on whether user wants generated questions
            if question.lower() == "generate questions":
                prompt = f"""As an expert interview coach, generate 5 important interview questions specific to the {st.session_state.job_position} role. Keep the response concise."""
            else:
                prompt = f"""As an expert interview coach helping someone prepare for a {st.session_state.job_position} position, provide a clear and concise response to: {question}"""
            
            # Show a spinner while processing
            with st.spinner("Generating response..."):
                try:
                    # Direct terminal command
                    command = f'ollama run mistral "{prompt}"'
                    
                    # Run command with longer timeout
                    process = subprocess.Popen(
                        command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    # Wait for output with longer timeout (60 seconds)
                    try:
                        stdout, stderr = process.communicate(timeout=60)
                        if process.returncode == 0:
                            st.write("HireMind:", stdout)
                        else:
                            st.error(f"Error: {stderr}")
                    except subprocess.TimeoutExpired:
                        process.kill()
                        st.error("Response is taking too long. Please try again with a simpler question.")
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    # Add a reset button in sidebar
    if st.sidebar.button("Start New Interview Prep"):
        st.session_state.job_position = None
        st.session_state.interview_started = False
        st.rerun()

# System status in sidebar
st.sidebar.markdown("---")
st.sidebar.write("System Status:")
try:
    # Quick check if Ollama is responsive
    check = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
    if check.returncode == 0:
        st.sidebar.success("✅ Ready to help")
    else:
        st.sidebar.error("❌ System not responding")
except Exception as e:
    st.sidebar.error(f"❌ Error: {str(e)}")

# Tips in sidebar
if st.session_state.interview_started:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Tips")
    st.sidebar.markdown("""
    - Type 'generate questions' to get role-specific questions
    - Ask about specific skills needed for the role
    - Request sample answers or feedback
    - Ask about interview best practices
    """)

    # Add example questions based on job position
    st.sidebar.markdown("### Example Questions to Ask")
    st.sidebar.markdown("""
    1. What skills are most important for this role?
    2. How should I prepare for technical questions?
    3. What are common interview questions for this position?
    4. How can I stand out in the interview?
    """)