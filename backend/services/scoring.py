def effect_size_from_ranks(true_ranks: list[int], n_candidates: int = 5) -> tuple[float, float]:
    """Compute linear effect size from average rank for a fixed number of candidates.

    ES maps chance avg rank ((n+1)/2) to 0.0; best avg rank (1.0) to +1.0; worst to -1.0.

    Returns (effect_size, average_rank).
    """
    if not true_ranks:
        return 0.0, 0.0

    # Guard against degenerate n to avoid division by zero
    n = max(2, int(n_candidates))

    avg_rank = sum(true_ranks) / len(true_ranks)
    es = (((n + 1) / 2.0) - avg_rank) / ((n - 1) / 2.0)
    return es, avg_rank
