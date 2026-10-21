"""
Bullet Point Optimization & Action-Oriented Rewriting Module
Author: Dilkhush Raj (https://github.com/Dilkhush144)
"""

import os
from typing import List, Optional


def suggest_bullets(
    role_title: str,
    jd_text: str,
    missing_keywords: List[str],
    openai_api_key: Optional[str] = None
) -> List[str]:
    """
    Generates high-impact resume bullet point suggestions tailored to target skills and JD requirements.
    Uses OpenAI GPT if an API key is available; otherwise delivers structured STAR/XYZ formula templates.
    """
    # 1. Attempt dynamic LLM generation if API key is provided
    api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
    if api_key and api_key.startswith("sk-") and len(api_key) > 20:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            prompt = (
                f"You are an expert technical resume coach. Target role: '{role_title}'.\n"
                f"Top missing keywords/skills from the Job Description: {', '.join(missing_keywords[:6])}.\n\n"
                "Generate 4 strong, impactful technical resume bullet points applying the Google XYZ formula: "
                "'Accomplished [X] as measured by [Y], by doing [Z]'. Lead with action verbs and include realistic metrics. "
                "Output only the 4 bullet points, one per line starting with '-'."
            )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional technical resume optimization assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=250
            )
            content = response.choices[0].message.content.strip()
            lines = [line.lstrip("- ").strip() for line in content.split("\n") if line.strip()]
            if lines:
                return lines
        except Exception:
            # Fall back to structured offline templates on any API or connection issue
            pass

    # 2. High-impact offline templates based on missing skills and industry standards
    tips = []
    if missing_keywords:
        for kw in missing_keywords[:5]:
            kw_clean = kw.title()
            tips.append(
                f"Demonstrate '{kw_clean}': Built and deployed a [feature/service] using {kw_clean}, improving system efficiency by 25% and reducing response latency."
            )
    
    # Standard engineering excellence bullets
    tips.extend([
        "Quantify performance (Google XYZ): Engineered a scalable data pipeline, reducing processing turnaround from 45 mins to 12 mins (73% speedup).",
        "Lead with strong action verbs: Spearheaded RESTful API architecture and integrated automated CI/CD workflows, eliminating manual deployment errors.",
        "Demonstrate reliability: Architected unit and integration testing suite with 85%+ code coverage, boosting sprint release stability."
    ])

    return tips[:6]
