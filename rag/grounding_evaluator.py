
import json
from openai import OpenAI

client = OpenAI()


def evaluate_grounding(
    question: str,
    context: str,
    answer: str
) -> dict:

    response = client.responses.create(
        model="gpt-5.5",
        instructions="""
        You are a strict RAG grounding evaluator
        for API test failure analysis.

        Your task is to determine whether the AI-generated
        analysis is supported by the supplied evidence.

        The question describes the current test failure.
        The context contains retrieved historical defects.
        The answer contains the generated failure analysis.

        Evaluation rules:

        1. Treat the current failure and historical defect
           records as the available evidence.

        2. Do not use external knowledge to establish
           facts or root causes.

        3. A confirmed root-cause claim must be supported
           by the supplied evidence.

        4. Possible causes are acceptable when clearly
           described as hypotheses, not confirmed facts.

        5. Debugging recommendations are acceptable even
           when they are not explicitly mentioned in the
           historical defects, provided they are reasonable
           and not presented as observed facts.

        6. Do not assume that similar historical defects
           prove the current failure has the same cause.

        7. Identify any unsupported factual claims.

        Return a valid JSON object containing:

        - is_grounded: boolean
        - unsupported_claims: array of strings
        - explanation: string
        """,
        input=f"""
        Current failure:
        {question}

        Retrieved historical defects:
        {context}

        Generated AI analysis:
        {answer}
        Return your evaluation as a valid JSON object.

        """,
        text={
            "format": {
                "type": "json_object"
            }
        }
    )

    evaluation = json.loads(response.output_text)

    return evaluation
