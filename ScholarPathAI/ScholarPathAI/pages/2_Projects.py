import streamlit as st
import pandas as pd
from datetime import datetime
from utils.storage import load_projects, save_project
from utils.research_tools import create_problem_statement, generate_research_questions

def create_new_project():
    st.header("Create New Project")
    
    project_data = {}
    
    project_data['title'] = st.text_input("Project Title")
    project_data['description'] = st.text_area("Project Description")
    
    # Problem Statement Builder
    st.subheader("Problem Statement Builder")
    context = st.text_area("Research Context")
    focus = st.text_area("Research Focus")
    significance = st.text_area("Research Significance")
    
    if context and focus and significance:
        problem_statement = create_problem_statement(context, focus, significance)
        st.write("Generated Problem Statement:")
        st.info(problem_statement)
        project_data['problem_statement'] = problem_statement
    
    # Research Questions
    if st.checkbox("Generate Research Questions"):
        if 'problem_statement' in project_data:
            questions = generate_research_questions(project_data['problem_statement'])
            st.write("Suggested Research Questions:")
            project_data['research_questions'] = []
            for i, q in enumerate(questions):
                if st.checkbox(q, key=f"q_{i}"):
                    project_data['research_questions'].append(q)
    
    # Project Timeline
    st.subheader("Project Timeline")
    project_data['start_date'] = st.date_input("Start Date")
    project_data['end_date'] = st.date_input("End Date")
    
    # Initial Progress
    project_data.update({
        'status': 'Active',
        'created_date': datetime.now().strftime('%Y-%m-%d'),
        'problem_formulation_progress': 0.0,
        'literature_review_progress': 0.0,
        'research_design_progress': 0.0,
        'data_collection_progress': 0.0,
        'analysis_progress': 0.0,
        'reporting_progress': 0.0
    })
    
    if st.button("Create Project"):
        save_project(project_data)
        st.success("Project created successfully!")
        st.session_state.current_project = project_data['title']

def view_projects():
    st.header("My Projects")
    
    projects = load_projects()
    if projects.empty:
        st.info("No projects found. Create your first project!")
        return
    
    for _, project in projects.iterrows():
        with st.expander(f"📋 {project['title']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write("**Description:**", project['description'])
                st.write("**Status:**", project['status'])
                st.write("**Created:**", project['created_date'])
            
            with col2:
                st.write("**Progress:**")
                st.progress(float(project['problem_formulation_progress']), "Problem")
                st.progress(float(project['literature_review_progress']), "Literature")
                st.progress(float(project['research_design_progress']), "Design")
                st.progress(float(project['data_collection_progress']), "Data")
                st.progress(float(project['analysis_progress']), "Analysis")
                st.progress(float(project['reporting_progress']), "Report")

def main():
    st.title("📋 Projects")
    
    tab1, tab2 = st.tabs(["My Projects", "Create New Project"])
    
    with tab1:
        view_projects()
    
    with tab2:
        create_new_project()

if __name__ == "__main__":
    main()
