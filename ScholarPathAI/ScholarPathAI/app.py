import streamlit as st
import pandas as pd
from pathlib import Path
import json
import os
from utils.storage import initialize_storage, load_projects
from utils.research_tools import create_problem_statement
import sys
from components.bottom_menu import show_bottom_menu

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/0_Login.py")

logger.info("Starting application initialization...")

# Initialize storage
try:
    storage_init = initialize_storage()
    logger.info(f"Storage initialization result: {storage_init}")
except Exception as e:
    logger.error(f"Storage initialization failed: {str(e)}")
    st.error("Failed to initialize storage. Please try refreshing the page.")
    sys.exit(1)

# Page configuration
try:
    logger.info("Configuring Streamlit page...")
    st.set_page_config(
        page_title="ScholarPath",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    logger.info("Page configuration successful")
except Exception as e:
    logger.error(f"Error in page configuration: {str(e)}")
    st.error("Failed to configure page. Please try refreshing.")
    sys.exit(1)

def main():
    try:
        logger.info("Starting main application...")
        st.title("📚 ScholarPath Research Assistant")

        # Welcome message with username
        st.write(f"Welcome back, {st.session_state.username}!")

        # Global search in sidebar
        with st.sidebar:
            st.text_input("🔍 Search", key="global_search", help="Search across all content")
            st.divider()

        # Dashboard layout
        col1, col2 = st.columns([2, 1])

        with col1:
            logger.info("Rendering research dashboard...")
            st.header("Research Dashboard")

            # Project selection
            projects = load_projects()
            if projects.empty:
                st.info("No projects yet. Create your first project in the Projects tab!")
            else:
                selected_project = st.selectbox(
                    "Select Active Project",
                    options=projects['title'].tolist(),
                    help="Choose a project to view its details"
                )

                # Show project progress only if a project is selected
                if selected_project:
                    try:
                        project_data = projects[projects['title'] == selected_project]
                        if not project_data.empty:
                            project_info = project_data.iloc[0]
                            st.subheader("Project Progress")
                            stages = ['Problem Formulation', 'Literature Review', 'Research Design', 
                                    'Data Collection', 'Analysis', 'Reporting']
                            for stage in stages:
                                progress = float(project_info.get(f'{stage.lower()}_progress', 0))
                                st.progress(progress, text=stage)
                        else:
                            st.warning("Selected project not found.")
                    except Exception as e:
                        logger.error(f"Error displaying project progress: {str(e)}")
                        st.error("Error loading project progress.")

        with col2:
            logger.info("Rendering quick actions...")
            st.header("Quick Actions")
            if st.button("📝 New Project", use_container_width=True):
                st.switch_page("pages/2_Projects.py")
            if st.button("📚 Manage Citations", use_container_width=True):
                st.switch_page("pages/3_Citations.py")
            if st.button("📊 Data Analysis", use_container_width=True):
                st.switch_page("pages/4_Analysis.py")
            if st.button("📄 Generate Report", use_container_width=True):
                st.switch_page("pages/5_Reports.py")

            # Recent Activities
            st.subheader("Recent Activities")
            st.info("No recent activities")

        # Show bottom menu
        show_bottom_menu()

        logger.info("Main application rendered successfully")

    except Exception as e:
        logger.error(f"Error in main application: {str(e)}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")
        if st.button("Retry"):
            st.rerun()

if __name__ == "__main__":
    main()