import fitz
import json
import os
import re
import time
from sentence_transformers import SentenceTransformer, util
from google import genai

# 🔥 Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# 🔐 Load API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


# ---------------------------
# 📄 TEXT EXTRACTION + CLEANING
# ---------------------------
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    return clean_text(text)


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return re.sub(r'\s+', ' ', text)


# ---------------------------
# 📚 LOAD SKILLS
# ---------------------------
def load_skills():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "data", "skills.json")

    with open(file_path, "r") as f:
        data = json.load(f)

    skills = []
    aliases = {}

    for key, values in data.items():
        if key == "aliases":
            aliases = values
        else:
            skills.extend(values)

    return list(set(skills)), aliases


# ---------------------------
# 🧠 SKILL EXTRACTION
# ---------------------------
def extract_skills(text, skills_list, aliases):
    text = clean_text(text)
    found = set()

    for skill in skills_list:
        if skill.lower() in text:
            found.add(skill)

    for main_skill, alias_list in aliases.items():
        for alias in alias_list:
            if alias.lower() in text:
                found.add(main_skill)

    return list(found)


# ---------------------------
# 🎯 KEYWORD SCORE
# ---------------------------
def calculate_keyword_score(resume_skills, jd_skills):
    matched = set(resume_skills) & set(jd_skills)

    if not jd_skills:
        return 0, []

    score = (len(matched) / len(jd_skills)) * 100
    return round(score, 2), list(matched)


# ---------------------------
# 🤖 SEMANTIC MATCH (OPTIMIZED)
# ---------------------------
def semantic_skill_match(resume_text, jd_skills):
    if not jd_skills:
        return []

    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    jd_embs = model.encode(jd_skills, convert_to_tensor=True)

    similarities = util.cos_sim(resume_emb, jd_embs)[0]

    matched = []
    for idx, score in enumerate(similarities):
        if float(score) > 0.4:
            matched.append(jd_skills[idx])

    return matched


def semantic_score(resume_text, jd_text):
    emb1 = model.encode(resume_text, convert_to_tensor=True)
    emb2 = model.encode(jd_text, convert_to_tensor=True)

    return float(util.cos_sim(emb1, emb2)) * 100


# ---------------------------
# 🧮 FINAL ATS SCORE
# ---------------------------
def calculate_final_score(keyword_score, semantic_score, missing_skills_count):
    skill_penalty = min(missing_skills_count * 5, 30)

    final = (
        0.4 * keyword_score +
        0.4 * semantic_score +
        0.2 * (100 - skill_penalty)
    )

    return round(final, 2)


# ---------------------------
# 🤖 AI FEEDBACK (STABLE)
# ---------------------------
import time

def generate_ai_feedback(resume_text, jd_text, missing_skills):
    if not client:
        return "AI feedback unavailable. Check API key."

    prompt = f"""
    You are a professional ATS (Applicant Tracking System) Resume Analyzer and Career Coach.

    Analyze the resume against the job description carefully and provide a detailed structured response.

    Your response MUST contain these sections:

    ATS MATCH SCORE (0-100)
    Give an estimated ATS compatibility score.
    Briefly explain why.
    STRONG MATCHING SKILLS
    List important skills and technologies present in both resume and job description.
    MISSING OR WEAK SKILLS
    Mention important missing skills, frameworks, tools, or technologies.
    EXPERIENCE ANALYSIS
    Analyze whether the candidate's projects and experience align with the role.
    RESUME IMPROVEMENT SUGGESTIONS
    Give specific improvements.
    Mention what should be added, rewritten, quantified, or improved.
    PROJECT SUGGESTIONS
    Suggest 2–3 projects the candidate can build to improve fit for this role.
    FINAL RECRUITER IMPRESSION
    Write a short realistic recruiter-style evaluation.

    IMPORTANT RULES:
    Be specific and practical.
    Avoid generic motivational lines.
    Keep formatting clean.
    Use bullet points where helpful.
    Focus on ATS optimization and recruiter expectations.

    ========================
    MISSING SKILLS:
    {missing_skills}

    ========================
    JOB DESCRIPTION:
    {jd_text}

    ========================
    RESUME:
    {resume_text}
    """

    models = ['gemini-2.5-flash', 'gemini-1.5-flash']

    for model_name in models:
        for attempt in range(2):
            try:
                print(f"Using model: {model_name}")

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config={"temperature": 0.4}
                )

                if response.candidates:
                    return response.candidates[0].content.parts[0].text

                return "No AI response generated."

            except Exception as e:
                print(f"Error with {model_name}: {e}")

                if "503" in str(e):
                    time.sleep(2)
                else:
                    break

    return "⚠️ AI service busy. Please try again later."
#---------------------------

#🧮 FINAL ATS SCORE

#---------------------------

def calculate_final_score(keyword_score, semantic_score, missing_skills_count):
    skill_penalty = min(missing_skills_count * 5, 30)

    final = (
        0.4 * keyword_score +
        0.4 * semantic_score +
        0.2 * (100 - skill_penalty)
        )

    return round(final, 2)


# ---------------------------

# 🔥 PRIORITIZE MISSING SKILLS

# ---------------------------

def prioritize_missing_skills(missing_skills):
    high_priority_keywords = [
        "aws", "docker", "kubernetes",
        "react", "node.js", "system design",
        "machine learning", "sql", "mongodb",
        "flask", "django", "api"
        ]

    medium_priority_keywords = [
    "git", "github", "testing",
    "ci/cd", "linux", "firebase"
    ]

    priority = {
        "high": [],
        "medium": [],
        "low": []
    }

    for skill in missing_skills:

        skill_lower = skill.lower()

        if skill_lower in high_priority_keywords:
            priority["high"].append(skill)

        elif skill_lower in medium_priority_keywords:
            priority["medium"].append(skill)

        else:
            priority["low"].append(skill)

    return priority
