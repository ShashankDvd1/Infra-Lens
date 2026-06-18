"""
LandScope AI — SQLAlchemy Models for Projects, Sources, and AI Summaries.
"""

import uuid
from datetime import datetime, date
from sqlalchemy import (
    Column, String, Text, Float, Boolean, Date, DateTime,
    ForeignKey, Enum as SAEnum, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from pgvector.sqlalchemy import Vector

from app.db.session import Base


# --- Enums ---

import enum


class ProjectType(str, enum.Enum):
    METRO = "metro"
    EXPRESSWAY = "expressway"
    RING_ROAD = "ring_road"
    IT_CITY = "it_city"
    IT_PARK = "it_park"
    WELLNESS_CITY = "wellness_city"
    TOWNSHIP = "township"
    LOGISTICS_PARK = "logistics_park"
    GOVT_HOUSING = "govt_housing"
    LDA = "lda"
    AWAS_VIKAS = "awas_vikas"
    FLYOVER = "flyover"
    BRIDGE = "bridge"
    OTHER = "other"


class ProjectStatus(str, enum.Enum):
    ANNOUNCED = "announced"
    APPROVED = "approved"
    UNDER_CONSTRUCTION = "under_construction"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


class SourceType(str, enum.Enum):
    GOVERNMENT_NOTIFICATION = "government_notification"
    AUTHORITY_WEBSITE = "authority_website"
    NEWS_ARTICLE = "news_article"
    TENDER_DOCUMENT = "tender_document"
    MASTER_PLAN = "master_plan"
    RERA_LISTING = "rera_listing"


class VerificationStatus(str, enum.Enum):
    VERIFIED = "verified"
    PARTIALLY_VERIFIED = "partially_verified"
    UNVERIFIED = "unverified"


# --- Models ---


class Project(Base):
    """Infrastructure project tracked by the platform."""

    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(500), nullable=False, index=True)
    slug = Column(String(500), unique=True, nullable=False, index=True)
    project_type = Column(SAEnum(ProjectType), nullable=False, index=True)
    status = Column(SAEnum(ProjectStatus), nullable=False, index=True)
    description = Column(Text, nullable=True)
    location = Column(Geometry("POINT", srid=4326), nullable=True)
    boundary = Column(Geometry("POLYGON", srid=4326), nullable=True)
    city = Column(String(100), nullable=False, default="Lucknow", index=True)
    district = Column(String(100), nullable=True)
    authority = Column(String(200), nullable=True)
    announced_date = Column(Date, nullable=True)
    expected_completion = Column(Date, nullable=True)
    budget_crore = Column(Float, nullable=True)
    impact_radius_km = Column(Float, nullable=True, default=5.0)
    confidence_score = Column(Float, nullable=True, default=0.0)
    verification_status = Column(
        SAEnum(VerificationStatus),
        nullable=False,
        default=VerificationStatus.UNVERIFIED,
    )
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sources = relationship("Source", back_populates="project", cascade="all, delete-orphan")
    ai_summaries = relationship("AISummary", back_populates="project", cascade="all, delete-orphan")
    embeddings = relationship("ProjectEmbedding", back_populates="project", cascade="all, delete-orphan")

    # Full-text search vector (populated via trigger)
    # search_vector = Column(TSVectorType('name', 'description'))

    __table_args__ = (
        Index("ix_projects_city_type_status", "city", "project_type", "status"),
        Index("ix_projects_location", "location", postgresql_using="gist"),
    )

    def __repr__(self):
        return f"<Project(name='{self.name}', type='{self.project_type}', status='{self.status}')>"


