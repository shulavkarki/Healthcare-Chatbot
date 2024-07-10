import streamlit as st
from llm import generate_response

def initialize_chat_history():
    """Initialize chat history if not already done."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    """Display chat messages from history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def add_user_message_to_history(prompt):
    """Add user message to chat history and display it."""
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

def add_assistant_message_to_history(response, source):
    """Add assistant message to chat history and display it."""
    source_list = "\n".join([f"- {src}" for src in source])
    response_with_source = f"{response}\n\n**Sources:**\n{source_list}"
    # response_with_source = response + "\n" + "Source:" + "\n".join(source)
    with st.chat_message("assistant"):
        st.markdown(response_with_source)
    st.session_state.messages.append({"role": "assistant", "content": response_with_source})

def main():
    st.title("Healthcare Chatbot")

    initialize_chat_history()
    display_chat_history()

    if prompt := st.chat_input("Ask anything regarding health-related"):
        add_user_message_to_history(prompt)
        
        response, source = generate_response(prompt)
        add_assistant_message_to_history(response, source)

if __name__ == "__main__":
    main()
