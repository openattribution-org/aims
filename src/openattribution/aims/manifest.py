"""AI Manifest - The core AIMS document."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from .did import AIMSDID
from .layers import ContentAccessLayer, DeploymentLayer, FoundationLayer


class AIManifest(BaseModel):
    """An AI Manifest documenting licensing and trust boundaries.

    The manifest combines three layers:
    - Foundation: Training data licensing provenance
    - Deployment: Commercial and operational context
    - Content Access: Runtime content access rights
    """

    # Identity
    did: str = Field(..., description="Decentralized Identifier for this AI system")
    version: str = Field("1.0", description="Manifest schema version")

    # Three layers
    foundation: FoundationLayer = Field(
        default_factory=FoundationLayer,
        description="Training data licensing provenance",
    )
    deployment: DeploymentLayer = Field(
        default_factory=DeploymentLayer,
        description="Commercial and operational context",
    )
    content_access: ContentAccessLayer = Field(
        default_factory=ContentAccessLayer,
        description="Runtime content access rights",
    )

    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    signature: str | None = Field(None, description="Cryptographic signature of manifest")

    # References to complementary standards
    model_card_url: str | None = Field(None, description="URL to Model Card")
    dataset_card_url: str | None = Field(None, description="URL to Dataset Card")
    a2a_card_url: str | None = Field(None, description="URL to A2A Agent Card")

    @property
    def parsed_did(self) -> AIMSDID:
        """Parse the DID string into components."""
        return AIMSDID.parse(self.did)

    def verify(self) -> bool:
        """Verify the manifest's cryptographic signature.

        Returns:
            True if signature is valid or absent, False if invalid

        Note:
            Full verification requires the signing key. This is a stub
            that will be implemented with proper crypto in a future version.
        """
        # TODO: Implement actual signature verification
        if self.signature is None:
            return True  # Unsigned manifests are valid but untrusted
        # Placeholder for signature verification
        return True

    def sign(self, private_key: bytes) -> None:
        """Sign the manifest with a private key.

        Args:
            private_key: Ed25519 private key bytes

        Note:
            Stub implementation - will be completed with proper crypto.
        """
        # TODO: Implement actual signing
        self.signature = "stub-signature"
        self.updated_at = datetime.now(UTC)
