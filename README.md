# AIMS - AI Manifest Standard

[![PyPI version](https://badge.fury.io/py/openattribution-aims.svg)](https://badge.fury.io/py/openattribution-aims)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**Licensing provenance, runtime access rights, and agent-to-agent trust for AI systems.**

Part of the [OpenAttribution](https://openattribution.org) project.

AIMS answers the questions other AI standards don't address:

- **Training Data Provenance**: What's the licensing status of the data that trained this model?
- **Runtime Access Rights**: What content can this system legally access during inference?
- **Agent-to-Agent Trust**: How can AI agents verify each other before exchanging information?

## Installation

```bash
pip install openattribution-aims
```

## Quick Start

```python
from openattribution.aims import AIManifest, ManifestStore
from openattribution.aims.layers import FoundationLayer, ContentAccessLayer

# Create a manifest for your AI system
manifest = AIManifest(
    did="did:aims:web:example.com:shopping-assistant",
    foundation=FoundationLayer(
        training_datasets=["dataset:openwebtext", "dataset:internal-reviews"],
        rsl_compliance=True,
    ),
    content_access=ContentAccessLayer(
        licensed_sources=["source:wirecutter", "source:rtings"],
        redistribution_policy="summary_only",
    ),
)

# Publish to a manifest store
store = ManifestStore("https://aims.openattribution.org")
await store.publish(manifest)

# Verify another agent's manifest
other_manifest = await store.resolve("did:aims:web:other.com:agent")
if other_manifest.verify():
    # Establish trust boundary
    ...
```

## Specification

Full specification: [SPECIFICATION.md](./SPECIFICATION.md)

## Three-Layer Model

| Layer | Purpose | Key Fields |
|-------|---------|------------|
| **Foundation** | Training data provenance | datasets, RSL compliance, Merkle commitments |
| **Deployment** | Commercial context | brand affiliations, biases, specialization |
| **Content Access** | Runtime rights | licensed sources, redistribution policy |

## Relationship to Other Standards

AIMS complements, not replaces:

- **Model Cards**: Performance and ethical evaluation
- **Dataset Cards**: Training data composition
- **A2A Agent Cards**: Functional capabilities
- **OpenAttribution**: Content influence measurement

## License

Apache 2.0
