from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base
import uuid

def uid(): return str(uuid.uuid4())

class Prospect(Base):
    __tablename__ = "prospects"
    id = Column(String, primary_key=True, default=uid)
    company = Column(String, nullable=False)
    owner_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    revenue_range = Column(String, nullable=False)
    signals_csv = Column(Text, default="")
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    deck = relationship("Deck", back_populates="prospect", uselist=False, cascade="all,delete-orphan")
    emails = relationship("EmailStep", back_populates="prospect", order_by="EmailStep.step_order", cascade="all,delete-orphan")

    @property
    def signals(self):
        return [s for s in (self.signals_csv or "").split(",") if s.strip()]

    @signals.setter
    def signals(self, values):
        self.signals_csv = ",".join(v.strip() for v in (values or []))

class Deck(Base):
    __tablename__ = "decks"
    id = Column(String, primary_key=True, default=uid)
    prospect_id = Column(String, ForeignKey("prospects.id", ondelete="CASCADE"), unique=True, nullable=False)
    generated = Column(Boolean, default=False)
    sent = Column(Boolean, default=False)
    file_name = Column(String)
    url = Column(String)
    last_edited = Column(DateTime)
    prospect = relationship("Prospect", back_populates="deck")

class EmailStep(Base):
    __tablename__ = "email_steps"
    __table_args__ = (UniqueConstraint("prospect_id", "step_order", name="uq_email_steps_prospect_order"),)
    id = Column(String, primary_key=True, default=uid)
    prospect_id = Column(String, ForeignKey("prospects.id", ondelete="CASCADE"), nullable=False)
    step_order = Column(Integer, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    sent = Column(Boolean, default=False)
    sent_at = Column(DateTime)
    prospect = relationship("Prospect", back_populates="emails")
