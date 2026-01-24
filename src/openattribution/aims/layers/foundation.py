"""Foundation Layer - Training data licensing provenance."""

from pydantic import BaseModel, Field


class DatasetReference(BaseModel):
    """Reference to a training dataset with licensing info."""

    identifier: str = Field(..., description="Dataset identifier (e.g., 'dataset:openwebtext')")
    license: str | None = Field(None, description="SPDX license identifier or custom license URL")
    rsl_compliant: bool = Field(False, description="Whether dataset is RSL compliant")
    merkle_root: str | None = Field(None, description="Merkle root for selective audit disclosure")


class FoundationLayer(BaseModel):
    """Training data licensing provenance layer.

    Documents what data trained the model and its licensing status.
    Enables cryptographic commitments for selective audit disclosure
    without full dataset exposure.
    """

    training_datasets: list[str] = Field(
        default_factory=list,
        description="List of dataset identifiers used in training",
    )
    dataset_details: list[DatasetReference] = Field(
        default_factory=list,
        description="Detailed dataset references with licensing info",
    )
    rsl_compliance: bool = Field(
        False,
        description="Whether the system claims RSL compliance for training data",
    )
    licensing_summary: str | None = Field(
        None,
        description="Human-readable summary of training data licensing",
    )
    audit_contact: str | None = Field(
        None,
        description="Contact for licensing audit requests",
    )
