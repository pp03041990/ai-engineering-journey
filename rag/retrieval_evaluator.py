def precision_at_k(relevant_ids: set[str], retrieved_ids: list[str], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be positive")

    if not relevant_ids:
        raise ValueError("relevant_ids cannot be empty")
    top_k = retrieved_ids[:k]
    total_relevant_answers= sum(
        1 for defect_id in top_k
        if defect_id in relevant_ids)
    return total_relevant_answers / k

def recall_at_k(relevant_ids: set[str], retrieved_ids: list[str], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be positive")

    if not relevant_ids:
        raise ValueError("relevant_ids cannot be empty")
    top_k = retrieved_ids[:k]
    total_relevant_answers= sum(
        1 for defect_id in top_k
        if defect_id in relevant_ids)
    return total_relevant_answers / len(relevant_ids)

def reciprocal_rank(
    relevant_ids: set[str],
    retrieved_ids: list[str]
) -> float:
    for rank, retrieved_id in enumerate(retrieved_ids, start=1):

        if retrieved_id in relevant_ids:
            return 1 / rank

    return 0.0