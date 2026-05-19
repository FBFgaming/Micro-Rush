"""Recall Memory — SQL-based storage for hard facts."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()


class MemoryFact(BaseModel):
    """A single factual memory."""

    id: int | None = None
    key: str
    value: str
    category: str  # e.g., "preference", "fact", "relationship"
    source: str | None = None  # Where this was learned
    created_at: datetime | None = None
    updated_at: datetime | None = None


class MemoryRecord(Base):
    """SQLAlchemy model for memory facts."""

    __tablename__ = "memory_facts"

    id = Column(Integer, primary_key=True)
    key = Column(String(255), nullable=False, index=True)
    value = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    source = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RecallMemory:
    """
    SQL-based memory for hard facts and preferences.

    Use Recall for:
    - User preferences (e.g., "coffee: black, no sugar")
    - Stated facts (e.g., "meeting with Dr. Smith at 3pm Thursday")
    - Relationships (e.g., "Alice is my manager")
    - Important dates and commitments
    """

    def __init__(self, db_path: str = "memory_recall.db"):
        self.engine = create_engine(f"sqlite+aiosqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def store(self, key: str, value: str, category: str = "fact", source: str | None = None) -> MemoryFact:
        """Store a new memory."""
        with self.Session() as session:
            record = MemoryRecord(
                key=key,
                value=value,
                category=category,
                source=source,
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return MemoryFact.model_validate(record)

    def recall(self, key: str) -> list[MemoryFact]:
        """Recall memories by exact key match."""
        with self.Session() as session:
            records = session.query(MemoryRecord).filter(MemoryRecord.key == key).all()
            return [MemoryFact.model_validate(r) for r in records]

    def search(self, query: str, category: str | None = None, limit: int = 10) -> list[MemoryFact]:
        """Search memories by content or category."""
        with self.Session() as session:
            q = session.query(MemoryRecord).filter(MemoryRecord.value.contains(query))
            if category:
                q = q.filter(MemoryRecord.category == category)
            records = q.limit(limit).all()
            return [MemoryFact.model_validate(r) for r in records]

    def forget(self, key: str) -> int:
        """Delete all memories matching a key."""
        with self.Session() as session:
            count = session.query(MemoryRecord).filter(MemoryRecord.key == key).delete()
            session.commit()
            return count


if __name__ == "__main__":
    print("💾 Recall Memory initialized")