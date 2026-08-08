import json
from typing import Dict, Any, Tuple, Optional, List
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.logging import logger
from app.models.rejected_topic import RejectedTopic
from app.models.editorial_history import EditorialHistory
from app.models.agent import Agent
from app.memory.breeth_engine import BreethMemoryEngine
from app.utils.constants import EDITORIAL_WEIGHTS, DEFAULT_PERSONA

class EditorialDecisionEngine:
    """
    Evaluates candidate topics against Ada's 7-factor editorial criteria,
    querying Breeth Memory first to enforce historical continuity and avoid duplicates.
    """

    def __init__(self, db: Session, threshold: float = settings.DEFAULT_EDITORIAL_THRESHOLD):
        self.db = db
        self.threshold = threshold
        self.memory_engine = BreethMemoryEngine(db)

    def _score_trustworthiness(self, source: str, url: str) -> float:
        trusted_domains = [
            "anthropic.com", "deepmind.google", "openai.com", "ai.meta.com",
            "microsoft.com", "huggingface.co", "arxiv.org", "owasp.org",
            "cve.mitre.org", "nist.gov", "github.com"
        ]
        url_lower = (url or "").lower()
        source_lower = (source or "").lower()
        
        for d in trusted_domains:
            if d in url_lower or d.split(".")[0] in source_lower:
                return 9.5
        if "research" in source_lower or "security" in source_lower or "ai" in source_lower:
            return 8.2
        return 6.0

    def _score_importance(self, title: str, content: str) -> float:
        high_impact_terms = [
            "security", "vulnerability", "jailbreak", "adversarial", "sandboxing",
            "mcp", "protocol", "alignment", "safety", "watermarking", "guardrail",
            "formal verification", "poisoning", "weights", "cve", "breach"
        ]
        text = f"{title} {content}".lower()
        matches = sum(1 for term in high_impact_terms if term in text)
        if matches >= 4:
            return 9.6
        elif matches >= 2:
            return 8.5
        elif matches == 1:
            return 7.2
        return 5.5

    def _score_technical_value(self, content: str) -> float:
        tech_indicators = [
            "benchmark", "architecture", "evaluation", "framework", "implementation",
            "latency", "api", "tokens", "mitigation", "cryptographic", "ast", "enclaves"
        ]
        text = content.lower()
        count = sum(1 for term in tech_indicators if term in text)
        return min(10.0, 6.0 + count * 0.8)

    def evaluate_topic(
        self,
        title: str,
        content: str,
        url: Optional[str] = None,
        source: str = "Tavily",
        custom_threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Executes complete 7-factor editorial evaluation.
        Always queries Breeth Memory before making final decision.
        """
        threshold = custom_threshold if custom_threshold is not None else self.threshold

        # 1. Query Breeth Memory for duplicate & novelty
        is_dup, dup_similarity, closest_mem = self.memory_engine.check_duplicate_and_novelty(
            topic_title=title,
            topic_content=content,
            url=url
        )

        # 2. Factor 1: Novelty (0-10)
        if is_dup:
            novelty = max(1.0, 10.0 - (dup_similarity * 10.0))
            duplicate_penalty = 8.5
        else:
            novelty = max(5.0, 10.0 - (dup_similarity * 6.0))
            duplicate_penalty = dup_similarity * 3.0

        # 3. Factor 2: Importance (0-10)
        importance = self._score_importance(title, content)

        # 4. Factor 3: Trustworthiness (0-10)
        trustworthiness = self._score_trustworthiness(source, url or "")

        # 5. Factor 4: Trending Score (0-10)
        trending_score = 8.4 if any(k in title.lower() for k in ["mcp", "reasoning", "llama", "deepmind", "openai"]) else 7.0

        # 6. Factor 5: Technical Value (0-10)
        technical_value = self._score_technical_value(content)

        # 7. Factor 6: Community Impact (0-10)
        community_impact = 8.2 if ("security" in title.lower() or "safety" in title.lower() or "open" in title.lower()) else 6.8

        # Weighted aggregate score
        raw_total = (
            EDITORIAL_WEIGHTS["novelty"] * novelty +
            EDITORIAL_WEIGHTS["importance"] * importance +
            EDITORIAL_WEIGHTS["trustworthiness"] * trustworthiness +
            EDITORIAL_WEIGHTS["trending_score"] * trending_score +
            EDITORIAL_WEIGHTS["technical_value"] * technical_value +
            EDITORIAL_WEIGHTS["community_impact"] * community_impact -
            EDITORIAL_WEIGHTS["duplicate_penalty"] * duplicate_penalty
        )
        total_score = round(max(0.0, min(10.0, raw_total)), 2)

        decision = "PUBLISH" if total_score >= threshold else "REJECT"

        scores = {
            "novelty": round(novelty, 2),
            "importance": round(importance, 2),
            "trustworthiness": round(trustworthiness, 2),
            "trending_score": round(trending_score, 2),
            "technical_value": round(technical_value, 2),
            "community_impact": round(community_impact, 2),
            "duplicate_penalty": round(duplicate_penalty, 2)
        }

        # Generate reasoning
        if decision == "PUBLISH":
            reasoning = (
                f"Approved for publication (Score: {total_score}/{threshold}). "
                f"High technical significance in AI Security (Importance={importance:.1f}, Technical Value={technical_value:.1f}). "
                f"Verified trustworthy research origin ({source}) with strong ecosystem relevance."
            )
        else:
            reasons = []
            if total_score < threshold:
                reasons.append(f"Aggregate score {total_score} below editorial cutoff {threshold}")
            if is_dup or duplicate_penalty > 5.0:
                reasons.append(f"High conceptual overlap with existing memory (similarity={dup_similarity:.2f})")
            if importance < 7.0:
                reasons.append("Insufficient technical depth or AI security impact")
            if trustworthiness < 7.0:
                reasons.append("Source credibility below rigorous peer-review baseline")
            reasoning = "Rejected by Editorial Engine: " + "; ".join(reasons)

        # Get active agent
        agent = self.db.query(Agent).filter(Agent.name == DEFAULT_PERSONA["name"], Agent.is_deleted == False).first()
        agent_id = agent.id if agent else None

        # Record decision
        if decision == "REJECT":
            rejected_entry = RejectedTopic(
                title=title,
                url=url,
                source=source,
                reason=reasoning,
                score_breakdown_json=json.dumps(scores),
                total_score=total_score,
                novelty=novelty,
                importance=importance,
                trustworthiness=trustworthiness,
                trending_score=trending_score,
                technical_value=technical_value,
                community_impact=community_impact,
                duplicate_penalty=duplicate_penalty
            )
            self.db.add(rejected_entry)
            self.db.commit()

            # Store in Breeth memory
            self.memory_engine.store_rejected_topic(
                topic_title=title,
                reason=reasoning,
                scores=scores,
                url=url
            )

        # Log to EditorialHistory table
        history = EditorialHistory(
            topic_title=title,
            topic_url=url,
            decision=decision,
            total_score=total_score,
            scores_json=json.dumps(scores),
            reasoning=reasoning,
            agent_id=agent_id
        )
        self.db.add(history)
        self.db.commit()

        logger.info(f"Editorial Engine evaluated '{title[:40]}...': {decision} (Score: {total_score})")

        return {
            "decision": decision,
            "total_score": total_score,
            "threshold": threshold,
            "scores": scores,
            "reasoning": reasoning,
            "topic_title": title,
            "topic_url": url,
            "agent_name": DEFAULT_PERSONA["name"]
        }
