# 🔥 Load environment FIRST
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS

from utils import (
    extract_text_from_pdf,
    load_skills,
    extract_skills,
    calculate_score,
    semantic_skill_match,
    generate_ai_feedback
)

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "Resume Analyzer Running 🚀"


# 🚀 Main Analysis Route
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400

    file = request.files['resume']
    jd_text = request.form.get('jd', "")

    if not jd_text.strip():
        return jsonify({"error": "Job description is empty"}), 400

    # 📄 Extract resume text
    resume_text = extract_text_from_pdf(file)

    # 📚 Load skills
    skills_list, aliases = load_skills()

    # 🧠 Extract skills
    resume_skills = extract_skills(resume_text, skills_list, aliases)
    jd_skills = extract_skills(jd_text.lower(), skills_list, aliases)

    # 🎯 Keyword score
    skill_score, matched = calculate_score(resume_skills, jd_skills)

    # 🤖 Semantic matching
    semantic_matched = semantic_skill_match(resume_text, jd_skills)

    # 🔥 Merge matches
    final_matched = list(set(matched + semantic_matched))

    # 📊 Final score
    final_score = round(
        (len(final_matched) / len(jd_skills)) * 100, 2
    ) if jd_skills else 0

    return jsonify({
        "skill_score": skill_score,
        "semantic_score": round((len(semantic_matched) / len(jd_skills)) * 100, 2) if jd_skills else 0,
        "final_score": final_score,
        "matched_skills": final_matched,
        "missing_skills": list(set(jd_skills) - set(final_matched))
    })


# 🤖 AI Suggestion Route
@app.route('/ai-suggest', methods=['POST'])
def ai_suggest():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400

    file = request.files['resume']
    jd_text = request.form.get('jd', "")

    if not jd_text.strip():
        return jsonify({"error": "Job description is empty"}), 400

    resume_text = extract_text_from_pdf(file)

    ai_feedback = generate_ai_feedback(resume_text, jd_text)

    return jsonify({
        "ai_feedback": ai_feedback
    })


if __name__ == '__main__':
    app.run(debug=True)