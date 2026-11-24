from app.agents.research.audience import (
    execute_audience_research,
)


def test_execute_audience_research():
    result = execute_audience_research(
        niche="Luxury Hotels",
        location="Bangladesh",
    )

    assert result is not None
    assert result.primary_audiences
    assert result.customer_needs
    assert result.pain_points
    assert result.motivations
    assert result.purchasing_behavior
    assert result.audience_personas
    assert isinstance(result.sources, list)

    print("\nAudience Research Output:\n")
    print(result.model_dump_json(indent=2))