from pydantic import BaseModel, EmailStr
from typing import List, Optional

class DeckOut(BaseModel):
    id: str
    generated: bool
    sent: bool
    file_name: Optional[str] = None
    url: Optional[str] = None
    last_edited: Optional[str] = None
    class Config: from_attributes = True

class EmailStepOut(BaseModel):
    id: str
    step_order: int
    subject: str
    body: str
    sent: bool
    sent_at: Optional[str] = None
    class Config: from_attributes = True

class ProspectCreate(BaseModel):
    company: str
    owner_name: str
    email: EmailStr
    phone: Optional[str] = None
    revenue_range: str
    signals: List[str] = []
    notes: Optional[str] = None

class ProspectOut(BaseModel):
    id: str
    company: str
    owner_name: str
    email: EmailStr
    phone: Optional[str]
    revenue_range: str
    signals: List[str]
    notes: Optional[str]
    deck: Optional[DeckOut] = None
    emails: List[EmailStepOut] = []
    class Config: from_attributes = True
