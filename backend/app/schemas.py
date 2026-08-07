"""Pydantic request/response schemas — the validation boundary for the API.

Kept separate from SQLAlchemy models deliberately: request/response shapes and
storage shapes are allowed to diverge, and conflating them tends to leak
internal columns into the API by accident.
"""

from pydantic import BaseModel, Field

from app.models.research import Condition, DeviceType, InputMethod, ModuleCode, RecruitmentChannel


class SessionCreateRequest(BaseModel):
    recruitment_channel: RecruitmentChannel
    consent_version: str
    consent_research: bool
    consent_open_data: bool = False
    device_type: DeviceType | None = None
    input_method: InputMethod | None = None
    viewport_width: int | None = None


class SessionCreateResponse(BaseModel):
    session_id: str
    participant_code: str
    condition: Condition


class ResponseIn(BaseModel):
    module_code: ModuleCode
    item_id: str
    item_bank_version: str
    position_in_module: int
    response_payload: dict
    latency_ms: int | None = None
    timed_out: bool = False
    focus_lost: bool = False
    revisions: int = 0


class ResponseBatchIn(BaseModel):
    responses: list[ResponseIn] = Field(min_length=1)


class SessionCompleteRequest(BaseModel):
    abandoned_at_module: str | None = None


class WithdrawRequest(BaseModel):
    participant_code: str
