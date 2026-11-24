from app.agents.research.seo import execute_seo_analysis
result = execute_seo_analysis(
    niche="Luxury Hotels",
    location="Dhaka, Bangladesh",
    brand_name="Grand Horizon",
)

print(result.model_dump_json(indent=2))