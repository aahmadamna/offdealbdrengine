from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/prospects", tags=["prospects"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.ProspectOut)
def create_prospect(payload: schemas.ProspectCreate, db: Session = Depends(get_db)):
    p = models.Prospect(
        company=payload.company,
        owner_name=payload.owner_name,
        email=payload.email,
        phone=payload.phone,
        revenue_range=payload.revenue_range,
        notes=payload.notes,
    )
    p.signals = payload.signals
    db.add(p)
    db.flush()

    d = models.Deck(prospect_id=p.id)
    db.add(d)

    for i, subj in enumerate(["Intro and Context", "Buyers & Fit", "Next Steps"], start=1):
        db.add(models.EmailStep(
            prospect_id=p.id, step_order=i, subject=subj, body="", sent=False
        ))

    db.commit()
    db.refresh(p)
    return p

@router.get("", response_model=list[schemas.ProspectOut])
def list_prospects(db: Session = Depends(get_db)):
    return db.query(models.Prospect).all()
