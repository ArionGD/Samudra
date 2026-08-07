"""Research-store models: no direct identifiers, ever.

Mirrors docs/04-data-schema.md. Deliberately absent from `Participant`: name,
email, phone, exact date of birth, city, employer, job title, IP address.
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import ResearchBase


def _uuid() -> str:
    return str(uuid.uuid4())


class RecruitmentChannel(str, enum.Enum):
    dev_community = "dev_community"
    college = "college"
    ngo = "ngo"
    professional = "professional"
    other = "other"


class AgeBand(str, enum.Enum):
    age_18_24 = "18-24"
    age_25_34 = "25-34"
    age_35_44 = "35-44"
    age_45_54 = "45-54"
    age_55_plus = "55+"


class WorkStatus(str, enum.Enum):
    student = "student"
    employed = "employed"
    self_employed = "self_employed"
    not_working = "not_working"
    prefer_not_to_say = "prefer_not_to_say"


class Condition(str, enum.Enum):
    honest_untimed = "honest_untimed"
    honest_timed = "honest_timed"
    fake_timed = "fake_timed"
    fake_untimed = "fake_untimed"


class DeviceType(str, enum.Enum):
    mobile = "mobile"
    tablet = "tablet"
    desktop = "desktop"


class InputMethod(str, enum.Enum):
    touch = "touch"
    mouse_keyboard = "mouse_keyboard"


class ModuleCode(str, enum.Enum):
    M1 = "M1"
    M2 = "M2"
    M3 = "M3"
    M4 = "M4"
    M5 = "M5"


class FlagType(str, enum.Enum):
    attention_check_failed = "attention_check_failed"
    straight_lining = "straight_lining"
    latency_floor = "latency_floor"
    excessive_timeouts = "excessive_timeouts"
    duplicate_suspected = "duplicate_suspected"


class Participant(ResearchBase):
    __tablename__ = "participants"

    participant_code: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    recruitment_channel: Mapped[RecruitmentChannel] = mapped_column(Enum(RecruitmentChannel))
    consent_version: Mapped[str] = mapped_column(String)
    consent_research: Mapped[bool] = mapped_column(Boolean, default=False)
    consent_open_data: Mapped[bool] = mapped_column(Boolean, default=False)

    age_band: Mapped[AgeBand | None] = mapped_column(Enum(AgeBand), nullable=True)
    education_band: Mapped[str | None] = mapped_column(String, nullable=True)
    state: Mapped[str | None] = mapped_column(String, nullable=True)
    primary_language: Mapped[str | None] = mapped_column(String, nullable=True)
    work_status: Mapped[WorkStatus | None] = mapped_column(Enum(WorkStatus), nullable=True)

    withdrawn: Mapped[bool] = mapped_column(Boolean, default=False)
    withdrawn_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    sessions: Mapped[list["Session"]] = relationship(back_populates="participant")


class Session(ResearchBase):
    __tablename__ = "sessions"

    session_id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    participant_code: Mapped[str] = mapped_column(ForeignKey("participants.participant_code"))

    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    condition: Mapped[Condition] = mapped_column(Enum(Condition))
    module_order: Mapped[list] = mapped_column(JSON, default=list)

    device_type: Mapped[DeviceType | None] = mapped_column(Enum(DeviceType), nullable=True)
    input_method: Mapped[InputMethod | None] = mapped_column(Enum(InputMethod), nullable=True)
    viewport_width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    user_agent_family: Mapped[str | None] = mapped_column(String, nullable=True)

    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    abandoned_at_module: Mapped[str | None] = mapped_column(String, nullable=True)

    participant: Mapped["Participant"] = relationship(back_populates="sessions")
    responses: Mapped[list["Response"]] = relationship(back_populates="session")


class ReadingBaseline(ResearchBase):
    """Chars/sec baseline — mandatory covariate for any latency analysis.

    See docs/03-platform-architecture.md: "Without the reading-speed baseline,
    your latency analysis is uninterpretable."
    """

    __tablename__ = "reading_baseline"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("sessions.session_id"))
    sentence_id: Mapped[str] = mapped_column(String)
    char_count: Mapped[int] = mapped_column(Integer)
    read_time_ms: Mapped[int] = mapped_column(Integer)


class Response(ResearchBase):
    __tablename__ = "responses"

    response_id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    session_id: Mapped[str] = mapped_column(ForeignKey("sessions.session_id"))

    module_code: Mapped[ModuleCode] = mapped_column(Enum(ModuleCode))
    item_id: Mapped[str] = mapped_column(String)
    item_bank_version: Mapped[str] = mapped_column(String)
    position_in_module: Mapped[int] = mapped_column(Integer)

    response_payload: Mapped[dict] = mapped_column(JSON)

    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    timed_out: Mapped[bool] = mapped_column(Boolean, default=False)
    focus_lost: Mapped[bool] = mapped_column(Boolean, default=False)
    revisions: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session: Mapped["Session"] = relationship(back_populates="responses")


class QualityFlag(ResearchBase):
    __tablename__ = "quality_flags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("sessions.session_id"))
    flag_type: Mapped[FlagType] = mapped_column(Enum(FlagType))
    detail: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
