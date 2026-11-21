import pytest

from ai.investigation_state import InvestigationState
def test_initial_investigation_state():
    state = InvestigationState(test_name="Test001",error="Test failed with error 503")
    assert state.test_name == "Test001"
    assert state.error == "Test failed with error 503"
    assert state.retrieved_defects == []
    assert state.tool_results == []
    assert state.errors == []
    assert state.analysis is None
    assert state.status == "NEW"

def test_invalid_investigation_status():
    with pytest.raises(ValueError):
        InvestigationState(test_name="Test001",error="Test failed with error 503",status="UNKNOWN")

def test_independent_investigation_states():
    state1 = InvestigationState(test_name="Test001",error="Test failed with error 503")
    state1.errors.append("new error")
    state1.status = 'COMPLETED'
    state2 = InvestigationState(test_name="Test002",error="Test failed with error 404")
    assert state2.errors == []
    assert state2.status == "NEW"
