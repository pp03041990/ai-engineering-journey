def collect_diagnostics(route: str, error: str) -> dict:
    diagnostics = {
        "route": route,
        "error": error,
        "checks": []
    }

    if route == "TEST_DATA":
        diagnostics["checks"].append("Verify resource exists")

    elif route == "AUTH":
        diagnostics["checks"].append("Verify token and permissions")

    elif route == "SERVICE":
        diagnostics["checks"].append("Check service health and logs")

    elif route == "ASSERTION":
        diagnostics["checks"].append("Compare expected and actual values")

    else:
        diagnostics["checks"].append("Inspect failure details")

    return diagnostics