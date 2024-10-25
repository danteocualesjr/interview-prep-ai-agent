import streamlit as st
import subprocess
import time

# Page config
st.set_page_config(page_title="Interview Prep AI", page_icon="💼", layout="wide")

st.title("Interview Prep AI 💼")

# Add interview type selector in sidebar
st.sidebar.title("Settings")
interview_type = st.sidebar.selectbox(
    "Choose Interview Type",
    [
        "General Questions",
        "Behavioral (STAR Method)",
        "Technical Interview",
        "Mock Interview"
    ]
)

# Display different instructions based on interview type
if interview_type == "Behavioral (STAR Method)":
    st.info("Format your answer using the STAR method:\n- Situation\n- Task\n- Action\n- Result")
elif interview_type == "Technical Interview":
    st.info("Be prepared to explain your thought process and approach.")
elif interview_type == "Mock Interview":
    st.info("I'll act as an interviewer. Answer as you would in a real interview.")

# Add a text input
question = st.text_input("Your question:")

# Add a submit button
if st.button("Ask"):
    if question:
        st.write("Your question:", question)
        
        # Prepare the context based on interview type
        context = f"You are an expert interview coach. Interview type: {interview_type}. "
        
        if interview_type == "Behavioral (STAR Method)":
            context += "Guide the user to structure their response using the STAR method. "
        elif interview_type == "Technical Interview":
            context += "Provide detailed technical guidance and evaluate the approach. "
        elif interview_type == "Mock Interview":
            context += "Act as a professional interviewer. Provide feedback after the response. "
        
        # Combine context and question
        prompt = f'{context} Question: "{question}"'
        
        # Show a spinner while processing
        with st.spinner("Generating response..."):
            # Escape the prompt for shell safety
            escaped_prompt = prompt.replace('"', '\\"')
            
            # Run the command and capture output
            try:
                process = subprocess.run(
                    f'ollama run mistral "{escaped_prompt}"',
                    shell=True,
                    text=True,
                    capture_output=True,
                    timeout=30
                )
                
                if process.returncode == 0:
                    st.write("Response:", process.stdout)
                else:
                    st.error(f"Error: {process.stderr}")
            
            except subprocess.TimeoutExpired:
                st.error("Request timed out after 30 seconds")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Add a status indicator
st.sidebar.markdown("---")
st.sidebar.write("System Status:")
try:
    check = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
    if check.returncode == 0:
        st.sidebar.success("✅ Ollama is running")
    else:
        st.sidebar.error("❌ Ollama is not running properly")
except Exception as e:
    st.sidebar.error(f"❌ Error checking Ollama: {str(e)}")

# Add a suggestion box based on interview type
st.sidebar.markdown("---")
st.sidebar.write("Sample Questions:")
if interview_type == "General Questions":
    st.sidebar.write("- Tell me about yourself")
    st.sidebar.write("- Why do you want this job?")
    st.sidebar.write("- What are your strengths?")
elif interview_type == "Behavioral (STAR Method)":
    st.sidebar.write("- Tell me about a time you handled a conflict")
    st.sidebar.write("- Describe a project you're proud of")
    st.sidebar.write("- Share an example of leadership")
elif interview_type == "Technical Interview":
    st.sidebar.write("- Explain your approach to testing")
    st.sidebar.write("- How would you design this system?")
    st.sidebar.write("- What's your debugging process?")
elif interview_type == "Mock Interview":
    st.sidebar.write("- Start with: 'I'm ready for the interview'")