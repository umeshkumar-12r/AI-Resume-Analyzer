# 🔥 Load environment FIRST
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS

from utils import (
    extract_text_from_pdf,
    load_skills,
    extract_skills,
    calculate_keyword_score,
    semantic_skill_match,
    semantic_score,
    calculate_final_score,
    generate_ai_feedback,
    prioritize_missing_skills
)

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "Resume Analyzer Running 🚀"


# 🚀 MAIN ANALYSIS ROUTE
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400

    file = request.files['resume']
    jd_text = request.form.get('jd', "")

    if not jd_text.strip():
        return jsonify({"error": "Job description is empty"}), 400

    # 📄 Extract text
    resume_text = extract_text_from_pdf(file)

    # 📚 Load skills
    skills_list, aliases = load_skills()

    # 🧠 Extract skills
    resume_skills = extract_skills(resume_text, skills_list, aliases)
    jd_skills = extract_skills(jd_text, skills_list, aliases)

    # 🎯 Keyword score
    keyword_score, matched_keywords = calculate_keyword_score(resume_skills, jd_skills)

    # 🤖 Semantic matching
    semantic_matched = semantic_skill_match(resume_text, jd_skills)
    semantic = semantic_score(resume_text, jd_text)

    # 🔥 Combine matches
    final_matched = list(set(matched_keywords + semantic_matched))

    # ❌ Missing skills
    missing_skills = list(set(jd_skills) - set(final_matched))
    priority_skills = prioritize_missing_skills(missing_skills)

    # 📊 FINAL SCORE (NEW LOGIC)
    final_score = calculate_final_score(
        keyword_score,
        semantic,
        len(missing_skills)
    )

    return jsonify({
        "final_score": final_score,
        "keyword_score": keyword_score,
        "semantic_score": round(semantic, 2),
        "matched_skills": final_matched,
        "missing_skills": missing_skills,
        "priority_skills": priority_skills
    })


# 🤖 AI SUGGESTION ROUTE
@app.route('/ai-suggest', methods=['POST'])
def ai_suggest():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400

    file = request.files['resume']
    jd_text = request.form.get('jd', "")

    if not jd_text.strip():
        return jsonify({"error": "Job description is empty"}), 400

    resume_text = extract_text_from_pdf(file)

    # 🧠 Load skills for better AI context
    skills_list, aliases = load_skills()
    resume_skills = extract_skills(resume_text, skills_list, aliases)
    jd_skills = extract_skills(jd_text, skills_list, aliases)

    missing_skills = list(set(jd_skills) - set(resume_skills))
    priority_skills = prioritize_missing_skills(missing_skills)

    # 🤖 Better AI input
    ai_feedback = generate_ai_feedback(
        resume_text,
        jd_text,
        missing_skills
    )

    return jsonify({
        "ai_feedback": ai_feedback
    })


if __name__ == '__main__':
    app.run(debug=True)