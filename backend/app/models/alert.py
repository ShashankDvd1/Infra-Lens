from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db.session import Base

class AlertSubscription(Base):
    __tablename__ = "alert_subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Alert criteria
    area_slug = Column(String, nullable=True) # E.g., 'gomti-nagar'
    project_type = Column(String, nullable=True) # E.g., 'commercial'
    min_opportunity_score = Column(Integer, nullable=True, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User")
