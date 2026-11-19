import pytest
from rag.retrieval_evaluator import precision_at_k,recall_at_k,reciprocal_rank
from vector_db.chroma_basics import search_defects


import pytest

@pytest.mark.parametrize(
    "relevant_ids,query,service,expected_precision,expected_recall,expected_rr",
    [
        (
            {"DEF-101", "DEF-108"},
            "Loan eligibility API returned HTTP 503",
            "loan",
            1/3, 0.5, 1/3
        ),
        (
            {"DEF-102", "DEF-111"},
            "Loan approval service temporarily unavailable",
            "loan",
            1/3, 0.5, 1/3
        ),
        (
            {"DEF-104", "DEF-112", "DEF-113"},
            "Loan EMI calculation returned incorrect amount",
            "loan",
            1/3, 1/3, 1/3
        ),
        (
            {"DEF-105", "DEF-115"},
            "Risk assessment endpoint timed out",
            "risk",
            1/3, 0.5, 1/3
        ),
        (
            {"DEF-106", "DEF-117"},
            "Risk assessment API returned HTTP 403",
            "risk",
            1/3, 0.5, 1/3
        ),
        (
            {"DEF-103", "DEF-119", "DEF-120"},
            "Customer email format validation failed",
            "domain",
            1/3, 1/3, 1/3
        ),
        (
            {"DEF-107", "DEF-121", "DEF-122"},
            "Booking API returned HTTP 404",
            "booking",
            1/3, 1/3, 1/3
        ),
        (
            {"DEF-125"},
            "Loan approval API created duplicate approval records",
            "loan",
            1/3, 1.0, 1/3
        ),
    ]
)
def test_retrieval_evaluator(
    relevant_ids,
    query,
    service,
    expected_precision,
    expected_recall,
    expected_rr
):
    retrieved_defects = search_defects(
        "loan_api_defects",
        [query],
        service,
        3
    )

    retrieved_ids = [
        defect["id"] for defect in retrieved_defects
    ]

    precision = precision_at_k(
        relevant_ids, retrieved_ids, 3
    )

    recall = recall_at_k(
        relevant_ids, retrieved_ids, 3
    )

    rr = reciprocal_rank(
        relevant_ids, retrieved_ids
    )

    print(f"\nQuery: {query}")
    print(f"Retrieved: {retrieved_ids}")
    print(f"Precision@3: {precision:.3f}")
    print(f"Recall@3: {recall:.3f}")
    print(f"RR: {rr:.3f}")

    assert precision >= expected_precision
    assert recall >= expected_recall
    assert rr >= expected_rr


# @pytest.mark.skip(reason = "not required")
# def test_retrieval_evaluator():
#     retrieved_defects = search_defects('loan_api_defects',['Loan eligibility API returned HTTP 503'],'loan',3)
#     retrieved_ids = [defects["id"] for defects in retrieved_defects]
#     print(retrieved_ids)
#     relevant_ids = {
#         "DEF-101"
#     }
#     print(retrieved_ids)
#     precision = precision_at_k(
#         relevant_ids,retrieved_ids,3
#     )
#     recall = recall_at_k(
#             relevant_ids,retrieved_ids,3
#         )
#     rr = reciprocal_rank(relevant_ids,retrieved_ids)
#     assert "DEF-101" in retrieved_ids
#     assert precision == pytest.approx(1 / 3)
#     assert recall == pytest.approx(1 / 1)
#     assert rr == 1.0

# @pytest.mark.parametrize("relevant_ids,retrieved_ids,expected",[
#     ({"DEF-101"},["DEF-101", "DEF-102"],1.0),
#     ({"DEF-101"},["DEF-102", "DEF-101"],0.5),
#     ({"DEF-101"},["DEF-102", "DEF-104", "DEF-101"],1/3),
#     ({"DEF-101"},["DEF-102", "DEF-104"],0.0)
# ])    
# def test_reciprocal_rank(relevant_ids,retrieved_ids,expected):
#     rr = reciprocal_rank(relevant_ids,retrieved_ids)
#     assert rr == pytest.approx(expected)