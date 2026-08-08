from typing import Dict, Any, List
from pydantic import BaseModel

class MetricCard(BaseModel):
    title: str
    value: Any
    change: str
    icon: str
    trend: str # UP, DOWN, NEUTRAL

class ChartDataPoint(BaseModel):
    label: str
    value: float
    secondary_value: float = 0.0

class AnalyticsDashboardResponse(BaseModel):
    cards: Dict[str, Any]
    daily_publishing: List[Dict[str, Any]]
    topic_categories: List[Dict[str, Any]]
    source_distribution: List[Dict[str, Any]]
    editorial_score_trends: List[Dict[str, Any]]
    rejection_reasons: List[Dict[str, Any]]
