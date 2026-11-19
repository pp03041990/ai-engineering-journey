import pytest
from rag.rag_pipeline import analyse_failure_with_rag


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

    
    try:
        result = analyse_failure_with_rag(
            failure,
            evaluate=True
        )

        if result is None:
            print("\nAI analysis not generated")
            return

        analysis = result["analysis"]
        evaluation = result["grounding_evaluation"]
        retrieved_defects = result["retrieved_defects"]

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

    except Exception as exc:
        print(f"\nAI analysis unavailable: {exc}")
