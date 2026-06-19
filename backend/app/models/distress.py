import uuid
from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class DistressProperty(Base):
    __tablename__ = "distress_properties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    location = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False, default="Lucknow")
    property_type = Column(String(100), nullable=False)  # "Bank Auction" or "Distress Sale"
    market_value = Column(Float, nullable=False)
    reserve_price = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    auction_date = Column(String(100), nullable=True)
    backing_authority = Column(String(200), nullable=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project")
