from pathlib import Path

import chromadb
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "chrome_db"

chroma_client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

collection = chroma_client.get_collection(
    name="loan_api_defects"
)

openai_client = OpenAI()

print("Stored defects:", collection.count())

def generate_query_embedding(failure: str) -> list[float]:
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=failure
    )
    return response.data[0].embedding

def retrieve_similar_defects(
    failure: str,
    service: str | None = None,
    top_k: int = 3,
) -> list[dict]:

    query_embedding = generate_query_embedding(failure)
    where_filter = (
                    {"service":service} 
                    if service is not None 
                    else None
                    )
    response = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
        where = where_filter
    )

    matches = []

    for defect_id, description, metadata, distance in zip(
        response["ids"][0],
        response["documents"][0],
        response["metadatas"][0],
        response["distances"][0]
    ):
        matches.append({
            "id": defect_id,
            "description": description,
            "metadata": metadata,
            "similarity": round(1 - distance, 4)
        })

    return matches


if __name__ == "__main__":

    new_failure = "Loan approval API returned HTTP 503"

    matches = retrieve_similar_defects(
        failure=new_failure,
        service = "loan",
        top_k=3
    )

    for match in matches:
        print(match)