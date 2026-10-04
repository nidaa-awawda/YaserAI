# YASER AI

### Small AI for Pediatric Leukemia Care Continuity

**World Bank Small AI for Development Challenge – Health**

> **YASER AI helps keep pediatric leukemia care connected when connectivity, mobility, and healthcare access are disrupted.**

---

## Overview

**YASER AI** is a lightweight **Small AI care-coordination system** designed to support continuity of care for children with leukemia in crisis-affected and low-resource settings.

When healthcare pathways are disrupted, families may face:

* Missed treatment or follow-up appointments
* Delayed laboratory monitoring
* Medication availability uncertainty
* Pending or interrupted referrals
* Limited internet connectivity
* Difficulty communicating with healthcare providers
* Fragmented information across different points of care

YASER AI addresses this problem by creating a lightweight digital layer between **caregivers and authorized health workers**.

The system uses:

* Arabic Natural Language Processing (NLP)
* SMS and voice-based interaction
* Offline-capable workflows
* Lightweight machine-learning models
* Care-pathway event extraction
* A Care Continuity Risk Engine
* Explainable alerts
* Human-in-the-loop review

**YASER AI does not diagnose leukemia, prescribe medication, or replace clinicians.**

---

## The Problem

Pediatric leukemia care can require repeated and coordinated interactions with healthcare services, including laboratory monitoring, treatment appointments, medication management, referrals, and follow-up.

In crisis-affected or resource-constrained environments, these activities can become disconnected.

For example:

```text
Caregiver
   │
   ├── Missed appointment
   ├── Delayed laboratory test
   ├── Medication uncertainty
   ├── Pending referral
   └── Limited connectivity
          │
          ▼
   Fragmented care pathway
          │
          ▼
   Risk of delayed follow-up
```

YASER AI focuses on **continuity of care**, rather than attempting to automate clinical diagnosis.

---

## Why Pediatric Leukemia?

Pediatric leukemia provides a focused initial use case because care can involve:

* Repeated follow-up
* Laboratory monitoring
* Treatment milestones
* Medication coordination
* Referrals
* Regular communication between families and healthcare workers

Starting with one disease allows the project to build and evaluate a focused MVP during the hackathon.

The architecture is designed to later expand to:

**Pediatric leukemia → Other pediatric cancers → Blood cancers → Broader cancer-care pathways**

---

# How YASER AI Works

YASER provides a lightweight communication and care-coordination layer.

A caregiver or authorized health worker can provide information through **SMS, voice, or an offline-capable application**.

The system then:

1. Receives the communication
2. Extracts relevant care information
3. Updates the patient's care timeline
4. Compares the current state with previous events
5. Detects potential continuity gaps
6. Calculates a workflow-oriented risk level
7. Explains why the case was flagged
8. Routes appropriate cases to an authorized health worker

```text
Caregiver
    │
    │ Arabic SMS / Voice
    ▼
┌──────────────────────┐
│   YASER AI Intake    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Arabic NLP        │
│ Event Extraction     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Care Continuity      │
│ Risk Engine          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Explainable Alert    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Human Health Worker  │
│       Review         │
└──────────────────────┘
```

---

# Core Innovation: Care Continuity Risk Engine

The central component of YASER AI is the **Care Continuity Risk Engine**.

Instead of attempting to predict a patient's medical outcome, the engine identifies potential **care-coordination gaps**.

| Signal                | Example                | System Response     |
| --------------------- | ---------------------- | ------------------- |
| Appointment           | Next follow-up unknown | Continuity gap      |
| Laboratory monitoring | Required test delayed  | Review flag         |
| Medication            | Availability uncertain | Follow-up required  |
| Symptoms              | New symptom reported   | Safety review       |
| Referral              | Referral pending       | Escalation workflow |

The resulting risk level is a **care-coordination signal**, not a medical diagnosis or prediction of survival.

---

# Example User Journey

A caregiver sends an Arabic message:

> "The child has a fever today, the last blood test was four days ago, and we have not received confirmation of the next appointment."

YASER converts the message into structured information:

```text
New symptom
    → Fever

Laboratory monitoring
    → Last test: 4 days ago

Appointment
    → Next appointment unknown

Care access
    → Possible follow-up disruption
```

