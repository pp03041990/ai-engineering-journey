from ai.test_executor import execute_test
from ai.investigation_orchestrator import investigate_failure

from ai.test_executor import execute_test
from ai.investigation_orchestrator import investigate_failure

import json
from pathlib import Path
from datetime import datetime, timezone


def run_test_agent(test_name: str) -> dict:
    execution = execute_test(test_name)

    report = {
        "execution": execution,
        "investigation": None
    }

    if execution["status"] != "FAILED":
        return report

    evidence = execution.get("evidence", {})

    failure = {
        "test_name": test_name,
        "error": (
            evidence.get("failure_details")
            or str(evidence.get("test_results", {}).get("tests", []))[:3000]
            or (execution.get("stdout") or "")[-3000:]
        )
    }

    state = investigate_failure(failure)

    investigation = state.model_dump()

    # Avoid duplicating evidence in the final report
    investigation.pop("evidence", None)
    investigation.pop("error", None)

    report["investigation"] = investigation

    return report

def save_report(report: dict) -> str:
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    report_path = output_dir / f"ai_test_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, indent=2, default=str),
        encoding="utf-8"
    )

    return str(report_path)

if __name__=="__main__":
    report = run_test_agent("booking_api")

    path = save_report(report)

    print("Execution:", report["execution"]["status"])
    print("Report saved:", path)

    if report["investigation"]:
        print("Investigation:", report["investigation"]["status"])
        print("Route:", report["investigation"]["route"])