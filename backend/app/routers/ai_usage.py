from typing import Dict, Any, List
from fastapi import APIRouter
from app.core.ai_tracker import ai_tracker
from app.schemas.ai_usage import AIUsageResponse

router = APIRouter(prefix="/api/ai-usage", tags=["AI Usage Tracker"])

@router.get("", response_model=AIUsageResponse)
def get_ai_usage_logs():
    """Returns real-time AI prompt logs, tokens used, latency, and milestone audit trail."""
    logs = ai_tracker.get_logs(limit=100)
    metrics = ai_tracker.get_summary_metrics()
    return AIUsageResponse(
        summary=metrics,
        logs=logs
    )

@router.get("/summary")
def get_ai_usage_summary():
    """Returns summary metrics of AI prompt executions."""
    return ai_tracker.get_summary_metrics()
