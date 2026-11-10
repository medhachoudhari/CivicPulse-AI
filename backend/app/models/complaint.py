
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from app.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    # Unique complaint ID
    id = Column(Integer, primary_key=True, index=True)

    # Complaint information
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)

    # Location information
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String(300), nullable=True)

    # Complaint processing information
    status = Column(
        String(50),
        nullable=False,
        default="Submitted"
    )

    priority_score = Column(
        Float,
        nullable=False,
        default=0.0
    )

    # Timestamps
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
