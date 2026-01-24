"""Content Access Layer - Runtime content access rights."""

from enum import StrEnum

from pydantic import BaseModel, Field


class RedistributionPolicy(StrEnum):
    """Policies for redistributing content to other agents."""

    NONE = "none"  # Cannot share content with other agents
    SUMMARY_ONLY = "summary_only"  # Can share summaries, not verbatim
    ATTRIBUTED = "attributed"  # Can share with attribution
    UNRESTRICTED = "unrestricted"  # No restrictions on sharing


class LicensedSource(BaseModel):
    """A content source this system has licensed access to."""

    identifier: str = Field(..., description="Source identifier")
    license_type: str = Field(..., description="Type of license (first-party, granted, marketplace)")
    scope: str | None = Field(None, description="Scope of access (full, partial, specific-content)")
    expires_at: str | None = Field(None, description="ISO 8601 expiration date if applicable")


class ContentAccessLayer(BaseModel):
    """Runtime content access rights layer.

    Specifies what content the system can legally access during inference
    and what it can share with other agents.
    """

    licensed_sources: list[str] = Field(
        default_factory=list,
        description="List of source identifiers this system can access",
    )
    source_details: list[LicensedSource] = Field(
        default_factory=list,
        description="Detailed licensed source information",
    )
    redistribution_policy: RedistributionPolicy = Field(
        RedistributionPolicy.SUMMARY_ONLY,
        description="Default policy for sharing content with other agents",
    )
    rsl_licenses: list[str] = Field(
        default_factory=list,
        description="RSL license identifiers held by this system",
    )
    content_partnerships: list[str] = Field(
        default_factory=list,
        description="Named content partnerships",
    )
