# 🚀 AI Resume Analyzer & ATS Fit Scoring Engine

<p align="center">
  <strong>Analyze Resume–JD Alignment • Semantic Embeddings • ATS Hygiene Audit • Keyword Gap Analysis</strong>
</p>

<p align="center">
  <a href="https://github.com/Dilkhush144/AI-Resume-Analyzer"><img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python 3.10+"></a>
  <a href="https://streamlit.io"><img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit" alt="Streamlit"></a>
  <a href="https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2"><img src="https://img.shields.io/badge/Embeddings-Sentence--Transformers-orange?logo=huggingface" alt="Sentence Transformers"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License"></a>
  <a href="https://github.com/Dilkhush144"><img src="https://img.shields.io/badge/Author-Dilkhush%20Raj-blueviolet" alt="Author Dilkhush Raj"></a>
</p>

---

## 🌐 Live Interactive Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dilkhush144-ai-resume-analyzer.streamlit.app)

🚀 **[👉 Click here to Open the Live App](https://dilkhush144-ai-resume-analyzer.streamlit.app)**  
*Live Application URL: [https://dilkhush144-ai-resume-analyzer.streamlit.app](https://dilkhush144-ai-resume-analyzer.streamlit.app)*

> ✨ **Quick Demo Test**: The app includes a built-in **"Load Sample SWE Intern Demo"** button so recruiters and visitors can test the analysis in 1 click without needing to upload a resume file!

---

## 📌 Project Overview

Modern Applicant Tracking Systems (ATS) and hiring teams process hundreds of applications per job posting. Traditional resume screeners rely on rigid keyword matches, failing to recognize synonyms or semantic context.

**AI Resume Analyzer** solves this by combining **dense NLP vector embeddings** (`all-MiniLM-L6-v2`) and **cosine similarity** with heuristic ATS compliance checks:

- Evaluates how contextually well a candidate's resume aligns with a given Job Description (JD).
- Detects missing technical skills and keyword opportunities across languages, frameworks, cloud, and databases.
- Audits critical formatting and ATS hygiene standards (contact info, LinkedIn/GitHub links, word density, quantifiable metrics, active verbs).
- Generates action-oriented bullet rewrite recommendations based on the **Google XYZ formula** (`Accomplished [X] as measured by [Y], by doing [Z]`).
- Exports a complete, formatted audit report ready for download.

---

## ✨ Key Features

### 🧠 Semantic NLP Matching
- Uses `sentence-transformers/all-MiniLM-L6-v2` to transform unstructured resume and JD text into 384-dimensional dense vectors.
- Calculates normalized **Cosine Similarity** to compute an objective match score (0–100) reflecting true contextual alignment, not just repetitive keyword stuffing.

### 🎯 Skill & Keyword Gap Detection
- Identifies recognized technical competencies present in both the resume and JD (**Matched Skills**).
- Pinpoints critical requirements from the JD absent in the resume (**Missing Skills**).
- Highlights high-frequency keywords to help candidates tailor their applications truthfully.

### 📋 ATS Hygiene & Best-Practice Audit
- **Filename Validation**: Flags spaces or risky characters that can cause parser truncation (e.g., recommends `Dilkhush_Raj_Resume.pdf`).
- **Contact Details Check**: Verifies presence of professional email and phone number.
- **Online Profiles Check**: Confirms LinkedIn and GitHub/portfolio profile links.
- **Section Heading Compliance**: Ensures standard headings (`Education`, `Skills`, `Projects`, `Experience`).
- **Word Density Heuristic**: Audits length for optimal single-page standards (~400–800 words).
- **Quantifiable Impact Scan**: Scans for numbers, percentages, and metrics validating engineering achievement.
- **Action Verbs Check**: Identifies strong active verbs (`Built`, `Optimized`, `Architected`, `Deployed`).

### ✏️ Bullet Optimizer & STAR Suggestions
- Provides high-impact rewrite suggestions following the STAR (Situation, Task, Action, Result) method and Google XYZ framework.
- Optional **OpenAI GPT** integration for tailored, dynamic bullet rewrites when an API key is provided.

### 💾 One-Click Downloadable Audit Report
- Generates a timestamped `.txt` summary containing score breakdowns, skill tables, ATS check items, and recommended next steps.

---

## 🏗️ Architecture & Data Workflow

```text
  ┌───────────────────────┐             ┌────────────────────────┐
  │ Candidate Resume (PDF)│             │  Job Description (JD)  │
  └───────────┬───────────┘             └───────────┬────────────┘
              │                                     │
              ▼ (pdfplumber)                        ▼
     Text Extraction & Normalization       Text Cleaning & Tokenization
              │                                     │
              ├─────────────────┬───────────────────┤
              │                 │                   │
              ▼                 ▼                   ▼
    ┌──────────────────┐ ┌─────────────┐ ┌──────────────────────┐
    │ Sentence-        │ │  Keyword    │ │  ATS Hygiene Audit   │
    │ Transformer      │ │  Gap Engine │ │  • Contact / Links   │
    │ (all-MiniLM-L6)  │ │  • Matched  │ │  • Standard Sections │
    └─────────┬────────┘ │  • Missing  │ │  • Quantified Metric │
              │          └──────┬──────┘ └──────────┬───────────┘
              ▼                 │                   │
       Cosine Similarity        │                   │
              │                 │                   │
              └─────────────────┼───────────────────┘
                                │
                                ▼
         ┌─────────────────────────────────────────────┐
         │     Streamlit Interactive Dashboard UI      │
         │  • Match Score KPI   • Skill Badges         │
         │  • ATS Checklist     • STAR Bullet Tips     │
         │  • Downloadable Audit Report (.txt)         │
         └─────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Description |
|---|---|---|
| **Language** | Python 3.10+ | Core application logic |
| **Web Framework** | Streamlit | Modern reactive user interface and state management |
| **Embeddings** | Sentence-Transformers | Dense vector representations via `all-MiniLM-L6-v2` |
| **Vector Math** | Scikit-Learn & NumPy | Cosine similarity calculation and array operations |
| **PDF Extraction** | pdfplumber | Reliable text extraction from multi-page PDFs |
| **Styling** | Custom CSS & TOML | Dark GitHub-inspired UI theme |
| **Optional LLM** | OpenAI API | Dynamic bullet point rewriting (optional) |

---

## 📁 Project Structure

```text
AI-Resume-Analyzer/
├── .streamlit/
│   └── config.toml           # Streamlit theme (dark mode, accent colors, server config)
├── src/
│   ├── __init__.py           # Package marker
│   ├── ats.py                # Comprehensive ATS hygiene & compliance checks
│   ├── embed.py              # SentenceTransformer model loader with @st.cache_resource
│   ├── extract.py            # PDF parsing & robust text normalization
│   ├── match.py              # Cosine similarity and tech skill gap analysis
│   ├── report.py             # Formatted text audit report generator
│   └── rewrite.py            # Action-oriented bullet optimizer (Google XYZ / STAR)
├── sample_data/
│   ├── jd_swe_intern.txt     # Sample software engineering internship JD
│   └── sample_resume_text.txt# Sample candidate resume for instant demo testing
├── app.py                    # Main interactive Streamlit application
├── streamlit_app.py          # Streamlit Cloud deployment entry point
├── requirements.txt          # Production dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore configuration
├── LICENSE                   # MIT License
└── README.md                 # Complete project documentation
```

---

## ⚙️ Local Setup & Installation

### 1. Prerequisites
- Python 3.9, 3.10, or 3.11 installed
- Git installed

### 2. Clone the Repository
```bash
git clone https://github.com/Dilkhush144/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 3. Create & Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. (Optional) Configure OpenAI API Key
If you want LLM-powered bullet point rewrites, copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your key inside `.env`:
```env
OPENAI_API_KEY=sk-...
```
*(Alternatively, enter your key directly in the app's sidebar during runtime).*

### 6. Run the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ How to Deploy on Streamlit Community Cloud (Free)

Deploying this app live takes under 2 minutes:

1. **Push your code to GitHub** (public repository `Dilkhush144/AI-Resume-Analyzer`).
2. Visit **[share.streamlit.io](https://share.streamlit.io)** and sign in with your GitHub account.
3. Click **"New app"**.
4. Configure the settings:
   - **Repository:** `Dilkhush144/AI-Resume-Analyzer`
   - **Branch:** `main`
   - **Main file path:** `app.py` *(or `streamlit_app.py`)*
   - **App URL:** Customize subdomain (e.g. `dilkhush-ai-resume-analyzer`)
5. Click **"Deploy!"**
   - Streamlit Cloud automatically installs packages from `requirements.txt`.
   - The `@st.cache_resource` decorator ensures the transformer model is cached smoothly on the CPU without exceeding memory limits.

---

## 👨‍💻 Author

### **Dilkhush Raj**
*B.Tech in Electronics and Communication Engineering, National Institute of Technology, Manipur (NIT Manipur)*

- 💻 **GitHub:** [@Dilkhush144](https://github.com/Dilkhush144)
- 🔗 **LinkedIn:** [Dilkhush Raj](https://www.linkedin.com/in/dilkhush-raj-bb81182ba)
- 📧 **Email:** kdilkhush844@gmail.com / dilkhushraj@nitmanipur.ac.in

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Feel free to use and adapt this project for your own learning and portfolio.
