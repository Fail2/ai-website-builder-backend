from pydantic import BaseModel, ConfigDict, Field


class ResearchSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    url: str
    summary: str


class NicheAnalysisOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    niche: str
    industry_overview: str

    industry_characteristics: list[str] = Field(min_length=1)
    market_trends: list[str] = Field(min_length=1)
    opportunities: list[str] = Field(min_length=1)
    challenges: list[str] = Field(min_length=1)
    typical_services: list[str] = Field(min_length=1)
    industry_terminology: list[str] = Field(min_length=1)

    sources: list[ResearchSource] = Field(min_length=1)


class AudienceResearchOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_audiences: list[str] = Field(min_length=1)
    secondary_audiences: list[str] = Field(default_factory=list)

    demographics: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)

    customer_needs: list[str] = Field(min_length=1)
    pain_points: list[str] = Field(min_length=1)
    motivations: list[str] = Field(min_length=1)
    purchasing_behavior: list[str] = Field(min_length=1)

    audience_personas: list[str] = Field(min_length=1)
    sources: list[ResearchSource] = Field(min_length=1)


class CompetitorProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    url: str
    positioning: str
    website_structure: list[str]
    common_features: list[str]
    content_strategy: str
    strengths: list[str]
    weaknesses: list[str]


class CompetitorAnalysisOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    competitors: list[CompetitorProfile] = Field(min_length=1)

    differentiation_opportunities: list[str] = Field(min_length=1)

    sources: list[ResearchSource] = Field(min_length=1)


class SEOAnalysisOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_keywords: list[str] = Field(min_length=1)
    secondary_keywords: list[str] = Field(default_factory=list)
    long_tail_keywords: list[str] = Field(default_factory=list)

    search_intent: list[str] = Field(min_length=1)
    seo_landing_page_recommendations: list[str] = Field(min_length=1)
    content_topics: list[str] = Field(min_length=1)

    seo_strategy: list[str] = Field(min_length=1)

    sources: list[ResearchSource] = Field(min_length=1)