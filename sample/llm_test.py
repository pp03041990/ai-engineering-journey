
from openai import OpenAI
import json
client = OpenAI()

response = client.responses.create(
    model="gpt-5.5",
    instructions=(
        "You are a QA automation assistant. "
        "Analyze API test failures objectively. "
        "Do not assume every test failure is an application defect."
    ),
    input="""
    Analyze this API test failure:

    Test: test_existing_booking
    Method: GET
    Endpoint: /booking/99999999
    Expected status: 200
    Actual status: 404

    Return a JSON object with:`
    - likely_cause: string
    - debugging_steps: array of two strings
    - is_definitely_a_bug: boolean
    """,
    text={
        "format": {
            "type": "json_object"
        }
    }
)
analysis=json.loads(response.output_text)
print(f" likely cause : {analysis["likely_cause"]}")
debugging_steps=analysis["debugging_steps"]
for step in debugging_steps:
        print(step)
print(f"is definitely a bug? {analysis["is_definitely_a_bug"]}")
# Validate the response structure
assert isinstance(analysis["likely_cause"], str)
assert len(analysis["debugging_steps"]) == 2
assert isinstance(analysis["is_definitely_a_bug"], bool)

print("JSON validation passed!")