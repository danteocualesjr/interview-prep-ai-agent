import streamlit as st
import ollama

# Set page configuration
st.set_page_config(
    page_title="Interview Prep AI",
    page_icon="💼",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# App title and description
st.title("Interview Prep AI 💼")
st.markdown("""
Welcome! I'm your AI interview preparation assistant. I can help you with:
- Mock interviews
- Common interview questions
- Technical interview practice
- Behavioral question preparation
""")

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask me anything about interview preparation..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        try:
            response = ollama.chat(
                model='mistral',
                messages=[{"role": m["role"], "content": m["content"]} 
                         for m in st.session_state.messages]
            )
            assistant_response = response['message']['content']
            st.markdown(assistant_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_response}
            )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")