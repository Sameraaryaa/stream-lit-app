import streamlit as st
import pandas as pd
from datetime import datetime
from utils.storage import load_projects, load_citations, save_citation

def add_citation():
    st.header("Add New Citation")

    citation_data = {}

    citation_data['title'] = st.text_input("Publication Title")
    citation_data['authors'] = st.text_input("Authors (comma-separated)")
    citation_data['year'] = st.text_input("Publication Year")
    citation_data['journal'] = st.text_input("Journal/Conference")
    citation_data['doi'] = st.text_input("DOI (if available)")

    # Project association
    projects = load_projects()
    if not projects.empty:
        project_options = ['None'] + projects['title'].tolist()
        citation_data['project'] = st.selectbox(
            "Associate with Project",
            options=project_options
        )
    else:
        citation_data['project'] = 'None'
        st.info("No projects found. Create a project first to associate citations.")

    if st.button("Add Citation"):
        if citation_data['title'] and citation_data['authors'] and citation_data['year']:
            if save_citation(citation_data):
                st.success("Citation added successfully!")
                st.rerun()
            else:
                st.error("Failed to save citation. Please try again.")
        else:
            st.error("Please fill in all required fields (Title, Authors, Year)")

def view_citations():
    st.header("My Citations")

    citations = load_citations()
    if citations.empty:
        st.info("No citations found. Add your first citation!")
        return

    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        year_filter = st.multiselect(
            "Filter by Year",
            options=sorted(citations['year'].unique())
        )
    with col2:
        project_filter = st.multiselect(
            "Filter by Project",
            options=sorted(citations['project'].unique())
        )

    # Apply filters
    filtered_citations = citations.copy()
    if year_filter:
        filtered_citations = filtered_citations[filtered_citations['year'].isin(year_filter)]
    if project_filter:
        filtered_citations = filtered_citations[filtered_citations['project'].isin(project_filter)]

    # Display citations
    for _, citation in filtered_citations.iterrows():
        with st.expander(f"📚 {citation['title']}"):
            st.write("**Authors:**", citation['authors'])
            st.write("**Year:**", citation['year'])
            st.write("**Journal/Conference:**", citation['journal'])
            if citation['doi']:
                st.write("**DOI:**", citation['doi'])
            if citation['project'] != 'None':
                st.write("**Project:**", citation['project'])

def export_citations():
    st.header("Export Citations")

    citations = load_citations()
    if citations.empty:
        st.info("No citations to export.")
        return

    export_format = st.selectbox(
        "Export Format",
        ["APA", "MLA", "Chicago"]
    )

    if st.button("Export"):
        formatted_citations = []
        if export_format == "APA":
            # Format citations in APA style
            for _, citation in citations.iterrows():
                formatted = f"{citation['authors']} ({citation['year']}). {citation['title']}. {citation['journal']}."
                if citation['doi']:
                    formatted += f" https://doi.org/{citation['doi']}"
                formatted_citations.append(formatted)

            st.download_button(
                "Download Citations",
                "\n\n".join(formatted_citations),
                f"citations_{datetime.now().strftime('%Y%m%d')}.txt",
                "text/plain"
            )

def main():
    st.title("📚 Citations Manager")

    tabs = st.tabs(["View Citations", "Add Citation", "Export"])

    with tabs[0]:
        view_citations()

    with tabs[1]:
        add_citation()

    with tabs[2]:
        export_citations()

if __name__ == "__main__":
    main()