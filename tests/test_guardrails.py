from backend.services.guardrails import is_leading_content


def test_leading_detection():
    assert is_leading_content('I perceive a bridge over water') is True
    assert is_leading_content('cool, rough, bright, curved, open') is False
