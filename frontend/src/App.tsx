import { useState } from 'react'
import { CONSENT_VERSION, ConsentScreen } from './consent/ConsentScreen'
import { ForcedChoiceBlock, type Statement } from './modules/m1/ForcedChoiceBlock'
import { completeSession, createSession } from './api/client'
import { enqueueResponse, flushQueue } from './offline/responseQueue'
import { getDeviceType, getInputMethod, getViewportWidth } from './timing/deviceInfo'
import type { Condition } from './api/types'

// Placeholder statements for wiring/testing only — NOT a reviewed,
// desirability-matched item bank. Real content loads from ../items/ via the
// backend's item-bank loader once M1's item pool is written and rated.
// See docs/01-instrument-design.md and docs/11-implementation-plan.md.
const DEMO_BLOCK: { blockId: string; statements: [Statement, Statement, Statement] } = {
  blockId: 'demo_blk_001',
  statements: [
    { id: 'demo_stmt_a', text: 'I keep a written plan for the week ahead.' },
    { id: 'demo_stmt_b', text: 'I stay level-headed when deadlines compress.' },
    { id: 'demo_stmt_c', text: 'I let others take the lead in group decisions.' },
  ],
}

type Stage = 'consent' | 'block' | 'done'

function App() {
  const [stage, setStage] = useState<Stage>('consent')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [condition, setCondition] = useState<Condition | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleConsent = async ({
    consentResearch,
    consentOpenData,
  }: {
    consentResearch: boolean
    consentOpenData: boolean
  }) => {
    try {
      const session = await createSession({
        recruitment_channel: 'dev_community',
        consent_version: CONSENT_VERSION,
        consent_research: consentResearch,
        consent_open_data: consentOpenData,
        device_type: getDeviceType(),
        input_method: getInputMethod(),
        viewport_width: getViewportWidth(),
      })
      setSessionId(session.session_id)
      setCondition(session.condition)
      setStage('block')
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to create session.')
    }
  }

  const handleAnswer = async (result: {
    most: string
    least: string
    latencyMs: number | null
    focusLost: boolean
  }) => {
    if (!sessionId) return
    try {
      await enqueueResponse(sessionId, {
        module_code: 'M1',
        item_id: DEMO_BLOCK.blockId,
        item_bank_version: 'demo',
        position_in_module: 1,
        response_payload: { most: result.most, least: result.least },
        latency_ms: result.latencyMs,
        focus_lost: result.focusLost,
      })
      await flushQueue(sessionId)
      await completeSession(sessionId)
      setStage('done')
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to submit response.')
    }
  }

  return (
    <main className="min-h-svh bg-white text-black dark:bg-neutral-950 dark:text-white">
      {error && (
        <p className="mx-auto max-w-md p-4 text-sm text-red-600">{error}</p>
      )}

      {stage === 'consent' && <ConsentScreen onConsent={handleConsent} />}

      {stage === 'block' && (
        <ForcedChoiceBlock
          blockId={DEMO_BLOCK.blockId}
          statements={DEMO_BLOCK.statements}
          onAnswer={handleAnswer}
        />
      )}

      {stage === 'done' && (
        <div className="mx-auto flex max-w-md flex-col gap-2 p-4 text-sm">
          <p>Thanks — response recorded.</p>
          <p className="text-xs text-neutral-500">
            Session {sessionId} — condition assigned server-side: {condition}
          </p>
          <p className="text-xs text-neutral-500">
            This is a wiring demo, not the real M1 module. See
            docs/11-implementation-plan.md for the build order.
          </p>
        </div>
      )}
    </main>
  )
}

export default App