class Source(Base):
    """Source document or reference for a project."""

    __tablename__ = "sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    source_type = Column(SAEnum(SourceType), nullable=False)
    title = Column(String(500), nullable=False)
    url = Column(String(2000), nullable=True)
    authority_name = Column(String(200), nullable=True)
    published_date = Column(Date, nullable=True)
    content_text = Column(Text, nullable=True)  # Extracted text for RAG
    is_active = Column(Boolean, default=True)
    last_checked = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="sources")
    embeddings = relationship("SourceEmbedding", back_populates="source", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_sources_project_id", "project_id"),
    )

    def __repr__(self):
        return f"<Source(title='{self.title}', type='{self.source_type}')>"


class AISummary(Base):
    """AI-generated summary for a project."""

    __tablename__ = "ai_summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    what_is_being_built = Column(Text, nullable=True)
    why_it_matters = Column(Text, nullable=True)
    expected_impact = Column(Text, nullable=True)
    nearby_benefiting_areas = Column(Text, nullable=True)
    model_used = Column(String(100), nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="ai_summaries")

    def __repr__(self):
        return f"<AISummary(project_id='{self.project_id}', model='{self.model_used}')>"


class Area(Base):
    """Geographic area / locality for intelligence reporting."""

    __tablename__ = "areas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False, index=True)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    city = Column(String(100), nullable=False, default="Lucknow", index=True)
    centroid = Column(Geometry("POINT", srid=4326), nullable=True)
    boundary = Column(Geometry("POLYGON", srid=4326), nullable=True)
    avg_price_sqft = Column(Float, nullable=True)
    growth_rate_pct = Column(Float, nullable=True)
    connectivity_data = Column(JSONB, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    growth_indicators = relationship("GrowthIndicator", back_populates="area", cascade="all, delete-orphan")
    embeddings = relationship("AreaEmbedding", back_populates="area", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_areas_centroid", "centroid", postgresql_using="gist"),
    )

    def __repr__(self):
        return f"<Area(name='{self.name}', city='{self.city}')>"


class GrowthIndicator(Base):
    """Growth metric for an area."""

    __tablename__ = "growth_indicators"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    area_id = Column(UUID(as_uuid=True), ForeignKey("areas.id", ondelete="CASCADE"), nullable=False)
    indicator_type = Column(String(100), nullable=False)  # e.g., "price_appreciation", "project_count"
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=True)  # e.g., "%", "count", "₹/sqft"
    measured_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    area = relationship("Area", back_populates="growth_indicators")

    def __repr__(self):
        return f"<GrowthIndicator(area_id='{self.area_id}', type='{self.indicator_type}')>"


# --- Vector Embedding Tables ---


class ProjectEmbedding(Base):
    """Vector embeddings for project semantic search."""

    __tablename__ = "project_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)  # The text that was embedded
    embedding = Column(Vector(768), nullable=False)  # bge-base-en-v1.5 = 768 dims
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="embeddings")

    __table_args__ = (
        Index("ix_project_embeddings_vector", "embedding",
              postgresql_using="ivfflat",
              postgresql_with={"lists": 100},
              postgresql_ops={"embedding": "vector_cosine_ops"}),
    )


class SourceEmbedding(Base):
    """Vector embeddings for source document chunks (RAG)."""

    __tablename__ = "source_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(Float, nullable=False, default=0)  # Position within document
    content = Column(Text, nullable=False)  # The chunk text
    embedding = Column(Vector(768), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    source = relationship("Source", back_populates="embeddings")

    __table_args__ = (
        Index("ix_source_embeddings_vector", "embedding",
              postgresql_using="ivfflat",
              postgresql_with={"lists": 100},
              postgresql_ops={"embedding": "vector_cosine_ops"}),
    )


class AreaEmbedding(Base):
    """Vector embeddings for area semantic search."""

    __tablename__ = "area_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    area_id = Column(UUID(as_uuid=True), ForeignKey("areas.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(768), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    area = relationship("Area", back_populates="embeddings")

    __table_args__ = (
        Index("ix_area_embeddings_vector", "embedding",
              postgresql_using="ivfflat",
              postgresql_with={"lists": 100},
              postgresql_ops={"embedding": "vector_cosine_ops"}),
    )
