import { useCallback, useEffect, useRef } from 'react'

/**
 * Millisecond-accurate item response timing.
 *
 * This is the most technically load-bearing piece of the frontend — see
 * ../../ARCHITECTURE.md §5. Two hypotheses in docs/06-analysis-plan.md
 * (H3, H4-adjacent latency work) depend on this being right, and it cannot
 * be retrofitted onto already-collected data.
 *
 * Rules encoded here, in order of importance:
 *  1. `performance.now()`, never `Date.now()` — monotonic, sub-millisecond,
 *     immune to NTP wall-clock adjustment mid-session.
 *  2. Anchor the clock to *paint*, not to React state change. The first
 *     requestAnimationFrame callback fires before paint; the second fires
 *     after — so the timestamp captured in the second rAF is the moment the
 *     participant could actually see the item.
 *  3. Flag (don't discard) responses where the tab was backgrounded mid-item
 *     — `visibilitychange` — so exclusion happens at analysis time per
 *     pre-specified rules, not silently here.
 */
export function useItemTimer(itemId: string) {
  const shownAtRef = useRef<number | null>(null)
  const focusLostRef = useRef(false)

  useEffect(() => {
    shownAtRef.current = null
    focusLostRef.current = false

    // First rAF fires before paint; second fires after. This double-anchor
    // is deliberate, not a typo — see ARCHITECTURE.md §5, rule 2.
    const raf1 = requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        shownAtRef.current = performance.now()
      })
    })

    const onVisibility = () => {
      if (document.hidden) focusLostRef.current = true
    }
    document.addEventListener('visibilitychange', onVisibility)

    return () => {
      cancelAnimationFrame(raf1)
      document.removeEventListener('visibilitychange', onVisibility)
    }
  }, [itemId])

  const capture = useCallback(() => {
    const latencyMs = shownAtRef.current
      ? Math.round(performance.now() - shownAtRef.current)
      : null
    return { latencyMs, focusLost: focusLostRef.current }
  }, [])

  return { capture }
}
