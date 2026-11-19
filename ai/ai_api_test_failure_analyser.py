from openai import OpenAI
import json
from .ai_test_helper import ai_response_validator
from .retry import retry_llm_call
from .ai_response_model import AIAnalysis
from pydantic import ValidationError
from .qa_tools import lookup_error_pattern

TOOLS = [
    {
        "type": "function",
        "name": "lookup_error_pattern",
        "description": "Look up common causes of a QA test error.",
        "parameters": {
            "type": "object",
            "properties": {
                "error_type": {"type": "string"}
            },
            "required": ["error_type"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


def dispatch_tool(name: str, arguments: dict) -> dict:
    if name != "lookup_error_pattern":
        return {
            "error": True,
            "message": f"Unsupported tool: {name}"
        }

    if (
        not isinstance(arguments, dict)
        or set(arguments) != {"error_type"}
        or not isinstance(arguments["error_type"], str)
    ):
        return {
            "error": True,
            "message": "Invalid arguments for lookup_error_pattern"
        }

    try:
        return lookup_error_pattern(**arguments)
    except Exception:
        return {
            "error": True,
            "message": "Tool execution failed. No result is available."
        }

client = OpenAI()

def ai_analyse_failure(failure_details):
    MAX_TOOL_ROUNDS = 5
    try:
        instructions = """
        You are a QA automation assistant.
        Analyse test failures objectively.
        Do not assume every failure is an application defect.

        Use lookup_error_pattern when helpful.
        If a tool returns an error, do not invent its result.
        Continue your analysis using the original failure details
        and clearly state any uncertainty.

        Return the final analysis as a valid JSON object
        containing:
        - likely_cause: string
        - debugging_steps: array of strings
        - defect_type: string
        """

        response = retry_llm_call(
            lambda: client.responses.create(
                model="gpt-5.5",
                instructions=instructions,
                input=(
                    "Return the analysis in JSON format.\n\n"
                    f"{failure_details}"
                ),
                tools=TOOLS,
                text={"format": {"type": "json_object"}},
            )
        )
        # tool calling loop: Agent Loop
        for _ in range(MAX_TOOL_ROUNDS):
            function_calls = [
                item for item in response.output
                if item.type == "function_call"
            ]

            if not function_calls:
                break

            outputs = []

            for call in function_calls:
                try:
                    print("Tool requested:", call.name)
                    arguments = json.loads(call.arguments)
                    print("Tool arguments:", arguments)
                except json.JSONDecodeError:
                    result = {
                        "error": True,
                        "message": "Invalid JSON tool arguments"
                    }
                else:
                    result = dispatch_tool(call.name, arguments)
                
                print("Tool result:", result)
                outputs.append({
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(result),
                })

            response = retry_llm_call(
                lambda: client.responses.create(
                    model="gpt-5.5",
                    instructions=instructions,
                    previous_response_id=response.id,
                    input=outputs,
                    tools=TOOLS,
                    text={"format": {"type": "json_object"}},
                )
            )
            
        else:
            # Check the final response before declaring the limit exceeded.
            if any(
                item.type == "function_call"
                for item in response.output
            ):
                raise RuntimeError("Agent exceeded maximum tool rounds")


        analysis_data = json.loads(response.output_text)
        analysis = AIAnalysis.model_validate(analysis_data)

        return analysis.model_dump()

    except (ValidationError, json.JSONDecodeError) as exc:
        print(f"AI response not valid {exc}")
        return None

    except (RuntimeError) as exc:
            print(f"AI response not valid {exc}")
            return None
        
    except Exception as exc:
        print(f"AI analysis not available {exc}")
        return None