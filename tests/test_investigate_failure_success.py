from unittest.mock import Mock, patch

import pytest

from ai.investigation_orchestrator import determine_route, investigate_failure
from ai.state_transitions import transition_state
from ai.investigation_state import InvestigationState


def test_investigate_failure_success():
    result = {
        "analysis": {
            "likely_cause": "Loan API service unavailable",
            "debugging_steps": ["Check service logs"],
            "defect_type": "SERVICE_ISSUE"
        },
        "retrieved_defects": [
            {"id": "DEF-101", "description": "Loan API returned HTTP 503"}
        ],
        "grounding_evaluation": {
            "is_grounded": True,
            "unsupported_claims": [],
            "explanation": "Analysis is supported by historical defects"
        }
    }
    # res = Mock()
    # res.return_value = result
    with patch("ai.investigation_orchestrator.analyse_failure_with_rag") as mock_analysis:
        mock_analysis.return_value = result
        state = investigate_failure({"test_name":"Test_001","error":"Test Failed"})
        assert state.status == "COMPLETED"
        assert state.retrieved_defects[0]["id"] == "DEF-101"
        assert state.grounding_evaluation["is_grounded"] == True
        assert state.analysis["likely_cause"] == "Loan API service unavailable"

def test_state_when_result_is_none():
    with patch("ai.investigation_orchestrator.analyse_failure_with_rag") as mock_analysis:
            mock_analysis.return_value = None
            state = investigate_failure({"test_name":"Test_001","error":"Test Failed"})
            assert state.status == "FAILED"
            assert state.errors[0] == "AI analysis not generated"
            assert state.retrieved_defects == []
            assert state.grounding_evaluation is None
            assert state.analysis is None

def test_state_when_exception_occurs():
    with patch("ai.investigation_orchestrator.analyse_failure_with_rag") as mock_analysis:
            mock_analysis.side_effect = ValueError("RAG service unavailable")
            state = investigate_failure({"test_name":"Test_001","error":"Test Failed"})
            assert state.status == "FAILED"
            assert state.errors == ["RAG service unavailable"]
            assert state.retrieved_defects == []
            assert state.grounding_evaluation is None
            assert state.analysis is None

@pytest.mark.parametrize(
    "error, expected_route",
    [
        ("HTTP 404 Not Found", "TEST_DATA"),
        ("HTTP 401 Unauthorized", "AUTH"),
        ("HTTP 403 Forbidden", "AUTH"),
        ("HTTP 500 Internal Server Error", "SERVICE"),
        ("HTTP 503 Service Unavailable", "SERVICE"),
        ("AssertionError: expected 200", "ASSERTION"),
        ("Connection reset", "GENERAL"),
    ]
)
def test_route_in_state_object(error, expected_route):
    with patch("ai.investigation_orchestrator.analyse_failure_with_rag") as mock_analysis:
        mock_analysis.return_value = None
        state = investigate_failure({"test_name":"Test_001","error":error})
        assert state.route == expected_route

@pytest.mark.parametrize(
    "error, expected_route",
    [
        ("HTTP 404 Not Found", "TEST_DATA"),
        ("HTTP 401 Unauthorized", "AUTH"),
        ("HTTP 403 Forbidden", "AUTH"),
        ("HTTP 500 Internal Server Error", "SERVICE"),
        ("HTTP 503 Service Unavailable", "SERVICE"),
        ("AssertionError: expected 200", "ASSERTION"),
        ("Connection reset", "GENERAL"),
    ]
)
def test_determine_route(error, expected_route):
    assert determine_route(error) == expected_route

def test_service_route_diagnostics():
    result = {
        "analysis": {
            "likely_cause": "Loan API service unavailable",
            "debugging_steps": ["Check service logs"],
            "defect_type": "SERVICE_ISSUE"
        },
        "retrieved_defects": [
            {"id": "DEF-101", "description": "Loan API returned HTTP 503"}
        ],
        "grounding_evaluation": {
            "is_grounded": True,
            "unsupported_claims": [],
            "explanation": "Analysis is supported by historical defects"
        }
    }
    with patch("ai.investigation_orchestrator.analyse_failure_with_rag") as mock_analysis:
        mock_analysis.return_value = result
        state = investigate_failure({
            "test_name": "test_loan_api",
            "error": "HTTP 503 Service Unavailable"
        })
        assert state.route == "SERVICE"
        assert "Check service health and logs" in state.tool_results[0]["result"]["checks"] 
        assert "DIAGNOSTICS" in state.completed_steps
        assert state.status == "COMPLETED"

def test_diagnostic_failed():
    result = {
            "analysis": {
                "likely_cause": "Loan API service unavailable",
                "debugging_steps": ["Check service logs"],
                "defect_type": "SERVICE_ISSUE"
            },
            "retrieved_defects": [
                {"id": "DEF-101", "description": "Loan API returned HTTP 503"}
            ],
            "grounding_evaluation": {
                "is_grounded": True,
                "unsupported_claims": [],
                "explanation": "Analysis is supported by historical defects"
            }
        }
    with patch("ai.investigation_orchestrator.collect_diagnostics") as mock_diagnostics,patch("ai.investigation_orchestrator.analyse_failure_with_rag") as mock_analysis:
        mock_diagnostics.side_effect = ValueError("Logging unavailable")
        mock_analysis.return_value = result
        state = investigate_failure({
            "test_name": "test_loan_api",
            "error": "HTTP 503 Service Unavailable"
        })
        assert state.tool_results == []
        assert state.completed_steps == ["AI_ANALYSIS"]
        assert state.errors == ["DIAGNOSTICS_FAILED: Logging unavailable"]
        assert state.status == "COMPLETED"
        
@pytest.mark.parametrize("current_status,new_status,expected",[
    ("NEW","IN_PROGRESS","Allowed"),
    ("IN_PROGRESS","COMPLETED","Allowed"),
    ("NEW","COMPLETED","ValueError")
])
def test_state_transitions(current_status,new_status,expected):
    state = InvestigationState(
        test_name="Test_001",
        error="HTTP 503",
        status=current_status
    )
    
    if expected == "Allowed":
        transition_state(state,new_status)
        assert state.status == new_status
    else:
        with pytest.raises(ValueError,match=f"Invalid transition: {state.status} -> {new_status}") as exc:
            transition_state(state,new_status)
        assert state.status == current_status