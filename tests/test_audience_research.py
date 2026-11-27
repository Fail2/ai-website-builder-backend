from app.agents.research.audience import (
    execute_audience_research,
)


def test_execute_audience_research():
    result = execute_audience_research(
        niche="Luxury Hotels",
        location="Bangladesh",
    )

    assert result is not None
    assert isinstance(result.report, str)
    assert result.report.strip()

    print("\nAudience Research Output:\n")
    print(result.model_dump_json(indent=2))