The system generates a **continuity alert** and routes the case to an authorized health worker according to the configured workflow.

### Important

YASER does **not** independently recommend treatment.

---

# Technology Architecture

The MVP is designed around lightweight technologies suitable for low-resource environments.

```text
┌──────────────────────────────────────┐
│             User Layer               │
│                                      │
│       SMS │ Voice │ Web / Mobile     │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          Arabic NLP Layer             │
│                                      │
│  Message Processing │ Event Extraction│
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│       Small AI Classification         │
│                                      │
│       Continuity Risk Detection       │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│       Rules & Safety Layer            │
│                                      │
│   Red Flags │ Escalation │ Validation │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          Care Database                │
│                                      │
│ Patient │ Timeline │ Events │ Alerts  │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│       Health Worker Dashboard         │
│                                      │
│ Timeline │ Alerts │ Reasons │ Status  │
└──────────────────────────────────────┘
```

### Planned MVP Components

* **Input:** SMS, voice, simple web/mobile interface
* **Arabic NLP:** Care-event and symptom extraction
* **Machine Learning:** Lightweight continuity-risk classifier
* **Rules:** Predefined safety and escalation rules
* **Storage:** Local/offline-capable storage
* **Synchronization:** Sync when connectivity becomes available
* **Dashboard:** Patient timeline, alerts, explanations, and follow-up status

The initial classifier can use lightweight approaches such as:

```text
TF-IDF
   +
Logistic Regression
```

The architecture can later evolve toward more capable Arabic-language models after validation.

Model selection will consider:

* Accuracy
* Latency
* Privacy
* Computational requirements
* Explainability
* Resource constraints

---

# Offline-First Design

YASER is designed for environments where reliable connectivity cannot be assumed.

```text
ONLINE
   │
   ▼
Receive → Process → Store → Sync

OFFLINE
   │
   ▼
Receive → Local Storage
             │
             │ Connectivity restored
             ▼
           Sync
             │
             ▼
         Health Worker
```

This allows the coordination layer to continue functioning even when internet connectivity is temporarily unavailable.

---

# Responsible AI & Safety

YASER is intentionally designed as an **assistive care-coordination system**, not an autonomous clinical decision-maker.

### Safety principles

* Clinical decisions remain with qualified health professionals.
* YASER does not diagnose leukemia.
* YASER does not prescribe medication.
* YASER does not determine treatment plans.
* YASER does not provide autonomous emergency medical decisions.
* Alerts include the information that triggered them.
* Only necessary patient information should be processed.
* Real patient data should only be used with appropriate authorization and safeguards.
* The hackathon prototype uses synthetic or appropriately permitted data.
* Arabic-language performance and potential bias should be evaluated before real-world deployment.

---

# Data Strategy

For the hackathon MVP, the project uses a **synthetic pediatric leukemia care dataset**.

The dataset represents realistic care-pathway scenarios such as:

* Stable follow-up
* Missed appointments
* Delayed laboratory monitoring
* Medication uncertainty
* Pending referrals
* New reported symptoms

The synthetic dataset will be clearly identified as such.

### Future Pilot

A real-world pilot would require:

* Authorized healthcare institution
* Appropriate data governance
* Privacy and security controls
* De-identification where appropriate
* Informed consent where applicable
* Ethics review
* Clinical oversight
* Regulatory compliance

---

# MVP Scope

The hackathon MVP will demonstrate an end-to-end workflow:

### 1. Arabic SMS Intake

A caregiver sends a message describing the child's situation.

### 2. Information Extraction

YASER identifies relevant care events.

### 3. Patient Timeline

The extracted information is added to the patient's care timeline.

### 4. Risk Detection

The Care Continuity Risk Engine identifies potential gaps.

### 5. Explainable Alert

The system shows why the case was flagged.

### 6. Human Review

An authorized health worker receives and reviews the alert.

### 7. Offline Demonstration

The system demonstrates local operation and synchronization after connectivity is restored.

---

# Prototype Success Metrics

These are **development targets**, not established clinical results.

