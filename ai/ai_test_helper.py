def ai_response_validator(response:dict)->bool:
    if not isinstance(response.get("likely_cause"),str):
        raise ValueError("likely_cause should be a string")
    if not isinstance(response.get("debugging_steps"),list):
        raise ValueError("debugging_steps should be a list")
    if not response["debugging_steps"]:
        raise ValueError("debugging_steps must not be empty")
    if not all(
        isinstance(step,str)
        for step in response.get("debugging_steps")
    ):
        raise ValueError("debugging steps should be a string")
    if not isinstance(response.get("defect_type"),str):
            raise ValueError("defect_type should be a string")
    return True