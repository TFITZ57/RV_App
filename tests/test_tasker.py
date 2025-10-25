from backend.services.tasker import _hmac_tag


def test_hmac_tag_stable():
    tag1 = _hmac_tag('abc123')
    tag2 = _hmac_tag('abc123')
    assert tag1 == tag2
