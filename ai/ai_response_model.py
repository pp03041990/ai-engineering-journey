from pydantic import BaseModel, Field

class AIAnalysis(BaseModel):
    likely_cause:str
    debugging_steps:list[str] = Field(min_length=1)
    defect_type:str