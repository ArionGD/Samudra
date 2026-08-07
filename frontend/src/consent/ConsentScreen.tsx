import { useState } from 'react'

const CONSENT_VERSION = 'v0.1-placeholder'

interface ConsentScreenProps {
  onConsent: (params: { consentResearch: boolean; consentOpenData: boolean }) => void
}

/**
 * Layered consent, per docs/02-ethics-and-consent.md §3.
 *
 * This is a structural placeholder proving the layering pattern, NOT final
 * consent copy — do not use this text with real participants. Real copy
 * needs ethics-panel review first (docs/07-roadmap.md, Gate 0).
 *
 * Non-negotiable patterns encoded here even in placeholder form:
 *  - checkboxes default unchecked
 *  - open-data consent is separate from and independent of research consent
 *  - no dark patterns — continue is not enabled until required consent is given
 */
export function ConsentScreen({ onConsent }: ConsentScreenProps) {
  const [detailOpen, setDetailOpen] = useState(false)
  const [consentResearch, setConsentResearch] = useState(false)
  const [consentOpenData, setConsentOpenData] = useState(false)

  return (
    <div className="mx-auto flex max-w-md flex-col gap-4 p-4 text-sm">
      <h1 className="text-lg font-medium">Research study</h1>
      <p>
        This is a research study about how people answer different kinds of
        questions. It takes about 10 minutes. Your answers are stored without
        your name. You can stop at any time. Taking part is entirely your
        choice.
      </p>

      <button
        type="button"
        className="text-left underline"
        onClick={() => setDetailOpen((open) => !open)}
      >
        {detailOpen ? 'Hide details' : 'What data is collected, and why?'}
      </button>

      {detailOpen && (
        <div className="rounded border p-3 text-xs leading-relaxed">
          <p>
            We record your responses, response times, and device type. We do
            not collect your name, email (unless you opt in below), or exact
            location. See the full information sheet for details on storage,
            retention, and withdrawal.
          </p>
        </div>
      )}

      <label className="flex items-start gap-2">
        <input
          type="checkbox"
          checked={consentResearch}
          onChange={(e) => setConsentResearch(e.target.checked)}
        />
        <span>I agree to take part in this study (required)</span>
      </label>

      <label className="flex items-start gap-2">
        <input
          type="checkbox"
          checked={consentOpenData}
          onChange={(e) => setConsentOpenData(e.target.checked)}
        />
        <span>
          I agree that my anonymised data may be included in a public open
          dataset (optional)
        </span>
      </label>

      <button
        type="button"
        disabled={!consentResearch}
        className="rounded bg-black px-4 py-2 text-white disabled:opacity-40"
        onClick={() => onConsent({ consentResearch, consentOpenData })}
      >
        Continue
      </button>
    </div>
  )
}

export { CONSENT_VERSION }
