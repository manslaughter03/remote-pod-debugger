"""

completer test
"""
from remote_pod_debugger.completer import Completer


def test_complete():
    """

    test complete function of Completer
    """
    _items = [
        "test1a",
        "test2a"
    ]
    _completer = Completer(_items)
    resp = _completer.complete("te", 0)
    assert resp == _items[0]
    resp = _completer.complete("test2", 0)
    assert resp == _items[1]
    resp = _completer.complete("test3", 0)
    assert not resp
