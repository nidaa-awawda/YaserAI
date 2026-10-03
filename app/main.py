from pathlib import Path
import json
from datetime import datetime

from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from .models import Patient, Message, Alert
from .engine import process_message


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "app" / "templates"
STATIC_DIR = BASE_DIR / "app" / "static"

TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# DATABASE
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="YASER AI",
    description="Small AI for Care Continuity",
    version="1.0.0"
)


# ============================================================
# STATIC + TEMPLATES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# ============================================================
# HOME
# ============================================================

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>YASER AI</title>
    </head>
    <body>
        <h1>YASER AI</h1>
        <p>Small AI for Care Continuity</p>
        <a href="/dashboard">Open Dashboard</a>
    </body>
    </html>
    """


# ============================================================
# DASHBOARD
# ============================================================

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    db: Session = SessionLocal()

    try:

        patients_count = db.query(Patient).count()

        open_alerts = (
            db.query(Alert)
            .filter(Alert.status == "OPEN")
            .count()
        )

        high_alerts = (
            db.query(Alert)
            .filter(Alert.priority == "HIGH_REVIEW")
            .count()
        )

        alerts = (
            db.query(Alert)
            .order_by(Alert.id.desc())
            .limit(50)
            .all()
        )

        patients = (
            db.query(Patient)
            .order_by(Patient.id.desc())
            .limit(50)
            .all()
        )

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "patients_count": patients_count,
                "open_alerts": open_alerts,
                "high_alerts": high_alerts,
                "alerts": alerts,
                "patients": patients,
            }
        )

    finally:
        db.close()


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health():

    return {
        "status": "online",
        "system": "YASER AI",
        "purpose": "Care Continuity",
        "human_review": True,
        "clinical_decision": False
    }


# ============================================================
# CREATE PATIENT
# ============================================================

@app.post("/api/patients")
def create_patient(payload: dict = Body(...)):

    name = str(
        payload.get("name", "")
    ).strip()

    age = payload.get("age")

    diagnosis = str(
        payload.get("diagnosis", "")
    ).strip()

    if not name:

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Patient name is required."
            }
        )

    try:

        age = int(age) if age not in [None, ""] else None

    except ValueError:

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Age must be a number."
            }
        )

    db: Session = SessionLocal()

    try:

        patient = Patient(
            name=name,
            age=age,
            diagnosis=diagnosis or None
        )

        db.add(patient)
        db.commit()
        db.refresh(patient)

        return {
            "success": True,
            "patient": {
                "id": patient.id,
                "name": patient.name,
                "age": patient.age,
                "diagnosis": patient.diagnosis,
            }
        }

    finally:
        db.close()


# ============================================================
# GET PATIENTS
# ============================================================

@app.get("/api/patients")
def get_patients():

    db: Session = SessionLocal()

    try:

        patients = (
            db.query(Patient)
            .order_by(Patient.id.desc())
            .all()
        )

        return {
            "success": True,
            "patients": [
                {
                    "id": patient.id,
                    "name": patient.name,
                    "age": patient.age,
                    "diagnosis": patient.diagnosis,
                    "created_at": (
                        patient.created_at.isoformat()
                        if patient.created_at
                        else None
                    )
                }
                for patient in patients
            ]
        }

    finally:
        db.close()


# ============================================================
# ANALYZE MESSAGE
# ============================================================

@app.post("/api/analyze")
def analyze_message(payload: dict = Body(...)):

    text = str(
        payload.get("text", "")
    ).strip()

    if not text:

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Please enter a caregiver message."
            }
        )

    result = process_message(text)

    return {
        "success": True,
        "message": text,
        "result": result
    }


# ============================================================
# ANALYZE + SAVE MESSAGE + CREATE ALERT
# ============================================================

@app.post("/api/analyze-and-create-alert")
def analyze_and_create_alert(
    payload: dict = Body(...)
):

    text = str(
        payload.get("text", "")
    ).strip()

    patient_id = payload.get("patient_id")

    if not text:

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Please enter a caregiver message."
            }
        )

    if not patient_id:

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Please select a patient."
            }
        )

    try:
        patient_id = int(patient_id)
    except ValueError:

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Invalid patient ID."
            }
        )

    db: Session = SessionLocal()

    try:

        patient = (
            db.query(Patient)
            .filter(Patient.id == patient_id)
            .first()
        )

        if not patient:

            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "Patient not found."
                }
            )

        result = process_message(text)

        message = Message(
            patient_id=patient_id,
            text=text
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        alert = Alert(
            patient_id=patient_id,
            message_id=message.id,
            priority=result["priority"],
            score=result["score"],
            reasons=json.dumps(
                result["reasons"]
            ),
            extracted_data=json.dumps(
                result["extracted_data"]
            ),
            status="OPEN"
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)

        return {
            "success": True,
            "patient": {
                "id": patient.id,
                "name": patient.name,
                "age": patient.age,
            },
            "message_id": message.id,
            "alert_id": alert.id,
            "result": result
        }

    finally:
        db.close()


# ============================================================
# PATIENT TIMELINE
# ============================================================

@app.get("/api/patients/{patient_id}/timeline")
def patient_timeline(patient_id: int):

    db: Session = SessionLocal()

    try:

        patient = (
            db.query(Patient)
            .filter(Patient.id == patient_id)
            .first()
        )

        if not patient:

            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "Patient not found."
                }
            )

        messages = (
            db.query(Message)
            .filter(Message.patient_id == patient_id)
            .order_by(Message.id.desc())
            .all()
        )

        alerts = (
            db.query(Alert)
            .filter(Alert.patient_id == patient_id)
            .order_by(Alert.id.desc())
            .all()
        )

        return {
            "success": True,

            "patient": {
                "id": patient.id,
                "name": patient.name,
                "age": patient.age,
                "diagnosis": patient.diagnosis,
            },

            "messages": [
                {
                    "id": message.id,
                    "text": message.text,
                    "created_at": (
                        message.created_at.isoformat()
                        if message.created_at
                        else None
                    )
                }
                for message in messages
            ],

            "alerts": [
                {
                    "id": alert.id,
                    "priority": alert.priority,
                    "score": alert.score,
                    "status": alert.status,
                    "reasons": (
                        json.loads(alert.reasons)
                        if alert.reasons
                        else []
                    ),
                    "created_at": (
                        alert.created_at.isoformat()
                        if alert.created_at
                        else None
                    )
                }
                for alert in alerts
            ]
        }

    finally:
        db.close()


# ============================================================
# CLOSE ALERT
# ============================================================

@app.post("/api/alerts/{alert_id}/close")
def close_alert(alert_id: int):

    db: Session = SessionLocal()

    try:

        alert = (
            db.query(Alert)
            .filter(Alert.id == alert_id)
            .first()
        )

        if not alert:

            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "Alert not found."
                }
            )

        alert.status = "REVIEWED"
        alert.reviewed_at = datetime.utcnow()

        db.commit()

        return {
            "success": True,
            "alert_id": alert.id,
            "status": alert.status
        }

    finally:
        db.close()