
import pytest

from ai.investigation_orchestrator import investigate_failure

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    failure = {
        "test_name": item.nodeid,
        "error": report.longreprtext
    }
    state = investigate_failure(failure)
    if state.status == "FAILED":
        print(f"\nAI investigation failed: {state.errors}")
        return

    analysis = state.analysis
    evaluation = state.grounding_evaluation
    retrieved_defects = state.retrieved_defects
    print("\n===== INVESTIGATION SUMMARY =====")
    print(f"Test: {state.test_name}")
    print(f"Route: {state.route}")
    print(f"Status: {state.status}")
    print(f"Completed steps: {state.completed_steps}")
    print(f"Errors: {state.errors}")

    print("\n===== RETRIEVED HISTORICAL DEFECTS =====")

    for defect in retrieved_defects:
        print(f"{defect['id']}: {defect['description']}")

    print("\n===== AI FAILURE ANALYSIS =====")

    print(f"\nLikely cause:\n{analysis['likely_cause']}")

    print("\nDebugging steps:")
    for step in analysis["debugging_steps"]:
        print(f"- {step}")

    print(f"\nDefect type:\n{analysis['defect_type']}")

    print("\n===== GROUNDING EVALUATION =====")

    print(f"\nIs grounded: {evaluation['is_grounded']}")

    print("\nUnsupported claims:")
    for claim in evaluation["unsupported_claims"]:
        print(f"- {claim}")

    print(f"\nExplanation:\n{evaluation['explanation']}")
