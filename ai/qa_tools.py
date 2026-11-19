def lookup_error_pattern(error_type: str) -> dict:
    patterns = {
        "TimeoutError": {
            "possible_causes": [
                "Element was not actionable",
                "Locator did not match the expected element"
            ]
        },
        "AssertionError": {
            "possible_causes": [
                "Actual result differed from expected result"
            ]
        }
    }

    return patterns.get(
        error_type,
        {"possible_causes": ["No known pattern found"]}
    )