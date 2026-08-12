from crewai import Task
from agents import (
    metadata_agent,
    community_agent,
    issue_agent,
    report_agent
)

def create_tasks(repo_data):

    metadata = Task(
        description=f"Analyze repository metadata:\n{repo_data}",
        expected_output="Repository metadata summary",
        agent=metadata_agent
    )

    community = Task(
        description=f"Analyze community activity:\n{repo_data}",
        expected_output="Community analysis",
        agent=community_agent
    )

    issues = Task(
        description=f"Analyze repository issues:\n{repo_data}",
        expected_output="Issue analysis",
        agent=issue_agent
    )

    report = Task(
        description="""
Combine all analyses into a professional GitHub
Repository Health Report.
""",
        expected_output="Markdown report",
        agent=report_agent
    )

    return metadata, community, issues, report