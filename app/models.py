from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from .database import Base


class Patient(Base):

    __tablename__ = "patients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(200),
        nullable=False
    )

    age = Column(
        Integer,
        nullable=True
    )

    diagnosis = Column(
        String(200),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Message(Base):

    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        nullable=True
    )

    text = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Alert(Base):

    __tablename__ = "alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        nullable=True
    )

    message_id = Column(
        Integer,
        nullable=True
    )

    priority = Column(
        String(50),
        nullable=False
    )

    score = Column(
        Integer,
        default=0
    )

    reasons = Column(
        Text,
        nullable=True
    )

    extracted_data = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(50),
        default="OPEN"
    )

    reviewed_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )