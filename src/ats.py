"""
ATS (Applicant Tracking System) Hygiene and Best-Practice Audit Module
Author: Dilkhush Raj (https://github.com/Dilkhush144)
"""

import re
from typing import List, Dict, Any


def basic_ats_checks(resume_text: str, filename: str = "Dilkhush_Raj_Resume.pdf") -> List[Dict[str, Any]]:
    """
    Performs comprehensive ATS checks and formatting hygiene heuristics on extracted resume text.
    Returns a list of structured check results with category, status, and actionable recommendations.
    """
    checks = []

    # 1. Filename Hygiene
    clean_filename = filename.strip()
    if re.search(r"\s", clean_filename):
        checks.append({
            "category": "Filename",
            "status": "warning",
            "title": "Filename Formatting",
            "message": "Filename contains spaces. Use underscores or hyphens (e.g., 'Dilkhush_Raj_Resume.pdf') so ATS parsers don't truncate the file path."
        })
    else:
        checks.append({
            "category": "Filename",
            "status": "pass",
            "title": "Filename Formatting",
            "message": "Filename has standard formatting without risky whitespace characters."
        })

    # 2. Contact Information: Email
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if re.search(email_pattern, resume_text):
        checks.append({
            "category": "Contact Info",
            "status": "pass",
            "title": "Professional Email",
            "message": "Valid email address detected in resume header."
        })
    else:
        checks.append({
            "category": "Contact Info",
            "status": "fail",
            "title": "Professional Email",
            "message": "No clearly identifiable email address found. Ensure your email is in plain text (not embedded in an image/table header)."
        })

    # 3. Contact Information: Phone Number
    phone_pattern = r"(?:(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b)"
    if re.search(phone_pattern, resume_text):
        checks.append({
            "category": "Contact Info",
            "status": "pass",
            "title": "Phone Number",
            "message": "Contact phone number detected."
        })
    else:
        checks.append({
            "category": "Contact Info",
            "status": "warning",
            "title": "Phone Number",
            "message": "Could not identify a standard phone number. Recruiters need a direct telephone contact."
        })

    # 4. Online Presence: LinkedIn
    if re.search(r"linkedin\.com/in/[\w-]+", resume_text, re.IGNORECASE):
        checks.append({
            "category": "Profiles",
            "status": "pass",
            "title": "LinkedIn Profile",
            "message": "LinkedIn profile link found."
        })
    else:
        checks.append({
            "category": "Profiles",
            "status": "warning",
            "title": "LinkedIn Profile",
            "message": "Add your customized LinkedIn URL (e.g., linkedin.com/in/yourname) in the header section."
        })

    # 5. Online Presence: GitHub / Portfolio
    if re.search(r"github\.com/[\w-]+", resume_text, re.IGNORECASE) or re.search(r"\b(?:portfolio|github)\b", resume_text, re.IGNORECASE):
        checks.append({
            "category": "Profiles",
            "status": "pass",
            "title": "GitHub / Portfolio",
            "message": "GitHub profile or technical portfolio detected."
        })
    else:
        checks.append({
            "category": "Profiles",
            "status": "tip",
            "title": "GitHub / Portfolio",
            "message": "Include your GitHub profile or technical portfolio to showcase real projects and code repositories."
        })

    # 6. Resume Length & Word Density
    words = len(resume_text.split())
    if words < 180:
        checks.append({
            "category": "Length",
            "status": "fail",
            "title": "Resume Length",
            "message": f"Resume is very short ({words} words). ATS scanners and hiring managers expect detailed project bullets and skills."
        })
    elif words > 950:
        checks.append({
            "category": "Length",
            "status": "warning",
            "title": "Resume Length",
            "message": f"Resume is lengthy ({words} words). For early career and engineering roles, a concise 1-page resume (~400-800 words) is optimal."
        })
    else:
        checks.append({
            "category": "Length",
            "status": "pass",
            "title": "Resume Length",
            "message": f"Optimal word count ({words} words) for an effective, single-page ATS-friendly resume."
        })

    # 7. Standard Section Headings
    must_sections = [
        ("Education", [r"\beducation\b", r"\bacademics\b"]),
        ("Skills", [r"\bskills\b", r"\btechnical skills\b", r"\btechnologies\b"]),
        ("Projects", [r"\bprojects\b", r"\btechnical projects\b", r"\bacademic projects\b"]),
        ("Experience", [r"\bexperience\b", r"\bwork experience\b", r"\binternships?\b", r"\bemployment\b"])
    ]

    for section_name, patterns in must_sections:
        found = any(re.search(pat, resume_text, re.IGNORECASE) for pat in patterns)
        if found:
            checks.append({
                "category": "Sections",
                "status": "pass",
                "title": f"'{section_name}' Section",
                "message": f"Recognized standard '{section_name}' heading."
            })
        else:
            checks.append({
                "category": "Sections",
                "status": "warning",
                "title": f"'{section_name}' Section",
                "message": f"Missing clear '{section_name}' heading. ATS parsers rely on standard section headings to index candidates."
            })

    # 8. Measurable Impact / Metrics (Numbers & Percentages)
    metric_matches = re.findall(r"\b(?:\d+%(?:\.\d+)?|\d+x|\$\d+|\d+\+?\s*(?:users|clients|stars|requests|ms|seconds|minutes|hours|days|weeks|months|years))\b", resume_text, re.IGNORECASE)
    if len(metric_matches) >= 3:
        checks.append({
            "category": "Impact",
            "status": "pass",
            "title": "Quantified Results",
            "message": f"Good use of quantifiable metrics ({len(metric_matches)} metric markers found). Numbers validate engineering impact."
        })
    else:
        checks.append({
            "category": "Impact",
            "status": "warning",
            "title": "Quantified Results",
            "message": "Few or no quantifiable metrics detected. Use numbers, percentages, or performance gains (e.g., 'reduced latency by 35%', 'handled 5k+ queries')."
        })

    # 9. Strong Action Verbs
    strong_verbs = [
        "built", "developed", "engineered", "designed", "implemented",
        "optimized", "deployed", "automated", "created", "architected",
        "reduced", "increased", "integrated", "spearheaded", "accelerated"
    ]
    resume_lower = resume_text.lower()
    matched_verbs = [v for v in strong_verbs if re.search(rf"\b{v}\b", resume_lower)]
    if len(matched_verbs) >= 4:
        checks.append({
            "category": "Language",
            "status": "pass",
            "title": "Strong Action Verbs",
            "message": f"Strong active verbs found ({', '.join(matched_verbs[:5])})."
        })
    else:
        checks.append({
            "category": "Language",
            "status": "tip",
            "title": "Strong Action Verbs",
            "message": "Begin bullet points with strong action verbs (e.g., Built, Developed, Optimized, Deployed) instead of passive phrasing."
        })

    return checks
