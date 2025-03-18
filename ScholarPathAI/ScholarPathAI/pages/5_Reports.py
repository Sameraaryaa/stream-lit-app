import streamlit as st
from utils.report_generator import generate_research_report
from utils.storage import load_projects, load_citations
from datetime import datetime

def generate_report():
    st.header("Generate Research Report")
    
    # Load project data
    projects = load_projects()
    if projects.empty:
        st.warning("No projects found. Create a project first!")
        return
    
    selected_project = st.selectbox(
        "Select Project",
        options=projects['title'].tolist()
    )
    
    if selected_project:
        project_data = projects[projects['title'] == selected_project].iloc[0].to_dict()
        
        # Load related citations
        citations = load_citations()
        project_citations = citations[citations['project'] == selected_project]
        
        # Report sections
        st.subheader("Report Sections")
        
        # Introduction
        st.write("Introduction")
        project_data['introduction'] = st.text_area(
            "Edit Introduction",
            value=project_data.get('problem_statement', ''),
            height=200
        )
        
        # Methodology
        st.write("Methodology")
        project_data['methodology'] = st.text_area(
            "Research Methodology",
            value=project_data.get('methodology', ''),
            height=200
        )
        
        # Results
        st.write("Results")
        results_text = st.text_area(
            "Research Results",
            value=project_data.get('results', ''),
            height=200
        )
        
        # Analysis Results
        analysis_results = {
            'summary': results_text
        }
        
        if st.button("Generate Report"):
            report = generate_research_report(
                project_data,
                analysis_results,
                project_citations
            )
            
            st.download_button(
                "Download Report",
                report,
                f"research_report_{datetime.now().strftime('%Y%m%d')}.txt",
                "text/plain"
            )
            
            st.subheader("Preview")
            st.text(report)

def view_reports():
    st.header("My Reports")
    st.info("This feature will show previously generated reports")
    
    # This would typically load from a reports database
    st.write("No saved reports found")

def main():
    st.title("📄 Research Reports")
    
    tab1, tab2 = st.tabs(["Generate Report", "View Reports"])
    
    with tab1:
        generate_report()
    
    with tab2:
        view_reports()

if __name__ == "__main__":
    main()
