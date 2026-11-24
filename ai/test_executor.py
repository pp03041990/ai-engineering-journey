import subprocess
import sys,os
from ai.test_registry import get_approved_test
from ai.evidence_collector import collect_playwright_evidence

import os
import sys
import subprocess

from ai.test_registry import get_approved_test
import re

def extract_failure_details(stdout: str) -> dict:
    evidence = {
        "test_id": None,
        "expected_status": None,
        "actual_status": None,
        "assertion_message": None,
        "failure_details": None
    }

    match = re.search(
        r"={3,}\s+FAILURES\s+={3,}(.*?)(?=\n={3,}\s+(?:warnings summary|short test summary info)\s+={3,}|\Z)",
        stdout,
        re.DOTALL | re.IGNORECASE
    )

    if not match:
        return evidence

    failure = match.group(1).strip()

    evidence["failure_details"] = failure

    test_match = re.search(
        r"_{3,}\s+(test_[^\n]+?)\s+_{3,}",
        failure
    )

    if test_match:
        evidence["test_id"] = test_match.group(1)

    status_match = re.search(
        r"assert\s+(\d{3})\s*==\s*(\d{3})",
        failure
    )

    if status_match:
        evidence["actual_status"] = int(status_match.group(1))
        evidence["expected_status"] = int(status_match.group(2))
        evidence["assertion_message"] = status_match.group(0)

    return evidence

import json

def extract_playwright_results(stdout: str) -> dict:
    report = json.loads(stdout)

    tests = []

    def collect(suites):
        for suite in suites:
            for spec in suite.get("specs", []):
                for test in spec.get("tests", []):
                    results = test.get("results", [])
                    errors = [
                        err.get("message", "")
                        for result in results
                        for err in result.get("errors", [])
                    ]

                    tests.append({
                        "test_name": spec["title"],
                        "test_id": test.get("id"),
                        "status": (
                            "PASSED" if test.get("status") == "expected"
                            else "FAILED" if test.get("status") == "unexpected"
                            else "SKIPPED" if test.get("status") == "skipped"
                            else "UNKNOWN"
                        ),
                        "errors": errors
                    })

            collect(suite.get("suites", []))

    collect(report.get("suites", []))

    return {
        "total": len(tests),
        "passed": sum(t["status"] == "PASSED" for t in tests),
        "failed": sum(t["status"] == "FAILED" for t in tests),
        "skipped": sum(t["status"] == "SKIPPED" for t in tests),
        "unknown": sum(t["status"] == "UNKNOWN" for t in tests),
        "tests": tests
    }


def execute_test(test_name: str) -> dict:
    config = get_approved_test(test_name)

    if config["framework"] == "pytest":
        command = [
            sys.executable, "-m", "pytest",
            config["test_path"], "-v"
        ]

    elif config["framework"] == "playwright":
        command = [
            "npx", "--no-install", "playwright",
            "test", config["test_path"],
            "--reporter=json"
        ]

    else:
        raise ValueError("Unsupported test framework")

    env = os.environ.copy()

    if config["framework"] == "pytest":
        env["AI_AGENT_MANAGED_RUN"] = "1"

    try:
        result = subprocess.run(
            command,
            cwd=config.get("project_dir"),
            capture_output=True,
            text=True,
            timeout=120,
            shell=False,
            env=env  # FIX 1: Prevent duplicate AI investigations
        )

        if result.returncode == 0:
            status = "PASSED"
        elif result.returncode == 1:
            status = "FAILED"
        else:
            status = "ERROR"

        evidence = {}

        if config["framework"] == "playwright":
            evidence = collect_playwright_evidence(config["project_dir"])
            evidence["test_results"] = extract_playwright_results(result.stdout)

        elif config["framework"] == "pytest":
            evidence = (
                extract_failure_details(result.stdout)
                if status == "FAILED"
                else {}
            )

        return {
            "test_name": test_name,
            "framework": config["framework"],
            "status": status,
            "exit_code": result.returncode,
            "stdout": result.stdout if config["framework"] == "pytest" else None,
            "stderr": result.stderr,
            "evidence": evidence  # FIX 2: No duplicate failure_details
        }

    except subprocess.TimeoutExpired as exc:
        return {
            "test_name": test_name,
            "framework": config["framework"],
            "status": "TIMEOUT",
            "exit_code": None,
            "stdout": (
                exc.stdout.decode(errors="replace")
                if isinstance(exc.stdout, bytes)
                else (exc.stdout or "")
            ),
            "stderr": (
                exc.stderr.decode(errors="replace")
                if isinstance(exc.stderr, bytes)
                else (exc.stderr or "")
            ),
            "error": "Test execution exceeded 120 seconds",
            "evidence": {}
        }

    except OSError as exc:
        return {
            "test_name": test_name,
            "framework": config["framework"],
            "status": "ERROR",
            "exit_code": None,
            "stdout": "",
            "stderr": "",
            "error": str(exc),
            "evidence": {}
        }
        
        
if __name__ == "__main__":
    result = execute_test("eventhub_ui")
    print(result["status"])
    print(result["evidence"])
    if result["status"] == "FAILED":
        failure = {
            "test_name": result["test_name"],
            "error": result["failure_details"]
        }
