"""Tests for AIMS DID handling."""

import pytest

from openattribution.aims.did import AIMSDID


class TestAIMSDID:
    """Tests for AIMSDID class."""

    def test_parse_valid_web_did(self):
        """Parse a valid web-method DID."""
        did = AIMSDID.parse("did:aims:web:example.com:shopping-assistant")

        assert did.method == "web"
        assert did.organization == "example.com"
        assert did.system_id == "shopping-assistant"

    def test_parse_valid_key_did(self):
        """Parse a valid key-method DID."""
        did = AIMSDID.parse("did:aims:key:z6MkTest:my-agent")

        assert did.method == "key"
        assert did.organization == "z6MkTest"
        assert did.system_id == "my-agent"

    def test_parse_invalid_did_raises(self):
        """Invalid DID format raises ValueError."""
        with pytest.raises(ValueError, match="Invalid AIMS DID format"):
            AIMSDID.parse("not-a-did")

    def test_parse_wrong_scheme_raises(self):
        """Non-AIMS DID raises ValueError."""
        with pytest.raises(ValueError, match="Invalid AIMS DID format"):
            AIMSDID.parse("did:web:example.com:agent")

    def test_str_roundtrip(self):
        """DID string roundtrips through parse."""
        original = "did:aims:web:mycompany.io:recommendation-engine"
        did = AIMSDID.parse(original)

        assert str(did) == original

    def test_create_web_did(self):
        """Create a new web-method DID."""
        did = AIMSDID.create("example.com", "my-agent")

        assert did.method == "web"
        assert str(did) == "did:aims:web:example.com:my-agent"

    def test_create_with_method(self):
        """Create a DID with explicit method."""
        did = AIMSDID.create("z6MkKey", "secure-agent", method="key")

        assert did.method == "key"
        assert str(did) == "did:aims:key:z6MkKey:secure-agent"

    def test_resolve_url_web_method(self):
        """Web method DIDs resolve to well-known URL."""
        did = AIMSDID.parse("did:aims:web:example.com:agent")

        assert did.resolve_url() == "https://example.com/.well-known/aims/agent.json"

    def test_resolve_url_key_method_returns_none(self):
        """Key method DIDs don't have resolution URLs."""
        did = AIMSDID.parse("did:aims:key:z6MkTest:agent")

        assert did.resolve_url() is None

    def test_did_is_immutable(self):
        """DID instances are frozen."""
        did = AIMSDID.create("example.com", "agent")

        with pytest.raises(AttributeError):
            did.method = "key"  # type: ignore
