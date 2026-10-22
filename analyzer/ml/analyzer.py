"""
Core ML/NLP engine for the Resume Analyzer.

Combines:
  - Rule-based skill extraction against a curated skills database
  - TF-IDF + cosine similarity for resume <-> job description matching (scikit-learn)
  - Heuristic structural/readability scoring for an overall ATS-style score
"""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .skills_data import ALL_SKILLS, SECTION_KEYWORDS

EMAIL_RE = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
PHONE_RE = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}')
ACTION_VERBS = {
    "achieved", "improved", "developed", "built", "designed", "led", "managed",
    "created", "implemented", "launched", "increased", "reduced", "optimized",
    "automated", "architected", "delivered", "spearheaded", "streamlined",
    "collaborated", "mentored", "analyzed", "engineered",
}


def _find_skills(text: str) -> dict:
    """Return {category: [skills found]} using whole-word, case-insensitive matching."""
    lower = text.lower()
    found = {}
    for skill, category in ALL_SKILLS.items():
        pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill) + r'(?![a-zA-Z0-9])'
        if re.search(pattern, lower):
            found.setdefault(category, []).append(skill)
    return found


def _detect_sections(text: str) -> dict:
    lower = text.lower()
    return {
        section: any(kw in lower for kw in kws)
        for section, kws in SECTION_KEYWORDS.items()
    }


def _keyword_match_score(resume_text: str, job_description: str) -> float:
    """Cosine similarity between resume and job description via TF-IDF (0-100)."""
    if not job_description or not job_description.strip():
        return 0.0
    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=2000)
        matrix = vectorizer.fit_transform([resume_text, job_description])
        score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return round(float(score) * 100, 1)
    except ValueError:
        return 0.0


def _readability_score(text: str) -> float:
    words = re.findall(r'\b\w+\b', text)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]
    word_count = len(words)

    if word_count < 150:
        length_score = max(0, (word_count / 150) * 100)
    elif word_count > 900:
        length_score = max(40, 100 - (word_count - 900) / 20)
    else:
        length_score = 100

    action_verb_hits = sum(1 for w in words if w.lower() in ACTION_VERBS)
    verb_score = min(100, (action_verb_hits / max(1, len(sentences))) * 200)

    return round((length_score * 0.6 + verb_score * 0.4), 1)


def analyze_resume(resume_text: str, job_description: str = "") -> dict:
    """
    Run the full analysis pipeline and return a structured result dict
    ready to be stored on the Resume model / rendered in the template.
    """
    found_skills_by_category = _find_skills(resume_text)
    resume_skill_set = {s for skills in found_skills_by_category.values() for s in skills}

    sections = _detect_sections(resume_text)
    section_score = round(sum(sections.values()) / len(sections) * 100, 1)

    has_email = bool(EMAIL_RE.search(resume_text))
    has_phone = bool(PHONE_RE.search(resume_text))
    contact_score = round(((has_email + has_phone) / 2) * 100, 1)

    readability = _readability_score(resume_text)

    job_skills_by_category = _find_skills(job_description) if job_description else {}
    job_skill_set = {s for skills in job_skills_by_category.values() for s in skills}

    matched_skills = sorted(resume_skill_set & job_skill_set) if job_skill_set else []
    missing_skills = sorted(job_skill_set - resume_skill_set) if job_skill_set else []

    keyword_score = _keyword_match_score(resume_text, job_description)

    if job_description.strip():
        overall_score = round(
            keyword_score * 0.40 +
            section_score * 0.20 +
            contact_score * 0.10 +
            readability * 0.15 +
            (len(matched_skills) / max(1, len(job_skill_set)) * 100 if job_skill_set else 0) * 0.15,
            1,
        )
    else:
        overall_score = round(
            section_score * 0.35 +
            contact_score * 0.15 +
            readability * 0.25 +
            min(100, len(resume_skill_set) * 5) * 0.25,
            1,
        )
    overall_score = max(0.0, min(100.0, overall_score))

    suggestions = []
    if not has_email:
        suggestions.append("Add a professional email address so recruiters can reach you.")
    if not has_phone:
        suggestions.append("Include a phone number in your contact details.")
    for section, present in sections.items():
        if not present:
            suggestions.append(f"Add a clear '{section}' section — it's missing right now.")
    if missing_skills:
        top_missing = ", ".join(missing_skills[:6])
        suggestions.append(f"Consider adding these job-relevant skills if you have them: {top_missing}.")
    if readability < 50:
        suggestions.append("Use more strong action verbs (e.g. 'led', 'built', 'improved') and keep bullet points concise.")
    if len(resume_skill_set) < 5:
        suggestions.append("List more of your technical and soft skills explicitly — a dedicated Skills section helps ATS parsing.")
    if not suggestions:
        suggestions.append("Great work — your resume covers the key sections and skills well!")

    return {
        "overall_score": overall_score,
        "keyword_score": keyword_score,
        "section_score": section_score,
        "contact_score": contact_score,
        "readability_score": readability,
        "sections": sections,
        "skills_by_category": found_skills_by_category,
        "all_skills_found": sorted(resume_skill_set),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "word_count": len(re.findall(r'\b\w+\b', resume_text)),
    }
