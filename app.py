import os
import re
import time
import streamlit as st

# --------------------------------------------------
# Import Crew Instance
# --------------------------------------------------
try:
    from main import crew
except ImportError:
    crew = None

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Repo Health Auditor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Modern Custom CSS Styling
# --------------------------------------------------
st.markdown(
    """
<style>
    /* Dark / Slate Modern Theme Overrides */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border: 1px solid #312e81;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        text-align: center;
    }
    .hero-title {
        font-size: 2.75rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 400;
    }

    /* Cards */
    .card-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .card-box:hover {
        border-color: #38bdf8;
        transform: translateY(-2px);
    }
    
    /* Status Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .badge-blue { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
    .badge-purple { background: rgba(129, 140, 248, 0.15); color: #818cf8; border: 1px solid rgba(129, 140, 248, 0.3); }
    .badge-green { background: rgba(52, 211, 153, 0.15); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); }

    /* Custom Button */
    .stButton > button {
        background: linear-gradient(90deg, #0284c7 0%, #4f46e5 100%);
        color: #ffffff;
        font-weight: 700;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.5);
        transform: translateY(-1px);
    }

    /* Hide Default Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Hero Header
# --------------------------------------------------
st.markdown(
    """
<div class="hero-container">
    <div class="hero-title">🛡️ Repo Health Auditor</div>
    <div class="hero-subtitle">Automated Multi-Agent GitHub Repository Analysis & Health Diagnostic</div>
</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Top KPI Metric Ribbon
# --------------------------------------------------
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="Active Agents", value="4 Autonomous")
with m2:
    st.metric(label="Execution Engine", value="CrewAI Sequential")
with m3:
    st.metric(label="LLM Gateway", value="OpenRouter")
with m4:
    st.metric(
        label="System Status",
        value="Ready" if crew else "Crew Missing",
        delta="OK" if crew else "Error",
    )

st.write("")

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ System Architecture")
    st.markdown(
        "<span class='badge badge-purple'>CrewAI Framework</span><span class='badge badge-blue'>v2.0</span>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("#### 🤖 Agent Roster")
    st.markdown("""
    1. **🔍 Metadata Collector**
       *File tree & commit history metrics*
    2. **🌐 Signal Researcher**
       *Community sentiment & PR velocity*
    3. **⚡ Issue Triager**
       *Bug frequency & backlog health*
    4. **📄 Report Writer**
       *Synthesizes diagnostic & score*
    """)

    st.markdown("---")

    st.markdown("#### 🛠️ Tech Stack")
    st.markdown("""
    - **Framework:** Streamlit + CrewAI
    - **API Gateway:** OpenRouter
    - **Search Engine:** Exa AI
    """)

# --------------------------------------------------
# Main Input & Action Layout
# --------------------------------------------------
col_input, col_info = st.columns([2, 1])

with col_input:
    st.markdown("### 🚀 Repository Details")
    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/streamlit/streamlit",
        help="Provide the full HTTPS link to the target public repository.",
    )

    col_b, col_empty = st.columns([1, 1])
    with col_b:
        branch = st.text_input("Branch Name", value="main")

    analyze_btn = st.button("⚡ Start Audit Process", use_container_width=True)

with col_info:
    st.markdown(
        """
    <div class="card-box">
        <h4 style="margin-top:0; color:#38bdf8;">📋 Included Deliverables</h4>
        <ul style="color:#cbd5e1; font-size:0.9rem; padding-left:1.2rem; margin-bottom:0;">
            <li>Repository Structural Score</li>
            <li>Issue Backlog Velocity Analysis</li>
            <li>Community Engagement Trends</li>
            <li>Actionable Recommendations</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# Execution Handler
# --------------------------------------------------
def run_repo_health(repo_url, branch):
    if crew is not None:
        crew.kickoff(inputs={"repo_url": repo_url, "branch": branch})
    else:
        st.error(
            "Could not import 'crew' from main.py. Please verify main.py exists."
        )


if analyze_btn:
    if not repo_url.strip():
        st.warning("⚠️ Please provide a valid GitHub Repository URL to proceed.")
        st.stop()

    st.markdown("---")
    st.markdown("### 🔄 Execution Progress")

    progress_bar = st.progress(0)
    status_box = st.empty()

    steps = [
        "1/4 | Collecting repository metadata and file trees...",
        "2/4 | Analyzing community sentiment & PR velocity...",
        "3/4 | Triaging open issues & backlog risks...",
        "4/4 | Generating final Markdown report...",
    ]

    for idx, step_msg in enumerate(steps):
        status_box.info(step_msg)
        time.sleep(0.4)
        progress_bar.progress((idx + 1) / len(steps))

    with st.spinner("🤖 Autonomous AI Agents are collaborating on the audit..."):
        run_repo_health(repo_url, branch)

    status_box.success("✅ Audit Completed Successfully!")

    # --------------------------------------------------
    # Results Presentation
    # --------------------------------------------------
    report_path = os.path.join("task_outputs", "health_report.md")

    st.markdown("---")
    st.markdown("## 📊 Repository Audit Results")

    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            report_text = f.read()

        tab1, tab2 = st.tabs(["📄 Formatted Report", "📥 Download & Raw Code"])

        with tab1:
            st.markdown(
                f"""
            <div class="card-box" style="background:#0f172a;">
                {report_text}
            </div>
            """,
                unsafe_allow_html=True,
            )

        with tab2:
            st.markdown("#### Raw Markdown Content")
            st.code(report_text, language="markdown")

            st.download_button(
                label="⬇️ Download Markdown Report",
                data=report_text,
                file_name=f"health_report_{int(time.time())}.md",
                mime="text/markdown",
                use_container_width=True,
            )
    else:
        st.error("""
        ❌ **Report File Missing**
        
        Expected output path: `task_outputs/health_report.md`
        
        Ensure your task definition in `main.py` specifies:
        `output_file="task_outputs/health_report.md"`
        """)