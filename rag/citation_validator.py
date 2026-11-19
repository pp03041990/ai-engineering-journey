
import re
def validate_defect_citations(
    answer: str,
    retrieved_defects: list[dict]
) -> dict:

    cited_ids = set(
        re.findall(r"\bDEF-\d+\b", answer)
    )

    retrieved_ids = {
        defect["id"]
        for defect in retrieved_defects
    }

    invalid_ids = cited_ids - retrieved_ids

    return {
        "valid": len(invalid_ids) == 0,
        "cited_ids": sorted(cited_ids),
        "invalid_ids": sorted(invalid_ids)
    }
