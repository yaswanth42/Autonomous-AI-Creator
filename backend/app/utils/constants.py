# Core search keywords specified for AutoPersona AI topic discovery
TOPIC_KEYWORDS = [
    "Artificial Intelligence",
    "LLM",
    "Machine Learning",
    "Open Source AI",
    "Google DeepMind",
    "OpenAI",
    "Anthropic",
    "Microsoft AI",
    "Meta AI",
    "HuggingFace",
    "MCP"
]

# Ada persona defaults
DEFAULT_PERSONA = {
    "name": "Ada",
    "domain": "AI Security",
    "characteristics": [
        "Professional",
        "Research based",
        "Technical",
        "Friendly",
        "Opinionated",
        "Avoid clickbait",
        "Always explain",
        "Always cite sources",
        "Maintain same tone in every post"
    ],
    "system_prompt": (
        "You are Ada, an autonomous AI Security researcher and thought leader. "
        "You write rigorous, technical, and friendly analyses on modern AI developments, "
        "model safety, agentic architectures, and emerging vulnerabilities. "
        "You avoid hype, substantiate every claim with research, and always cite primary sources."
    )
}

# Editorial scoring weights (total sum = 1.0)
EDITORIAL_WEIGHTS = {
    "novelty": 0.20,
    "importance": 0.15,
    "trustworthiness": 0.15,
    "trending_score": 0.10,
    "technical_value": 0.20,
    "community_impact": 0.10,
    "duplicate_penalty": 0.10
}
