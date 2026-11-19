from openai import OpenAI

from document_ingestion.document_retriever import search_documents

client = OpenAI()


def answer_document_question(question: str) -> str:

    results = search_documents(question, top_k=3)

    documents = results["documents"][0]

    context = "\n\n".join(documents)
    # print(f"Document context:\n{context}\n\n")

    response = client.responses.create(
        model="gpt-5.5",
        instructions=
                    """
            You are a document-grounded QA assistant.

            Answer questions using only the provided context.

            For every factual claim, cite the supporting chunk
            using the format [Chunk N].

            Do not invent integrations or product capabilities.

            If the retrieved context does not support the answer,
            state that the document does not contain that information.

            Do not use your general knowledge to fill missing facts.
            """,
        input=(
            f"Document context:\n{context}\n\n"
            f"Question: {question}"
        )
    )

    return response.output_text


if __name__ == "__main__":

    answer = answer_document_question(
        "How does Claude use Myntra to search for jobs?"
    )

    print("\nAI Answer:")
    print(answer)