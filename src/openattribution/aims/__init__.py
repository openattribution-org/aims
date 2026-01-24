"""AIMS - AI Manifest Standard.

Licensing provenance, runtime access rights, and agent-to-agent trust for AI systems.

Usage:
    from openattribution.aims import AIManifest, AIMSDID, ManifestStore
    from openattribution.aims.layers import FoundationLayer, ContentAccessLayer
"""

from .manifest import AIManifest
from .store import ManifestStore
from .did import AIMSDID

__version__ = "0.1.0"
__all__ = ["AIManifest", "ManifestStore", "AIMSDID"]
