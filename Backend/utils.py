import fitz
import json
import os
import time
from sentence_transformers import SentenceTransformer, util
from google import genai

# 🔥 Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# 🔐 Load API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("API KEY:", GEMINI_API_KEY)

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


# 📄 Extract text from PDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.lower()


# 📚 Load skills
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


# 🧠 Extract skills
def extract_skills(text, skills_list, aliases):
    text = text.lower()
    text = text.replace("-", " ").replace(".", " ").replace(",", " ")

    found = set()

    for skill in skills_list:
        if skill.lower() in text:
            found.add(skill)

    for main_skill, alias_list in aliases.items():
        for alias in alias_list:
            if alias.lower() in text:
                found.add(main_skill)

    return list(found)


# 🎯 Score
def calculate_score(resume_skills, jd_skills):
    matched = set(resume_skills) & set(jd_skills)

    if len(jd_skills) == 0:
        return 0, []

    score = (len(matched) / len(jd_skills)) * 100
    return round(score, 2), list(matched)


# 🤖 Semantic matching
def semantic_skill_match(resume_text, jd_skills):
    matched = []

    resume_emb = model.encode(resume_text, convert_to_tensor=True)

    for skill in jd_skills:
        skill_emb = model.encode(skill, convert_to_tensor=True)
        sim = util.cos_sim(resume_emb, skill_emb)

        if float(sim) > 0.4:
            matched.append(skill)

    return matched


# 🤖 AI feedback
import time

def generate_ai_feedback(resume_text, jd_text):
    if not client:
        return "AI feedback unavailable. Check API key."

    prompt = f"""
You are an expert ATS Resume Analyzer.

Give:
1. Missing skills
2. Strengths
3. Improvements

Job Description:
{jd_text}

Resume:
{resume_text}
"""

    models = ['gemini-2.5-flash', 'gemini-1.5-flash']

    for model_name in models:
        for attempt in range(2):  # retry each model 2 times
            try:
                print(f"Using model: {model_name} (attempt {attempt+1})")

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                return response.candidates[0].content.parts[0].text

            except Exception as e:
                if "503" in str(e):
                    print(f"⚠️ {model_name} busy, retrying...")
                    time.sleep(2)
                else:
                    print(f"❌ Error with {model_name}: {e}")
                    break  # move to next model

    return "⚠️ AI service is currently busy. Please try again later."