/**
 * Mirrors backend/app/schemas.py and backend/app/models/research.py enums.
 * Kept hand-written and in sync deliberately rather than code-generated, at
 * this project size — revisit if the API surface grows enough that drift
 * becomes a real risk (see backend/README.md for the current endpoint list).
 */

export type RecruitmentChannel =
  | 'dev_community'
  | 'college'
  | 'ngo'
  | 'professional'
  | 'other'

export type Condition =
  | 'honest_untimed'
  | 'honest_timed'
  | 'fake_timed'
  | 'fake_untimed'

export type DeviceType = 'mobile' | 'tablet' | 'desktop'
export type InputMethod = 'touch' | 'mouse_keyboard'
export type ModuleCode = 'M1' | 'M2' | 'M3' | 'M4' | 'M5'

export interface SessionCreateRequest {
  recruitment_channel: RecruitmentChannel
  consent_version: string
  consent_research: boolean
  consent_open_data?: boolean
  device_type?: DeviceType
  input_method?: InputMethod
  viewport_width?: number
}

export interface SessionCreateResponse {
  session_id: string
  participant_code: string
  condition: Condition
}

export interface ResponseIn {
  module_code: ModuleCode
  item_id: string
  item_bank_version: string
  position_in_module: number
  response_payload: Record<string, unknown>
  latency_ms: number | null
  timed_out?: boolean
  focus_lost?: boolean
  revisions?: number
}
