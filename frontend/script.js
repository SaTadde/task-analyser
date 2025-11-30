// ====== CONFIG ======
const API_BASE_URL = "http://127.0.0.1:8000/api/tasks";

// ====== STATE ======
let tasks = [];

// ====== DOM ELEMENTS ======
const taskForm = document.getElementById("taskForm");
const titleInput = document.getElementById("title");
const dueDateInput = document.getElementById("due_date");
const hoursInput = document.getElementById("estimated_hours");
const importanceInput = document.getElementById("importance");
const dependenciesInput = document.getElementById("dependencies");

const taskListEl = document.getElementById("taskList");
const taskCountEl = document.getElementById("taskCount");

const analyzeBtn = document.getElementById("analyzeBtn");
const suggestBtn = document.getElementById("suggestBtn");
const strategySelect = document.getElementById("strategySelect");

const resultsContainer = document.getElementById("resultsContainer");
const statusMessageEl = document.getElementById("statusMessage");
const loadingIndicatorEl = document.getElementById("loadingIndicator");

const clearTasksBtn = document.getElementById("clearTasksBtn");

// Toast
const toastEl = document.getElementById("toast");

// Modal
const jsonModal = document.getElementById("jsonModal");
const openJsonModalBtn = document.getElementById("openJsonModalBtn");
const closeJsonModalBtn = document.getElementById("closeJsonModalBtn");
const cancelJsonBtn = document.getElementById("cancelJsonBtn");
const applyJsonBtn = document.getElementById("applyJsonBtn");
const jsonInput = document.getElementById("jsonInput");

// ====== UTIL: Toast ======
let toastTimeoutId = null;

function showToast(message, type = "info") {
  if (!toastEl) return;
  toastEl.textContent = message;
  toastEl.classList.remove("hidden", "toast--error", "toast--success");
  if (type === "error") toastEl.classList.add("toast--error");
  if (type === "success") toastEl.classList.add("toast--success");
  toastEl.classList.add("toast--show");

  if (toastTimeoutId) clearTimeout(toastTimeoutId);
  toastTimeoutId = setTimeout(() => {
    toastEl.classList.remove("toast--show");
  }, 2600);
}

// ====== UTIL: Loading / status ======
function setLoading(isLoading, message = "") {
  if (isLoading) {
    loadingIndicatorEl.classList.remove("hidden");
    if (message) statusMessageEl.textContent = message;
  } else {
    loadingIndicatorEl.classList.add("hidden");
    if (message) statusMessageEl.textContent = message;
  }
}

// ====== TASK STATE RENDERING ======
function renderPendingTasks() {
  taskCountEl.textContent = tasks.length.toString();

  if (tasks.length === 0) {
    taskListEl.className = "task-list-empty";
    taskListEl.textContent =
      "No tasks added yet. Start by using the form above.";
    return;
  }

  taskListEl.className = "";
  taskListEl.innerHTML = "";

  tasks.forEach((task, index) => {
    const chip = document.createElement("div");
    chip.className = "pending-task-chip";
    chip.innerHTML = `
      <span class="title">${task.title}</span>
      <span class="meta">Due: ${task.due_date}</span>
      <span class="meta">Hrs: ${task.estimated_hours}</span>
      <span class="meta">Imp: ${task.importance}</span>
    `;
    taskListEl.appendChild(chip);
  });
}

// ====== VALIDATION ======
function validateSingleTaskInput() {
  const title = titleInput.value.trim();
  const dueDate = dueDateInput.value.trim();
  const hoursStr = hoursInput.value.trim();
  const importanceStr = importanceInput.value.trim();

  if (!title || !dueDate || !hoursStr || !importanceStr) {
    showToast("Please fill all required fields.", "error");
    return null;
  }

  const estimated_hours = Number(hoursStr);
  const importance = Number(importanceStr);

  if (Number.isNaN(estimated_hours) || estimated_hours < 0) {
    showToast("Estimated hours must be a non-negative number.", "error");
    return null;
  }

  if (
    Number.isNaN(importance) ||
    importance < 1 ||
    importance > 10
  ) {
    showToast("Importance must be between 1 and 10.", "error");
    return null;
  }

  let dependencies = [];
  const depStr = dependenciesInput.value.trim();
  if (depStr) {
    dependencies = depStr
      .split(",")
      .map((d) => d.trim())
      .filter((d) => d.length > 0);
  }

  return {
    title,
    due_date: dueDate,
    estimated_hours,
    importance,
    dependencies,
  };
}

