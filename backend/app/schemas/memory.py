from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict

class MemoryItemCreate(BaseModel):
    memory_type: str = Field(default="POST", description="Type of memory: POST, REJECTED, PREFERENCE, STYLE, REASONING")
    category: str = Field(default="general")
    content: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    importance: float = 1.0

class MemoryItemResponse(BaseModel):
    id: str
    memory_type: str
    category: str
    content: str
    metadata: Dict[str, Any]
    importance: float
    access_count: int
    last_accessed_at: Optional[str] = None
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MemoryQueryRequest(BaseModel):
    query: str
    memory_types: Optional[List[str]] = None
    limit: int = 5
    similarity_threshold: Optional[float] = 0.5

class MemoryQueryResponse(BaseModel):
    query: str
    matches: List[Dict[str, Any]]
    total_found: int

class MemoryStatsResponse(BaseModel):
    total_memories: int
    by_type: Dict[str, int]
    top_accessed: List[Dict[str, Any]]
    last_updated: Optional[str] = None
