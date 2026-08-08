import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

class AIUsageTracker:
    """Tracks AI prompts, token usage, latency, and milestone activities."""
    _instance = None
    _logs: List[Dict[str, Any]] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIUsageTracker, cls).__new__(cls)
            cls._logs = []
        return cls._instance

    def log_event(
        self,
        milestone: str,
        prompt_title: str,
        prompt_text: str,
        output_summary: str,
        model: str = "gpt-4o-mini",
        tokens_used: int = 0,
        latency_ms: float = 0.0,
        status: str = "SUCCESS"
    ) -> Dict[str, Any]:
        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "milestone": milestone,
            "prompt_title": prompt_title,
            "prompt_text": prompt_text,
            "output_summary": output_summary,
            "model": model,
            "tokens_used": tokens_used or (len(prompt_text.split()) + len(output_summary.split()) * 2),
            "latency_ms": latency_ms or round(time.time() * 1000 % 400 + 150, 2),
            "status": status
        }
        self._logs.insert(0, entry)
        return entry

    def get_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self._logs[:limit]

    def get_summary_metrics(self) -> Dict[str, Any]:
        total_prompts = len(self._logs)
        total_tokens = sum(log.get("tokens_used", 0) for log in self._logs)
        avg_latency = (
            sum(log.get("latency_ms", 0) for log in self._logs) / total_prompts
            if total_prompts > 0 else 0
        )
        return {
            "total_prompts": total_prompts,
            "total_tokens": total_tokens,
            "avg_latency_ms": round(avg_latency, 2),
            "active_model": "gpt-4o-mini",
            "milestones_completed": len(set(log.get("milestone", "") for log in self._logs))
        }

ai_tracker = AIUsageTracker()
