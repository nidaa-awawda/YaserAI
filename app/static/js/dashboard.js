// ============================================================
// YASER AI DASHBOARD
// ============================================================

// ============================================================
// CREATE PATIENT
// ============================================================

async function createPatient() {
  const name = document.getElementById("patientName").value.trim();

  const age = document.getElementById("patientAge").value;

  const diagnosis = document.getElementById("patientDiagnosis").value.trim();

  const messageBox = document.getElementById("patientMessage");

  if (!name) {
    showMessage(messageBox, "Please enter the patient name.", "error");

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

        age: age || null,

        diagnosis: diagnosis || "Pediatric leukemia care",
      }),
    });

    const data = await response.json();

    if (!response.ok || !data.success) {
      throw new Error(data.error || "Unable to create patient.");
    }

    showMessage(
      messageBox,

      `Patient created successfully. Patient ID: #${data.patient.id}`,

      "success"
    );

    addPatientToSelect(data.patient);

    document.getElementById("patientName").value = "";

    document.getElementById("patientAge").value = "";
  } catch (error) {
    showMessage(messageBox, error.message, "error");
  }
}

// ============================================================
// ADD PATIENT TO SELECT
// ============================================================

function addPatientToSelect(patient) {
  const select = document.getElementById("patientSelect");

  const option = document.createElement("option");

  option.value = patient.id;

  option.textContent = `#${patient.id} — ${patient.name}`;

  select.appendChild(option);

  select.value = patient.id;
}

// ============================================================
// ANALYZE + CREATE ALERT
// ============================================================

async function analyzeAndCreateAlert() {
  const patientId = document.getElementById("patientSelect").value;

  const message = document.getElementById("caregiverMessage").value.trim();

  const errorBox = document.getElementById("analysisError");

  const analysisPanel = document.getElementById("analysisPanel");

  const alertCreated = document.getElementById("alertCreated");

  errorBox.classList.add("hidden");

  alertCreated.classList.add("hidden");

  if (!patientId) {
    showMessage(errorBox, "Please select a patient.", "error");

    return;
  }

  if (!message) {
    showMessage(errorBox, "Please enter a caregiver message.", "error");

    return;
  }

  analysisPanel.classList.remove("hidden");

  analysisPanel.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });

  try {
    const response = await fetch("/api/analyze-and-create-alert", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        patient_id: patientId,

        text: message,
      }),
    });

    const data = await response.json();

    if (!response.ok || !data.success) {
      throw new Error(data.error || "Analysis failed.");
    }

    displayAnalysis(data.result);

    alertCreated.textContent = `Alert #${data.alert_id} created successfully for Patient #${patientId}.`;

    alertCreated.classList.remove("hidden");
  } catch (error) {
    showMessage(errorBox, error.message, "error");
  }
}

// ============================================================
// DISPLAY ANALYSIS
// ============================================================

function displayAnalysis(result) {
  const priority = result.priority || "LOW_REVIEW";

  const priorityElement = document.getElementById("finalPriority");

  priorityElement.textContent = formatPriority(priority);

  priorityElement.className = "priority-value " + priority.toLowerCase();

  document.getElementById("mlPrediction").textContent =
    result.ml_prediction || "Unavailable";

  const confidence = result.ml_confidence;

  document.getElementById("mlConfidence").textContent =
    confidence !== null && confidence !== undefined
      ? Math.round(confidence * 100) + "%"
      : "Unavailable";

  document.getElementById("ruleScore").textContent = result.score ?? "0";

  displayDetectedInformation(result.extracted_data || {});

  displayReasons(result.reasons || []);
}

// ============================================================
// FORMAT PRIORITY
// ============================================================

function formatPriority(priority) {
  return priority.replaceAll("_", " ");
}

// ============================================================
// DETECTED INFORMATION
// ============================================================

function displayDetectedInformation(data) {
  const container = document.getElementById("detectedInformation");

  container.innerHTML = "";

  const items = [];

  if (data.symptoms && data.symptoms.length) {
    items.push({
      label: "Symptoms",
      value: data.symptoms.join(", "),
    });
  }

  if (data.lab_days_ago !== null && data.lab_days_ago !== undefined) {
    items.push({
      label: "Last laboratory test",

      value: data.lab_days_ago + " days ago",
    });
  }

  if (data.appointment_status) {
    items.push({
      label: "Appointment",

      value: data.appointment_status,
    });
  }

  if (data.medication_status) {
    items.push({
      label: "Medication",

      value: data.medication_status,
    });
  }

  if (data.referral_status) {
    items.push({
      label: "Referral",

      value: data.referral_status,
    });
  }

  if (data.connectivity_issue) {
    items.push({
      label: "Connectivity",

      value: "Issue detected",
    });
  }

  if (!items.length) {
    container.innerHTML = `<div class="no-signal">
                No structured signals detected.
            </div>`;

    return;
  }

  items.forEach((item) => {
    const element = document.createElement("div");

    element.className = "detected-item";

    element.innerHTML = `
                <span>${escapeHtml(item.label)}</span>
                <strong>${escapeHtml(item.value)}</strong>
            `;

    container.appendChild(element);
  });
}

// ============================================================
// REASONS
// ============================================================

function displayReasons(reasons) {
  const list = document.getElementById("reasonsList");

  list.innerHTML = "";

  reasons.forEach((reason) => {
    const li = document.createElement("li");

    li.textContent = reason;

    list.appendChild(li);
  });
}

// ============================================================
// DEMO MESSAGE
// ============================================================

function loadDemoMessage() {
  const message = document.getElementById("caregiverMessage");

  message.value = "The child has fever and the appointment is not confirmed.";
}

// ============================================================
// MESSAGE HELPER
// ============================================================

function showMessage(element, message, type) {
  element.textContent = message;

  element.classList.remove("hidden", "success-message", "error-message");

  if (type === "success") {
    element.classList.add("success-message");
  } else {
    element.classList.add("error-message");
  }
}

// ============================================================
// HTML SAFETY
// ============================================================

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")

    .replaceAll("<", "&lt;")

    .replaceAll(">", "&gt;")

    .replaceAll('"', "&quot;")

    .replaceAll("'", "&#039;");
}
