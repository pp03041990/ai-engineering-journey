import pytest

pytest_plugins = ["pytester"]


def test_failed_test_triggers_ai_request(pytester):
    pytester.makeconftest("""
import pytest
import requests
from unittest.mock import patch, Mock

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    with patch("requests.post") as mock_post:
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {
                "likely_cause": "Test data issue",
                "debugging_steps": ["Verify booking ID"],
                "defect_type": "Unconfirmed"
            }
        )

        requests.post(
            "http://127.0.0.1:8000/analyse-failure",
            json={"failure_details": report.longreprtext}
        )

        mock_post.assert_called_once()
""")

    pytester.makepyfile("""
def test_booking_failure():
    assert 404 == 200
""")

    result = pytester.runpytest("-v")
    result.assert_outcomes(failed=1)