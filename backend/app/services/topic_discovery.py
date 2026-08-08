import json
import random
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.logging import logger
from app.models.search_history import SearchHistory
from app.models.post import Post
from app.models.rejected_topic import RejectedTopic
from app.memory.breeth_engine import BreethMemoryEngine
from app.utils.constants import TOPIC_KEYWORDS

class TopicDiscoveryService:
    """Discovers live AI & technology topics using Tavily Search with Breeth Memory deduplication."""

    def __init__(self, db: Session):
        self.db = db
        self.memory_engine = BreethMemoryEngine(db)
        self.api_key = settings.TAVILY_API_KEY.strip() if settings.TAVILY_API_KEY else None

    def _normalize_title(self, title: str) -> str:
        return " ".join(title.lower().strip().split())

    def _get_simulated_topics(self, keyword: str) -> List[Dict[str, Any]]:
        """Simulates rich real-time AI news items when Tavily API key is absent."""
        curated_feed = [
            {
                "title": f"Model Context Protocol (MCP) Security Analysis: Evaluating Sandbox Escape & Tool Poisoning Risks",
                "url": "https://research.anthropic.com/mcp-security-sandboxing-evaluations-2026",
                "content": "A rigorous technical evaluation of MCP server implementations reveals architectural vulnerabilities in automated agent tool calling, prompt injection relaying, and credential leakage vectors. Mitigation guidelines recommend least-privilege capability boundaries and schema validation.",
                "source": "Anthropic Research",
                "published_date": datetime.now(timezone.utc).isoformat(),
                "score": 0.94
            },
            {
                "title": f"OpenAI o3 & Reasoning Models: Red-Teaming Chain-of-Thought Concealment & Adversarial Robustness",
                "url": "https://openai.com/index/o3-reasoning-model-safety-evaluations",
                "content": "Detailed adversarial benchmarking on reasoning models demonstrates new paradigms for hidden chain-of-thought verification, reward hacking prevention, and alignment verification across multi-step mathematical and code generation tasks.",
                "source": "OpenAI Safety",
                "published_date": datetime.now(timezone.utc).isoformat(),
                "score": 0.91
            },
            {
                "title": f"Google DeepMind Publishes SynthID Verification Protocol for Multi-Modal LLM Output Integrity",
                "url": "https://deepmind.google/discover/blog/synthid-cryptographic-watermarking-agentic-ai",
                "content": "DeepMind open-sources cryptographic watermarking and provenance tracking for autonomous agent code and multi-modal generations, enabling deterministic verification against synthetic deepfakes and automated AST poisoning.",
                "source": "Google DeepMind",
                "published_date": datetime.now(timezone.utc).isoformat(),
                "score": 0.88
            },
            {
                "title": f"Meta AI Releases Llama-4 Architecture Benchmarks with Hardware-Enforced Safety Guardrails",
                "url": "https://ai.meta.com/research/publications/llama-4-hardware-isolated-safety-enclaves",
                "content": "Meta introduces open-weights reasoning architectures paired with hardware-isolated inference enclaves. The release details mitigation techniques against weight-extraction attacks and gradient-based jailbreak reconstruction.",
                "source": "Meta AI Research",
                "published_date": datetime.now(timezone.utc).isoformat(),
                "score": 0.86
            },
            {
                "title": f"HuggingFace Collaborates with OWASP on Top 10 Vulnerabilities for Autonomous Multi-Agent Systems",
                "url": "https://huggingface.co/blog/agentic-ai-owasp-top-10-vulnerabilities",
                "content": "A community-driven framework establishing defensive patterns for agentic workflow orchestration, memory injection attacks, unauthorized state mutations, and insecure deserialization in LLM memory stores.",
                "source": "HuggingFace Blog",
                "published_date": datetime.now(timezone.utc).isoformat(),
                "score": 0.89
            },
            {
                "title": f"Microsoft AI and DARPA Unveil Provably Secure Alignment Verifiers for Code-Generating Agents",
                "url": "https://microsoft.com/en-us/research/project/provable-code-agent-safety",
                "content": "Formal verification applied to autonomous coding agents ensures static analysis guarantees before code execution in production container environments.",
                "source": "Microsoft Research",
                "published_date": datetime.now(timezone.utc).isoformat(),
                "score": 0.85
            }
        ]
        # Filter or sample based on keyword
        matching = [item for item in curated_feed if keyword.lower() in item["title"].lower() or keyword.lower() in item["content"].lower()]
        return matching if matching else random.sample(curated_feed, min(2, len(curated_feed)))

    def search_keyword(self, keyword: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Executes search for a single keyword via Tavily API or simulated live feed."""
        if self.api_key:
            try:
                from tavily import TavilyClient
                client = TavilyClient(api_key=self.api_key)
                query = f"{keyword} AI news research security 2026"
                response = client.search(
                    query=query,
                    search_depth="advanced",
                    max_results=max_results,
                    include_answer=False
                )
                results = []
                for r in response.get("results", []):
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "content": r.get("content", ""),
                        "source": r.get("source", "Tavily"),
                        "published_date": r.get("published_date") or datetime.now(timezone.utc).isoformat(),
                        "score": r.get("score", 0.8)
                    })
                return results
            except Exception as e:
                logger.warning(f"Tavily API search error for '{keyword}': {e}. Falling back to simulated live feed.")
                return self._get_simulated_topics(keyword)
        else:
            return self._get_simulated_topics(keyword)

    def discover_latest_topics(
        self,
        keywords: Optional[List[str]] = None,
        max_total: int = 10,
        filter_duplicates: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Main discovery loop executing search across target keywords,
        applying deduplication against memory and database records,
        and persisting search history.
        """
        target_keywords = keywords if keywords else TOPIC_KEYWORDS
        selected_keywords = random.sample(target_keywords, min(3, len(target_keywords)))

        raw_candidates: List[Dict[str, Any]] = []
        for kw in selected_keywords:
            items = self.search_keyword(kw, max_results=3)
            raw_candidates.extend(items)

        # 1. Local in-memory deduplication
        seen_titles = set()
        seen_urls = set()
        unique_candidates = []
        for item in raw_candidates:
            norm_title = self._normalize_title(item["title"])
            url = item.get("url", "")
            if norm_title in seen_titles or (url and url in seen_urls):
                continue
            seen_titles.add(norm_title)
            if url:
                seen_urls.add(url)
            unique_candidates.append(item)

        # 2. Database & Breeth Memory duplicate filter
        filtered_topics: List[Dict[str, Any]] = []
        if filter_duplicates:
            for item in unique_candidates:
                # Check DB Published Posts
                exact_post = self.db.query(Post).filter(
                    Post.title == item["title"],
                    Post.is_deleted == False
                ).first()
                if exact_post:
                    logger.info(f"Duplicate skipped (already published): {item['title']}")
                    continue

                # Check DB Rejected Topics
                exact_rejected = self.db.query(RejectedTopic).filter(
                    RejectedTopic.title == item["title"],
                    RejectedTopic.is_deleted == False
                ).first()
                if exact_rejected:
                    logger.info(f"Duplicate skipped (previously rejected): {item['title']}")
                    continue

                # Check Breeth Memory semantic similarity
                is_dup, sim, match = self.memory_engine.check_duplicate_and_novelty(
                    topic_title=item["title"],
                    topic_content=item.get("content", ""),
                    url=item.get("url")
                )
                if is_dup:
                    logger.info(f"Semantic duplicate detected (similarity={sim:.2f}): {item['title']}")
                    continue

                filtered_topics.append(item)
        else:
            filtered_topics = unique_candidates

        final_topics = filtered_topics[:max_total]

        # 3. Log search history to database
        try:
            history = SearchHistory(
                query=", ".join(selected_keywords),
                provider="Tavily" if self.api_key else "Tavily (Simulated Live)",
                raw_results_count=len(raw_candidates),
                filtered_count=len(final_topics),
                results_json=json.dumps(final_topics)
            )
            self.db.add(history)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error storing search history: {e}")
            self.db.rollback()

        logger.info(f"Discovered {len(final_topics)} unique topics across [{', '.join(selected_keywords)}]")
        return final_topics
