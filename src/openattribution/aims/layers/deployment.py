"""Deployment Layer - Commercial and operational context."""

from pydantic import BaseModel, Field


class BrandAffiliation(BaseModel):
    """Declared brand affiliation that may influence outputs."""

    brand: str = Field(..., description="Brand name")
    relationship: str = Field(..., description="Type of relationship (owner, partner, sponsor)")
    influence_type: str | None = Field(None, description="How this affects outputs (boost, exclusive, etc.)")


class DeploymentLayer(BaseModel):
    """Deployment context layer.

    Discloses commercial and operational factors that affect system behavior.
    Critical for agent-to-agent trust decisions.
    """

    operator: str | None = Field(
        None,
        description="Organization operating this AI system",
    )
    brand_affiliations: list[BrandAffiliation] = Field(
        default_factory=list,
        description="Declared brand affiliations affecting outputs",
    )
    domain_specialization: list[str] = Field(
        default_factory=list,
        description="Domains this system specializes in",
    )
    declared_biases: list[str] = Field(
        default_factory=list,
        description="Known biases or limitations disclosed by operator",
    )
    commercial_purpose: str | None = Field(
        None,
        description="Primary commercial purpose of this system",
    )
