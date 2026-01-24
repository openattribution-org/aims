"""Tests for AI Manifest."""

import pytest

from openattribution.aims import AIManifest
from openattribution.aims.layers import ContentAccessLayer, DeploymentLayer, FoundationLayer
from openattribution.aims.layers.content_access import RedistributionPolicy


class TestAIManifest:
    """Tests for AIManifest class."""

    def test_create_minimal_manifest(self):
        """Create a manifest with just a DID."""
        manifest = AIManifest(did="did:aims:web:example.com:agent")

        assert manifest.did == "did:aims:web:example.com:agent"
        assert manifest.version == "1.0"
        assert manifest.foundation is not None
        assert manifest.deployment is not None
        assert manifest.content_access is not None

    def test_create_full_manifest(self):
        """Create a manifest with all layers populated."""
        manifest = AIManifest(
            did="did:aims:web:retailer.com:shopping-assistant",
            foundation=FoundationLayer(
                training_datasets=["dataset:openwebtext", "dataset:product-reviews"],
                rsl_compliance=True,
                licensing_summary="Trained on licensed and public domain data",
            ),
            deployment=DeploymentLayer(
                operator="Retailer Inc.",
                domain_specialization=["e-commerce", "consumer-electronics"],
                commercial_purpose="Product recommendations",
            ),
            content_access=ContentAccessLayer(
                licensed_sources=["source:wirecutter", "source:rtings"],
                redistribution_policy=RedistributionPolicy.SUMMARY_ONLY,
            ),
        )

        assert manifest.foundation.rsl_compliance is True
        assert len(manifest.foundation.training_datasets) == 2
        assert manifest.deployment.operator == "Retailer Inc."
        assert manifest.content_access.redistribution_policy == RedistributionPolicy.SUMMARY_ONLY

    def test_parsed_did_property(self):
        """Access parsed DID from manifest."""
        manifest = AIManifest(did="did:aims:web:example.com:my-agent")

        parsed = manifest.parsed_did
        assert parsed.organization == "example.com"
        assert parsed.system_id == "my-agent"

    def test_verify_unsigned_manifest(self):
        """Unsigned manifests verify as true (but untrusted)."""
        manifest = AIManifest(did="did:aims:web:example.com:agent")

        assert manifest.verify() is True

    def test_manifest_serialization(self):
        """Manifest can be serialized to JSON."""
        manifest = AIManifest(
            did="did:aims:web:example.com:agent",
            foundation=FoundationLayer(rsl_compliance=True),
        )

        data = manifest.model_dump(mode="json")

        assert data["did"] == "did:aims:web:example.com:agent"
        assert data["foundation"]["rsl_compliance"] is True
        assert "created_at" in data

    def test_manifest_deserialization(self):
        """Manifest can be deserialized from JSON."""
        data = {
            "did": "did:aims:web:example.com:agent",
            "version": "1.0",
            "foundation": {"rsl_compliance": True},
            "deployment": {},
            "content_access": {"redistribution_policy": "attributed"},
        }

        manifest = AIManifest.model_validate(data)

        assert manifest.did == "did:aims:web:example.com:agent"
        assert manifest.foundation.rsl_compliance is True
        assert manifest.content_access.redistribution_policy == RedistributionPolicy.ATTRIBUTED
