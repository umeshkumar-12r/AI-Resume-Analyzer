// File Drag and Drop functionality
const dropzone = document.getElementById('upload-dropzone');
const fileInput = document.getElementById('resume');
const fileNameDisplay = document.getElementById('file-name-display');
const fileNameText = document.getElementById('file-name-text');
const removeFileBtn = document.getElementById('remove-file');

// Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Highlight dropzone when item is dragged over it
['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropzone.classList.add('dragover');
}

function unhighlight(e) {
    dropzone.classList.remove('dragover');
}

// Handle dropped files
dropzone.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;
    fileInput.files = files;
    updateFileDisplay();
}

// Handle click to open file dialog
dropzone.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', updateFileDisplay);

function updateFileDisplay() {
    if (fileInput.files.length > 0) {
        fileNameText.textContent = fileInput.files[0].name;
        dropzone.style.display = 'none';
        fileNameDisplay.classList.remove('hidden');
    }
}

removeFileBtn.addEventListener('click', () => {
    fileInput.value = '';
    dropzone.style.display = 'flex';
    fileNameDisplay.classList.add('hidden');
});

// Analyze Function
async function analyze() {
    const file = fileInput.files[0];
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

    // Show loading, hide previous results
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

        if (!res.ok) {
            throw new Error(`Server error: ${res.status}`);
        }

        let data = await res.json();

        // Hide loading, show results
        loadingState.classList.add('hidden');
        resultContainer.classList.remove('hidden');

        displayResults(data);

    } catch (error) {
        console.error("Analysis failed:", error);
        alert("An error occurred during analysis. Make sure the backend server is running.");
        loadingState.classList.add('hidden');
    } finally {
        // Reset button
        btn.disabled = false;
        btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i><span>Analyze Resume</span>`;
    }
}

function displayResults(data) {
    const resultContainer = document.getElementById("result");

    const finalScore = Math.round(data.final_score);

    // 🎯 Score color logic
    let scoreClass = "score-low";
    let barClass = "low";

    if (finalScore >= 75) {
        scoreClass = "score-high";
        barClass = "high";
    } else if (finalScore >= 40) {
        scoreClass = "score-medium";
        barClass = "medium";
    }

    // ✅ Matched skills
    let matchedTags = data.matched_skills.length
        ? data.matched_skills.map(skill =>
            `<span class="skill-tag matched">${skill}</span>`).join('')
        : `<p class="empty-state">No matching skills found.</p>`;

    // ❌ Missing skills
    let missingTags = data.missing_skills.length
        ? data.missing_skills.map(skill =>
            `<span class="skill-tag missing">${skill}</span>`).join('')
        : `<p class="empty-state">Perfect match 🎉</p>`;

    resultContainer.innerHTML = `
        <div class="score-section">
            <div class="score-title">Final Match Score</div>
            <div class="score-value ${scoreClass}">${finalScore}%</div>

            <div class="progress-container">
                <div class="progress-bar ${barClass}" id="progress-bar" style="width:0%"></div>
            </div>

            <div class="semantic-score">
                🧠 Skill Match: ${Math.round(data.skill_score)}% <br>
                🤖 AI Semantic Match: ${Math.round(data.semantic_score)}%
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

    // 🎬 Progress bar animation
    setTimeout(() => {
        document.getElementById('progress-bar').style.width = `${finalScore}%`;
    }, 100);
}
// AI Suggestions Function 
async function getAISuggestion() {
    const file = document.getElementById("resume").files[0];
    const jd = document.getElementById("jd").value;

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

    const resultContainer = document.getElementById("result");

    resultContainer.innerHTML = "🤖 Generating AI suggestions...";

    try {
        let res = await fetch("http://127.0.0.1:5000/ai-suggest", {
            method: "POST",
            body: formData
        });

        let data = await res.json();

        resultContainer.innerHTML += `
            <div class="ai-box">
                <h3>🤖 AI Suggestions</h3>
                <p>${data.ai_feedback}</p>
            </div>
        `;
    } catch (err) {
        alert("AI request failed");
        console.error(err);
    }
}