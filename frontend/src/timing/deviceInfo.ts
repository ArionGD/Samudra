/**
 * Confound capture — device type, input method, viewport width.
 *
 * Latency data is uninterpretable without these alongside it. See
 * docs/03-platform-architecture.md §"Capture the confounds" and
 * docs/04-data-schema.md (sessions table).
 */

export type DeviceType = 'mobile' | 'tablet' | 'desktop'
export type InputMethod = 'touch' | 'mouse_keyboard'

export function getDeviceType(): DeviceType {
  const width = window.innerWidth
  if (width < 640) return 'mobile'
  if (width < 1024) return 'tablet'
  return 'desktop'
}

export function getInputMethod(): InputMethod {
  return window.matchMedia('(pointer: coarse)').matches ? 'touch' : 'mouse_keyboard'
}

export function getViewportWidth(): number {
  return window.innerWidth
}
