"""

completer test
"""
from unittest.mock import patch

import pytest

from remote_pod_debugger.completer import Completer


@pytest.mark.parametrize("data, expected_result, options", [
    (
        "te",
        "test1a",
        [
            "test1a",
            "test2a"
        ]
    ),
    (
        "test1",
        "test1a",
        [
            "test1a",
            "test2a"
        ]
    ),
    (
        "test2",
        "test2a",
        [
            "test1a",
            "test2a"
        ]
    ),
    (
        "teaaa",
        None,
        [
            "test1a",
            "test2a"
        ]
    ),
])
def test_complete(data, expected_result, options):
    """

    test complete function of Completer
    """
    _completer = Completer(options)
    with patch("remote_pod_debugger.completer.readline.get_line_buffer", return_value=data):
        resp = _completer.complete(data, 0)
        assert resp == expected_result
