from typing import Optional

from pydantic import BaseModel


class PatientCreate(BaseModel):

    name: str

    age: Optional[int] = None

    diagnosis: Optional[str] = None


class MessageCreate(BaseModel):

    patient_id: Optional[int] = None

    text: str