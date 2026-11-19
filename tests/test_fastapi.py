from fastapi.testclient import TestClient
from openai import APITimeoutError
from api.main import app
from unittest.mock import patch

client= TestClient(app)

def test_invalid_failure_details():
    response = client.post(
        "/analyse-failure",
        json={"failure_details":"404"}
    )
    assert response.status_code == 422


def test_successful_analysis():
    mock_result = {
        "likely_cause": "Booking may not exist",
        "debugging_steps": [
            "Verify the booking ID",
            "Check expected API behavior"
        ],
        "defect_type": "Unconfirmed"
    }
    with patch(
               "api.main.ai_analyse_failure",
               return_value=mock_result
    ) as mock_analyser:
        response = client.post(
            '/analyse-failure',
            json={
                "failure_details":
                    "Expected HTTP 200 but received HTTP 404"
            }
        )
    assert response.status_code == 200
    assert response.json() == mock_result 
    assert mock_analyser.assert_called_once()
    
def test_503_error():
    with patch(
        'api.main.ai_analyse_failure',
        side_effect=None
        ) as mock_analyser:
          response = client.post(
                    '/analyse-failure',
                    json={
                        "failure_details":
                            "Expected HTTP 200 but received HTTP 404"
                    }
                )
          assert response.status_code == 503
          assert response.json() == {
                "detail": "AI analysis service unavailable"
            }
          mock_analyser.assert_called_once()