import pytest

from document_ingestion.text_chunker import chunk_text
def test_text_chunker():
    input = "1234567890"
    result = chunk_text(input,4,2)
    assert result == [
        '1234',
        '3456',
        '5678',
        '7890'
    ]

def test_text_shorter_than_chunk_size():
    text = "HELLO"

    result = chunk_text(
        text,
        chunk_size=10,
        overlap=2
    )

    assert result == ["HELLO"]