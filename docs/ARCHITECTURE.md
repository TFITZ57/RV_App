# Architecture

## Three-role split
- **Tasker**: Target selection & HMAC Target IDs (no contact with the viewer). Writes `target_truth` mapping in DB.
- **Monitor Agent**: Finite‑state machine that produces only **whitelisted utterances**. Sees **Target ID only**.
- **Judge**: Post‑session process assembling a pool and computing **average rank** & **effect size**.

## Data Flow
1. Tasker picks target from `targets/targets.yaml`, computes `target_id = HMAC(secret, sha256)` and stores `(target_id -> path)` in DB.
2. Session starts → viewer interacts with Monitor. All inputs saved to `transcript_page` & `sketch`.
3. Finish → Judging builds a pool, ranks, persists `judging_result`, computes stats.
4. Feedback reveals the true target and presents a session packet.

## Guardrails
- Output validation: monitor emits only templates; detection of leading nouns triggers **AOL break**.
- Separation of duties: the Monitor process never touches `target_truth` mapping.
