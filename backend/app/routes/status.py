from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.complaint import Complaint
from app.models.status_history import ComplaintStatusHistory
from app.schemas.status import ComplaintStatusUpdate

router = APIRouter(
    prefix="/api/v1/complaints",
    tags=["Complaint Status"]
)

ALLOWED_STATUSES = {
    "Submitted",
    "Needs Review",
    "Classified",
    "Prioritized",
    "Assigned",
    "In Progress",
    "Resolved - Pending Verification",
    "Verified",
    "Reopened",
    "Rejected",
}


@router.patch("/{complaint_id}/status")
def update_complaint_status(
    complaint_id: int,
    status_data: ComplaintStatusUpdate,
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()

    if complaint is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    if status_data.status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Invalid complaint status"
        )

    # Save previous status
    old_status = complaint.status

    # Update current status
    complaint.status = status_data.status

    # Record status history
    history = ComplaintStatusHistory(
        complaint_id=complaint.id,
        old_status=old_status,
        new_status=status_data.status
    )

    db.add(history)
    db.commit()
    db.refresh(complaint)

    return {
        "message": "Complaint status updated successfully",
        "complaint_id": complaint.id,
        "old_status": old_status,
        "new_status": complaint.status
    }


@router.get("/{complaint_id}/status/history")
def get_complaint_status_history(
    complaint_id: int,
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()

    if complaint is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    history = db.query(ComplaintStatusHistory).filter(
        ComplaintStatusHistory.complaint_id == complaint_id
    ).order_by(ComplaintStatusHistory.changed_at.desc()).all()

    return history
