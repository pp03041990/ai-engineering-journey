import chromadb
from openai import OpenAI

client = OpenAI()

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_collection(
    name="document_knowledge"
)


def search_documents(query: str, top_k: int = 3):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    return results

if __name__ == "__main__":

    results = search_documents(
        "How does Claude use Apify to search for jobs?"
    )

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        print("\nSource:", metadata["source"])
        print("Chunk index:", metadata["chunk_index"])
        print("Distance:", round(distance, 4))
        print("Content:", document[:300])