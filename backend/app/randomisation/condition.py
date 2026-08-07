"""Server-side, stratified, minimisation-based condition assignment.

This cannot live client-side — see ARCHITECTURE.md #7 and
docs/10-tech-stack-and-system-design.md. Assigns each new session to whichever
condition currently has the fewest participants within that recruitment
channel, breaking ties randomly. Keeps cells balanced without becoming
predictable.
"""

import random

from sqlalchemy import func, select
from sqlalchemy.orm import Session as OrmSession

from app.models.research import Condition, RecruitmentChannel
from app.models.research import Session as SessionModel


def assign_condition(db: OrmSession, channel: RecruitmentChannel) -> Condition:
    rows = db.execute(
        select(SessionModel.condition, func.count())
        .join(SessionModel.participant)
        .where(SessionModel.participant.has(recruitment_channel=channel))
        .group_by(SessionModel.condition)
    ).all()

    tally = {c: 0 for c in Condition}
    tally.update({c: n for c, n in rows})

    fewest = min(tally.values())
    candidates = [c for c, n in tally.items() if n == fewest]
    return random.choice(candidates)
