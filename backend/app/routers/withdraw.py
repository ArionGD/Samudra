"""Withdrawal / deletion on request.

docs/10-tech-stack-and-system-design.md is explicit: "`/withdraw` performs a
real delete, not a flag. Test this before launch." This performs a real
delete of responses, reading-baseline rows, and quality flags, then removes
the session and participant rows. Nothing about this participant survives
except an implicit gap in the ID sequence.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete
from sqlalchemy.orm import Session as OrmSession

from app.database import get_research_db
from app.models.research import Participant, QualityFlag, ReadingBaseline, Response
from app.models.research import Session as SessionModel
from app.schemas import WithdrawRequest

router = APIRouter(prefix="/withdraw", tags=["withdraw"])


@router.post("", status_code=204)
def withdraw(payload: WithdrawRequest, db: OrmSession = Depends(get_research_db)) -> None:
    participant = db.get(Participant, payload.participant_code)
    if participant is None:
        raise HTTPException(status_code=404, detail="Participant not found.")

    session_ids = [s.session_id for s in participant.sessions]

    if session_ids:
        db.execute(delete(Response).where(Response.session_id.in_(session_ids)))
        db.execute(delete(ReadingBaseline).where(ReadingBaseline.session_id.in_(session_ids)))
        db.execute(delete(QualityFlag).where(QualityFlag.session_id.in_(session_ids)))
        db.execute(delete(SessionModel).where(SessionModel.session_id.in_(session_ids)))

    db.delete(participant)
    db.commit()
