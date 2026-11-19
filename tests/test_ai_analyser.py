import json
from unittest.mock import call, patch, Mock

from openai import (APITimeoutError,BadRequestError)
import pytest
from ai.ai_api_test_failure_analyser import ai_analyse_failure

# fake_output = """
# {
#     "likely_cause": "API returned 404",
#     "debugging_steps": 
#         [
#             "Check the booking ID",
#             "Verify the endpoint"
#         ],
#     "defect_type": "Test data issue"
# }
# """
# def test_ai_analyser():
#     # Create a fake API response
#     mock_response= Mock()
#     mock_response.output_text=fake_output
#     mock_response.output = []

#     # Replace the real OpenAI API call with our mock
#     with patch(
#         "ai.ai_api_test_failure_analyser.client.responses.create",
#         return_value=mock_response,
#     ) as mock_create:
#         result = ai_analyse_failure("Test failed with 404")
#     assert result is not None
#     mock_create.assert_called_once()
        
# def test_ai_analyser_retries_on_timeout():
#     with patch(
#             "ai.ai_api_test_failure_analyser.client.responses.create",
#             side_effect=APITimeoutError(request=None),
#         ) as mock_create:
#             result = ai_analyse_failure("Test failed with 404")
#             assert result is None
#             assert mock_create.call_count == 3
            
# def test_ai_analyser_does_not_retry_on_bad_request():
#     with patch(
#             "ai.ai_api_test_failure_analyser.client.responses.create",
#             side_effect=BadRequestError(
#                     "Bad Request",
#                     response=Mock(status_code=400),
#                     body={"error": {"message": "Invalid request"}},
#                 )
#         ) as mock_create:
#             result = ai_analyse_failure("Test failed with 404")
#             assert result is None
#             assert mock_create.call_count == 1

# import json
# from unittest.mock import Mock, patch

# def test_ai_analyser_tool_calling():

#     tool_call = Mock()
#     tool_call.type = "function_call"
#     tool_call.name = "lookup_error_pattern"
#     tool_call.arguments = '{"error_type": "HTTP 404"}'
#     tool_call.call_id = "call_001"

#     res1 = Mock()
#     res1.id = "resp_001"
#     res1.output = [tool_call]

#     res2 = Mock()
#     res2.id = "resp_002"
#     res2.output = []
#     res2.output_text = json.dumps({
#         "likely_cause": "API returned 404",
#         "debugging_steps": ["Verify booking ID"],
#         "defect_type": "POSSIBLE_TEST_DATA_ISSUE"
#     })

#     with patch(
#         "ai.ai_api_test_failure_analyser.client.responses.create"
#     ) as mock_create, patch(
#         "ai.ai_api_test_failure_analyser.dispatch_tool"
#     ) as mock_dispatch:

#         mock_create.side_effect = [res1, res2]
#         mock_dispatch.return_value = {
#             "possible_causes": ["No known pattern found"]
#         }

#         result = ai_analyse_failure("Test failed with 404")

#         assert result is not None
#         assert mock_create.call_count == 2

#         mock_dispatch.assert_called_once_with(
#             "lookup_error_pattern",
#             {"error_type": "HTTP 404"}
#         )

#         second_call = mock_create.call_args_list[1].kwargs

#         assert second_call["previous_response_id"] == "resp_001"

#         tool_outputs = second_call["input"]

#         assert len(tool_outputs) == 1
#         assert tool_outputs[0]["type"] == "function_call_output"
#         assert tool_outputs[0]["call_id"] == "call_001"

#         tool_result = json.loads(tool_outputs[0]["output"])

#         assert tool_result["possible_causes"] == [
#             "No known pattern found"
#         ]

#         assert result["defect_type"] == "POSSIBLE_TEST_DATA_ISSUE"
#         assert result["likely_cause"] == "API returned 404"

# def test_ai_analyser_multiple_tool_calls():
#     tool1 = Mock(
#         type="function_call",
#         name="lookup_error_pattern",
#         arguments='{"error_type": "HTTP 404"}',
#         call_id="call_001"
#     )

