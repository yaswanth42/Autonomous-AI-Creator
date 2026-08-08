import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, declared_attr

class Base(DeclarativeBase):
    pass

class UUIDMixin:
    @declared_attr
    def id(cls):
        return Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
            nullable=False
        )

class SoftDeleteMixin:
    @declared_attr
    def is_deleted(cls):
        return Column(Boolean, default=False, nullable=False, index=True)

    @declared_attr
    def deleted_at(cls):
        return Column(DateTime, nullable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)
