
from pydantic import BaseModel
from typing import Optional


class ComplaintCreate(BaseModel):
    title: str
    description: str
    category: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None


class ComplaintResponse(BaseModel):
    id: int
    title: str
    description: str
    category: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    address: Optional[str]
    status: str
    priority_score: float

    model_config = {"from_attributes": True}