#     tool2 = Mock(
#         type="function_call",
#         name="lookup_error_pattern",
#         arguments='{"error_type": "HTTP 503"}',
#         call_id="call_002"
#     )

#     tool3 = Mock(
#         type="function_call",
#         name="lookup_error_pattern",
#         arguments='{"error_type": "HTTP 500"}',
#         call_id="call_003"
#     )
#     tool1.name = "lookup_error_pattern"
#     tool2.name = "lookup_error_pattern"
#     tool3.name = "lookup_error_pattern"
#     res1 = Mock()
#     res1.output = [tool1,tool2,tool3]
#     res1.id = "123"
    
#     res2 = Mock()
#     res2.id = "resp_002"
#     res2.output = []
#     res2.output_text = json.dumps({
#         "likely_cause": "API returned 404",
#         "debugging_steps": ["Verify booking ID"],
#         "defect_type": "POSSIBLE_TEST_DATA_ISSUE"
#     })
#     with patch(
#         "ai.ai_api_test_failure_analyser.client.responses.create"
#     ) as mock_create, patch(
#         "ai.ai_api_test_failure_analyser.dispatch_tool"
#     ) as mock_dispatch:
#         mock_dispatch.side_effect = [
#             {"possible_causes": ["No known pattern found"]}
#         ] * 3
#         mock_create.side_effect = [res1, res2]
#         result = ai_analyse_failure("Test failed with 404")
#         assert result is not None
#         assert mock_create.call_count == 2
#         assert mock_dispatch.call_count == 3
#         assert mock_dispatch.call_args_list == [
#             call("lookup_error_pattern", {"error_type": "HTTP 404"}),
#             call("lookup_error_pattern", {"error_type": "HTTP 503"}),
#             call("lookup_error_pattern", {"error_type": "HTTP 500"}),
#         ]
#         second_call = mock_create.call_args_list[1].kwargs

#         assert second_call["previous_response_id"] == "123"

#         tool_outputs = second_call["input"]

#         assert len(tool_outputs) == 3
#         assert tool_outputs[0]["type"] == "function_call_output"
#         assert tool_outputs[0]["call_id"] == "call_001"
#         assert tool_outputs[1]["type"] == "function_call_output"
#         assert tool_outputs[1]["call_id"] == "call_002"
#         assert tool_outputs[2]["type"] == "function_call_output"
#         assert tool_outputs[2]["call_id"] == "call_003"
#         tool_result = json.loads(tool_outputs[0]["output"])

#         assert tool_result["possible_causes"] == [
#             "No known pattern found"
#         ]

#         assert result["defect_type"] == "POSSIBLE_TEST_DATA_ISSUE"
#         assert result["likely_cause"] == "API returned 404"

# def test_ai_analyser_unauthorized_tool():
#     tool1 = Mock(
#         type="function_call",
#         name="delete_all_the_bookings",
#         arguments='{"error_type": "HTTP 404"}',
#         call_id="call_001"
#     )
#     tool1.name = "delete_all_the_bookings"
#     res1 = Mock()
#     res1.output = [tool1]
#     res2 = Mock()
#     res2.output = []
#     res2.output_text = json.dumps({
#         "likely_cause": "Unable to verify the failure",
#         "debugging_steps": ["Investigate the original API error"],
#         "defect_type": "UNKNOWN"
#     })
#     with patch(
#         "ai.ai_api_test_failure_analyser.client.responses.create"
#     ) as mock_create:
#         mock_create.side_effect = [res1, res2]
#         result = ai_analyse_failure("Booking API returned HTTP 404")
#         assert result is not None
#         assert result["likely_cause"] == "Unable to verify the failure"
#         second_LLM_call_first_output = mock_create.call_args_list[1].kwargs["input"][0]
#         assert json.loads(second_LLM_call_first_output["output"]) == {
#             "error": True, "message": f"Unsupported tool: {tool1.name}"
#         }

# def test_ai_analyser_exceeds_max_tool_rounds():
#     tool_call = Mock()
#     tool_call.type = "function_call"
#     tool_call.name = "lookup_error_pattern"
#     tool_call.arguments = '{"error_type": "HTTP 404"}'
#     tool_call.call_id = "call_001"

