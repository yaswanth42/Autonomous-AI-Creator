from datetime import datetime, timezone
from typing import Dict, Any, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.core.config import settings
from app.core.logging import logger
from app.scheduler.jobs import execute_autonomous_cycle

class SchedulerService:
    """Manages APScheduler background execution for autonomous cycles."""
    _instance = None
    scheduler: Optional[BackgroundScheduler] = None
    is_running: bool = False
    last_run_time: Optional[str] = None
    last_run_result: Optional[Dict[str, Any]] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SchedulerService, cls).__new__(cls)
            cls.scheduler = BackgroundScheduler(daemon=True)
            cls.is_running = False
            cls.last_run_time = None
            cls.last_run_result = None
        return cls._instance

    def _scheduled_job_wrapper(self):
        logger.info("Triggering scheduled autonomous cycle...")
        result = execute_autonomous_cycle()
        SchedulerService.last_run_time = datetime.now(timezone.utc).isoformat()
        SchedulerService.last_run_result = result

    def start(self):
        if not self.is_running and self.scheduler:
            try:
                # Add 4-hour recurring cycle
                self.scheduler.add_job(
                    self._scheduled_job_wrapper,
                    trigger=IntervalTrigger(hours=settings.SCHEDULER_INTERVAL_HOURS),
                    id="autonomous_cycle_job",
                    name="Autonomous 4-Hour Post Generation Cycle",
                    replace_existing=True
                )
                self.scheduler.start()
                self.is_running = True
                logger.info(f"APScheduler started. Autonomous cycle scheduled every {settings.SCHEDULER_INTERVAL_HOURS} hours.")
            except Exception as e:
                logger.error(f"Failed to start APScheduler: {e}")

    def shutdown(self):
        if self.is_running and self.scheduler:
            try:
                self.scheduler.shutdown(wait=False)
                self.is_running = False
                logger.info("APScheduler stopped.")
            except Exception as e:
                logger.error(f"Error shutting down scheduler: {e}")

    def pause(self):
        if self.is_running and self.scheduler:
            try:
                self.scheduler.pause()
                logger.info("APScheduler paused.")
            except Exception as e:
                logger.error(f"Error pausing scheduler: {e}")

    def resume(self):
        if self.is_running and self.scheduler:
            try:
                self.scheduler.resume()
                logger.info("APScheduler resumed.")
            except Exception as e:
                logger.error(f"Error resuming scheduler: {e}")

    def trigger_now(self) -> Dict[str, Any]:
        """Manually runs one complete autonomous cycle immediately."""
        logger.info("Manual trigger requested for autonomous cycle.")
        result = execute_autonomous_cycle()
        self.last_run_time = datetime.now(timezone.utc).isoformat()
        self.last_run_result = result
        return result

    def get_status(self) -> Dict[str, Any]:
        next_run = None
        if self.is_running and self.scheduler:
            job = self.scheduler.get_job("autonomous_cycle_job")
            if job and job.next_run_time:
                next_run = job.next_run_time.isoformat()

        return {
            "is_running": self.is_running,
            "cadence_hours": settings.SCHEDULER_INTERVAL_HOURS,
            "next_run_time": next_run,
            "last_run_time": self.last_run_time,
            "last_run_result": self.last_run_result,
            "active_jobs_count": len(self.scheduler.get_jobs()) if self.scheduler else 0
        }

scheduler_service = SchedulerService()
