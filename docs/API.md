# API Reference

Base URL: `/`

## `GET /health`
Returns `{ ok: true }`.

## `POST /sessions/start`
Starts a session.
- **Response**: `{ session_id, target_id, opening_prompt }`

## `POST /sessions/log`
Append viewer text and get the monitor’s next prompt.
- **Body**: `{ session_id, stage: 'I'..'VI', viewer_text }`
- **Response**: `{ monitor_prompt }`

## `POST /sessions/advance`
Advance to a new stage.
- **Body**: `{ session_id, to_stage }`
- **Response**: `{ monitor_prompt }`

## `POST /sessions/finish`
Close a session.
- **Body**: `{ session_id }`

## `POST /judging/run`
Run rank‑order judging (random baseline or CLIP if enabled).
- **Body**: `{ session_id, n_candidates=5, use_clip=false }`
- **Response**: `{ judge_run_id, average_rank, effect_size, ranking: [{candidate_path, rank}] }`

## `POST /judging/feedback`
Return true target path for a session.
- **Body**: `{ session_id }`
- **Response**: `{ target_path }`

## `POST /targets/upload`
Upload one or more target images (admin/dev).
- **Form**: files[]

## `GET /targets/list`
List packaged targets from `targets.yaml`.
