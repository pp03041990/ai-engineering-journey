from pathlib import Path

from document_ingestion.document_loader import load_document
from document_ingestion.text_chunker import chunk_text

import re

import re
import unicodedata

def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[^\S\n]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def prepare_chunk_metadata(
    chunks: list[str],
    filename: str
) -> list[dict]:

    metadatas = []

    for index, chunk in enumerate(chunks):
        metadatas.append({
            "source": filename,
            "chunk_index": index,
            "character_count": len(chunk)
        })

    return metadatas

from openai import OpenAI

client = OpenAI()

def generate_embeddings(chunks: list[str]) -> list[list[float]]:

    if not chunks:
        return []

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunks
    )

    return [item.embedding for item in response.data]

import chromadb

def store_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict],
    document_id: str
):
    if not chunks:
        return

    if not (
        len(chunks) == len(embeddings) == len(metadatas)
    ):
        raise ValueError("Chunks, embeddings and metadata counts differ")

    chroma_client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = chroma_client.get_or_create_collection(
        name="document_knowledge"
    )

    ids = [
        f"{document_id}_chunk_{index}"
        for index in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("Total stored chunks:", collection.count())

def ingest_document(file_path: str):

    text = load_document(file_path)

    chunks = chunk_text(
        text,
        chunk_size=500,
        overlap=100
    )

    filename = Path(file_path).name

    metadatas = prepare_chunk_metadata(
        chunks,
        filename
    )

    embeddings = generate_embeddings(chunks)

    # Use a stable ID derived from the document path
    import hashlib

    document_id = hashlib.sha256(
        str(Path(file_path).resolve()).encode()
    ).hexdigest()[:16]

    store_chunks(
        chunks,
        embeddings,
        metadatas,
        document_id
    )

    return chunks

if __name__ == "__main__":

    pdf_path = (
        Path(__file__).resolve().parent
        / "sample_docs"
        / "Claude-Apify-Job-Search-Agent-Guide.pdf"
    )

    chunks = ingest_document(str(pdf_path))
