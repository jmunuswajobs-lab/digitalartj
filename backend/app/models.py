
from pydantic import BaseModel, Field
from typing import Optional, Literal

IntensityLevel = Literal["L1", "L2", "L3"]

class GenerateRequest(BaseModel):
    style_family: str = Field(..., description="C1..C6 style cluster code or custom style name")
    intensity: IntensityLevel = Field(..., description="L1 (soft), L2 (strong), L3 (max sensual allowed)")
    art_style_variant: str = Field("oil_painting", description="e.g. oil_painting, anime, hyperreal, watercolor")
    pose_description: str
    clothing_description: str
    environment_description: str

class GenerateResponse(BaseModel):
    job_id: str
    image_url: str
    prompt_used: str