#     response = Mock()
#     response.id = "resp_001"
#     response.output = [tool_call]
#     with patch(
#         "ai.ai_api_test_failure_analyser.client.responses.create"
#     ) as mock_create, patch(
#         "ai.ai_api_test_failure_analyser.dispatch_tool"
#     ) as mock_dispatch:

#         mock_create.return_value = response
#         mock_dispatch.return_value = {"possible_causes": []}

#         result = ai_analyse_failure("Booking API returned 404")

#         assert mock_create.call_count == 6
#         assert mock_dispatch.call_count == 5

# @pytest.mark.parametrize("arguments", [
#     {"wrong_field": "HTTP 404"},
#     {},
#     {"error_type": 404},
#     {"error_type": "HTTP 404", "extra": 1},
# ])
# def test_dispatch_tool_invalid_arguments(arguments):
#     tool1 = Mock(
#         type="function_call",
#         name="lookup_error_pattern",
#         arguments=json.dumps(arguments),
#         call_id="call_001"
#     )
#     tool1.name = "lookup_error_pattern"
#     res1 = Mock()
#     res1.output = [tool1]
#     res2 = Mock()
#     res2.output = []
#     res2.output_text = json.dumps({
#         "likely_cause": "Unable to verify the failure",
#         "debugging_steps": ["Investigate the original API error"],
#         "defect_type": "UNKNOWN"
#     })
#     with patch(
#         "ai.ai_api_test_failure_analyser.client.responses.create"
#     ) as mock_create,patch(
#         "ai.qa_tools.lookup_error_pattern"
#     ) as mock_lookup:
#         mock_create.side_effect = [res1, res2]
#         result = ai_analyse_failure("Booking API returned HTTP 404")
#         assert result is not None
#         results_of_req1= mock_create.call_args_list[1].kwargs["input"]
#         assert json.loads(results_of_req1[0].get("output"))== {
#             "error": True,
#             "message": "Invalid arguments for lookup_error_pattern"
#         }
#         mock_lookup.assert_not_called()
        
import json
from unittest.mock import Mock, patch

def test_dispatch_tool_failure():
    # LLM requests a tool
    tool1 = Mock()
    tool1.type = "function_call"
    tool1.name = "lookup_error_pattern"
    tool1.arguments = '{"error_type": "HTTP 404"}'
    tool1.call_id = "call_001"

    # First LLM response: tool request
    res1 = Mock()
    res1.id = "resp_001"
    res1.output = [tool1]

    # Second LLM response: final analysis
    res2 = Mock()
    res2.output = []
    res2.output_text = json.dumps({
        "likely_cause": "Unable to verify the failure",
        "debugging_steps": ["Investigate the original API error"],
        "defect_type": "UNKNOWN"
    })

    with patch(
        "ai.ai_api_test_failure_analyser.client.responses.create"
    ) as mock_create, patch(
        "ai.ai_api_test_failure_analyser.lookup_error_pattern"
    ) as mock_lookup:

        mock_create.side_effect = [res1, res2]
        mock_lookup.side_effect = RuntimeError("Tool failed")

        result = ai_analyse_failure("Booking API returned HTTP 404")

        # Verify underlying tool was executed
        mock_lookup.assert_called_once_with(error_type="HTTP 404")

        # Verify two LLM calls
        assert mock_create.call_count == 2

        # Verify tool failure was forwarded to LLM
        second_input = mock_create.call_args_list[1].kwargs["input"]

        assert len(second_input) == 1
        assert second_input[0]["type"] == "function_call_output"
        assert second_input[0]["call_id"] == "call_001"

        tool_result = json.loads(second_input[0]["output"])

        assert tool_result == {
            "error": True,
            "message": "Tool execution failed. No result is available."
        }

        # Verify agent recovered and returned final analysis
        assert result is not None
        assert result["likely_cause"] == "Unable to verify the failure"
        assert result["defect_type"] == "UNKNOWN"
