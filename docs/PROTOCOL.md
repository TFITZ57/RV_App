# Protocol essentials (CRV structure & judging)

## Roles
- **Tasker**: chooses target, computes HMAC Target ID, stores mapping privately.
- **Monitor**: enforces structure; does **not** know target content.
- **Judge**: after session, assembles pool and assigns **rank order**; app computes **effect size**.

## Stage rules (Monitor utterances only)
- **I**: Ideogram/I-A-B; prompt: “Describe the target.”
- **II**: Sensory lists only; prompt: “List colors, textures, temperatures, sounds, and smells.”
- **III**: Sketch & movement; prompt: “From the top of the target, look down and describe.”
- **IV**: Matrix (S‑2, D, AI/EI, T, I, AOL, AOL/S); prompt: “Describe the target.”
- **V**: Attribute reductions (short chains).
- **VI**: 3‑D modeling and localization.

**AOL handling**: whenever the viewer names/labels, say **“AOL—write it, break.”** Then return to neutral prompts.

## Judging
- Build a pool: 1 true + (n‑1) decoys.
- Rank‑order the transcripts vs target (or targets vs transcript).
- Compute **average rank** and **effect size** (linear map of avg rank; chance → 0.0).

