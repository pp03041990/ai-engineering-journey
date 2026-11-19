import chromadb
from embeddings.semantic_search import (createEmbeddings,historical_defects,getDescriptions,callEmbeddingModel)
client = chromadb.PersistentClient(
    path = "./chrome_db"
)
print("chromaDB client created")

collection = client.get_or_create_collection(
    name="loan_api_defects",
    metadata={"hnsw:space": "cosine"}
)
print("collection name : ",collection.name)
print("collection count : ",collection.count())
embeddings=createEmbeddings(historical_defects)
collection.upsert(
    ids=[defect["id"] for defect in historical_defects],
    documents=getDescriptions(historical_defects),
    embeddings=embeddings,
    metadatas=[
        {
            key: value
            for key, value in defect.items()
            if key not in ("id", "description")
        }
        for defect in historical_defects
    ]
)

print("Stored defects:", collection.count())

new_failure = "Loan approval API returned HTTP 503"
response = callEmbeddingModel(new_failure)
embedding_new_failure=response.data[0].embedding
result=collection.query(
    query_embeddings=[embedding_new_failure],
    n_results=3,
    include=["metadatas", "documents", "distances"],
    where= {
        "service": "loan"
    }
)
for id,desc,distance in zip(
    result["ids"][0],
    result["documents"][0],
    result["distances"][0]
):
    print(f" id {id} description - {desc} distance - {distance}")
    
def search_defects(collection_name:str, querries: list[str], service, top_k=3):
    client = chromadb.PersistentClient(
        path = "./chrome_db"
    )
    print("chromaDB client created")

    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    response = callEmbeddingModel(querries)
    query_embedding = [embeddings.embedding for embeddings in response.data]
    response = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "distances", "metadatas"],
        where = {
            "service": service
        }
    )

    matches = []

    for defect_id, description, distance in zip(
        response["ids"][0],
        response["documents"][0],
        response["distances"][0]
    ):
        matches.append({
            "id": defect_id,
            "description": description,
            "similarity": 1 - distance
        })

    return matches