import type { ResponseIn, SessionCreateRequest, SessionCreateResponse } from './types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...init?.headers },
  })
  if (!res.ok) {
    const detail = await res.text().catch(() => '')
    throw new Error(`${init?.method ?? 'GET'} ${path} -> ${res.status}: ${detail}`)
  }
  if (res.status === 204) return undefined as T
  return (await res.json()) as T
}

export function createSession(payload: SessionCreateRequest): Promise<SessionCreateResponse> {
  return request('/session', { method: 'POST', body: JSON.stringify(payload) })
}

export function submitResponses(sessionId: string, responses: ResponseIn[]): Promise<void> {
  return request(`/session/${sessionId}/responses`, {
    method: 'POST',
    body: JSON.stringify({ responses }),
  })
}

export function completeSession(
  sessionId: string,
  abandonedAtModule?: string,
): Promise<void> {
  return request(`/session/${sessionId}/complete`, {
    method: 'POST',
    body: JSON.stringify({ abandoned_at_module: abandonedAtModule ?? null }),
  })
}

export function withdrawParticipant(participantCode: string): Promise<void> {
  return request('/withdraw', {
    method: 'POST',
    body: JSON.stringify({ participant_code: participantCode }),
  })
}
