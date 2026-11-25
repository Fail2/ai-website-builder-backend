from pydantic import BaseModel, ConfigDict, Field


class BrandGuideline(BaseModel):
    model_config = ConfigDict(extra="forbid")

    brand_positioning: str = Field(description="Market position and differentiation. 2-3 short sentences, about 300 characters.")
    brand_personality: str = Field(description="4-5 personality traits, one short phrase each. About 150 characters.")
    tone_of_voice: str = Field(description="Tone and writing style for website copy. 2-3 short sentences, about 300 characters.")
    brand_messaging: str = Field(description="A tagline and three value propositions. About 300 characters.")
    color_palette: str = Field(description="Primary, secondary, accent, background, and text colors, each with a HEX code and its use. About 300 characters.")
    typography: str = Field(description="Heading and body fonts (free Google Fonts only) and when to use each. About 250 characters.")
    logo_direction: str = Field(description="Text-based logo guidance: logo type (wordmark, lettermark, or combination), how the brand name is styled as text, and one simple icon idea that can be drawn with inline SVG or CSS. Use the palette and fonts already defined. Do not generate a logo. About 300 characters.")
    visual_identity: str = Field(description="Design language in CSS-friendly terms: corner radius, shadows, spacing, background patterns or gradients, icon style, and mood. About 300 characters.")
    image_guidelines: str = Field(description="For the main website sections: image subjects, photography or illustration style, composition, lighting, and mood. Describe a placeholder style using the palette colors for when images are unavailable. Do not generate images. About 400 characters.")
    ui_ux_direction: str = Field(description="Layout, hierarchy, spacing, interaction style. 2-3 short sentences, about 300 characters.")
    design_inspiration: str = Field(description="Relevant design styles. Do not invent websites or URLs. About 250 characters.")