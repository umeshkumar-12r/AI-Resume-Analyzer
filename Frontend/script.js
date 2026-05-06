// ===============================
// 📁 FILE UPLOAD (DRAG + CLICK)
// ===============================

const dropzone = document.getElementById('upload-dropzone');
const fileInput = document.getElementById('resume');
const fileNameDisplay = document.getElementById('file-name-display');
const fileNameText = document.getElementById('file-name-text');
const removeFileBtn = document.getElementById('remove-file');
let selectedFile = null;


// Prevent default drag behavior
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Highlight dropzone
['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, () => dropzone.classList.add('dragover'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, () => dropzone.classList.remove('dragover'), false);
});

// Handle dropped file
dropzone.addEventListener('drop', (e) => {
    let files = e.dataTransfer.files;


    if (files.length > 0) {
        handleFile(files[0]);
    }


}, false);

// Handle file selection (CLICK)
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

// 🔥 Central handler
function handleFile(file) {

    selectedFile = file; // 🔥 store file globally

    fileNameText.textContent = file.name;
    dropzone.style.display = 'none';
    fileNameDisplay.classList.remove('hidden');
}

// Remove file
removeFileBtn.addEventListener('click', () => {

    selectedFile = null;

    fileInput.value = '';
    dropzone.style.display = 'flex';
    fileNameDisplay.classList.add('hidden');
});

// ===============================
// 🚀 ANALYZE FUNCTION
// ===============================

async function analyze() {
    const file = selectedFile;
    const jd = document.getElementById("jd").value;
    const btn = document.getElementById("analyze-btn");
    const loadingState = document.getElementById("loading-state");
    const resultContainer = document.getElementById("result");


    if (!file) {
        alert("Please upload a resume file.");
        return;
    }

    if (!jd.trim()) {
        alert("Please paste a job description.");
        return;
    }

    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i><span>Analyzing...</span>`;

    resultContainer.classList.add('hidden');
    loadingState.classList.remove('hidden');

    let formData = new FormData();
    formData.append("resume", file);
    formData.append("jd", jd);

    try {
        let res = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            body: formData
        });

        if (!res.ok) throw new Error(`Server error: ${res.status}`);

        let data = await res.json();

        loadingState.classList.add('hidden');
        resultContainer.classList.remove('hidden');

        displayResults(data);

    } catch (error) {
        console.error("Analysis failed:", error);
        alert("Error during analysis. Check backend.");
        loadingState.classList.add('hidden');
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i><span>Analyze Resume</span>`;
    }


}

// ===============================
// 📊 DISPLAY RESULTS
// ===============================

function displayResults(data) {
    const resultContainer = document.getElementById("result");


    const finalScore = Math.round(data.final_score);

    let scoreClass = "score-low";
    let barClass = "low";
    let scoreMessage = "Low match ❌";

    if (finalScore >= 75) {
        scoreClass = "score-high";
        barClass = "high";
        scoreMessage = "Strong match 🚀";
    } else if (finalScore >= 40) {
        scoreClass = "score-medium";
        barClass = "medium";
        scoreMessage = "Moderate match ⚠️";
    }

    let matchedTags = data.matched_skills.length
        ? data.matched_skills.map(skill =>
            `<span class="skill-tag matched">${skill}</span>`).join('')
        : `<p class="empty-state">No matching skills found.</p>`;

    let missingTags = data.missing_skills.length
        ? data.missing_skills.map(skill =>
            `<span class="skill-tag missing">${skill}</span>`).join('')
        : `<p class="empty-state">Perfect match 🎉</p>`;

    resultContainer.innerHTML = `
    <div class="score-section">
        <div class="score-title">Final Match Score</div>
        <div class="score-value ${scoreClass}">${finalScore}%</div>
        <div class="score-message">${scoreMessage}</div>

        <div class="progress-container">
            <div class="progress-bar ${barClass}" id="progress-bar" style="width:0%"></div>
        </div>

        <div class="semantic-score">
            🎯 Keyword Match: ${Math.round(data.keyword_score)}% <br>
            🤖 Semantic Match: ${Math.round(data.semantic_score)}%
        </div>
    </div>

    <div class="skills-grid">
        <div class="skills-card matched">
            <h3><i class="fa-solid fa-circle-check"></i> Matched Skills</h3>
            <div class="tags-container">${matchedTags}</div>
        </div>

        <div class="skills-card missing">
            <h3><i class="fa-solid fa-circle-xmark"></i> Missing Skills</h3>
            <div class="tags-container">${missingTags}</div>
        </div>
    </div>
`;

    setTimeout(() => {
        document.getElementById('progress-bar').style.width = `${finalScore}%`;
    }, 100);

}

// ===============================
// 🤖 AI SUGGESTIONS
// ===============================

async function getAISuggestion() {

    const file = selectedFile;
    const jd = document.getElementById("jd").value;

    const aiContainer = document.getElementById("ai-result");

    if (!file) {
        alert("Upload resume first");
        return;
    }

    if (!jd.trim()) {
        alert("Enter job description");
        return;
    }

    let formData = new FormData();
    formData.append("resume", file);
    formData.append("jd", jd);

    // Show loading state
    aiContainer.classList.remove("hidden");

    aiContainer.innerHTML = `
        <div class="ai-box">
            <h3>🤖 AI Suggestions</h3>
            <p>Generating AI suggestions...</p>
        </div>
    `;

    try {

        let res = await fetch("http://127.0.0.1:5000/ai-suggest", {
            method: "POST",
            body: formData
        });

        let data = await res.json();

        aiContainer.innerHTML = `
            <div class="ai-box">
                <h3>🤖 AI Suggestions</h3>
                <pre>${data.ai_feedback}</pre>
            </div>
        `;

    } catch (err) {

        aiContainer.innerHTML = `
            <div class="ai-box">
                <h3>⚠️ Error</h3>
                <p>AI request failed.</p>
            </div>
        `;

        console.error(err);
    }
}