// ====== FORM HANDLERS ======
taskForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const task = validateSingleTaskInput();
  if (!task) return;

  tasks.push(task);
  renderPendingTasks();

  // Clear inputs except strategy
  titleInput.value = "";
  dueDateInput.value = "";
  hoursInput.value = "";
  importanceInput.value = "";
  dependenciesInput.value = "";

  showToast("Task added.", "success");
  statusMessageEl.textContent = "Tasks added. Ready to analyze.";
  showAnalyzeHint();
});

clearTasksBtn.addEventListener("click", () => {
  tasks = [];
  renderPendingTasks();
  resultsContainer.innerHTML = `
    <div class="empty-card">
      <h3>No results yet</h3>
      <p>Add some tasks on the left and click <strong>Analyze Tasks</strong>.</p>
    </div>
  `;
  resultsContainer.classList.add("empty-state");
  setLoading(false, "Waiting for input…");
  showToast("All tasks cleared.");
});

// ====== MODAL HANDLERS ======
function openJsonModal() {
  jsonModal.classList.remove("hidden");
}

function closeJsonModal() {
  jsonModal.classList.add("hidden");
}

openJsonModalBtn.addEventListener("click", openJsonModal);
closeJsonModalBtn.addEventListener("click", closeJsonModal);
cancelJsonBtn.addEventListener("click", closeJsonModal);

applyJsonBtn.addEventListener("click", () => {
  const raw = jsonInput.value.trim();
  if (!raw) {
    showToast("Please paste a JSON array of tasks.", "error");
    return;
  }

  try {
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      showToast("JSON must be an array of task objects.", "error");
      return;
    }

    // Minimal validation: ensure required fields exist
    const cleaned = parsed.map((t, idx) => {
      if (
        !t.title ||
        !t.due_date ||
        t.estimated_hours === undefined ||
        t.importance === undefined
      ) {
        throw new Error(`Task at index ${idx} is missing required fields.`);
      }
      return {
        title: String(t.title),
        due_date: String(t.due_date),
        estimated_hours: Number(t.estimated_hours),
        importance: Number(t.importance),
        dependencies: Array.isArray(t.dependencies)
          ? t.dependencies
          : [],
      };
    });

    tasks = cleaned;
    renderPendingTasks();
    
    closeJsonModal();
    showToast("Tasks loaded from JSON.", "success");
    statusMessageEl.textContent = "Tasks loaded. Ready to analyze.";
    showAnalyzeHint();
  } catch (err) {
    console.error("JSON parse error:", err);
    showToast(err.message || "Invalid JSON input.", "error");
  }
});


// ====== RENDER RESULTS ======
function renderResultsFromArray(taskArray) {
  if (!Array.isArray(taskArray) || taskArray.length === 0) {
    resultsContainer.classList.add("empty-state");
    resultsContainer.innerHTML = `
      <div class="empty-card">
        <h3>No results</h3>
        <p>The API returned an empty list. Try adding more tasks.</p>
      </div>
    `;
    return;
  }

  resultsContainer.classList.remove("empty-state");
  resultsContainer.innerHTML = ""; // IMPORTANT: clear old results (fix duplicates)

  taskArray.forEach((task) => {
    const score = typeof task.score === "number" ? task.score : 0;
    const scoreRounded = Math.round(score * 100) / 100;

    let priorityClass = "priority-low";
    let priorityLabelClass = "priority-low-label";
    let scoreClass = "score-low";
    let labelText = "Low";

    if (score >= 7) {
      priorityClass = "priority-high";
      priorityLabelClass = "priority-high-label";
      scoreClass = "score-high";
      labelText = "High";
    } else if (score >= 4) {
      priorityClass = "priority-med";
      priorityLabelClass = "priority-med-label";
      scoreClass = "score-med";
      labelText = "Medium";
    }

    const card = document.createElement("article");
    card.className = `task-card ${priorityClass}`;
    // Highlight circular dependency tasks
    if (
        window.lastCycleNodes && 
        window.lastCycleNodes.includes(task.title)
    ) {
        card.classList.add("cycle-task");
    }

    card.innerHTML = `
      <div class="task-main">
        <div class="task-title-row">
          <div class="task-title">${task.title}</div>
          <span class="priority-chip ${priorityLabelClass}">
            ${labelText} priority
          </span>
        </div>
        <div class="task-meta-row">
          <span class="meta-pill">Due: ${task.due_date}</span>
          <span class="meta-pill">Effort: ${task.estimated_hours}h</span>
          <span class="meta-pill">Importance: ${task.importance}/10</span>
          ${
            task.dependencies && task.dependencies.length > 0
              ? `<span class="meta-pill">Deps: ${task.dependencies.join(", ")}</span>`
              : ""
          }
        </div>
        ${
          task.explanation
            ? `<div class="task-explanation">Reasoning: ${task.explanation}</div>`
            : ""
        }
      </div>
      <div class="task-score">
        <span class="score-label">Score</span>
        <span class="score-value ${scoreClass}">
          ${Number.isFinite(scoreRounded) ? scoreRounded : "-"}
        </span>
      </div>
    `;
    resultsContainer.appendChild(card);
  });
}
function renderEisenhowerMatrix(tasks) {
  const matrix = document.getElementById("eisenhowerMatrix");

  // Clear previous
  ["doNowList", "scheduleList", "delegateList", "eliminateList"]
    .forEach(id => document.getElementById(id).innerHTML = "");

  if (!tasks || tasks.length === 0) {
    matrix.classList.add("hidden");
    return;
  }

  matrix.classList.remove("hidden");

  tasks.forEach(task => {
    const today = new Date();
    const due = new Date(task.due_date);
    const daysLeft = Math.round((due - today) / (1000 * 60 * 60 * 24));

    const urgent = daysLeft <= 2;       // urgent = due soon
    const important = task.importance >= 6;

    const div = document.createElement("div");
    div.textContent = `${task.title} (${task.due_date})`;

    if (urgent && important) {
      document.getElementById("doNowList").appendChild(div);
    } else if (!urgent && important) {
      document.getElementById("scheduleList").appendChild(div);
    } else if (urgent && !important) {
      document.getElementById("delegateList").appendChild(div);
    } else {
      document.getElementById("eliminateList").appendChild(div);
    }
  });
}

