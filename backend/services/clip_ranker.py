# Optional: CLIP-based pre-ranking helper
# Keeps imports optional so the project runs without heavy deps.
from __future__ import annotations


def clip_rank(transcript_text: str, candidate_paths: list[str]) -> list[tuple[str, float]]:
    try:
        import clip
        import torch
        from PIL import Image
    except ModuleNotFoundError:
        return [(path, 0.0) for path in candidate_paths]

    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, preprocess = clip.load("ViT-B/32", device=device)
        text_tokens = clip.tokenize([transcript_text]).to(device)
        images = [preprocess(Image.open(path).convert("RGB")) for path in candidate_paths]
        image_tensor = torch.stack(images).to(device)
        with torch.no_grad():
            text_features = model.encode_text(text_tokens).float()
            image_features = model.encode_image(image_tensor).float()
            text_features /= text_features.norm(dim=-1, keepdim=True)
            image_features /= image_features.norm(dim=-1, keepdim=True)
            similarities = (image_features @ text_features.T).squeeze(1).cpu().numpy()
        order = list(reversed(similarities.argsort()))
        return [(candidate_paths[index], float(similarities[index])) for index in order]
    except Exception:  # pragma: no cover - best-effort helper
        return [(path, 0.0) for path in candidate_paths]
