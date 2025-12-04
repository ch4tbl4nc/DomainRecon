# =============================================================================
# DomainRecon - Modèles SQLAlchemy
# =============================================================================

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from .database import Base


class Scan(Base):
    """Table des scans de domaines."""
    
    __tablename__ = "scans"
    
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)
    security_headers = Column(JSON, nullable=True)
    whois_data = Column(JSON, nullable=True)
    scan_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(50), default="success", nullable=False)
    error_message = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Scan(id={self.id}, domain='{self.domain}')>"
