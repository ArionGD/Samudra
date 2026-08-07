import { del, get, set } from 'idb-keyval'
import type { ResponseIn } from '../api/types'
import { submitResponses } from '../api/client'

/**
 * IndexedDB-backed response queue.
 *
 * Indian mobile connectivity makes disconnection the normal case, not an
 * edge case — see ARCHITECTURE.md §6. Responses are written here as they
 * happen and flushed in small batches; never held purely in memory, because
 * backgrounded mobile tabs get killed by the OS and in-memory state goes
 * with them.
 */

const QUEUE_KEY_PREFIX = 'response-queue:'
const FLUSH_BATCH_SIZE = 5
const MAX_RETRIES = 5

function queueKey(sessionId: string): string {
  return `${QUEUE_KEY_PREFIX}${sessionId}`
}

async function readQueue(sessionId: string): Promise<ResponseIn[]> {
  return (await get(queueKey(sessionId))) ?? []
}

async function writeQueue(sessionId: string, queue: ResponseIn[]): Promise<void> {
  await set(queueKey(sessionId), queue)
}

export async function enqueueResponse(sessionId: string, response: ResponseIn): Promise<void> {
  const queue = await readQueue(sessionId)
  queue.push(response)
  await writeQueue(sessionId, queue)
}

/**
 * Attempt to flush the queue to the backend. Safe to call repeatedly (e.g.
 * after every enqueue, and on reconnect) — it's a no-op on an empty queue.
 * Retries with exponential backoff up to MAX_RETRIES; a batch that still
 * fails stays queued for the next flush attempt rather than being dropped.
 */
export async function flushQueue(sessionId: string): Promise<void> {
  let queue = await readQueue(sessionId)

  while (queue.length > 0) {
    const batch = queue.slice(0, FLUSH_BATCH_SIZE)
    let attempt = 0
    let sent = false

    while (attempt < MAX_RETRIES && !sent) {
      try {
        await submitResponses(sessionId, batch)
        sent = true
      } catch {
        attempt += 1
        const backoffMs = Math.min(1000 * 2 ** attempt, 15_000)
        await new Promise((resolve) => setTimeout(resolve, backoffMs))
      }
    }

    if (!sent) return // give up for now; remaining queue stays persisted for next call

    queue = queue.slice(batch.length)
    await writeQueue(sessionId, queue)
  }
}

export async function clearQueue(sessionId: string): Promise<void> {
  await del(queueKey(sessionId))
}
