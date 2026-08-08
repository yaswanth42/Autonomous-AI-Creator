from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/dashboard")
def get_analytics_dashboard(db: Session = Depends(get_db)):
    """Returns complete dashboard cards, daily publishing trends, and topic distribution charts."""
    svc = AnalyticsService(db)
    return svc.get_dashboard_metrics()
