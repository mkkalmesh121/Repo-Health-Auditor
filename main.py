import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# Load environment variables from .env
load_dotenv()

# Define OpenRouter LLM Configuration
openrouter_llm = LLM(
    model="openrouter/openai/gpt-4o-mini",  # You can also use openrouter/anthropic/claude-3.5-sonnet, openrouter/meta-llama/llama-3.3-70b-instruct, etc.
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


@CrewBase
class RepoHealthAuditorCrew:
    """Repo Health Auditor CrewAI Configuration"""

    @agent
    def repo_metadata_collector(self) -> Agent:
        return Agent(
            role="Repo Metadata Collector",
            goal="Collect repository metadata for {repo_url} on branch {branch}.",
            backstory="Expert GitHub auditor.",
            llm=openrouter_llm,  # Attach OpenRouter LLM
            verbose=True,
        )

    @agent
    def community_signal_researcher(self) -> Agent:
        return Agent(
            role="Community Signal Researcher",
            goal="Research discussions and usage trends for {repo_url}.",
            backstory="Analyzes community velocity and feedback.",
            llm=openrouter_llm,  # Attach OpenRouter LLM
            verbose=True,
        )

    @agent
    def issue_triage_engineer(self) -> Agent:
        return Agent(
            role="Issue Triage Engineer",
            goal="Analyze open issues and bug reports.",
            backstory="Senior DevOps engineer identifying issue backlogs.",
            llm=openrouter_llm,  # Attach OpenRouter LLM
            verbose=True,
        )

    @agent
    def health_report_writer(self) -> Agent:
        return Agent(
            role="Health Report Writer",
            goal="Synthesize metadata, community signals, and issue triage into Markdown report.",
            backstory="Writes technical audit reports.",
            llm=openrouter_llm,  # Attach OpenRouter LLM
            verbose=True,
        )

    # --- TASKS ---
    @task
    def collect_metadata_task(self) -> Task:
        return Task(
            description="Extract repository metadata for: {repo_url} on branch {branch}.",
            expected_output="Summary of repository metadata.",
            agent=self.repo_metadata_collector(),
        )

    @task
    def research_community_task(self) -> Task:
        return Task(
            description="Gather community engagement metrics for {repo_url}.",
            expected_output="Summary of community signals.",
            agent=self.community_signal_researcher(),
        )

    @task
    def triage_issues_task(self) -> Task:
        return Task(
            description="Examine open issues and risks for {repo_url}.",
            expected_output="Detailed triage analysis.",
            agent=self.issue_triage_engineer(),
        )

    @task
    def write_health_report_task(self) -> Task:
        return Task(
            description="Synthesize findings into a complete Markdown report with Health Score (0-100) and recommendations.",
            expected_output="Markdown report saved to task_outputs/health_report.md.",
            agent=self.health_report_writer(),
            output_file="task_outputs/health_report.md",
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


crew = RepoHealthAuditorCrew().crew()