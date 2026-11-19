import json

from rag.retriever import retrieve_similar_defects
from rag.augmentation import build_augmented_prompt
from ai.ai_api_test_failure_analyser import ai_analyse_failure

from rag.grounding_evaluator import evaluate_grounding


def analyse_failure_with_rag(
    failure: dict,
    evaluate: bool = False
):
    matches = retrieve_similar_defects(
        failure=failure["error"],
        top_k=3
    )

    augmented_prompt = build_augmented_prompt(
        failure,
        matches
    )

    analysis = ai_analyse_failure(augmented_prompt)

    if not evaluate:
        return analysis

    context = "\n".join(
        f"{defect['id']}: {defect['description']}"
        for defect in matches
    )

    evaluation = evaluate_grounding(
        question=failure["error"],
        context=context,
        answer= json.dumps(analysis, ensure_ascii=False)
    )

    return {
        "analysis": analysis,
        "retrieved_defects": matches,
        "grounding_evaluation": evaluation
    }