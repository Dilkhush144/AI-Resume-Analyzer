"""
AI Resume Analyzer & ATS Fit Scoring Engine
Author: Dilkhush Raj (https://github.com/Dilkhush144)
"""

import os
from pathlib import Path
import streamlit as st

from src.extract import read_pdf, clean_text
from src.embed import embed_single
from src.match import similarity, keyword_gap
from src.ats import basic_ats_checks
from src.rewrite import suggest_bullets
from src.report import build_report

# 1. Page Configuration (must be called first)
st.set_page_config(
    page_title="AI Resume Analyzer | Dilkhush Raj",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Load Custom CSS Safely
css_path = Path(__file__).parent / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Helper for rendering skill tag pills
def render_skill_badges(skills: list[str], badge_type: str = "matched") -> str:
    if not skills:
        return "<span style='color: #8B949E; font-style: italic;'>None detected</span>"
    css_class = f"skill-tag skill-{badge_type}"
    return " ".join([f"<span class='{css_class}'>{s.upper()}</span>" for s in skills])


# 3. Sidebar UI (Always Persistent)
with st.sidebar:
    st.markdown("## 🧠 AI Resume Analyzer")
    st.caption("Dense Vector Embeddings & ATS Hygiene Audit")
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Developer Profile")
    st.markdown(
        """
        **Dilkhush Raj**  
        *B.Tech ECE, NIT Manipur*  
        
        [![GitHub](https://img.shields.io/badge/GitHub-Dilkhush144-181717?style=flat&logo=github)](https://github.com/Dilkhush144)  
        [![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/dilkhush-raj-bb81182ba)  
        [![Repository](https://img.shields.io/badge/Source-Repo-blue?style=flat&logo=git)](https://github.com/Dilkhush144/AI-Resume-Analyzer)
        """
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ How It Works")
    st.markdown(
        """
        1. **NLP Embeddings**: Encodes resume & JD into dense semantic vectors using `all-MiniLM-L6-v2`.
        2. **Cosine Similarity**: Measures contextual alignment beyond naive keyword matching.
        3. **Skill Gap Detection**: Pinpoints exact technical competencies missing from the target JD.
        4. **ATS Hygiene Audit**: Validates section headings, contact links, word counts, and quantifiable metrics.
        """
    )
    
    st.markdown("---")
    with st.expander("🔑 Optional: OpenAI Bullet Rewriter"):
        user_api_key = st.text_input(
            "OpenAI API Key (Optional)",
            type="password",
            placeholder="sk-...",
            help="If provided, bullet points will be rewritten using GPT-3.5. Otherwise, offline STAR formulas are used."
        )


# 4. Main Header
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 2.8rem; margin-bottom: 0.2rem; font-weight: 800;">
            🚀 <span style="background: linear-gradient(135deg, #00BFFF 0%, #0077B6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI Resume Analyzer</span>
        </h1>
        <p style="color: #8B949E; font-size: 1.15rem; margin-top: 0.3rem;">
            Match score, deep keyword gap analysis, and ATS compliance audit in seconds.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Quick Sample Loader
col_sample_btn, col_sample_info = st.columns([1, 3])
with col_sample_btn:
    if st.button("✨ Load Sample SWE Intern Demo", help="Pre-populates sample JD and resume for quick evaluation"):
        sample_jd_path = Path(__file__).parent / "sample_data" / "jd_swe_intern.txt"
        sample_resume_path = Path(__file__).parent / "sample_data" / "sample_resume_text.txt"
        
        if sample_jd_path.exists():
            st.session_state["jd_input"] = sample_jd_path.read_text(encoding="utf-8")
        if sample_resume_path.exists():
            st.session_state["sample_resume_text"] = sample_resume_path.read_text(encoding="utf-8")
            st.session_state["use_sample_resume"] = True
        st.rerun()

with col_sample_info:
    if st.session_state.get("use_sample_resume"):
        st.info("Loaded sample data! Click **'Analyze Fit & ATS Score'** below to run.")


# 5. User Input Section
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 1. Target Job Description")
    default_jd = st.session_state.get("jd_input", "")
    jd_text_input = st.text_area(
        "Paste the complete Job Description here:",
        value=default_jd,
        height=260,
        placeholder="e.g. Looking for a Software Engineer with experience in Python, React, RESTful APIs, Docker, and AWS..."
    )

with col2:
    st.markdown("### 📎 2. Candidate Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume in PDF format:",
        type=["pdf"],
        help="Upload a standard single-page or two-page resume PDF."
    )
    
    use_sample = False
    if "sample_resume_text" in st.session_state:
        use_sample = st.checkbox("Use pre-loaded sample resume text", value=st.session_state.get("use_sample_resume", False))


st.markdown("---")
analyze_btn = st.button("🔍 Analyze Fit & ATS Score", type="primary", use_container_width=True)


# 6. Analysis Execution
if analyze_btn:
    clean_jd = clean_text(jd_text_input)
    
    if not clean_jd:
        st.error("⚠️ Please provide a Job Description to compare against.")
    elif not uploaded_file and not (use_sample and "sample_resume_text" in st.session_state):
        st.error("⚠️ Please upload a Resume PDF (or check 'Use pre-loaded sample resume').")
    else:
        with st.spinner("Extracting text and running neural embedding model..."):
            filename = "Dilkhush_Raj_Resume.pdf"
            if uploaded_file is not None:
                filename = uploaded_file.name
                resume_raw = read_pdf(uploaded_file)
            else:
                resume_raw = st.session_state["sample_resume_text"]
                filename = "Sample_SWE_Resume.pdf"

            clean_resume = clean_text(resume_raw)

            if not clean_resume or len(clean_resume.strip()) < 30:
                st.error("Could not extract readable text from the uploaded PDF. Please make sure it is not a scanned image PDF.")
            else:
                # 1. Embeddings & Cosine Similarity
                r_vec = embed_single(clean_resume)
                j_vec = embed_single(clean_jd)
                score = similarity(r_vec, j_vec)

                # 2. Keyword & Skill Gap Analysis
                gap_results = keyword_gap(clean_jd, clean_resume)

                # 3. ATS & Hygiene Audit
                ats_results = basic_ats_checks(clean_resume, filename=filename)

                # 4. Bullet Suggestions
                suggested_bullets = suggest_bullets(
                    role_title="Software Engineer",
                    jd_text=clean_jd,
                    missing_keywords=gap_results["missing_skills"],
                    openai_api_key=user_api_key
                )

                # Cache in session state
                st.session_state["results"] = {
                    "score": score,
                    "gap_results": gap_results,
                    "ats_results": ats_results,
                    "suggested_bullets": suggested_bullets,
                    "clean_jd": clean_jd,
                    "filename": filename
                }


# 7. Render Results Dashboard
if "results" in st.session_state:
    res = st.session_state["results"]
    score = res["score"]
    score_pct = round(score * 100, 1)
    gap_results = res["gap_results"]
    ats_results = res["ats_results"]
    suggested_bullets = res["suggested_bullets"]
    filename = res["filename"]

    st.markdown("## 📊 Analysis Dashboard")

    # Match Score Top Bar
    score_col1, score_col2, score_col3 = st.columns([1.5, 2, 2.5])

    with score_col1:
        st.metric(label="ATS Match Score", value=f"{score_pct} / 100")

    with score_col2:
        if score_pct >= 75:
            tier_label = "🟢 High Alignment"
            tier_desc = "Strong contextual match with job requirements."
        elif score_pct >= 55:
            tier_label = "🟡 Moderate Alignment"
            tier_desc = "Good foundation; adding missing skills will boost ranking."
        else:
            tier_label = "🔴 Needs Optimization"
            tier_desc = "Significant gap between JD expectations and resume keywords."
        
        st.markdown(f"**Fit Status:** {tier_label}")
        st.caption(tier_desc)

    with score_col3:
        st.write("Score Progress")
        st.progress(min(max(score, 0.0), 1.0))

    st.markdown("<br>", unsafe_allow_html=True)

    # Detailed Tabs
    tab_skills, tab_ats, tab_bullets, tab_report = st.tabs([
        "🎯 Technical Skill Gaps",
        "📋 ATS & Formatting Audit",
        "✏️ Action Bullet Suggestions",
        "💾 Full Audit Report"
    ])

    with tab_skills:
        st.markdown("### 🔍 Technical Competencies Overview")
        
        matched = gap_results.get("matched_skills", [])
        missing = gap_results.get("missing_skills", [])
        general = gap_results.get("general_gaps", [])

        st.markdown(f"#### ✅ Matched Skills in Resume ({len(matched)})")
        st.markdown(render_skill_badges(matched, "matched"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"#### ⚠️ Missing Target Skills from Job Description ({len(missing)})")
        if missing:
            st.markdown(render_skill_badges(missing, "missing"), unsafe_allow_html=True)
            st.info("Tip: If you have experience with these skills, add them into your project bullets and skills section.")
        else:
            st.success("🎉 Great job! Your resume covers all prominent technical skills requested in the job description.")

        if general:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"#### 🔑 Additional High-Frequency JD Keywords ({len(general)})")
            st.markdown(render_skill_badges(general[:15], "general"), unsafe_allow_html=True)

    with tab_ats:
        st.markdown("### 📋 ATS Hygiene & Formatting Audit")
        
        pass_count = sum(1 for c in ats_results if c["status"] == "pass")
        warn_count = sum(1 for c in ats_results if c["status"] != "pass")

        st.caption(f"Passed: **{pass_count}** checks | Opportunities for improvement: **{warn_count}**")

        for item in ats_results:
            with st.container():
                if item["status"] == "pass":
                    st.success(f"**{item['title']}** ({item['category']}): {item['message']}")
                elif item["status"] == "warning":
                    st.warning(f"**{item['title']}** ({item['category']}): {item['message']}")
                else:
                    st.info(f"**{item['title']}** ({item['category']}): {item['message']}")

    with tab_bullets:
        st.markdown("### ✏️ High-Impact Bullet Rewrites (Google XYZ / STAR Formula)")
        st.caption("Apply these formulas to integrate missing skills and highlight measurable engineering impact.")

        for bullet in suggested_bullets:
            st.markdown(f"- {bullet}")

    with tab_report:
        st.markdown("### 💾 Export Complete Audit Report")
        report_text = build_report(score, gap_results, ats_results, filename=filename)

        st.text_area("Audit Report Preview", value=report_text, height=280)

        st.download_button(
            label="⬇️ Download Audit Report (.txt)",
            data=report_text.encode("utf-8"),
            file_name="AI_Resume_Analyzer_Audit_Report.txt",
            mime="text/plain",
            type="primary"
        )
