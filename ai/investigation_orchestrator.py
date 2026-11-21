from ai.investigation_state import InvestigationState
from ai.diagnostics import collect_diagnostics
from rag.rag_pipeline import analyse_failure_with_rag
from ai.state_transitions import transition_state
def determine_route(error: str) -> str:
    error = error.upper()

    if "HTTP 404" in error:
        return "TEST_DATA"

    if "HTTP 401" in error or "HTTP 403" in error:
        return "AUTH"

    if "HTTP 500" in error or "HTTP 503" in error:
        return "SERVICE"

    if "ASSERTIONERROR" in error:
        return "ASSERTION"

    return "GENERAL"

def investigate_failure(failure: dict) -> InvestigationState:

    state = InvestigationState(
        test_name=failure["test_name"],
        error=failure["error"]
    )

    transition_state(state, "IN_PROGRESS")
    state.route = determine_route(state.error)
    try:
        diagnostics = collect_diagnostics(state.route, state.error)

        state.tool_results.append({
            "tool": "collect_diagnostics",
            "result": diagnostics
        })
        state.completed_steps.append("DIAGNOSTICS")
    except Exception as exc:
        state.errors.append(f"DIAGNOSTICS_FAILED: {exc}") 
    try:
        result = analyse_failure_with_rag(
            failure,
            evaluate=True
        )

        if result is None:
            state.errors.append("AI analysis not generated")
            transition_state(state, "FAILED")
            return state

        state.retrieved_defects = result["retrieved_defects"]
        state.analysis = result["analysis"]
        state.grounding_evaluation = result["grounding_evaluation"]
        state.completed_steps.append("AI_ANALYSIS")
        transition_state(state, "COMPLETED")

    except Exception as exc:
        state.errors.append(str(exc))
        transition_state(state, "FAILED")

    return state