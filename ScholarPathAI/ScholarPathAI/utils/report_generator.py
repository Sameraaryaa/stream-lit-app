from datetime import datetime

def generate_research_report(project_data, analysis_results, citations):
    """Generate a research report"""
    report = f"""
Research Report
{'-' * 50}

Title: {project_data['title']}
Date: {datetime.now().strftime('%Y-%m-%d')}

1. Introduction
{'-' * 20}
{project_data.get('problem_statement', 'No problem statement provided')}

2. Research Questions
{'-' * 20}
{format_research_questions(project_data.get('research_questions', []))}

3. Methodology
{'-' * 20}
{project_data.get('methodology', 'Methodology not specified')}

4. Results
{'-' * 20}
{format_analysis_results(analysis_results)}

5. References
{'-' * 20}
{format_citations(citations)}
"""
    return report

def format_research_questions(questions):
    """Format research questions for the report"""
    if not questions:
        return "No research questions defined"
    
    formatted = "Research Questions:\n"
    for i, q in enumerate(questions, 1):
        formatted += f"{i}. {q}\n"
    return formatted

def format_analysis_results(results):
    """Format analysis results for the report"""
    if not results:
        return "No analysis results available"
    
    formatted = "Analysis Results:\n"
    for key, value in results.items():
        formatted += f"\n{key}:\n{value}\n"
    return formatted

def format_citations(citations):
    """Format citations in APA style"""
    if citations.empty:
        return "No citations"
    
    formatted = "References:\n"
    for _, citation in citations.iterrows():
        formatted += f"\n{citation['authors']} ({citation['year']}). {citation['title']}. {citation['journal']}."
    return formatted
