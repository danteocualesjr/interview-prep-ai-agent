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
                prompt = f"""As an expert interview coach, generate 5 important interview questions specific to the {st.session_state.job_position} role. 
                For each question, explain why it's important for this role. Format the response clearly with numbers and explanations."""
            else:
                prompt = f"""As an expert interview coach helping someone prepare for a {st.session_state.job_position} position, 
                provide a detailed and helpful response to this question: {question}"""
            
            # Show a spinner while processing
            with st.spinner("Generating response..."):
                try:
                    # Escape the prompt for shell safety
                    escaped_prompt = prompt.replace('"', '\\"')
                    
                    # Run the command and capture output
                    process = subprocess.run(
                        f'ollama run mistral "{escaped_prompt}"',
                        shell=True,
                        text=True,
                        capture_output=True,
                        timeout=30
                    )
                    
                    if process.returncode == 0:
                        st.write("HireMind:", process.stdout)
                    else:
                        st.error(f"Error: {process.stderr}")
                
                except subprocess.TimeoutExpired:
                    st.error("Request timed out after 30 seconds")
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
    check = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
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