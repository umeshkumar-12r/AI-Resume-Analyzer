import fitz  # PyMuPDF
import json
import os
from sentence_transformers import SentenceTransformer, util
from google import genai
# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load Gemini client (only if API key exists)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


# 🔹 Extract text from PDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.lower()


# 🔹 Load skills + aliases
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


# 🔹 Extract skills (with alias support)
def extract_skills(text, skills_list, aliases):
    text = text.lower()

    # 🔥 Normalize text (important)
    text = text.replace("-", " ").replace(".", " ").replace(",", " ")

    found = set()

    # Direct match
    for skill in skills_list:
        if skill.lower() in text:
            found.add(skill)

    # Alias match
    for main_skill, alias_list in aliases.items():
        for alias in alias_list:
            if alias.lower() in text:
                found.add(main_skill)

    return list(found)


# 🔹 Skill-based score
def calculate_score(resume_skills, jd_skills):
    matched = set(resume_skills) & set(jd_skills)

    if len(jd_skills) == 0:
        return 0, []

    score = (len(matched) / len(jd_skills)) * 100
    return round(score, 2), list(matched)


# 🔹 Semantic AI score
def semantic_skill_match(resume_text, jd_skills):
    matched = []

    resume_emb = model.encode(resume_text, convert_to_tensor=True)

    for skill in jd_skills:
        skill_emb = model.encode(skill, convert_to_tensor=True)
        sim = util.cos_sim(resume_emb, skill_emb)

        if float(sim) > 0.4:  # threshold
            matched.append(skill)

    return matched