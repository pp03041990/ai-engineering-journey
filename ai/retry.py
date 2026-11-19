import time
from openai import APIConnectionError,APITimeoutError

def retry_operation(operation):
    for attempt in range(3):
        try:
            return operation()

        except Exception:
            if attempt == 2:
                raise
            delay= 2 ** attempt 
            time.sleep(delay)


def retry_llm_call(operation):
    for attempt in range(3):
        try:
            return operation()

        except (APIConnectionError, APITimeoutError):
            if attempt == 2:
                raise

            delay = 2 ** attempt
            time.sleep(delay)
