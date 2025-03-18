import pandas as pd
from datetime import datetime

def create_problem_statement(context, focus, significance):
    """Generate a structured problem statement"""
    template = f"""Research Problem Statement:

Context: {context}

Focus: {focus}

Significance: {significance}

This research aims to address {focus} within the context of {context}, 
which is significant because {significance}."""
    
    return template

def generate_research_questions(problem_statement, num_questions=3):
    """Generate research questions based on problem statement"""
    # This would typically use NLP, but for now we'll return template questions
    questions = [
        "What are the primary factors affecting the research problem?",
        "How do these factors interact with each other?",
        "What are the potential solutions to address this problem?"
    ]
    return questions[:num_questions]

def create_research_timeline(start_date, end_date):
    """Create a research timeline with milestones"""
    timeline = {
        'Problem Formulation': {'start': start_date, 'duration': '2 weeks'},
        'Literature Review': {'start': None, 'duration': '4 weeks'},
        'Research Design': {'start': None, 'duration': '3 weeks'},
        'Data Collection': {'start': None, 'duration': '6 weeks'},
        'Data Analysis': {'start': None, 'duration': '4 weeks'},
        'Report Writing': {'start': None, 'duration': '4 weeks'}
    }
    return timeline

def calculate_sample_size(confidence_level, margin_error, population_size=None):
    """Calculate required sample size"""
    # Basic sample size calculation
    z_scores = {
        0.90: 1.645,
        0.95: 1.96,
        0.99: 2.576
    }
    z = z_scores.get(confidence_level, 1.96)
    
    if population_size:
        sample_size = (z**2 * 0.25 * population_size) / ((margin_error**2 * (population_size - 1)) + (z**2 * 0.25))
    else:
        sample_size = (z**2 * 0.25) / (margin_error**2)
    
    return round(sample_size)
