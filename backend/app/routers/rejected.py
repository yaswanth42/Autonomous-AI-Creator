from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.rejected_topic import RejectedTopic
from app.schemas.editorial import RejectedTopicResponse

router = APIRouter(prefix="/api/rejected", tags=["Rejected Topics"])

@router.get("/topics", response_model=List[RejectedTopicResponse])
def get_rejected_topics(
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Returns topics rejected by the editorial decision engine with full reason and score breakdown."""
    rejected = db.query(RejectedTopic).filter(
        RejectedTopic.is_deleted == False
    ).order_by(RejectedTopic.created_at.desc()).limit(limit).all()

    return [r.to_dict() for r in rejected]
