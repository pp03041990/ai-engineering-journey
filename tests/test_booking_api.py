from api.booking_api import get_booking
from datetime import date
import pytest

@pytest.mark.parametrize(
    "booking_id,expected_status",
    [
        ('10',200),
        # ('999999999',200)
    ]
)
def test_booking_status(booking_id, expected_status):
    response = get_booking(booking_id)

    assert response is not None
    assert response.status_code == expected_status