let latestAnalysis = null;

let latestAlertId = null;

let latestPatientId = null;

/* =========================================
   NAVIGATION
========================================= */

function showSection(sectionId, button) {
  document.querySelectorAll(".dashboard-section").forEach((section) => {
    section.classList.remove("active-section");
  });

  const section = document.getElementById(sectionId);

  if (section) {
    section.classList.add("active-section");
  }

  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.remove("active");
  });

  if (button) {
    button.classList.add("active");
  }

  if (sectionId === "evaluation") {
    loadEvaluation();
  }
}

function showSectionById(sectionId) {
  const button = document.querySelector(`.nav-item[onclick*="'${sectionId}'"]`);

  showSection(sectionId, button);
}

/* =========================================
   PATIENT MANAGEMENT
========================================= */

async function loadPatients() {
  const select = document.getElementById("patient-select");

  if (!select) {
    return;
  }

  try {
    const response = await fetch("/api/patients");

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Unable to load patients.");
    }

    select.innerHTML = "";

    const defaultOption = document.createElement("option");

    defaultOption.value = "";

    defaultOption.textContent = "Select patient";

    select.appendChild(defaultOption);

    if (!data.patients || data.patients.length === 0) {
      const emptyOption = document.createElement("option");

      emptyOption.disabled = true;

      emptyOption.textContent = "No patients available — add a patient";

      select.appendChild(emptyOption);

      return;
    }

    data.patients.forEach((patient) => {
      const option = document.createElement("option");

      option.value = patient.id;

      let label = patient.name;

      if (patient.age !== null && patient.age !== undefined) {
        label += ` — Age ${patient.age}`;
      }

      option.textContent = label;

      select.appendChild(option);
    });
  } catch (error) {
    console.error("Patient loading error:", error);

    select.innerHTML = `<option value="">
                Unable to load patients
            </option>`;
  }
}

function openPatientForm() {
  const form = document.getElementById("patient-form");

  if (form) {
    form.classList.remove("hidden");
  }

  const nameInput = document.getElementById("new-patient-name");

  if (nameInput) {
    nameInput.focus();
  }
}

function closePatientForm() {
  const form = document.getElementById("patient-form");

  if (form) {
    form.classList.add("hidden");
  }

  const nameInput = document.getElementById("new-patient-name");

  const ageInput = document.getElementById("new-patient-age");

  if (nameInput) {
    nameInput.value = "";
  }

  if (ageInput) {
    ageInput.value = "";
  }
}

async function createPatient() {
  const nameInput = document.getElementById("new-patient-name");

  const ageInput = document.getElementById("new-patient-age");

  const name = nameInput.value.trim();

  const age = ageInput.value.trim();

  if (!name) {
    alert("Please enter a patient name.");

    return;
  }

  if (age && (Number(age) < 0 || Number(age) > 18)) {
    alert("Patient age must be between 0 and 18.");

    return;
  }

  try {
    const response = await fetch("/api/patients", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        name: name,

        age: age ? Number(age) : null,

        diagnosis: "Pediatric leukemia",
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Unable to create patient.");
    }

    await loadPatients();

    const select = document.getElementById("patient-select");

    if (data.patient && data.patient.id) {
      select.value = data.patient.id;

      latestPatientId = data.patient.id;
    }

    closePatientForm();

    updatePatientCount();
  } catch (error) {
    alert(error.message);
  }
}

function updatePatientCount() {
  const select = document.getElementById("patient-select");

  const countElement = document.getElementById("patients-count");

  if (!select || !countElement) {
    return;
  }

  const patientOptions = Array.from(select.options).filter(
    (option) => option.value !== ""
  );

  countElement.textContent = patientOptions.length;
}

/* =========================================
   DEMO EXAMPLES
========================================= */

function useExample(type) {
  const message = document.getElementById("caregiver-message");

  const examples = {
    "en-high":
      "The medication is unavailable and we could not reach the hospital for two weeks.",

    "ar-high": "الدواء غير متوفر ولم نستطع الوصول إلى المستشفى منذ أسبوعين.",

    "en-medium":
      "The appointment is not confirmed and the referral is still pending.",

    "en-low": "The child is doing well and the next visit is confirmed.",
  };

  message.value = examples[type] || "";
}

