import pytest
from ai.ai_api_test_failure_analyser import ai_analyse_failure
import requests
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome=yield
    report = outcome.get_result()
    if report.when == 'call' and report.failed:
        failure_details= f"""
        test name: {item.nodeid},
        failure details: {report.longreprtext}
        Analyze the failure and return:
        - likely_cause: string
        - debugging_steps: array of two strings
        - defect_type: string
        """
        analysis=ai_analyse_failure(failure_details)
        # try:
        #     response=requests.post(
        #         "http://127.0.0.1:8000/analyse-failure",
        #         json={
        #         "failure_details": failure_details
        #     },
        #     timeout=30  
        #     )
        #     if response.status_code == 200:
        #         analysis = response.json()
        #         print(f"likely_cause : \n{analysis['likely_cause']}")
        #         print("Debugging steps \n")
        #         debugging_steps=analysis["debugging_steps"]
        #         for step in debugging_steps:
        #                 print(step)
        #         print(f"defect_type : \n{analysis['defect_type']}")
        #     elif response.status_code == 503:
        #         print("AI analysis unavailable. Skipping AI report.")
        #     else:
        #         print(
        #             f"\n AI analysis returned "
        #             f"{response.status_code}"
        #         )
        # except requests.exceptions.RequestException as exc:
        #     print(f"AI analysis unavailable {exc}")
        if analysis is not None:
            print(f"likely_cause : \n{analysis['likely_cause']}")
            print("Debugging steps \n")
            debugging_steps=analysis["debugging_steps"]
            for step in debugging_steps:
                    print(step)
            print(f"defect_type : \n{analysis['defect_type']}")
        else:
            print("AI analysis not generated")
        
