APPROVED_TESTS = {
    "booking_api": {
        "framework": "pytest",
        "test_path": "tests/test_booking_api.py"
    },
    "eventhub_ui": {
        "framework": "playwright",
        "test_path": "tests/login.spec.ts",
        "project_dir": "/Users/manishpushkar/Documents/work-pp/playwright-demo-project"
    }
}
def get_approved_test(test_name: str) -> dict:
    if test_name not in APPROVED_TESTS:
        raise ValueError(f"Test not approved: {test_name}")

    return APPROVED_TESTS[test_name]