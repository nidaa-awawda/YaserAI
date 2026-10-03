Small AI for Pediatric Leukemia Care Continuity
World Bank Small AI for Development Challenge – Health
1. Executive Summary
YASER AI is a Small AI solution designed to help maintain continuity of care for children with leukemia in crisis-affected and low-resource settings. The system focuses on a practical problem: treatment and follow-up can become fragmented when families face disrupted connectivity, difficult access to health facilities, missing appointments, delayed tests, medication availability problems, or interrupted referrals.
YASER does not diagnose leukemia, prescribe medication, or replace clinicians. Instead, it uses lightweight AI, Arabic natural-language processing, SMS/voice interfaces, offline-capable workflows, and a human-in-the-loop safety layer to identify potential gaps in a child's care pathway and alert an authorized health worker for review.
2. The Problem
Children with leukemia require coordinated and repeated interactions with the health system, including laboratory monitoring, treatment appointments, medication management, referrals, and follow-up. In crisis-affected or resource-constrained settings, these activities can become disconnected.
•	A family may miss or lose a treatment or follow-up appointment.
•	A required laboratory test may be delayed.
•	Medication availability may be uncertain.
•	A referral may remain pending.
•	A family may have limited internet access or only a basic phone.
•	Health workers may lack a simple consolidated view of what changed since the previous contact.
The project therefore addresses continuity of care rather than attempting to automate clinical diagnosis.
3. Why Pediatric Leukemia?
Leukemia provides a focused and measurable first use case because pediatric leukemia care can involve repeated monitoring, treatment milestones, laboratory follow-up, medication and referral coordination. Starting with one disease allows the team to build and test a credible minimum viable product within a short hackathon while leaving a clear pathway for expansion.
The first version will focus on pediatric leukemia. Later versions can expand to other pediatric cancers, other blood cancers, and eventually broader cancer-care pathways.
4. The Proposed Solution
YASER creates a lightweight digital care-continuity layer between families and health workers. A parent, caregiver, or authorized health worker can submit information through SMS, voice, or an offline-capable application.
The system then:
•	Extracts relevant care information from Arabic messages or voice transcripts.
•	Organizes information into a patient care timeline.
•	Detects potential gaps such as a missing follow-up, delayed monitoring, or unresolved referral.
•	Calculates a Care Continuity Risk level for workflow prioritization.
•	Explains which information triggered the alert.
•	Escalates appropriate cases to an authorized human health worker.
The risk level is a care-coordination signal, not a medical diagnosis or prediction of survival.
5. Core Innovation: Care Continuity Risk Engine
The central innovation is a Small AI engine that compares the current care state with the previous recorded state.
Signal	Example	System response
Appointment	Next follow-up unknown	Continuity gap
Laboratory monitoring	Required test delayed	Review flag
Medication	Availability uncertain	Follow-up required
Symptoms	New reported symptom	Safety review
Referral	Referral pending	Escalation workflow
6. Example User Journey
A caregiver sends an Arabic message: “The child has a fever today, the last blood test was four days ago, and we have not received confirmation of the next appointment.”
YASER converts the message into structured information:
•	New symptom reported: fever
•	Last laboratory monitoring: four days ago
•	Next appointment: unknown
•	Access/follow-up disruption: possible
The system generates a continuity alert and routes the case to a human health worker according to the configured workflow. The system does not independently recommend treatment.
7. Technology Architecture
The MVP will use a lightweight architecture designed for low-resource environments.
•	Input: SMS, voice, and simple web/mobile interface.
•	Arabic NLP: symptom and care-event extraction.
•	Small classification model: continuity-risk classification.
•	Rules and safety layer: predefined escalation and red-flag checks.
•	Local/offline storage: temporary storage when connectivity is unavailable.
•	Synchronization: upload when connectivity returns.
•	Health-worker dashboard: patient timeline, alerts, explanations, and follow-up status.
The MVP can begin with a lightweight classifier such as TF-IDF plus Logistic Regression and evolve toward more capable Arabic models after validation. The technical choice will be driven by accuracy, latency, privacy, and resource constraints.
8. Responsible AI and Safety
•	YASER is an assistive care-coordination tool, not an autonomous clinical decision-maker.
•	Clinical decisions remain with qualified health professionals.
•	The system will display the reasons for a continuity alert.
•	Only minimum necessary patient information should be processed.
•	Real patient data should only be used with appropriate authorization, privacy safeguards, and ethical oversight.
•	The hackathon prototype will use synthetic or appropriately permitted data rather than claiming access to confidential patient records.
•	Performance will be evaluated for Arabic-language errors and potential bias before any real-world deployment.
9. Data Strategy
For the hackathon MVP, the team will create a synthetic pediatric leukemia care dataset representing realistic care-pathway events. Scenarios will include stable follow-up, missed appointments, delayed laboratory monitoring, medication uncertainty, pending referrals, and new reported symptoms. The dataset will be clearly labeled as synthetic.
A later pilot would require collaboration with an authorized health institution, appropriate governance, informed consent where applicable, de-identification, security controls, and ethics review.
10. MVP to Build During the Hackathon
•	Arabic SMS intake and response flow.
•	Simple voice-to-text demonstration.
•	Synthetic pediatric leukemia patient records.
•	Patient care timeline.
•	Continuity-risk classifier.
•	Explainable alert showing why a case was flagged.
•	Health-worker dashboard.
•	Offline/local storage demonstration.
•	End-to-end demo from caregiver message to human-review alert.
11. Success Metrics for the Prototype
The following are prototype targets to be measured during development; they are not pre-established clinical results.
Metric	What will be measured	Purpose
Information extraction accuracy	Correct extraction of key care events	Assess Arabic NLP
Risk classification performance	Precision/recall on synthetic test cases	Assess model utility
Alert explanation coverage	Percentage of alerts with traceable reasons	Support transparency
Offline functionality	Successful operation without live connectivity	Test constrained environment
Workflow completion	Successful caregiver-to-health-worker flow	Assess usability
12. Development Roadmap
Phase 1 – Hackathon: Pediatric leukemia; Arabic; SMS/voice; offline MVP; human review.
Phase 2: Expand to other pediatric cancers and improve clinical workflow integration.
Phase 3: Expand to other blood cancers and additional cancer-care pathways.
Phase 4: Pilot in authorized low-resource or crisis-affected health settings.
Phase 5: Adapt and scale the architecture to multiple countries and health systems.
13. Scalability
YASER is designed around a reusable care-continuity architecture rather than a single disease model. The first deployment focuses narrowly on pediatric leukemia to keep the problem measurable and the MVP feasible. The same architecture can later support other cancer pathways by changing the relevant clinical workflow, data fields, and safety rules.
14. Why Palestine?
Palestine is the project's initial design environment. The system is designed around constraints that can affect continuity of care in crisis-affected settings: intermittent connectivity, mobility barriers, constrained resources, fragmented referrals, and the need for simple communication channels. The ambition is not to build a system only for Palestine, but to develop a model that can be adapted to other low-resource and crisis-affected contexts.
15. Expected Development Impact
•	Help health workers identify disrupted follow-up earlier.
•	Make care-pathway information easier to organize.
•	Support communication through basic phones and low-bandwidth channels.
•	Reduce dependence on continuous internet connectivity for the coordination layer.
•	Provide a transparent, human-supervised AI workflow.
•	Create a reusable architecture for other cancer-care pathways.
16. One-Sentence Value Proposition
YASER AI helps keep pediatric leukemia care connected when connectivity, mobility, and healthcare access are disrupted.
17. 30-Second Pitch
A child's cancer treatment should not depend on whether a family can maintain a stable internet connection, reach a hospital, or keep track of a disrupted care pathway. YASER is a Palestinian Small AI system designed to help families and health workers maintain continuity of care for children with leukemia through SMS, voice, and offline-capable tools. It identifies potential gaps in follow-up and routes appropriate cases to human health workers. It does not diagnose cancer or replace clinicians. We start with pediatric leukemia as a focused use case in Palestine, then expand the architecture to other cancers and crisis-affected health systems.
18. Important Scope Statement
YASER is a prototype concept for care coordination. It must not be used for independent diagnosis, medication dosing, treatment selection, or emergency medical decision-making without validation, clinical governance, regulatory review, and appropriate deployment safeguards.
19. Evidence and References
•	World Health Organization (WHO) – occupied Palestinian territory health emergency and oncology-related reporting: https://www.emro.who.int/
•	World Bank – Global AI & Digital Summit 2026 / Small AI for Development Challenge information: https://www.worldbank.org/
•	International Agency for Research on Cancer (IARC), GLOBOCAN: https://gco.iarc.who.int/
•	Palestinian Ministry of Health: https://www.moh.ps/
