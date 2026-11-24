from pydantic import BaseModel, Field
from typing import Literal

class InvestigationState(BaseModel):
    test_name: str
    error: str
    retrieved_defects: list[dict] = Field(default_factory=list)
    tool_results: list[dict] = Field(default_factory=list)
    analysis: dict | None = None
    status: Literal[
        "NEW",
        "IN_PROGRESS",
        "COMPLETED",
        "FAILED"
    ] = "NEW"
    errors: list[str] = Field(default_factory=list)
    grounding_evaluation: dict | None = None
    route: Literal[
        "TEST_DATA", "AUTH", "SERVICE", "ASSERTION", "GENERAL"
    ] | None = None
    completed_steps: list[str] = Field(default_factory=list)
    evidence: dict = Field(default_factory=dict)

if __name__ == "__main__":
    state = InvestigationState(test_name="Test001",error="Test failed with error 503")
    print(state)