// ====== API CALLS ======
async function analyzeTasks() {
  if (tasks.length === 0) {
    showToast("Add at least one task before analyzing.", "error");
    return;
  }

  const strategy = strategySelect.value || "smart";
  const url = `${API_BASE_URL}/analyze/?strategy=${encodeURIComponent(
    strategy
  )}`;

  try {
    setLoading(true, "Analyzing tasks...");
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(tasks),
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(
        `API error (${res.status}): ${text || res.statusText}`
      );
    }

    const data = await res.json();
    /* ===== CYCLE WARNING UI HERE ===== */
    const cycleWarning = document.getElementById("cycleWarning");
    if (data.has_cycle) {
        cycleWarning.classList.remove("hidden");
        cycleWarning.innerHTML =
            "⚠️ Circular dependency detected:<br><strong>" +
            data.cycle_nodes.join(", ") +
            "</strong>";
    } else {
    cycleWarning.classList.add("hidden");
    }
    window.lastCycleNodes = data.cycle_nodes || [];

 /* ================================= */
    renderResultsFromArray(data.tasks);
    renderEisenhowerMatrix(data.tasks);
    setLoading(false, "Analysis complete.");
    showToast("Tasks analyzed successfully!", "success");
  } catch (err) {
    console.error("Analyze error:", err);
    setLoading(false, "Error while analyzing.");
    showToast(err.message || "Failed to analyze tasks.", "error");
  }
}

async function suggestTasks() {
  if (tasks.length === 0) {
    showToast("Add at least one task before getting suggestions.", "error");
    return;
  }

  const url = `${API_BASE_URL}/suggest/`;

  try {
    setLoading(true, "Fetching suggestions...");
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(tasks),
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(
        `API error (${res.status}): ${text || res.statusText}`
      );
    }

    const data = await res.json();
    if (!data || !Array.isArray(data.suggested_tasks)) {
      throw new Error("Unexpected response format from suggest API.");
    }

    renderResultsFromArray(data.suggested_tasks);
    renderEisenhowerMatrix(data.suggested_tasks);
    setLoading(false, "Top 3 suggestions loaded.");
    showToast("Loaded today’s top 3 tasks.", "success");
  } catch (err) {
    console.error("Suggest error:", err);
    setLoading(false, "Error while fetching suggestions.");
    showToast(err.message || "Failed to fetch suggestions.", "error");
  }
}

function showAnalyzeHint() {
  const bubble = document.getElementById("helperBubble");
  if (!bubble) return;

  bubble.classList.add("show");

  setTimeout(() => {
    bubble.classList.remove("show");
  }, 5000);
}



// ====== BUTTON HANDLERS ======
analyzeBtn.addEventListener("click", analyzeTasks);
suggestBtn.addEventListener("click", suggestTasks);



// Initial render
renderPendingTasks();
setLoading(false, "Waiting for input…");
