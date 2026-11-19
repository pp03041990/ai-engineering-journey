from pathlib import Path
from document_ingestion.document_loader import load_document

import pytest
def test_doc_loader():
    path = Path(__file__).resolve().parent.parent / "document_ingestion" / "sample_docs" / "Claude-Apify-Job-Search-Agent-Guide.pdf"
    content = load_document(path)
    assert "FREE RESOURCE" in content
    

def test_doc_loader_negative_validation():
    path = Path(__file__).resolve().parent.parent / "document_ingestion" / "sample_docs" / "Salesforce_QE_Master_Workbook.xlsx"
    with pytest.raises(ValueError,match='this format of document not supported'):
        load_document(path)