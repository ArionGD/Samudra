import { useState } from 'react'
import { useItemTimer } from '../../timing/useItemTimer'

export interface Statement {
  id: string
  text: string
}

interface ForcedChoiceBlockProps {
  blockId: string
  statements: [Statement, Statement, Statement]
  onAnswer: (result: { most: string; least: string; latencyMs: number | null; focusLost: boolean }) => void
}

/**
 * M1 forced-choice triplet — pick MOST and LEAST like you.
 * See docs/01-instrument-design.md §M1 for the full design rationale
 * (desirability matching, 12s countdown, etc.) — this component renders one
 * block; the countdown/pacing wrapper is a separate concern, not yet built.
 */
export function ForcedChoiceBlock({ blockId, statements, onAnswer }: ForcedChoiceBlockProps) {
  const { capture } = useItemTimer(blockId)
  const [most, setMost] = useState<string | null>(null)
  const [least, setLeast] = useState<string | null>(null)

  const canSubmit = most !== null && least !== null && most !== least

  const handleSubmit = () => {
    if (!canSubmit || most === null || least === null) return
    const { latencyMs, focusLost } = capture()
    onAnswer({ most, least, latencyMs, focusLost })
  }

  return (
    <div className="mx-auto flex max-w-md flex-col gap-4 p-4">
      <p className="text-sm font-medium">
        Which is MOST like you, and which is LEAST like you?
      </p>

      <fieldset className="flex flex-col gap-2">
        {statements.map((s) => (
          <div key={s.id} className="flex items-center gap-3 rounded border p-2 text-sm">
            <span className="flex-1">{s.text}</span>
            <label className="flex items-center gap-1 text-xs">
              <input
                type="radio"
                name={`${blockId}-most`}
                checked={most === s.id}
                onChange={() => setMost(s.id)}
              />
              Most
            </label>
            <label className="flex items-center gap-1 text-xs">
              <input
                type="radio"
                name={`${blockId}-least`}
                checked={least === s.id}
                onChange={() => setLeast(s.id)}
              />
              Least
            </label>
          </div>
        ))}
      </fieldset>

      <button
        type="button"
        disabled={!canSubmit}
        className="rounded bg-black px-4 py-2 text-sm text-white disabled:opacity-40"
        onClick={handleSubmit}
      >
        Next
      </button>
    </div>
  )
}
