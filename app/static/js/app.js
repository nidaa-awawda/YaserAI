async function submitIntake(event) {
  event.preventDefault();

  const demoCode = document.getElementById("demoCode").value;

  const channel = document.getElementById("channel").value;

  const text = document.getElementById("message").value;

  const result = document.getElementById("result");

  result.classList.remove("hidden");

  result.innerHTML = "<p>Analyzing message...</p>";

  try {
    const response = await fetch("/api/intake", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        demo_code: demoCode,
        channel: channel,
        text: text,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Request failed.");
    }

    result.innerHTML = `
            <h3>Alert Created</h3>

            <p>
                <strong>Alert ID:</strong>
                ${data.alert_id}
            </p>

            <p>
                <strong>Risk Level:</strong>
                <span class="risk ${data.risk_level.toLowerCase()}">
                    ${data.risk_level}
                </span>
            </p>

            <h4>Reasons</h4>

            <ul>
                ${
                  data.reasons.length
                    ? data.reasons
                        .map((reason) => `<li>${reason}</li>`)
                        .join("")
                    : "<li>No continuity gap detected.</li>"
                }
            </ul>

            <h4>Extracted Information</h4>

            <pre>${JSON.stringify(data.extracted, null, 2)}</pre>

            <p class="notice">
                This result is for human workflow review
                only and is not a clinical decision.
            </p>
        `;
  } catch (error) {
    result.innerHTML = `
            <h3>Request Error</h3>
            <p>${error.message}</p>
        `;
  }
}

async function loadAlerts() {
  const container = document.getElementById("alerts");

  if (!container) {
    return;
  }

  const response = await fetch("/api/alerts");

  const alerts = await response.json();

  if (!alerts.length) {
    container.innerHTML = `
            <div class="card">
                <p>No alerts yet.</p>
            </div>
        `;

    return;
  }

  container.innerHTML = alerts
    .map(
      (alert) => `

            <article class="alert-card">

                <div class="alert-header">

                    <div>

                        <h3>
                            Alert #${alert.id}
                        </h3>

                        <p>
                            Patient:
                            ${alert.patient}
                        </p>

                    </div>

                    <span
                        class="risk ${alert.risk_level.toLowerCase()}"
                    >
                        ${alert.risk_level}
                    </span>

                </div>


                <p>
                    <strong>Status:</strong>
                    ${alert.status}
                </p>


                <p>
                    ${alert.message}
                </p>


                <h4>Reasons</h4>

                <ul>
                    ${alert.reasons
                      .map((reason) => `<li>${reason}</li>`)
                      .join("")}
                </ul>


                <div class="actions">

                    <button
                        onclick="updateAlert(
                            ${alert.id},
                            'IN_REVIEW'
                        )"
                    >
                        Start Review
                    </button>


                    <button
                        onclick="updateAlert(
                            ${alert.id},
                            'RESOLVED'
                        )"
                    >
                        Mark Resolved
                    </button>

                </div>

            </article>

        `
    )
    .join("");
}

async function updateAlert(id, status) {
  await fetch(`/api/alerts/${id}/status`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      status: status,
    }),
  });

  loadAlerts();
}

function setupVoiceInput() {
  const button = document.getElementById("voiceButton");

  if (!button) {
    return;
  }

  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    button.disabled = true;

    button.textContent = "Voice Input Not Supported";

    return;
  }

  const recognition = new SpeechRecognition();

  recognition.lang = "en-US";

  recognition.interimResults = false;

  recognition.continuous = false;

  button.addEventListener("click", () => {
    button.textContent = "Listening...";

    recognition.start();
  });

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;

    document.getElementById("message").value = transcript;

    button.textContent = "Voice Input";
  };

  recognition.onerror = () => {
    button.textContent = "Voice Input";
  };
}

const intakeForm = document.getElementById("intakeForm");

if (intakeForm) {
  intakeForm.addEventListener("submit", submitIntake);
}

setupVoiceInput();

loadAlerts();
