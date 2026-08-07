"""Admin endpoints: monitoring only for now. Export pipeline lands separately
per docs/11-implementation-plan.md build order (step 10, before pilot).

Auth is a single shared API key for now — see ARCHITECTURE.md §11 "Open
architectural questions". Fine at N=0; revisit before any real deploy.
"""

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session as OrmSession

from app.config import settings
from app.database import get_research_db
from app.models.research import Participant
from app.models.research import Session as SessionModel

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(x_admin_key: str = Header(default="")) -> None:
    if x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=401, detail="Invalid admin key.")


@router.get("/monitor", dependencies=[Depends(require_admin)])
def monitor(db: OrmSession = Depends(get_research_db)) -> dict:
    """N per channel per condition, and overall completion rate.

    Per docs/05-recruitment-plan.md: monitor this weekly; do NOT look at trait
    score distributions or run hypothesis tests before collection is complete.
    """
    rows = db.execute(
        select(
            Participant.recruitment_channel,
            SessionModel.condition,
            func.count(),
        )
        .join(SessionModel, SessionModel.participant_code == Participant.participant_code)
        .group_by(Participant.recruitment_channel, SessionModel.condition)
    ).all()

    total = db.execute(select(func.count()).select_from(SessionModel)).scalar_one()
    completed = db.execute(
        select(func.count()).select_from(SessionModel).where(SessionModel.completed.is_(True))
    ).scalar_one()

    return {
        "n_by_channel_condition": [
            {"channel": channel, "condition": condition, "n": n}
            for channel, condition, n in rows
        ],
        "total_sessions": total,
        "completed_sessions": completed,
        "completion_rate": (completed / total) if total else None,
    }
