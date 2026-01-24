"""Decentralized Identifier (DID) handling for AIMS.

AIMS DIDs follow the format: did:aims:<method>:<organization>:<system-id>

Examples:
    did:aims:web:example.com:shopping-assistant
    did:aims:key:z6Mk...:recommendation-engine
"""

import re
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class AIMSDID:
    """A Decentralized Identifier for an AI system.

    Attributes:
        method: Resolution method (web, key, etc.)
        organization: Organization identifier
        system_id: Unique system identifier within the organization
    """

    method: str
    organization: str
    system_id: str

    DID_PATTERN = re.compile(
        r"^did:aims:(?P<method>[a-z]+):(?P<organization>[a-zA-Z0-9.-]+):(?P<system_id>[a-zA-Z0-9_-]+)$"
    )

    def __str__(self) -> str:
        """Return the full DID string."""
        return f"did:aims:{self.method}:{self.organization}:{self.system_id}"

    @classmethod
    def parse(cls, did_string: str) -> Self:
        """Parse a DID string into components.

        Args:
            did_string: A full DID string like 'did:aims:web:example.com:my-agent'

        Returns:
            AIMSDID instance

        Raises:
            ValueError: If the DID string is invalid
        """
        match = cls.DID_PATTERN.match(did_string)
        if not match:
            raise ValueError(f"Invalid AIMS DID format: {did_string}")

        return cls(
            method=match.group("method"),
            organization=match.group("organization"),
            system_id=match.group("system_id"),
        )

    @classmethod
    def create(cls, organization: str, system_id: str, method: str = "web") -> Self:
        """Create a new AIMS DID.

        Args:
            organization: Organization identifier (domain for web method)
            system_id: Unique system identifier
            method: Resolution method (default: web)

        Returns:
            AIMSDID instance
        """
        return cls(method=method, organization=organization, system_id=system_id)

    def resolve_url(self) -> str | None:
        """Get the URL to resolve this DID's document.

        Returns:
            URL string for web method, None for other methods
        """
        if self.method == "web":
            return f"https://{self.organization}/.well-known/aims/{self.system_id}.json"
        return None
