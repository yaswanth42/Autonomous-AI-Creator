from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.editorial_history import EditorialHistory
from app.schemas.editorial import EditorialEvaluationRequest, EditorialEvaluationResponse
from app.services.editorial_engine import EditorialDecisionEngine

router = APIRouter(prefix="/api/editorial", tags=["Editorial"])

@router.get("/history")
def get_editorial_history(
    decision: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Returns editorial decisions (PUBLISH/REJECT) and 7-factor score breakdowns."""
    q = db.query(EditorialHistory).filter(EditorialHistory.is_deleted == False)
    if decision:
        q = q.filter(EditorialHistory.decision == decision.upper())
    
    results = q.order_by(EditorialHistory.created_at.desc()).limit(limit).all()
    return [r.to_dict() for r in results]

@router.post("/evaluate", response_model=EditorialEvaluationResponse)
def evaluate_candidate_topic(
    request: EditorialEvaluationRequest,
    db: Session = Depends(get_db)
):
    """Runs 7-factor editorial decision engine against candidate text."""
    engine = EditorialDecisionEngine(db, threshold=request.threshold or 7.0)
    result = engine.evaluate_topic(
        title=request.title,
        content=request.content,
        url=request.url,
        source=request.source or "Manual Submission",
        custom_threshold=request.threshold
    )
    return EditorialEvaluationResponse(**result)
