from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field
from ai.ai_api_test_failure_analyser import ai_analyse_failure
app=FastAPI()
class FailureRequest(BaseModel):
    failure_details: str = Field(min_length=10)
    
@app.get("/health")
def health_check():
    return {"status":"ok"}

@app.get("/version")
def version_check():
    return {
        "application": "AI Failure Analyser",
        "version":"1.0"
    }

@app.post("/analyse-failure")
def analyse_failure(request:FailureRequest):
    result = ai_analyse_failure(request.failure_details)
    if(result == None):
        raise HTTPException(
        status_code=503,
        detail="AI analysis service unavailable"
    )
    return result