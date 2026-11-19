from pathlib import Path
from pypdf import PdfReader

def load_txt(filepath:str)->str:
    with open(file=filepath,mode="r",encoding="utf-8") as fp:
        return fp.read()
    
def load_markdown(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_PDF(file_path: str) -> str:
    pdf_reader= PdfReader(file_path)
    pages = []
    for page in pdf_reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n".join(pages)

def load_document(filepath:str) -> str:
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(
            f"Document not found: {filepath}"
        )
    if path.suffix.lower() in (".txt",".md"):
        return load_txt(filepath)
    elif path.suffix.lower() == ".pdf":
        return load_PDF(filepath)
    else:
     raise ValueError("this format of document not supported")
    
if __name__ == "__main__":
    path = Path(__file__).resolve().parent / "sample_docs" / "Claude-Apify-Job-Search-Agent-Guide.pdf"
    # path = Path(__file__).resolve().parent / "sample_docs" / "api_troubleshooting.md"
    content = load_PDF(str(path))
    print(content)