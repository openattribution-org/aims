"""AIMS manifest layers.

The three-layer model:
- Foundation: Training data licensing provenance
- Deployment: Commercial and operational context
- ContentAccess: Runtime content access rights
"""

from .foundation import FoundationLayer
from .deployment import DeploymentLayer
from .content_access import ContentAccessLayer

__all__ = ["FoundationLayer", "DeploymentLayer", "ContentAccessLayer"]