/* =========================================
   AI ANALYSIS
========================================= */

async function analyzeCase() {
  const messageElement = document.getElementById("caregiver-message");

  const patientElement = document.getElementById("patient-select");

  const text = messageElement.value.trim();

  const patientId = patientElement.value;

  if (!patientId) {
    alert("Please select a patient first.");

    patientElement.focus();

    return;
  }

  if (!text) {
    alert("Please enter a caregiver message.");

    messageElement.focus();

    return;
  }

  const button = document.getElementById("analyze-button");

  const originalText = button.textContent;

  button.disabled = true;

  button.textContent = "Analyzing...";

  try {
    const response = await fetch("/api/analyze-and-create-alert", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        text: text,

        patient_id: Number(patientId),
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Analysis failed.");
    }

    latestAnalysis = data.result;

    latestAlertId = data.alert_id;

    latestPatientId = data.patient.id;

    renderAnalysis(data);

    renderWorkerCase(data);

    updateDashboardStats();

    showSectionById("analysis");
  } catch (error) {
    alert(error.message);
  } finally {
    button.disabled = false;

    button.textContent = originalText;
  }
}

/* =========================================
   ANALYSIS RENDERING
========================================= */

function renderAnalysis(data) {
  const result = data.result;

  document.getElementById("analysis-empty").classList.add("hidden");

  document.getElementById("analysis-result").classList.remove("hidden");

  document.getElementById("result-priority").textContent = formatPriority(
    result.priority
  );

  document.getElementById("result-score").textContent = result.score;

  const reasonsContainer = document.getElementById("result-reasons");

  reasonsContainer.innerHTML = "";

  if (!result.reasons || result.reasons.length === 0) {
    reasonsContainer.innerHTML = `<div class="reason-item">
                No care-continuity barrier detected.
            </div>`;
  } else {
    result.reasons.forEach((reason) => {
      const item = document.createElement("div");

      item.className = "reason-item";

      item.textContent = reason;

      reasonsContainer.appendChild(item);
    });
  }

  renderExtractedData(result.extracted_data);
}

function renderExtractedData(data) {
  const container = document.getElementById("result-data");

  container.innerHTML = "";

  const entries = Object.entries(data || {});

  entries.forEach(([key, value]) => {
    let displayValue = value;

    if (Array.isArray(value)) {
      displayValue = value.length ? value.join(", ") : "None";
    }

    if (value === true) {
      displayValue = "Detected";
    }

    if (value === false) {
      displayValue = "Not detected";
    }

    if (value === null || value === undefined) {
      displayValue = "Not available";
    }

    const item = document.createElement("div");

    item.className = "data-item";

    const keyElement = document.createElement("div");

    keyElement.className = "data-key";

    keyElement.textContent = formatKey(key);

    const valueElement = document.createElement("div");

    valueElement.className = "data-value";

    valueElement.textContent = String(displayValue);

    item.appendChild(keyElement);

    item.appendChild(valueElement);

    container.appendChild(item);
  });
}

/* =========================================
   HEALTH WORKER
========================================= */

function renderWorkerCase(data) {
  const result = data.result;

  document.getElementById("worker-empty").classList.add("hidden");

  document.getElementById("worker-case").classList.remove("hidden");

  document.getElementById("worker-priority").textContent = formatPriority(
    result.priority
  );

  document.getElementById(
    "worker-patient"
  ).textContent = `${data.patient.name} · Patient #${data.patient.id}`;

  document.getElementById("worker-status").textContent = "OPEN";

  const reasons = document.getElementById("worker-reasons");

  reasons.innerHTML = "";

  if (result.reasons && result.reasons.length) {
    result.reasons.forEach((reason) => {
      const item = document.createElement("div");

      item.className = "reason-item";

      item.textContent = reason;

      reasons.appendChild(item);
    });
  }
}

function sendToHealthWorker() {
  showSectionById("health-worker");
}

