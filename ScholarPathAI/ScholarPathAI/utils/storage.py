import pandas as pd
import json
from pathlib import Path
import os
import logging

logger = logging.getLogger(__name__)

def initialize_storage():
    """Initialize storage directories and files"""
    try:
        logger.info("Initializing storage directories...")

        # Create necessary directories
        for directory in ["data", "data/projects", "data/citations", "data/reports"]:
            Path(directory).mkdir(exist_ok=True, parents=True)
            logger.info(f"Created directory: {directory}")

        # Initialize projects database if not exists
        if not Path("data/projects.csv").exists():
            projects_df = pd.DataFrame({
                'title': [],
                'description': [],
                'status': [],
                'created_date': [],
                'problem_formulation_progress': [],
                'literature_review_progress': [],
                'research_design_progress': [],
                'data_collection_progress': [],
                'analysis_progress': [],
                'reporting_progress': []
            })
            projects_df.to_csv("data/projects.csv", index=False)
            logger.info("Created projects database")

        # Initialize citations database if not exists
        if not Path("data/citations.csv").exists():
            citations_df = pd.DataFrame({
                'title': [],
                'authors': [],
                'year': [],
                'journal': [],
                'doi': [],
                'project': []
            })
            citations_df.to_csv("data/citations.csv", index=False)
            logger.info("Created citations database")

        return True
    except Exception as e:
        logger.error(f"Error initializing storage: {str(e)}", exc_info=True)
        return False

def load_projects():
    """Load projects database"""
    try:
        if Path("data/projects.csv").exists():
            return pd.read_csv("data/projects.csv")
        logger.warning("Projects database not found, returning empty DataFrame")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading projects: {str(e)}", exc_info=True)
        return pd.DataFrame()

def save_project(project_data):
    """Save project to database"""
    try:
        projects = load_projects()
        projects = pd.concat([projects, pd.DataFrame([project_data])], ignore_index=True)
        projects.to_csv("data/projects.csv", index=False)
        logger.info(f"Saved project: {project_data.get('title', 'Unknown')}")
        return True
    except Exception as e:
        logger.error(f"Error saving project: {str(e)}", exc_info=True)
        return False

def load_citations():
    """Load citations database"""
    try:
        if Path("data/citations.csv").exists():
            return pd.read_csv("data/citations.csv")
        logger.warning("Citations database not found, returning empty DataFrame")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading citations: {str(e)}", exc_info=True)
        return pd.DataFrame()

def save_citation(citation_data):
    """Save citation to database"""
    try:
        citations = load_citations()
        citations = pd.concat([citations, pd.DataFrame([citation_data])], ignore_index=True)
        citations.to_csv("data/citations.csv", index=False)
        logger.info(f"Saved citation: {citation_data.get('title', 'Unknown')}")
        return True
    except Exception as e:
        logger.error(f"Error saving citation: {str(e)}", exc_info=True)
        return False