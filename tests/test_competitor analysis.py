from app.agents.research.competitor import (
    execute_competitor_analysis,
)


def test_competitor_analysis():
    result = execute_competitor_analysis(
        brand_name="Test Luxury Hotel",
        niche="Luxury Hospitality",
        location="Dhaka, Bangladesh",
    )

    print(result.model_dump_json(indent=2))

    assert result.competitors
    assert result.differentiation_opportunities
    assert result.sources