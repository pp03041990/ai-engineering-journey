from openai import OpenAI
import numpy as np
from embeddings.first_embedding import cosine_similarity

client = OpenAI()

historical_defects = [
    {
        "id": "DEF-101",
        "description": "Loan eligibility API returned HTTP 503",
        "severity": "medium",
        "service": "loan",
        "http_status": 503
    },
    {
        "id": "DEF-102",
        "description": "Loan approval service temporarily unavailable",
         "severity": "medium",
         "service": "loan"
    },
    {
        "id": "DEF-103",
        "description": "Customer email format validation failed",
         "severity": "low",
         "service": "domain",
    },
    {
        "id": "DEF-104",
        "description": "Loan EMI calculation returned incorrect amount",
         "severity": "high",
         "service": "loan"
    },
    {
        "id": "DEF-105",
        "description": "Risk assessment endpoint request timed out",
        "severity": "medium",
        "service": "risk"
    },
    {
        "id": "DEF-106",
        "description": "Risk assessment endpoint returned forbidden",
        "severity": "medium",
        "service": "risk",
        "http_status": 403
    },
    {
        "id": "DEF-107",
        "description": "Booking api returned 404",
        "severity": "medium",
        "service": "booking",
        "http_status": 404
    }
]

additional_defects = [
    {
        "id": "DEF-108",
        "description": "Loan eligibility API returned HTTP 503 due to downstream service unavailability",
        "severity": "high",
        "service": "loan",
        "http_status": 503
    },
    {
        "id": "DEF-109",
        "description": "Loan eligibility endpoint returned HTTP 500 when applicant income was missing",
        "severity": "high",
        "service": "loan",
        "http_status": 500
    },
    {
        "id": "DEF-110",
        "description": "Loan approval API returned HTTP 504 gateway timeout",
        "severity": "high",
        "service": "loan",
        "http_status": 504
    },
    {
        "id": "DEF-111",
        "description": "Loan approval request failed because the underwriting service was unavailable",
        "severity": "high",
        "service": "loan",
        "http_status": 503
    },
    {
        "id": "DEF-112",
        "description": "Loan EMI calculation returned incorrect monthly installment for zero interest rate",
        "severity": "high",
        "service": "loan"
    },
    {
        "id": "DEF-113",
        "description": "Loan EMI calculation produced incorrect rounding for long tenure loans",
        "severity": "medium",
        "service": "loan"
    },
    {
        "id": "DEF-114",
        "description": "Loan eligibility API approved an applicant whose income was below the minimum threshold",
        "severity": "critical",
        "service": "loan"
    },
    {
        "id": "DEF-115",
        "description": "Risk assessment API timed out while calculating applicant credit risk",
        "severity": "high",
        "service": "risk"
    },
    {
        "id": "DEF-116",
        "description": "Risk scoring service returned HTTP 503 during peak traffic",
        "severity": "high",
        "service": "risk",
        "http_status": 503
    },
    {
        "id": "DEF-117",
        "description": "Risk assessment endpoint returned HTTP 403 for a user with valid permissions",
        "severity": "high",
        "service": "risk",
        "http_status": 403
    },
    {
        "id": "DEF-118",
        "description": "Risk score was incorrectly calculated for applicants with no credit history",
        "severity": "high",
        "service": "risk"
    },
    {
        "id": "DEF-119",
        "description": "Customer registration API accepted an invalid email address",
        "severity": "medium",
        "service": "domain"
    },
    {
        "id": "DEF-120",
        "description": "Customer email validation rejected valid addresses containing plus signs",
        "severity": "medium",
        "service": "domain"
    },
    {
        "id": "DEF-121",
        "description": "Booking API returned HTTP 404 when retrieving an existing booking",
        "severity": "high",
        "service": "booking",
        "http_status": 404
    },
    {
        "id": "DEF-122",
        "description": "Booking details endpoint returned HTTP 404 after successful booking creation",
        "severity": "high",
        "service": "booking",
        "http_status": 404
    },
    {
        "id": "DEF-123",
        "description": "Booking API returned HTTP 500 when booking dates were invalid",
        "severity": "medium",
        "service": "booking",
        "http_status": 500
    },
    {
        "id": "DEF-124",
        "description": "Booking cancellation API returned HTTP 409 for an already cancelled booking",
        "severity": "low",
        "service": "booking",
        "http_status": 409
    },
    {
        "id": "DEF-125",
        "description": "Loan approval API created duplicate approval records after request retries",
        "severity": "critical",
        "service": "loan"
    }
]

historical_defects.extend(additional_defects)

print(f"Total historical defects: {len(historical_defects)}")


def getDescriptions(historical_defects):
    return [defect["description"] for defect in historical_defects]

def callEmbeddingModel(description):
    response = client.embeddings.create(
            model='text-embedding-3-small' ,
            input= description
        )
    return response

def createEmbeddings(historical_defects):
    if not historical_defects:
        return []
    descriptions = getDescriptions(historical_defects)
    response = callEmbeddingModel(descriptions)
    defect_embeddings = [item.embedding for item in sorted(response.data,key = lambda x:x.index)]
    return defect_embeddings

def search_similar_defects(new_failure, historical_defects, top_k=3):
        defect_embeddings = createEmbeddings(historical_defects)
        query_response = client.embeddings.create(
            model="text-embedding-3-small",
            input=new_failure
        )

        query_embedding = query_response.data[0].embedding

        results = []

        for defect, embedding in zip(
            historical_defects,
            defect_embeddings
        ):
            score = cosine_similarity(
                query_embedding,
                embedding
            )

            results.append({
                "id": defect["id"],
                "description": defect["description"],
                "similarity": float(score)
            })
        ranked_results = sorted(
            results,
            key=lambda item: item['similarity'],
            reverse= True
        )

        return ranked_results[:top_k]  