async function completeFollowUp(action) {
  if (!latestAlertId) {
    alert("No active review case.");

    return;
  }

  try {
    const response = await fetch(`/api/alerts/${latestAlertId}/close`, {
      method: "POST",
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Unable to close alert.");
    }

    document.getElementById("worker-status").textContent = "REVIEWED";

    showFollowUpResult(action);

    updateDashboardStats();
  } catch (error) {
    alert(error.message);
  }
}

function showFollowUpResult(action) {
  const existing = document.getElementById("follow-up-result");

  if (existing) {
    existing.remove();
  }

  const panel = document.createElement("div");

  panel.id = "follow-up-result";

  panel.className = "panel";

  panel.innerHTML = `
        <span class="section-kicker">
            STEP 04
        </span>

        <h3>
            Follow-up Completed
        </h3>

        <div class="reason-item">
            <strong>Status:</strong>
            Human review completed.
        </div>

        <div class="reason-item">
            <strong>Action:</strong>
            ${escapeHtml(action)}
        </div>
    `;

  document.getElementById("worker-case").appendChild(panel);
}

/* =========================================
   EVALUATION
========================================= */

async function loadEvaluation() {
  try {
    const response = await fetch("/api/evaluation");

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Evaluation unavailable.");
    }

    const results = data.results;

    const metrics = results.metrics;

    document.getElementById("eval-total").textContent =
      results.dataset.total_cases;

    document.getElementById("eval-accuracy").textContent = formatMetric(
      metrics.accuracy
    );

    document.getElementById("eval-precision").textContent = formatMetric(
      metrics.macro_precision
    );

    document.getElementById("eval-f1").textContent = formatMetric(
      metrics.macro_f1
    );

    renderConfusionMatrix(results.confusion_matrix);

    renderMultilingualTests(results.multilingual_tests);
  } catch (error) {
    console.error(error);

    const total = document.getElementById("eval-total");

    if (total) {
      total.textContent = "N/A";
    }
  }
}

function renderConfusionMatrix(data) {
  const container = document.getElementById("confusion-matrix");

  const labels = data.labels || [];

  const matrix = data.matrix || [];

  let html = "<table><thead><tr>" + "<th>Actual / Predicted</th>";

  labels.forEach((label) => {
    html += `<th>
                    ${formatPriority(label)}
                </th>`;
  });

  html += "</tr></thead><tbody>";

  matrix.forEach((row, index) => {
    html += `<tr>
                    <th>
                        ${formatPriority(labels[index])}
                    </th>`;

    row.forEach((value) => {
      html += `<td>
                            ${value}
                        </td>`;
    });

    html += "</tr>";
  });

  html += "</tbody></table>";

  container.innerHTML = html;
}

function renderMultilingualTests(tests) {
  const container = document.getElementById("multilingual-tests");

  container.innerHTML = "";

  (tests || []).forEach((test) => {
    const row = document.createElement("div");

    row.className = "test-row";

    const status = test.passed ? "PASS" : "FAIL";

    const statusClass = test.passed ? "test-passed" : "test-failed";

    const text = document.createElement("span");

    text.textContent = test.text;

    const statusElement = document.createElement("span");

    statusElement.className = statusClass;

    statusElement.textContent = status;

    row.appendChild(text);

    row.appendChild(statusElement);

    container.appendChild(row);
  });
}

/* =========================================
   DASHBOARD STATS
========================================= */

async function updateDashboardStats() {
  try {
    const response = await fetch("/api/patients");

    const data = await response.json();

    if (response.ok && data.patients) {
      const count = document.getElementById("patients-count");

      if (count) {
        count.textContent = data.patients.length;
      }
    }
  } catch (error) {
    console.error("Unable to update dashboard:", error);
  }
}

/* =========================================
   FORMATTERS
========================================= */

function formatPriority(priority) {
  return String(priority || "")
    .replaceAll("_", " ")
    .replace("HIGH REVIEW", "HIGH PRIORITY")
    .replace("MEDIUM REVIEW", "MEDIUM PRIORITY")
    .replace("LOW REVIEW", "LOW PRIORITY");
}

function formatKey(key) {
  return String(key || "").replaceAll("_", " ");
}

function formatMetric(value) {
  if (value === null || value === undefined) {
    return "N/A";
  }

  return `${(Number(value) * 100).toFixed(1)}%`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")

    .replaceAll("<", "&lt;")

    .replaceAll(">", "&gt;")

    .replaceAll('"', "&quot;")

    .replaceAll("'", "&#039;");
}

/* =========================================
   INITIALIZATION
========================================= */

document.addEventListener("DOMContentLoaded", () => {
  loadEvaluation();

  loadPatients();
});
