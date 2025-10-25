from backend.services.scoring import effect_size_from_ranks


def test_effect_size_mapping():
    # For n=5, chance avg is 3.0 -> ES 0
    es, avg = effect_size_from_ranks([3])
    assert round(es, 6) == 0.0
    # Perfect (rank=1) -> ES +1.0
    es, avg = effect_size_from_ranks([1])
    assert round(es, 6) == 1.0
    # Worst (rank=5) -> ES -1.0
    es, avg = effect_size_from_ranks([5])
    assert round(es, 6) == -1.0
