
from pydantic import BaseModel, Field


class ComplaintStatusUpdate(BaseModel):
    status: str = Field(
        ...,
        description="New complaint status"
    )
