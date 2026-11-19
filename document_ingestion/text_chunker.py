from pathlib import Path

from document_ingestion.document_loader import load_PDF, load_document


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
) -> list[str]:
    if chunk_size <= 0:
      raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid overlap")
    result = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        result.append(text[start:end])
        if end == len(text):
            break;
        start = end - overlap
        
    return result
    
    
if __name__ == "__main__":
    path = Path(__file__).resolve().parent / "sample_docs" / "booking_incident.txt"
    content = load_document(str(path))
    chunk_text(content)