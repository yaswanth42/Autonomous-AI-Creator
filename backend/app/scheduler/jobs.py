import time
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.core.logging import logger
from app.core.ai_tracker import ai_tracker
from app.services.topic_discovery import TopicDiscoveryService
from app.services.editorial_engine import EditorialDecisionEngine
from app.services.post_generator import PostGeneratorService
from app.services.persona_engine import PersonaEngine
from app.agents.graph import create_persona_graph
from app.memory.breeth_engine import BreethMemoryEngine

def execute_autonomous_cycle() -> Dict[str, Any]:
    """
    Executes the complete autonomous 4-hour cycle:
    Search -> Editorial Review -> Memory Check -> Generate Post -> Store -> Publish internally -> Sleep
    """
    start_time = time.time()
    logger.info("==================================================")
    logger.info("Starting Autonomous AI Persona Cycle (Ada)...")
    logger.info("==================================================")

    db: Session = SessionLocal()
    cycle_summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "topics_discovered": 0,
        "topics_evaluated": 0,
        "posts_published": 0,
        "topics_rejected": 0,
        "published_titles": [],
        "rejection_reasons": [],
        "status": "COMPLETED",
        "duration_seconds": 0.0
    }

    try:
        topic_service = TopicDiscoveryService(db)
        editorial_engine = EditorialDecisionEngine(db)
        post_generator = PostGeneratorService(db)
        memory_engine = BreethMemoryEngine(db)

        # 1. Search / Topic Discovery
        logger.info("1. Discovering live AI & security topics via Tavily...")
        topics = topic_service.discover_latest_topics(max_total=5, filter_duplicates=True)
        cycle_summary["topics_discovered"] = len(topics)

        if not topics:
            logger.info("No new unique topics found in this cycle. Sleeping.")
            cycle_summary["status"] = "NO_NEW_TOPICS"
            return cycle_summary

        # Create LangGraph workflow instance
        def post_gen_wrapper(top, eval_res):
            post = post_generator.generate_post(top, eval_res)
            return {
                "generated_post_id": post.id,
                "draft_title": post.title,
                "raw_markdown": post.raw_markdown,
                "rationale": post.rationale,
                "sources": post.sources
            }

        graph_app = create_persona_graph(
            post_generator_fn=post_gen_wrapper,
            memory_engine_fn=lambda: memory_engine
        )

        # 2. Process candidate topics
        for topic in topics:
            cycle_summary["topics_evaluated"] += 1
            logger.info(f"2. Editorial Review for: '{topic.get('title')}'")

            # 3. Editorial Evaluation (checks Breeth Memory internally)
            editorial_eval = editorial_engine.evaluate_topic(
                title=topic.get("title", ""),
                content=topic.get("content", ""),
                url=topic.get("url"),
                source=topic.get("source", "Tavily")
            )

            if editorial_eval["decision"] == "REJECT":
                logger.info(f"-> REJECTED: {editorial_eval['reasoning']}")
                cycle_summary["topics_rejected"] += 1
                cycle_summary["rejection_reasons"].append({
                    "title": topic.get("title"),
                    "reason": editorial_eval["reasoning"],
                    "score": editorial_eval["total_score"]
                })
                continue

            # 4. LangGraph Autonomous Generation & Publishing
            logger.info(f"-> APPROVED (Score: {editorial_eval['total_score']}). Invoking LangGraph Persona Graph...")
            
            initial_state = {
                "topic": topic,
                "editorial_eval": editorial_eval,
                "persona_name": "Ada",
                "status": "START"
            }
            
            graph_result = graph_app.invoke(initial_state)
            
            if graph_result.get("status") == "COMPLETED" or graph_result.get("generated_post_id"):
                cycle_summary["posts_published"] += 1
                cycle_summary["published_titles"].append(topic.get("title"))
                logger.info(f"-> Published post internally: '{topic.get('title')}'")

                # Limit to 1 post per scheduled cycle to maintain high editorial standard
                break

        # Log to Breeth Memory publishing history
        memory_engine.store_publishing_history(
            summary_text=f"Cycle executed: Discovered {cycle_summary['topics_discovered']}, Evaluated {cycle_summary['topics_evaluated']}, Published {cycle_summary['posts_published']}, Rejected {cycle_summary['topics_rejected']}."
        )

    except Exception as e:
        logger.error(f"Error during autonomous scheduler cycle: {e}", exc_info=True)
        cycle_summary["status"] = "ERROR"
        cycle_summary["error"] = str(e)
    finally:
        db.close()
        duration = round(time.time() - start_time, 2)
        cycle_summary["duration_seconds"] = duration
        logger.info(f"Cycle completed in {duration}s. Published: {cycle_summary['posts_published']}, Rejected: {cycle_summary['topics_rejected']}.")

    return cycle_summary
