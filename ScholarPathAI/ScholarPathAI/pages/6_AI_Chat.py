import streamlit as st
from datetime import datetime
from groq import Groq
import logging
import os

logger = logging.getLogger(__name__)

def initialize_chat():
    """Initialize chat session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I'm your research assistant. How can I help you today? You can ask me to explain research papers or anything else you're curious about!"
            }
        ]

def get_groq_key():
    """Safely retrieve Groq API key"""
    try:
        # Try multiple methods to get the API key
        api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment or secrets")
        return api_key
    except Exception as e:
        logger.error(f"Error accessing Groq API key: {str(e)}")
        return None

def setup_groq_client():
    """Set up Groq client with error handling"""
    try:
        api_key = get_groq_key()
        if not api_key:
            st.error("Groq API key not found or invalid. Please check your secrets configuration.")
            logger.error("Missing or invalid Groq API key")
            return None

        client = Groq(api_key=api_key)
        logger.info("Groq client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Error setting up Groq client: {str(e)}")
        st.error(f"Error setting up Groq client: {str(e)}")
        return None

def main():
    try:
        st.title("🤖 Research Assistant Chat")
        st.subheader("~ Powered by GROQ")

        # Initialize chat history
        initialize_chat()

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Setup Groq client
        client = setup_groq_client()
        if not client:
            st.warning("Chat functionality is currently unavailable. Please ensure the API key is properly configured.")
            st.info("Contact the administrator to verify the Groq API configuration.")
            return

        # Chat input
        if user_input := st.chat_input("Ask me about your research..."):
            logger.info("Received user input")

            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Display user message
            with st.chat_message("user"):
                st.write(user_input)

            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        chat_completion = client.chat.completions.create(
                            messages=[
                                {
                                    "role": "system",
                                    "content": "You are a helpful research assistant. Provide clear, concise explanations about research topics and papers when asked."
                                },
                                *st.session_state.messages
                            ],
                            model="deepseek-r1-distill-qwen-32b",
                            stream=False,
                        )
                        response = chat_completion.choices[0].message.content
                        st.write(response)
                        logger.info("Generated response successfully")

                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = f"Error generating response: {str(e)}"
                        logger.error(error_msg)
                        st.error(error_msg)
                        # Provide fallback response
                        fallback_msg = "I apologize, but I'm having trouble generating a response right now. Please try again in a moment."
                        st.write(fallback_msg)
                        st.session_state.messages.append({"role": "assistant", "content": fallback_msg})

        # Clear chat button
        if st.button("Clear Chat", key="clear_chat"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Conversation cleared! How can I assist you now?"
                }
            ]
            logger.info("Chat history cleared")
            st.rerun()

    except Exception as e:
        error_msg = f"Error in chat application: {str(e)}"
        logger.error(error_msg)
        st.error(error_msg)
        if st.button("Retry"):
            st.rerun()

if __name__ == "__main__":
    main()