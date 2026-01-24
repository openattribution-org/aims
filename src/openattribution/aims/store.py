"""Manifest Store - Distributed registry for AIMS manifests."""

import httpx
from pydantic import BaseModel, Field

from .manifest import AIManifest


class ManifestStore:
    """Client for interacting with an AIMS manifest store.

    Manifest stores are distributed registries where AI systems publish
    their manifests for discovery and verification by other agents.
    """

    def __init__(self, base_url: str, timeout: float = 30.0):
        """Initialize the manifest store client.

        Args:
            base_url: Base URL of the manifest store
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def publish(self, manifest: AIManifest) -> str:
        """Publish a manifest to the store.

        Args:
            manifest: The AI manifest to publish

        Returns:
            The DID of the published manifest

        Raises:
            httpx.HTTPError: If the request fails
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/manifests",
                json=manifest.model_dump(mode="json"),
            )
            response.raise_for_status()
            return manifest.did

    async def resolve(self, did: str) -> AIManifest | None:
        """Resolve a DID to its manifest.

        Args:
            did: The DID to resolve

        Returns:
            The AI manifest if found, None otherwise

        Raises:
            httpx.HTTPError: If the request fails (except 404)
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/manifests/{did}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return AIManifest.model_validate(response.json())

    async def verify(self, did: str) -> bool:
        """Verify a manifest exists and has valid signature.

        Args:
            did: The DID to verify

        Returns:
            True if manifest exists and is valid
        """
        manifest = await self.resolve(did)
        if manifest is None:
            return False
        return manifest.verify()


class ManifestStoreConfig(BaseModel):
    """Configuration for a manifest store."""

    url: str = Field(..., description="Store URL")
    name: str = Field("default", description="Store name")
    priority: int = Field(0, description="Resolution priority (higher = preferred)")
