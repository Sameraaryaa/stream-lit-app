import streamlit as st

def show_bottom_menu():
    # Create a container for the bottom menu
    with st.container():
        # Add some space before the menu
        st.write("")
        st.write("")
        
        # Create columns for menu items
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("🏠 Home", use_container_width=True):
                st.switch_page("app.py")
                
        with col2:
            if st.button("📚 Research", use_container_width=True):
                st.switch_page("pages/2_Projects.py")
                
        with col3:
            if st.button("📊 Analysis", use_container_width=True):
                st.switch_page("pages/4_Analysis.py")
                
        with col4:
            if st.button("🤖 AI Chat", use_container_width=True):
                st.switch_page("pages/6_AI_Chat.py")
                
        with col5:
            if st.button("⚙️ Settings", use_container_width=True):
                st.switch_page("pages/7_Settings.py")
        
        # Add styling
        st.markdown(
            """
            <style>
            .stButton button {
                background-color: transparent;
                border: none;
                padding: 10px 0;
                width: 100%;
            }
            .stButton button:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            </style>
            """,
            unsafe_allow_html=True
        )
