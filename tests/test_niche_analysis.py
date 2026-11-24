from app.agents.research.niche import execute_niche_analysis


def test_execute_niche_analysis():
    result = execute_niche_analysis(
        niche="Luxury Hotels",
        location="Bangladesh",
    )

    assert result is not None
    assert result.niche
    assert result.industry_overview
    assert isinstance(result.sources, list)

    print(result.model_dump_json(indent=2))