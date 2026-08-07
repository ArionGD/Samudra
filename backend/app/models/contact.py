"""Contact-store model. Physically separate database from the research store.

Holds only what's needed to deliver results by email. No link to
`participant_code` is persisted here — see ARCHITECTURE.md #4. If a
persistent link is ever genuinely required, it belongs in a third, minimal,
access-restricted store, never in either primary database.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import ContactBase


def _uuid() -> str:
    return str(uuid.uuid4())


class Contact(ContactBase):
    __tablename__ = "contacts"

    contact_id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    email: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    delivered: Mapped[bool] = mapped_column(Boolean, default=False)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
