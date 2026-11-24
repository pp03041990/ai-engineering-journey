from ai.test_registry import get_approved_test
import pytest

def test_get_approved_test():
    details = get_approved_test("booking_api")
    assert details["framework"] == "pytest"
    assert details["test_path"] == "tests/test_booking_api.py"

def test_reject_unapproved_test():
    with pytest.raises(ValueError,match=f"Test not approved: bookin_api"):
     get_approved_test("bookin_api")