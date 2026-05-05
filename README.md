# 📝 ATS Resume Checker (AI-Powered)

An intelligent **ATS (Applicant Tracking System) Resume Analyzer** built using **Streamlit + Flask + Google Gemini AI**.
This tool evaluates resumes against job descriptions and provides actionable insights to improve alignment.

---

## 🚀 Features

* 📄 Upload Resume (PDF / TXT)
* 🧠 AI-based Resume Analysis using Gemini
* 📊 Match Score (0–100)
* 🔍 Missing Keywords & Skills Detection
* 🎯 Role Alignment Evaluation
* 💡 Actionable Improvement Suggestions
* ⚡ Clean and interactive UI with Streamlit

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Flask
* **AI Model:** Google Gemini AI
* **Language:** Python
* **Libraries:**

  * PyPDF2
  * python-dotenv
  * streamlit
  * flask
  * google-generativeai

---

## 📂 Project Structure

```
ATS-Resume-Checker/
│
├── frontend/
│   └── app.py              # Streamlit UI
│
├── backend/
│   └── app.py              # Flask API
│
├── .env                    # API Keys (not pushed)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/ATS-Resume-Checker.git
cd ATS-Resume-Checker
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create a `.env` file in root:

```
GEMINI_API_KEY=your_api_key_here
```

---

### 5️⃣ Run Backend (Flask)

```
cd backend
python app.py
```

Runs on:

```
http://127.0.0.1:5000
```

---

### 6️⃣ Run Frontend (Streamlit)

Open new terminal:

```
cd frontend
streamlit run app.py
```

Runs on:

```
http://localhost:8501
```

---

## 🔄 Workflow

1. User uploads resume & job description
2. Frontend sends request to Flask backend
3. Backend processes text and calls Gemini API
4. AI analyzes and returns structured feedback
5. Results displayed on UI

---

## 📊 Example Output

* **Match Score:** 78/100
* **Missing Skills:** Docker, Kubernetes, CI/CD
* **Role Alignment:** Moderate
* **Suggestions:**

  * Add quantifiable achievements
  * Include relevant frameworks
  * Highlight project impact

---

## ⚠️ Known Issues

* Large PDFs may cause slower response
* AI response may vary slightly
* Requires active internet connection

---

## 🔮 Future Improvements

* ✅ JSON structured output parsing
* 📈 Resume score visualization (charts)
* 🧾 Downloadable report (PDF)
* 🔍 Keyword highlighting in resume
* 🌐 Deployment (Streamlit Cloud / AWS)

---