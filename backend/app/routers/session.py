"""Session lifecycle: create (with server-side condition assignment), ingest
responses, and mark complete. See docs/10-tech-stack-and-system-design.md
§"Endpoints".
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession

from app.database import get_research_db
from app.models.research import Participant, Response
from app.models.research import Session as SessionModel
from app.randomisation.condition import assign_condition
from app.schemas import (
    ResponseBatchIn,
    SessionCompleteRequest,
    SessionCreateRequest,
    SessionCreateResponse,
)

router = APIRouter(prefix="/session", tags=["session"])


@router.post("", response_model=SessionCreateResponse, status_code=201)
def create_session(
    payload: SessionCreateRequest, db: OrmSession = Depends(get_research_db)
) -> SessionCreateResponse:
    if not payload.consent_research:
        raise HTTPException(status_code=422, detail="Research consent is required.")

    participant = Participant(
        recruitment_channel=payload.recruitment_channel,
        consent_version=payload.consent_version,
        consent_research=payload.consent_research,
        consent_open_data=payload.consent_open_data,
    )
    db.add(participant)
    db.flush()  # populate participant_code before use below

    condition = assign_condition(db, payload.recruitment_channel)

    session = SessionModel(
        participant_code=participant.participant_code,
        condition=condition,
        device_type=payload.device_type,
        input_method=payload.input_method,
        viewport_width=payload.viewport_width,
        module_order=[],
    )
    db.add(session)
    db.commit()

    return SessionCreateResponse(
        session_id=session.session_id,
        participant_code=participant.participant_code,
        condition=condition,
    )


@router.post("/{session_id}/responses", status_code=204)
def ingest_responses(
    session_id: str, batch: ResponseBatchIn, db: OrmSession = Depends(get_research_db)
) -> None:
    session = db.get(SessionModel, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    for item in batch.responses:
        db.add(
            Response(
                session_id=session_id,
                module_code=item.module_code,
                item_id=item.item_id,
                item_bank_version=item.item_bank_version,
                position_in_module=item.position_in_module,
                response_payload=item.response_payload,
                latency_ms=item.latency_ms,
                timed_out=item.timed_out,
                focus_lost=item.focus_lost,
                revisions=item.revisions,
            )
        )
    db.commit()


@router.post("/{session_id}/complete", status_code=204)
def complete_session(
    session_id: str, payload: SessionCompleteRequest, db: OrmSession = Depends(get_research_db)
) -> None:
    session = db.get(SessionModel, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    session.completed_at = datetime.utcnow()
    session.completed = payload.abandoned_at_module is None
    session.abandoned_at_module = payload.abandoned_at_module
    db.commit()
