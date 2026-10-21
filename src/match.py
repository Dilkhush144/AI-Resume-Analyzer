"""
Semantic Matching and Keyword Gap Analysis Module
Author: Dilkhush Raj (https://github.com/Dilkhush144)
"""

import re
from typing import Dict, List, Set
import numpy as np

# Common industry skill terms for high-precision technical gap identification
KNOWN_TECH_SKILLS = {
    # Languages
    "python", "javascript", "typescript", "c++", "c", "java", "c#", "golang", "go",
    "rust", "ruby", "php", "swift", "kotlin", "sql", "html", "css", "bash", "shell",
    # Frontend / Backend Frameworks & Libraries
    "react", "react.js", "next.js", "vue", "vue.js", "angular", "node.js", "node", "express",
    "express.js", "django", "flask", "fastapi", "spring", "spring boot", "tailwind",
    # Cloud, DevOps & Tools
    "aws", "amazon web services", "azure", "gcp", "google cloud", "docker", "kubernetes",
    "k8s", "terraform", "ci/cd", "git", "github", "gitlab", "linux", "jenkins", "nginx",
    # Databases & Storage
    "postgresql", "postgres", "mysql", "mongodb", "redis", "sqlite", "dynamodb",
    "elasticsearch", "supabase", "firebase",
    # AI / ML / Data
    "machine learning", "deep learning", "nlp", "computer vision", "pytorch",
    "tensorflow", "scikit-learn", "sklearn", "pandas", "numpy", "opencv", "llm",
    # Core Engineering Concepts
    "rest", "restful", "rest api", "graphql", "microservices", "data structures",
    "algorithms", "dsa", "oop", "system design", "distributed systems", "agile", "scrum"
}

# General English stopwords that should never count as keyword gaps
STOP_WORDS = {
    "and", "the", "for", "with", "you", "are", "will", "our", "your", "from", "that", "have",
    "this", "into", "work", "team", "skills", "experience", "years", "per", "week", "job", "role",
    "requirements", "responsibilities", "preferred", "must", "about", "company", "ability",
    "strong", "excellent", "good", "including", "candidate", "looking", "apply", "working",
    "opportunity", "equal", "status", "plus", "understanding", "knowledge", "using", "across"
}


def similarity(resume_vec: np.ndarray, jd_vec: np.ndarray) -> float:
    """
    Calculates cosine similarity between resume and job description vectors, normalized to [0.0, 1.0].
    Uses pure numpy for high speed and zero extra dependency overhead.
    """
    a = np.asarray(resume_vec, dtype=np.float32).flatten()
    b = np.asarray(jd_vec, dtype=np.float32).flatten()

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    score = float(np.dot(a, b) / (norm_a * norm_b))
    # Bound between 0.0 and 1.0
    return max(0.0, min(1.0, score))


def tokenize_text(text: str) -> List[str]:
    """
    Tokenizes text while preserving terms with special characters like c++, node.js, c#.
    """
    text = text.lower()
    # Normalize punctuation while keeping symbols important in tech terms
    tokens = re.findall(r"\b[a-zA-Z0-9+#./-]+\b", text)
    return [t.strip(".-/") for t in tokens if len(t.strip(".-/")) > 1]


def extract_skills_from_text(text: str) -> Set[str]:
    """
    Extracts recognized technical skills from given text using exact phrase and token matching.
    """
    text_lower = f" {text.lower()} "
    found_skills = set()

    for skill in KNOWN_TECH_SKILLS:
        pattern = rf"(?:^|[\s,;./()\-])({re.escape(skill)})(?:$|[\s,;./()\-])"
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return found_skills


def keyword_gap(jd_text: str, resume_text: str, top_k: int = 20) -> Dict[str, List[str]]:
    """
    Performs comprehensive skill and keyword gap analysis:
    - matched_skills: Skills present in both JD and Resume.
    - missing_skills: Recognized technical skills required by JD but missing in Resume.
    - additional_keywords: High-frequency relevant tokens in JD not found in Resume.
    """
    jd_skills = extract_skills_from_text(jd_text)
    resume_skills = extract_skills_from_text(resume_text)

    matched_skills = sorted(list(jd_skills.intersection(resume_skills)))
    missing_skills = sorted(list(jd_skills.difference(resume_skills)))

    # General token-level gaps
    jd_tokens = set(tokenize_text(jd_text))
    rs_tokens = set(tokenize_text(resume_text))

    general_gaps = []
    for token in jd_tokens:
        if token not in rs_tokens and token not in STOP_WORDS and len(token) > 2:
            # Skip if already captured in missing skills
            if not any(token in s for s in missing_skills):
                general_gaps.append(token)

    # Sort general gaps by word length and alphabet
    general_gaps.sort(key=lambda w: (-len(w), w))

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "general_gaps": general_gaps[:top_k]
    }
