from crewai import Agent

metadata_agent = Agent(
    role="Repo Metadata Collector",
    goal="Collect GitHub repository metadata.",
    backstory="GitHub repository expert."
)

community_agent = Agent(
    role="Community Signal Researcher",
    goal="Analyze repository community activity.",
    backstory="Open-source community analyst."
)

issue_agent = Agent(
    role="Issue Triage Engineer",
    goal="Analyze repository issues.",
    backstory="Software maintenance engineer."
)

report_agent = Agent(
    role="Health Report Writer",
    goal="Generate a professional repository health report.",
    backstory="Technical documentation expert."
)