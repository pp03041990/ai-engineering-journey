from ai.ai_response_model import AIAnalysis


def test_ai_response_model():
    analysis= AIAnalysis(
        likely_cause='API returned 404',
        debugging_steps=['check the booking Id'],
        defect_type='Test data Issue'
    )

    assert analysis.likely_cause == "API returned 404"
    assert len(analysis.debugging_steps) >= 1