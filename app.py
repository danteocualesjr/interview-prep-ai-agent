import streamlit as st
import subprocess
import time

st.title("Interview Prep AI 💼")

# Add a text input
question = st.text_input("Your question:")

# Add a submit button
if st.button("Ask"):
    if question:
        st.write("Your question:", question)
        
        # Show a spinner while processing
        with st.spinner("Generating response..."):
            # Escape the question for shell safety
            escaped_question = question.replace('"', '\\"')
            
            # Log the command we're about to run
            command = f'ollama run mistral "{escaped_question}"'
            st.write("Sending request...")
            
            try:
                # Run the command and capture output
                process = subprocess.run(
                    command,
                    shell=True,
                    text=True,
                    capture_output=True,
                    timeout=30  # Add a timeout of 30 seconds
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
st.sidebar.write("System Status:")
try:
    check = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
    if check.returncode == 0:
        st.sidebar.success("✅ Ollama is running")
    else:
        st.sidebar.error("❌ Ollama is not running properly")
except Exception as e:
    st.sidebar.error(f"❌ Error checking Ollama: {str(e)}")