| Metric                          | What is Measured                               | Purpose                       |
| ------------------------------- | ---------------------------------------------- | ----------------------------- |
| Information Extraction Accuracy | Correct extraction of care events              | Evaluate Arabic NLP           |
| Risk Classification             | Precision / recall on synthetic cases          | Evaluate model utility        |
| Alert Explanation Coverage      | Alerts with traceable reasons                  | Support transparency          |
| Offline Functionality           | Successful operation without live connectivity | Test constrained environments |
| Workflow Completion             | Caregiver-to-health-worker flow                | Assess usability              |

---

# Development Roadmap

### Phase 1 — Hackathon MVP

* Pediatric leukemia
* Arabic language
* SMS / voice
* Offline-capable workflow
* Synthetic data
* Human review

### Phase 2 — Workflow Expansion

Expand to additional pediatric cancer pathways and improve healthcare workflow integration.

### Phase 3 — Broader Cancer Care

Adapt the architecture to other blood cancers and cancer-care pathways.

### Phase 4 — Authorized Pilot

Test the system in an appropriately governed low-resource or crisis-affected healthcare setting.

### Phase 5 — Multi-Context Scaling

Adapt the architecture to different countries, languages, and healthcare systems.

---

# Scalability

YASER is designed as a **reusable care-continuity architecture**, rather than a single-disease model.

The first implementation focuses on pediatric leukemia to keep the MVP:

* Focused
* Measurable
* Feasible
* Clinically bounded

The underlying architecture can later be adapted by changing:

* Clinical workflows
* Relevant data fields
* Care-event definitions
* Safety rules
* Escalation protocols

---

# Why Palestine?

Palestine is the project's initial design environment.

The project is informed by challenges that can affect continuity of care in crisis-affected settings, including:

* Intermittent connectivity
* Mobility constraints
* Limited resources
* Fragmented referrals
* Disrupted healthcare access
* Dependence on simple communication channels

The objective is **not** to build a system exclusively for Palestine.

Instead, Palestine provides the initial environment for developing and testing a model that can potentially be adapted to other low-resource and crisis-affected contexts.

---

# Expected Development Impact

YASER aims to:

* Help health workers identify disrupted follow-up earlier
* Organize care-pathway information
* Support communication through basic phones
* Reduce dependence on continuous internet connectivity
* Provide transparent human-supervised AI workflows
* Create a reusable architecture for cancer-care coordination

---

# Project Scope & Limitations

YASER is currently a **prototype concept / hackathon MVP**.

It should **not** be used for:

* Independent diagnosis
* Medication dosing
* Treatment selection
* Autonomous emergency decisions
* Clinical deployment without validation

Real-world deployment would require appropriate:

* Clinical validation
* Healthcare partnerships
* Ethics review
* Data governance
* Security controls
* Regulatory review
* Human oversight

---

# One-Sentence Value Proposition

> **YASER AI helps keep pediatric leukemia care connected when connectivity, mobility, and healthcare access are disrupted.**

---

# 30-Second Pitch

> A child's cancer treatment should not depend on whether a family can maintain a stable internet connection, reach a hospital, or keep track of a disrupted care pathway.
>
> **YASER AI** is a Palestinian Small AI system designed to help families and health workers maintain continuity of care for children with leukemia through SMS, voice, and offline-capable tools.
>
> It identifies potential gaps in follow-up and routes appropriate cases to human health workers. It does not diagnose cancer or replace clinicians.
>
> We start with pediatric leukemia as a focused use case in Palestine, then aim to adapt the architecture to other cancers and crisis-affected health systems.

---

# Evidence & References

* [World Health Organization – Eastern Mediterranean Region](https://www.emro.who.int/)
* [World Bank](https://www.worldbank.org/)
* [International Agency for Research on Cancer – GLOBOCAN](https://gco.iarc.who.int/)
* [Palestinian Ministry of Health](https://www.moh.ps/)

---

# Project Status

**Current stage:** Hackathon MVP / Prototype

**Focus:** Health · Small AI · Pediatric Leukemia · Care Continuity · Arabic NLP · Offline AI · Responsible AI
<img width="1310" height="599" alt="image" src="https://github.com/user-attachments/assets/f89ce9a8-da89-4439-bd5e-8b64232f0243" />



---

## Disclaimer

YASER AI is a research and development prototype. It is not a medical device and should not be used to make independent clinical decisions. Any future clinical deployment requires appropriate validation, clinical governance, ethical oversight, privacy protection, security controls, and regulatory approval.
