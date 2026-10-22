"""
Curated skill keyword database used for rule-based skill extraction.
Organized by category so results can be grouped nicely in the UI.
"""

SKILLS_DB = {
    "Programming Languages": [
        "python", "java", "c++", "c#", "javascript", "typescript", "go", "golang",
        "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "perl", "c",
    ],
    "Web Development": [
        "html", "css", "react", "angular", "vue", "django", "flask", "fastapi",
        "node.js", "nodejs", "express", "next.js", "redux", "bootstrap", "tailwind",
        "jquery", "rest api", "graphql", "webpack", "sass",
    ],
    "Data & Machine Learning": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "scikit-learn", "sklearn", "tensorflow", "pytorch", "keras",
        "pandas", "numpy", "data analysis", "data science", "data visualization",
        "matplotlib", "seaborn", "power bi", "tableau", "statistics", "regression",
        "classification", "clustering", "neural network", "opencv", "xgboost",
    ],
    "Databases": [
        "sql", "mysql", "postgresql", "postgres", "mongodb", "sqlite", "redis",
        "oracle", "cassandra", "elasticsearch", "dynamodb", "firebase",
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "jenkins",
        "ci/cd", "terraform", "ansible", "linux", "git", "github", "gitlab",
        "microservices", "devops", "nginx", "cloud computing",
    ],
    "Tools & Methodologies": [
        "jira", "agile", "scrum", "kanban", "figma", "postman", "unit testing",
        "test driven development", "tdd", "object oriented programming", "oop",
        "design patterns", "api development", "version control",
    ],
    "Soft Skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "critical thinking", "time management", "adaptability", "collaboration",
        "project management", "presentation", "mentoring", "analytical",
    ],
}

# Flat lookup: lowercase skill -> category
ALL_SKILLS = {
    skill: category
    for category, skills in SKILLS_DB.items()
    for skill in skills
}

SECTION_KEYWORDS = {
    "Contact Information": ["email", "phone", "linkedin", "@"],
    "Education": ["education", "university", "college", "bachelor", "master", "degree", "b.tech", "m.tech", "b.sc", "m.sc"],
    "Experience": ["experience", "employment", "work history", "internship", "professional experience"],
    "Skills": ["skills", "technical skills", "core competencies", "proficiencies"],
    "Projects": ["project", "projects", "portfolio"],
    "Certifications": ["certification", "certificate", "certified", "license"],
}
