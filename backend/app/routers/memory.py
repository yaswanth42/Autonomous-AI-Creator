from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.memory import MemoryItemCreate, MemoryItemResponse, MemoryQueryRequest, MemoryQueryResponse, MemoryStatsResponse
from app.services.memory_service import MemoryService
from app.models.memory import Memory

router = APIRouter(prefix="/api/memory", tags=["Breeth Memory"])

@router.get("/stats", response_model=MemoryStatsResponse)
def get_memory_stats(db: Session = Depends(get_db)):
    """Returns Breeth Memory size, categories, and top accessed nodes."""
    svc = MemoryService(db)
    stats = svc.get_stats()
    return MemoryStatsResponse(
        total_memories=stats["total_memories"],
        by_type=stats["by_type"],
        top_accessed=stats["top_accessed"]
    )

@router.get("/items", response_model=List[MemoryItemResponse])
def get_memory_items(
    memory_type: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lists all cognitive memory items."""
    q = db.query(Memory).filter(Memory.is_deleted == False)
    if memory_type:
        q = q.filter(Memory.memory_type == memory_type.upper())
    items = q.order_by(Memory.created_at.desc()).limit(limit).all()
    return [i.to_dict() for i in items]

@router.post("/query", response_model=MemoryQueryResponse)
def query_breeth_memory(request: MemoryQueryRequest, db: Session = Depends(get_db)):
    """Semantic vector query against Breeth Memory."""
    svc = MemoryService(db)
    matches = svc.query_memories(
        query=request.query,
        memory_types=request.memory_types,
        limit=request.limit,
        min_similarity=request.similarity_threshold or 0.1
    )
    return MemoryQueryResponse(
        query=request.query,
        matches=matches,
        total_found=len(matches)
    )

@router.post("/item", response_model=MemoryItemResponse)
def add_memory_item(item: MemoryItemCreate, db: Session = Depends(get_db)):
    """Manually inserts an item into Breeth Memory."""
    svc = MemoryService(db)
    mem = svc.engine.store(
        memory_type=item.memory_type,
        category=item.category,
        content=item.content,
        metadata=item.metadata,
        importance=item.importance
    )
    return mem.to_dict()
