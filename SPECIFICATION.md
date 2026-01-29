---
layout: spec
title: "Full Specification"
description: "Complete AIMS specification in a single document"
---

# OpenAttribution AI Manifest Standard

**An Open Standard for AI System Transparency, Provenance, and Agent-to-Agent Trust**

**Incomplete Draft Specification v0.1** | December 2025

> **Note on Completeness:** This specification is complete for content usage transparency and training data licensing provenance. Sections requiring cryptographic expertise (DID method specification, Merkle proof formats, verification protocol bindings) are marked as incomplete and require expert contribution. See [Section 13](#13-open-questions-for-discussion) for areas needing community input.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Design Principles](#3-design-principles)
4. [Architecture Overview](#4-architecture-overview)
5. [Foundation Layer Specification](#5-foundation-layer-specification)
6. [Deployment Context Layer Specification](#6-deployment-context-layer-specification)
7. [Content Access Layer Specification](#7-content-access-layer-specification)
8. [Agent Verification Protocol](#8-agent-verification-protocol)
9. [Integration with Existing Standards](#9-integration-with-existing-standards)
10. [Core Manifest Schema](#10-core-manifest-schema)
11. [Use Cases](#11-use-cases)
12. [Governance and Adoption](#12-governance-and-adoption)
13. [Open Questions for Discussion](#13-open-questions-for-discussion)
14. [Conclusion](#14-conclusion)
- [Appendix A: How AIMS Relates to Other Standards](#appendix-a-how-aims-relates-to-other-standards)
- [Appendix B: Related Standards Reference](#appendix-b-related-standards-reference)
- [Appendix C: Glossary](#appendix-c-glossary)

---

> **This is an incomplete draft specification.** The specification is complete for content usage transparency and training data licensing provenance. Cryptographic components (DID method specification, verification protocol bindings, Merkle proof formats) require expert contribution. See [Section 13: Open Questions](#13-open-questions-for-discussion) for details.

---

## 1. Executive Summary

The OpenAttribution AI Manifest Standard (AIMS) is a focused standard for **AI training data licensing provenance, runtime content access rights, and agent-to-agent cryptographic trust**. While other standards document model performance (Model Cards), dataset composition (Dataset Cards), and agent capabilities (A2A Agent Cards), AIMS answers the licensing and provenance questions those standards don't address.

AI agents now routinely interact with each other and with content across the web. They need a way to verify each other's identity, understand licensing status for training data and runtime content access, and establish trust boundaries before sharing information.

This specification addresses three technical requirements:

1. **Training Data Licensing Provenance:** What's the licensing status of the data that trained this model? Can it prove RSL compliance or other licensing agreements? What cryptographic commitments enable selective audit disclosure?

2. **Runtime Content Access Rights:** What content can this system legally access during inference? What content partnerships and licenses does it hold? What are its redistribution rights when sharing information with other agents?

3. **Agent-to-Agent Trust:** How can AI agents cryptographically verify each other's identity and understand each other's licensing boundaries before exchanging sensitive information?

AIMS builds on established W3C standards including Decentralized Identifiers (DIDs) and Verifiable Credentials. It integrates with Really Simple Licensing (RSL) and other licensing standards for content rights, and works alongside the Agent-to-Agent (A2A) protocol for inter-agent communication.

**Relationship to Other Standards:** AIMS complements Model Cards (performance and ethical evaluation), Dataset Cards (training data composition), and A2A Agent Cards (functional capabilities). Organizations should publish AIMS manifests for licensing transparency alongside these other documentation standards.

---

## 2. Problem Statement

### 2.1 The Licensing and Provenance Gap

AI systems today lack standardized ways to declare and verify the licensing status of their training data and runtime content access. When AI systems generate content, make recommendations, or interact with other agents, no machine-readable method exists to understand their licensing boundaries.

**Copyright and Licensing Compliance:** Content creators and publishers cannot tell whether their work trained an AI model. They also cannot determine the licensing terms. RSL provides machine-readable licensing for web content. However, AI systems have no corresponding standard to declare their training data licensing provenance or prove compliance with licensing agreements.

**Content Access Rights:** When AI systems access licensed content at runtime (news archives, proprietary databases, content partnerships), no standard method exists to declare what content they can legally access. There is also no standard for declaring redistribution rights. This creates problems when agents share information with each other.

**Agent-to-Agent Trust:** AI agents increasingly work together. A user's personal assistant might interact with a retailer's product recommendation agent. Currently, no method exists for agents to cryptographically verify each other's identity. Agents also cannot understand each other's licensing boundaries before sharing potentially licensed information.

### 2.2 The Agent Interoperability Problem

A user asks their personal AI assistant to help design a kitchen renovation. The assistant needs to interact with a home improvement retailer's AI agent to explore products, check availability, and compare options. This raises hard questions:

- How does the user's agent verify it is talking to the legitimate retailer agent and not an imposter?
- What data sources inform the retailer agent's recommendations?
- Does the retailer agent have access to proprietary content the user's agent cannot directly use?
- How should content licensing work when agents with different access rights share information?

AIMS answers these questions through cryptographically verifiable manifests that travel with AI systems or can be looked up on demand.

---

## 3. Design Principles

The OpenAttribution AI Manifest Standard follows these principles:

**Standards Alignment:** Use established W3C specifications (DIDs, Verifiable Credentials, JSON-LD) rather than inventing parallel systems. Integrate with RSL for content licensing and A2A/MCP for agent communication.

**Progressive Disclosure:** Support different levels of detail. Some consumers need high-level categorical summaries. Others need cryptographic commitments for selective audit disclosure. Not everyone needs terabytes of training data metadata.

**Verifiable Claims:** Every manifest assertion should be cryptographically signed and verifiable. Claims without verification mechanisms are documentation only and cannot be independently validated.

**Layered Architecture:** Keep stable identity (the fingerprint/DID) separate from dynamic content (the manifest). Manifests change over time. Identifiers persist.

**Privacy by Design:** Support selective disclosure. An AI system should be able to prove it trained on licensed data without revealing its complete training corpus.

**Platform Independence:** The standard must work across AI providers, hosting platforms, and jurisdictions. No single entity controls the registry or verification infrastructure.

---

## 4. Architecture Overview

The OpenAttribution AI Manifest Standard has four components:

### 4.1 AI System Identifier (Fingerprint)

Every AI system gets a stable, globally unique identifier based on the W3C Decentralized Identifier (DID) specification. This identifier anchors all manifest data cryptographically and is used for identity verification during inter-agent communication.

**Identifier Format:**

```
did:aims:<method>:<organization>:<system-id>
```

**Examples:**

- `did:aims:web:anthropic:claude-4-sonnet`: Anthropic's Claude Sonnet model
- `did:aims:web:homedepot:product-assistant-v2`: Home Depot's product recommendation agent
- `did:aims:web:user-12345:personal-agent`: An individual user's personal AI agent

The DID resolves to a DID Document containing the public keys needed to verify signed manifests and the service endpoints for manifest lookup.

> **Note: Requires Cryptographic Expertise.** The full `did:aims` method specification (syntax, CRUD operations, resolution algorithm) requires expert contribution. See Section 13, Open Questions.

### 4.2 Manifest Store

The Manifest Store is a distributed registry. AI providers publish manifests to the store. Clients retrieve manifests from the store. Multiple implementations can coexist: centralized registries run by industry consortia, decentralized solutions using content-addressed storage (IPFS, blockchain anchoring), or simple HTTPS endpoints hosted by AI providers.

**Key Properties:**

- **Content Addressable:** Each manifest version has a unique hash for integrity verification
- **Version History:** Manifests are versioned with timestamps; historical versions stay accessible for audit
- **Federated:** No single registry monopoly; resolvers can query multiple stores
- **Cached:** Clients should cache manifests with appropriate TTLs to reduce lookup latency

### 4.3 AI Manifest

The AI Manifest is the core payload. It's a structured JSON-LD document describing an AI system's licensing provenance and content access rights. It can be cryptographically signed as a Verifiable Credential. The manifest has three layers:

- **Foundation Layer:** Training data licensing provenance (Section 5)
- **Deployment Context Layer:** Commercial and operational biases (Section 6)
- **Content Access Layer:** Runtime content access, licensing, and usage rights (Section 7)

### 4.4 Verification Protocol

The Verification Protocol defines how AI systems authenticate to each other and verify manifest claims. It combines cryptographic identity verification with manifest lookup for capability understanding. See Section 8 for details.

---

## 5. Foundation Layer Specification

The Foundation Layer documents the **licensing provenance** of a base model's training data. This layer focuses specifically on licensing status, compliance attestations, and cryptographic commitments for selective disclosure.

**Scope:** This layer documents licensing and provenance. For detailed dataset composition (temporal distribution, language breakdown, annotation procedures, collection methodology), see Dataset Cards / Datasheets for Datasets (Section 9.9).

*Core question: What's the licensing status of the data that trained this model?*

### 5.1 Schema Structure

```json
{
  "foundation": {
    "version": "2025-12-19T00:00:00Z",
    "baseModel": {
      "name": "string",
      "version": "string",
      "releaseDate": "ISO-8601 date",
      "parentModel": "did:aims:... (optional)"
    },
    "trainingData": {
      "datasets": [ ... ],
      "commitments": { ... },
      "licensingCompliance": { ... }
    }
  }
}
```

### 5.2 Training Datasets

List of datasets used for training, with references to Dataset Cards for compositional details and AIMS-specific licensing information.

```json
"datasets": [
  {
    "name": "Common Crawl 2024-Q2",
    "datasetCard": "https://commoncrawl.org/dataset-card",
    "description": "Web crawl of publicly accessible internet content",
    "sourceType": "webCrawl",
    "licensingStatus": {
      "rslCompliant": true,
      "licensingNotes": "RSL compliance verified for crawl period"
    }
  },
  {
    "name": "Project Gutenberg",
    "datasetCard": "https://gutenberg.org/dataset-card",
    "description": "Public domain books",
    "sourceType": "books",
    "licensingStatus": {
      "status": "publicDomain",
      "licensingNotes": "All content is in the public domain"
    }
  },
  {
    "name": "GitHub Public Repositories",
    "datasetCard": "https://github.com/datasets/public-code/dataset-card",
    "description": "Open source code under permissive licenses",
    "sourceType": "code",
    "licensingStatus": {
      "licenses": ["MIT", "Apache-2.0", "BSD-3-Clause"],
      "licensingNotes": "Filtered to permissive OSS licenses only"
    }
  }
]
```

**Dataset Card References:** The `datasetCard` URL should point to a Datasheet for Datasets (Gebru et al., 2018) or HuggingFace Dataset Card that documents:
- Dataset composition and statistics
- Collection methodology
- Annotation procedures
- Temporal, geographic, and linguistic distributions
- Known biases and limitations

**AIMS Licensing Layer:** The `licensingStatus` field adds licensing-specific information not typically in Dataset Cards:
- RSL compliance status
- Licensing agreements
- Permission documentation

### 5.3 Cryptographic Commitments

> **Note: Requires Cryptographic Expertise.** This section describes cryptographic commitment mechanisms that allow selective disclosure of training data provenance. The Merkle proof generation, format, and verification procedures require expert contribution to complete.

Detailed provenance that cannot be fully disclosed publicly but must remain verifiable.

#### 5.3.1 Merkle Root

A hash commitment to the complete training data manifest. This enables a system to prove specific sources were or were not included without revealing the full dataset.

```json
"commitments": {
  "merkleRoot": "sha256:a1b2c3d4e5f6...",
  "algorithm": "sha256",
  "leafCount": 2847293847,
  "generated": "2025-06-15T00:00:00Z"
}
```

#### 5.3.2 Audit Endpoint

URL for authorized third-party auditors to verify detailed provenance claims. Access requires authentication and audit agreements.

```json
"auditEndpoint": {
  "url": "https://api.anthropic.com/aims/audit/v1",
  "authMethod": "oauth2",
  "auditorRequirements": "https://anthropic.com/aims-auditor-program"
}
```

### 5.4 Licensing Compliance

Declarations of compliance with content licensing standards and agreements.

#### 5.4.1 RSL Compliance

For systems that crawled web content, declaration of compliance with Really Simple Licensing terms:

```json
"rslCompliance": {
  "compliant": true,
  "policyVersion": "1.0",
  "crawlPolicy": {
    "respectsRobotsTxt": true,
    "respectsRslHeaders": true,
    "honoredSince": "2024-01-01"
  },
  "attestation": {
    "issuer": "did:web:anthropic.com",
    "issued": "2025-06-15T00:00:00Z",
    "signature": "..."
  }
}
```

#### 5.4.2 Other Licensing Standards

For compliance with other licensing frameworks:

```json
"otherLicensingStandards": [
  {
    "standard": "Creative Commons",
    "compliance": true,
    "version": "4.0",
    "notes": "All CC-licensed content used per license terms"
  },
  {
    "standard": "Open Source Initiative",
    "compliance": true,
    "licenses": ["MIT", "Apache-2.0", "GPL-3.0"],
    "notes": "Code datasets filtered to OSI-approved licenses"
  }
]
```

#### 5.4.3 Licensing Summary

Aggregate statistics on the licensing status of training data:

```json
"licensingSummary": {
  "publicDomain": 0.12,
  "creativeCommons": 0.08,
  "commercialLicense": 0.25,
  "rslCompliant": 0.35,
  "proprietaryLicensed": 0.15,
  "unknownStatus": 0.05
}
```

### 5.5 Derivative Models

When a model is fine-tuned from a base model, reference the parent:

```json
"baseModel": {
  "name": "product-assistant-v2",
  "version": "2.1.0",
  "releaseDate": "2025-12-01",
  "parentModel": "did:aims:web:meta:llama-3-70b",
  "derivationType": "fine-tune",
  "additionalTrainingData": {
    "summary": { ... }
  }
}
```

The `parentModel` DID lets consumers look up the base model's Foundation Layer and trace the full provenance chain.

---

## 6. Deployment Context Layer Specification

The Deployment Context Layer documents intentional commercial and operational biases that affect an AI system's behavior. This layer is focused specifically on disclosing affiliations and priorities that are relevant to agent-to-agent trust decisions.

**Scope:** This layer documents only commercial/operational alignment. For comprehensive documentation of model alignment methodology, safety training, content policies, known limitations, and ethical considerations, see Model Cards (Section 9.8).

*Core question: What commercial or operational biases affect this system's behavior?*

### 6.1 Why This Matters for Agent Trust

When a user's personal assistant interacts with a retailer's product recommendation agent, the personal assistant needs to know: "Does this agent have commercial incentives that might bias its recommendations?" Similarly, when agents collaborate on tasks, understanding commercial affiliations helps set appropriate trust boundaries.

This layer is intentionally narrow. It does NOT attempt to document general model safety, alignment methodology, or content policies. Those belong in Model Cards.

### 6.2 Schema Structure

```json
{
  "deploymentContext": {
    "version": "2025-12-19T00:00:00Z",
    "modelCardUrl": "https://example.com/model-card",
    "brandAffiliation": { ... },
    "operationalBiases": [ ... ],
    "domainFocus": "string"
  }
}
```

### 6.3 Brand Affiliation

For AI systems operated by or on behalf of commercial entities:

```json
"brandAffiliation": {
  "organization": "The Home Depot, Inc.",
  "relationship": "operated_by",
  "description": "This agent is operated by Home Depot to assist customers with home improvement product selection and project planning"
}
```

Possible values for `relationship`:
- `operated_by`: The organization directly operates this AI system
- `developed_for`: The system was custom-developed for this organization
- `licensed_to`: The organization licenses this system from another provider
- `independent`: No commercial affiliation

### 6.4 Operational Biases

Intentional biases introduced to serve the system's commercial or operational purpose:

```json
"operationalBiases": [
  {
    "type": "product_prioritization",
    "description": "Product recommendations prioritize Home Depot inventory over competitors",
    "rationale": "System designed to assist Home Depot customers in finding products available for purchase"
  },
  {
    "type": "content_source_priority",
    "description": "Research citations prioritize peer-reviewed journals over web content",
    "rationale": "Academic research assistant designed for scholarly use"
  }
]
```

Common bias types (not exhaustive):
- `product_prioritization`: Favors certain products or brands
- `content_source_priority`: Favors certain information sources
- `geographic_focus`: Optimized for specific regions or markets
- `domain_specialization`: Prioritizes certain knowledge domains

### 6.5 Domain Focus

High-level description of the system's operational focus:

```json
"domainFocus": "home improvement and residential construction"
```

### 6.6 Example: Brand-Affiliated Agent

```json
{
  "deploymentContext": {
    "version": "2025-12-19T00:00:00Z",
    "modelCardUrl": "https://homedepot.com/ai/product-assistant/model-card",
    "brandAffiliation": {
      "organization": "The Home Depot, Inc.",
      "relationship": "operated_by",
      "description": "Shopping assistant for Home Depot customers"
    },
    "operationalBiases": [
      {
        "type": "product_prioritization",
        "description": "Recommendations prioritize Home Depot inventory",
        "rationale": "System serves Home Depot customers finding in-stock products"
      },
      {
        "type": "geographic_focus",
        "description": "Product availability based on US and Canada stores",
        "rationale": "Home Depot operates primarily in North America"
      }
    ],
    "domainFocus": "home improvement, construction materials, and tool selection"
  }
}
```

### 6.7 Example: Independent General-Purpose Agent

```json
{
  "deploymentContext": {
    "version": "2025-12-19T00:00:00Z",
    "modelCardUrl": "https://anthropic.com/claude/model-card",
    "brandAffiliation": {
      "organization": "Anthropic",
      "relationship": "operated_by",
      "description": "General-purpose AI assistant"
    },
    "operationalBiases": [],
    "domainFocus": "general-purpose conversational assistance"
  }
}
```

### 6.8 Reference to Model Cards

For comprehensive documentation of:
- Alignment methodology (RLHF, Constitutional AI, etc.)
- Safety training and red teaming
- Content policies and prohibited content
- Ethical frameworks and value alignment
- Known limitations and failure modes
- Disaggregated performance evaluation
- Bias mitigation techniques

Organizations should publish Model Cards (see Section 9.8) and reference them via the `modelCardUrl` field.

---

## 7. Content Access Layer Specification

The Content Access Layer documents what content an AI system can legally access at inference time: data sources, licensed content partnerships, and usage rights. This is the most dynamic layer, potentially changing per deployment, per session, or per user context.

*Core questions: What content can this system legally access? What are its usage rights?*

### 7.1 Why Licensed Content Matters

When AI agents interact, content licensing creates problems. Consider: Agent A has a license to access Reuters news content. Agent B does not. Agent A summarizes a Reuters article for Agent B. Has Agent B now received content it is not licensed for?

The Content Access Layer makes these licensing boundaries explicit. Agents can check each other's manifests before deciding what information to share.

### 7.2 Schema Structure

```json
{
  "contentAccess": {
    "version": "2025-12-19T00:00:00Z",
    "scope": "deployment | session | user",
    "dataSources": { ... },
    "tools": { ... },
    "licensedContent": { ... }
  }
}
```

### 7.3 Content Access Scope

Content access rights can be declared at different levels:

| Scope | Description | Update Frequency |
|-------|-------------|------------------|
| `deployment` | Fixed for this deployment of the system | Rarely changes |
| `session` | Varies per conversation/session | Per session |
| `user` | Varies based on authenticated user | Per user |

### 7.4 Data Sources

#### 7.4.1 Web Access

```json
"dataSources": {
  "webAccess": {
    "enabled": true,
    "searchEngines": ["google", "bing"],
    "directFetch": true,
    "domainRestrictions": {
      "allowlist": null,
      "blocklist": ["example-blocked.com"]
    }
  }
}
```

#### 7.4.2 Knowledge Bases

Proprietary or curated knowledge repositories:

```json
"knowledgeBases": [
  {
    "name": "Product Catalog",
    "description": "Current Home Depot product inventory",
    "type": "proprietary",
    "owner": "The Home Depot, Inc.",
    "realtime": true
  },
  {
    "name": "Installation Guides",
    "description": "How-to guides for home improvement projects",
    "type": "proprietary",
    "owner": "The Home Depot, Inc.",
    "realtime": false,
    "lastUpdated": "2025-12-01"
  }
]
```

#### 7.4.3 Real-Time Feeds

```json
"realtimeFeeds": [
  { "name": "Stock Prices", "provider": "Bloomberg", "type": "financial", "latency": "15-minute delay" },
  { "name": "Weather", "provider": "National Weather Service", "type": "weather", "latency": "real-time" }
]
```

### 7.5 Tools and Capabilities

**For detailed tool and capability documentation,** see:
- **A2A Agent Card** (Section 9.4): Describes functional capabilities, skills, and I/O modes
- **Model Context Protocol** (Section 9.5): Documents MCP server connections

**AIMS Focus:** The Content Access Layer documents only tool/capability aspects relevant to licensing and content access rights.

```json
"toolsAndCapabilities": {
  "agentCardUrl": "https://example.com/.well-known/agent-card.json",
  "mcpConfigUrl": "https://example.com/mcp-config.json",
  "licensingNotes": [
    {
      "tool": "Reuters News MCP Server",
      "licensingStatus": "Licensed for inference access only",
      "restrictions": "Cannot redistribute raw content to other agents"
    },
    {
      "tool": "Getty Images API",
      "licensingStatus": "Licensed for thumbnail display only",
      "restrictions": "Full-resolution images require separate licensing"
    }
  ]
}
```

**What Goes Here vs. A2A/MCP:**
- **A2A Agent Card:** Lists all skills, capabilities, I/O modes, endpoints
- **MCP Configuration:** Details of MCP server connections, permissions, scopes
- **AIMS (here):** Notes about which tools access licensed content and what usage restrictions apply

### 7.6 Licensed Content

The `licensedContent` section declares what content this system can access and redistribute. Other agents read this to understand licensing boundaries before sharing information.

#### 7.6.1 Content Partnerships

Formal content licensing agreements:

```json
"licensedContent": {
  "partnerships": [
    {
      "provider": "Reuters",
      "contentType": "news",
      "scope": "Full archive access",
      "redistribution": { "allowed": false, "summaryAllowed": true, "summaryMaxLength": 100 },
      "validUntil": "2026-12-31"
    },
    {
      "provider": "Getty Images",
      "contentType": "images",
      "scope": "Editorial use",
      "redistribution": { "allowed": false, "thumbnailsAllowed": true },
      "validUntil": "2026-06-30"
    }
  ]
}
```

#### 7.6.2 RSL Licenses Held

RSL license tokens the system has acquired for specific content:

```json
"rslLicenses": {
  "held": true,
  "licenseCount": 47,
  "categories": [
    { "type": "news", "publishers": 12, "tier": "ai-training-inference" },
    { "type": "reference", "publishers": 35, "tier": "ai-inference-only" }
  ],
  "verificationEndpoint": "https://api.anthropic.com/rsl/verify"
}
```

#### 7.6.3 Redistribution Rights

What happens when this agent shares licensed content with other agents:

```json
"redistributionPolicy": {
  "default": "no-redistribution",
  "exceptions": [
    { "contentType": "public-domain", "policy": "unrestricted" },
    { "contentType": "creative-commons", "policy": "per-license-terms" }
  ],
  "watermarking": { "enabled": true, "method": "metadata-tag" }
}
```

### 7.7 Content Producer Identification

#### 7.7.1 Design Decision: No Registry

AIMS does not define a content producer registry. Content producers are identified using existing identifiers:

| Identifier Type | Use Case | Example |
|----------------|----------|---------|
| Domain | Web publishers | `nytimes.com` |
| RSL Publisher ID | RSL-participating publishers | `rsl:pub:nytimes` |
| ISNI | Organizations with existing identifiers | `isni:0000000121691048` |
| DOI prefix | Academic publishers | `doi:10.1038` |
| Custom | Proprietary content systems | `homedepot:catalog:v2` |

A global content registry would require ongoing maintenance and governance, create centralization risks, and duplicate work RSL is already doing.

#### 7.7.2 Minimum Viable Producer Reference

For practical use, a content producer reference needs only:

```json
{
  "producer": "nytimes.com",
  "type": "domain"
}
```

The domain is already a globally unique identifier. More sophisticated identification can be layered on through `alternateIdentifiers` when available.

### 7.8 OLP Integration

The Open License Protocol (part of RSL) handles dynamic license negotiation at runtime. AIMS declares static licensing status; OLP handles negotiation.

```json
"olpEndpoint": {
  "url": "https://api.example.com/olp/v1",
  "capabilities": ["query", "acquire"]
}
```

---

## 8. Agent Verification Protocol

> **Note: Requires Cryptographic Expertise.** This section describes the conceptual verification model. Detailed protocol bindings, attestation formats, and cryptographic signature schemes require expert contribution to complete.

When AI agents interact, they need to establish identity and understand each other's capabilities before exchanging sensitive information. This section describes the verification model.

### 8.1 Overview

The verification process has two phases:

1. **Identity verification:** Confirm the agent is who it claims to be via cryptographic proof tied to its DID
2. **Capability discovery:** Retrieve and validate the agent's manifest to understand its data sources, licensing status, and behavioral constraints

These phases can occur synchronously at connection time or asynchronously depending on trust requirements and latency constraints.

### 8.2 Identity Verification

Identity verification proves that an agent controls the private key associated with its DID (see Section 4.1 for identifier format).

**Conceptual flow:**

1. Agent A initiates connection to Agent B
2. Agent B returns a signed attestation containing: its DID, current timestamp, manifest version hash, and a nonce
3. Agent A resolves Agent B's DID to retrieve the DID Document
4. Agent A verifies the attestation signature against the public key in the DID Document
5. If verification succeeds, identity is established

**Requirements:**

- Verification MUST resist replay attacks (hence timestamp and nonce)
- Verification MUST NOT require a centralized authority at runtime
- Verification SHOULD complete within latency bounds acceptable for interactive use cases
- Failed verification MUST prevent the exchange of sensitive information

### 8.3 Manifest Retrieval

Once identity is verified, the connecting agent retrieves the full manifest to understand capabilities and establish trust boundaries.

1. Check local cache for the counterparty's DID
2. If cached manifest version matches the hash from the attestation, use cached manifest
3. Otherwise, fetch current manifest from the Manifest Store (see Section 4.2)
4. Verify the fetched manifest hash matches the attestation
5. Parse manifest layers as needed (Sections 5, 6, 7)

Caching behavior and TTLs are implementation-dependent but should balance freshness against lookup latency.

### 8.4 Trust Decisions

Manifest contents inform trust decisions. Based on the retrieved manifest, an agent can determine:

- Whether to proceed with the interaction
- What information can be shared (considering licensing constraints in the Content Access Layer)
- How to handle content with redistribution restrictions
- Whether the counterparty's data sources are relevant to the task

Trust policy is application-specific. AIMS provides the information; agents decide how to act on it.

### 8.5 Protocol Requirements

The verification protocol must satisfy these properties:

| Requirement | Description |
|-------------|-------------|
| **Mutual authentication** | Both parties can verify each other's identity |
| **Replay resistance** | Attestations cannot be reused by attackers |
| **No central dependency** | Verification works without real-time access to a central authority |
| **Graceful degradation** | Agents can define fallback behavior when verification fails or times out |
| **A2A compatibility** | The protocol should integrate with existing A2A authentication flows where possible |

### 8.6 Open Design Questions

The following questions are explicitly left open for community input:

1. **Protocol binding:** Should AIMS define a standalone verification handshake, or specify an extension to A2A's existing authentication mechanism?

2. **Attestation format:** What's the minimal attestation schema? Should it use JWT, Verifiable Presentations, or something simpler?

3. **Partial verification:** Can agents proceed with partial trust (e.g., identity verified but manifest unavailable)? What are the security implications?

4. **Session continuity:** How should verification state persist across multiple interactions? Re-verify per request, per session, or per time window?

5. **Revocation checking:** How do agents learn that a previously-valid DID or manifest has been revoked?

### 8.7 Security Considerations

A full threat model is outside the scope of this draft. However, implementers should consider:

- **Man-in-the-middle:** Attestations should be bound to the transport session
- **Key compromise:** Revocation mechanisms (unspecified) are necessary for production deployments
- **Manifest tampering:** Content-addressed manifests and signed attestations mitigate this, but the trust anchor is the DID Document
- **Denial of service:** Verification should not introduce amplification vectors

---

## 9. Integration with Existing Standards

AIMS complements existing standards rather than replacing them.

### 9.1 W3C Decentralized Identifiers (DIDs)

AIMS uses DIDs as the core identifier for AI systems. The DID specification (W3C Recommendation, July 2022) provides globally unique, cryptographically verifiable identifiers that do not depend on centralized registries. AIMS defines a new DID method (`did:aims`) with resolution semantics specific to AI system manifests.

> **Note: Requires Cryptographic Expertise.** The full `did:aims` method specification (syntax, CRUD operations, resolution algorithm, security considerations) requires expert contribution to complete.

### 9.2 W3C Verifiable Credentials

AI Manifests can be packaged as Verifiable Credentials (W3C Recommendation, May 2025), which provides cryptographic signing, selective disclosure, revocation checking, and credential chaining for derivative models.

### 9.3 Really Simple Licensing (RSL)

RSL (v1.0, November 2025) provides machine-readable licensing terms for web content. AIMS integrates with RSL at two levels:

- The **Foundation Layer** can reference RSL compliance for training data
- The **Content Access Layer** can declare RSL licenses held for runtime content access

The Open License Protocol (OLP) handles agent-to-agent license negotiation.

### 9.4 Agent-to-Agent Protocol (A2A)

A2A (originally launched by Google in April 2025, now under Linux Foundation governance as of June 2025) standardizes inter-agent communication. AIMS is complementary to A2A, not competitive with it. They solve different problems:

**A2A Agent Card answers: "What can this agent do?"**

The A2A Agent Card (available at `.well-known/agent-card.json`) describes an agent's functional capabilities:

- **Skills**: Specific tasks the agent can perform (e.g., "search the web", "book appointments")
- **Input/Output Modes**: Supported media types (text, JSON, images, audio)
- **Endpoint URL**: Where to reach the agent's A2A service
- **Capabilities**: Protocol features like streaming or push notifications
- **Examples**: Sample prompts for each skill

Example A2A Agent Card:
```json
{
  "name": "Shopping Assistant",
  "skills": [
    {"id": "product_search", "name": "Search products", "inputModes": ["text"]},
    {"id": "price_compare", "name": "Compare prices", "inputModes": ["text"]}
  ],
  "url": "https://api.retailer.com/agent",
  "contentAccess": {"streaming": true}
}
```

**AIMS Manifest answers: "What is this agent? Where did it come from? What can it ethically access?"**

The AIMS Manifest describes provenance, transparency, and licensing:

- **Foundation Layer**: Training data licensing status, RSL compliance, cryptographic commitments
- **Deployment Context Layer**: Commercial and operational biases relevant to agent trust
- **Content Access Layer**: Licensed content partnerships, runtime access rights, RSL compliance
- **Verification**: Cryptographic identity and manifest integrity

Example scenario showing both:

A user's personal agent connects to a retailer's shopping agent:

1. **A2A handshake** establishes the functional interface:
   - "I offer product search and price comparison skills"
   - "I accept text input and return JSON"

2. **AIMS verification** establishes trust boundaries:
   - "I was trained on retailer product data and public web content"
   - "I have a known bias: recommendations prioritize our products"
   - "I hold licensed access to manufacturer spec sheets and images"
   - "I'm RSL-compliant for web-crawled training data"

The personal agent can now make informed decisions: use the retailer agent's product search skill (A2A), but understand that recommendations are biased toward that retailer (AIMS), and verify that product images are properly licensed (AIMS).

**Integration Points:**

- AIMS verification handshake can slot into A2A's authentication flow
- A2A Agent Card can reference an AIMS Manifest URL for transparency-conscious clients
- Both standards use DIDs for agent identity
- AIMS provides the trust layer A2A needs for sensitive inter-agent collaboration

An agent would typically publish both:
- **Agent Card** at `.well-known/agent-card.json` (A2A)
- **AIMS Manifest** in the Manifest Store, referenced via DID (AIMS)

### 9.5 Model Context Protocol (MCP)

MCP (developed by Anthropic) standardizes how AI systems connect to tools and data sources. The AIMS Content Access Layer can reference MCP server configurations, making it transparent which MCP tools an AI system can access.

### 9.6 C2PA Content Credentials

The C2PA specification provides content provenance for media assets. AIMS can reference C2PA manifests for training data where available, bridging content-level and system-level provenance. AI-generated content could carry both:

- C2PA credentials (for the output)
- AIMS references (to the generating system)

### 9.7 EU AI Act Compliance

The EU AI Act (Regulation 2024/1689) requires transparency documentation for high-risk AI systems and general-purpose AI models. AIMS manifests can satisfy many of these requirements, particularly:

- Article 11 (technical documentation)
- Article 13 (transparency to deployers)
- Article 53 (obligations for GPAI model providers)

### 9.8 Model Cards for Model Reporting

Model Cards (Mitchell et al., 2019) provide standardized transparency documentation for machine learning models, with emphasis on:
- Disaggregated evaluation across demographic and phenotypic groups
- Intended and out-of-scope use cases
- Quantitative performance metrics with confidence intervals
- Ethical considerations in model development
- Known limitations and failure modes

**Relationship to AIMS:**

| Standard | Focus | Key Questions Answered |
|----------|-------|----------------------|
| **Model Cards** | Performance & ethics | "How well does it work? For whom? What are the limitations?" |
| **AIMS Foundation** | Licensing provenance | "What's the licensing status of training data?" |
| **AIMS Deployment Context** | Deployment context and biases | "What commercial or operational factors affect this system?" |
| **AIMS Content Access** | Runtime licensing | "What content can it legally access and redistribute?" |

Model Cards document empirical performance and ethical considerations. AIMS documents licensing provenance and content access rights. These are complementary transparency mechanisms addressing different stakeholder needs.

**Integration Points:**
- AIMS manifests reference Model Card URLs via `modelCardUrl` field
- Model Cards may reference AIMS manifests for licensing transparency
- Organizations deploying AI systems should publish both

**Example references:**
- HuggingFace Model Cards: https://huggingface.co/docs/hub/model-cards
- Model Card Guidebook: https://huggingface.co/docs/hub/en/model-card-guidebook
- Original Paper: Mitchell et al. (2019), "Model Cards for Model Reporting"

### 9.9 Dataset Cards (Datasheets for Datasets)

Dataset Cards, also known as "Datasheets for Datasets" (Gebru et al., 2018), provide standardized documentation for datasets used in machine learning:
- Dataset composition and statistics
- Collection methodology and annotation procedures
- Temporal, geographic, and linguistic distributions
- Recommended uses and known limitations
- Privacy and ethical considerations

**Relationship to AIMS:**

| Standard | Focus | Key Questions Answered |
|----------|-------|----------------------|
| **Dataset Cards** | Dataset composition | "What's in the dataset? How was it collected? What biases exist?" |
| **AIMS Foundation** | Licensing status | "What's the licensing status of this training data?" |

Dataset Cards document dataset contents and creation methodology. AIMS adds a licensing layer on top, documenting compliance with RSL and other licensing standards.

**Integration Points:**
- AIMS Foundation Layer references Dataset Card URLs via `datasetCard` field for each training dataset
- Dataset Cards document composition; AIMS documents licensing status
- Together they provide comprehensive training data transparency

**Example references:**
- HuggingFace Dataset Cards: https://huggingface.co/docs/hub/datasets-cards
- Original Paper: Gebru et al. (2018), "Datasheets for Datasets"

---

## 10. Core Manifest Schema

The following JSON-LD schema shows how the three layers compose into a complete manifest, with references to complementary standards. This is a draft specification subject to community review.

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://openattribution.org/aims/v1"
  ],
  "@type": "AIManifest",
  "@id": "did:aims:web:anthropic:claude-4-sonnet",
  "version": "2025-12-19T00:00:00Z",
  "previousVersion": "ipfs://bafybeif...",
  "issuer": {
    "@id": "did:web:anthropic.com",
    "name": "Anthropic",
    "verificationMethod": "did:web:anthropic.com#key-1"
  },

  "foundation": {
    "baseModel": {
      "name": "Claude 4 Sonnet",
      "version": "2025-12-19",
      "releaseDate": "2025-12-19T00:00:00Z"
    },
    "trainingData": {
      "datasets": [
        {
          "name": "Common Crawl 2024-Q2",
          "datasetCard": "https://commoncrawl.org/dataset-card",
          "sourceType": "webCrawl",
          "licensingStatus": {
            "rslCompliant": true
          }
        }
      ],
      "commitments": {
        "merkleRoot": "sha256:a1b2c3d4...",
        "auditEndpoint": "https://api.anthropic.com/aims/audit/v1"
      },
      "licensingCompliance": {
        "rslCompliance": { "compliant": true },
        "licensingSummary": {
          "publicDomain": 0.12,
          "rslCompliant": 0.35,
          "commercialLicense": 0.25,
          "unknownStatus": 0.28
        }
      }
    }
  },

  "deploymentContext": {
    "modelCardUrl": "https://anthropic.com/claude/model-card",
    "brandAffiliation": {
      "organization": "Anthropic",
      "relationship": "operated_by"
    },
    "operationalBiases": [],
    "domainFocus": "general-purpose conversational assistance"
  },

  "contentAccess": {
    "scope": "deployment",
    "toolsAndCapabilities": {
      "agentCardUrl": "https://api.anthropic.com/.well-known/agent-card.json",
      "mcpConfigUrl": "https://api.anthropic.com/mcp-config.json"
    },
    "licensedContent": {
      "partnerships": [],
      "rslLicenses": { "held": false },
      "redistributionPolicy": { "default": "no-redistribution" }
    }
  },

  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "ecdsa-rdfc-2019",
    "created": "2025-12-19T00:00:00Z",
    "verificationMethod": "did:web:anthropic.com#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `@context` | JSON-LD context declaring the vocabulary |
| `@type` | Document type (always `AIManifest`) |
| `@id` | The DID of this AI system |
| `version` | ISO-8601 timestamp of this manifest version |
| `previousVersion` | Content-addressed link to prior version (for audit trail) |
| `issuer` | Organization publishing this manifest |
| `foundation` | Training data licensing provenance (Section 5) |
| `deploymentContext` | Commercial/operational biases (Section 6) |
| `contentAccess` | Runtime content access and licensing (Section 7) |
| `proof` | Cryptographic signature over the manifest |

### External Standard References

Notice the manifest includes URLs linking to complementary standards:
- `datasetCard`: Links to Dataset Cards (Datasheets for Datasets) for training data composition
- `modelCardUrl`: Links to Model Card for performance evaluation and ethical considerations
- `agentCardUrl`: Links to A2A Agent Card for functional capabilities and skills
- `mcpConfigUrl`: Links to MCP configuration for tool/server connection details

**Layered Transparency:** AIMS provides licensing and provenance transparency. Other standards provide performance, composition, and capability transparency. Together they enable comprehensive AI system transparency.

> **Note:** A normative JSON Schema for validation is planned for a future version of this specification.

---

## 11. Use Cases

These examples illustrate how AIMS addresses real-world problems.

### 11.1 Agent-to-Agent Commerce

A user's personal AI assistant helps plan a kitchen renovation by interacting with a home improvement retailer's product recommendation agent.

The user's agent verifies the retailer agent's identity via DID handshake (Section 8.2), then retrieves its manifest (Section 8.3). The manifest confirms:

1. This is the legitimate Home Depot agent
2. It has access to current inventory data
3. Its recommendations may prioritize Home Depot products (a disclosed bias in the Deployment Context Layer)
4. It holds licenses to specialty content like design guides

The user's agent can now make informed decisions about which recommendations to trust and what information to share.

### 11.2 Content Licensing Transparency

A news publisher wants to verify whether an AI search engine has properly licensed their content for training or inference.

The publisher queries the AI system's manifest to check:

1. Its Foundation Layer RSL compliance attestations
2. Whether the publisher's domain appears in licensed content declarations in the Content Access Layer
3. Audit endpoints for third-party verification

If no license is present, the publisher has documentation to support licensing discussions or enforcement actions.

### 11.3 Regulatory Compliance

An organization deploying an AI system in the EU needs to demonstrate compliance with AI Act transparency requirements.

The organization retrieves the AI system's AIMS manifest, which provides machine-readable documentation of:

- Training data categories and provenance
- Alignment methodology and content policies
- Capability limitations and known biases
- Version history for audit trails

This manifest can be submitted to regulators as part of conformity assessment, with selective disclosure protecting trade secrets.

### 11.4 Model Derivative Tracking

A company fine-tunes an open-source base model and deploys it as a specialized product assistant.

The derivative model's manifest references the base model's DID in its Foundation Layer (Section 5.5), creating a provenance chain. The Deployment Context Layer documents the company's brand affiliation and commercial priorities. Users interacting with the product assistant can trace its lineage back to the base model while understanding what commercial customizations were applied.

---

## 12. Governance and Adoption

### 12.1 Governance Model

AIMS is designed for multi-stakeholder governance, potentially operating under an established standards body (W3C, Linux Foundation, or similar).

- **Specification Maintenance:** A Technical Steering Committee with representation from AI providers, content publishers, civil society, and academia
- **Registry Operations:** Multiple independent registries can coexist; no single entity controls the manifest store
- **Verification Infrastructure:** Third-party auditors can be accredited to verify manifest claims
- **Dispute Resolution:** Mechanisms for challenging inaccurate manifest claims

### 12.2 Adoption Pathway

**Phase 1: Foundation (2025-2026)**

- Finalize core specification through community review
- Establish reference implementations and test suites
- Initial adoption by founding AI providers
- Integration with RSL and A2A specifications

**Phase 2: Industry Adoption (2026-2027)**

- Launch federated manifest registries
- Develop auditor accreditation program
- Browser and platform integration for manifest display
- Tooling for manifest generation and verification

**Phase 3: Maturity (2027+)**

- Regulatory recognition (EU AI Act safe harbor)
- Industry-wide adoption and interoperability
- Content marketplace integration with RSL

---

## 13. Open Questions for Discussion

This specification is complete for content usage transparency and training data licensing provenance. The following areas require cryptographic expertise and community input.

### 13.1 Technical Specification Gaps Requiring Cryptographic Expertise

1. **DID Method Specification:** The `did:aims` method is referenced but not specified. A complete DID method requires: method-specific identifier syntax, CRUD operations, resolution algorithm, and security considerations. **Requires cryptographic expertise.**

2. **Merkle Proof Verification:** The Foundation Layer mentions a Merkle root for selective disclosure, but proof generation, format, and verification procedures are not defined. **Requires cryptographic expertise.**

3. **Revocation:** How do you revoke a manifest? What if a signing key is compromised? What is the revocation distribution mechanism? **Requires cryptographic expertise.**

4. **Verification Protocol Bindings:** Section 8 describes the conceptual verification model, but detailed protocol bindings, attestation formats, and signature schemes need specification. **Requires cryptographic expertise.**

### 13.2 Design Tradeoffs

5. **Recursive Provenance:** When AI-generated content becomes training data for new models, how deep should provenance chains extend? What are the practical limits of tracking synthetic data origins?

6. **Verification Granularity:** What level of training data detail should be verifiable? Per-document attribution may be computationally prohibitive. What aggregation levels provide meaningful transparency?

7. **Manifest Freshness:** For dynamic Content Access Layers, how often should manifests update? What is the right balance between accuracy and caching efficiency?

8. **Trade Secret Protection:** How do we balance transparency with legitimate intellectual property protection? What selective disclosure mechanisms are sufficient for regulatory compliance while preserving competitive advantage?

### 13.3 Adoption Questions

9. **Gaming Resistance:** How do we prevent manifest claims from becoming performative compliance rather than genuine transparency? What third-party verification mechanisms are needed?

10. **Liability Allocation:** If an AI system's manifest is inaccurate, who bears liability? The issuing organization? The registry? How do we create appropriate incentives for accuracy?

11. **Transitive Licensing:** If Agent A has a license and summarizes content for Agent B, does the summary inherit licensing restrictions?

12. **Incentive Alignment:** Why would AI providers publish manifests voluntarily before regulation requires it? What is the value proposition for early adopters?

---

## 14. Conclusion

The OpenAttribution AI Manifest Standard specifies what trained an AI system, how it was aligned, and what it can access at runtime.

This specification is complete for content usage transparency and training data licensing provenance. Cryptographic components require expert contribution. Section 13 lists technical gaps: the DID method specification, protocol bindings, and verification procedures need cryptographic expertise.

AIMS enables:

- **Content creators** to see if their work trained a model
- **AI developers** to prove responsible data practices
- **Organizations** to assess systems for bias and safety
- **AI agents** to verify each other before sharing information
- **Regulators** to get machine-readable audit trails

Similar to DNS for identity resolution, TLS for transport security, and HTTP for content delivery, AI systems require standardized provenance verification.

We invite comment, contribution, and critique from AI developers, content publishers, standards bodies, policymakers, and civil society.

**Contribute:** [AIMS on GitHub](https://github.com/openattribution-org/openattribution-org.github.io/tree/main/aims)

---

## Appendix A: How AIMS Relates to Other Standards

AIMS works alongside several other standards in the AI space. Here's what each one does and how they fit together.

### RSL (Really Simple Licensing)

**What it does:** Machine-readable licensing terms for web content

**Who uses it:** Content publishers, website owners

**Problem it solves:** "How do I tell AI systems what they can/can't do with my content?"

**How it works:**
- Publishers declare licensing terms via robots.txt, HTTP headers, HTML meta tags, RSS feeds
- Specifies allowed uses: training, inference, commercial, research
- Sets pricing and payment requirements
- Open License Protocol (OLP) handles runtime license negotiation between agents

**Example:** NYTimes.com declares: "AI training allowed with paid license. Inference requires separate agreement. Contact licensing@nytimes.com"

**Relationship to AIMS:**
- RSL lives on the content side (publishers state terms)
- AIMS lives on the AI side (systems declare what licenses they hold)
- AIMS Foundation Layer references RSL compliance for training data
- AIMS Content Access Layer declares which RSL licenses the AI system holds
- Together: RSL states the rules, AIMS proves compliance

### A2A (Agent-to-Agent Protocol)

**What it does:** Standardizes how AI agents communicate and work together

**Who uses it:** AI developers building agents that need to collaborate

**Problem it solves:** "How do agents from different vendors discover each other's capabilities and coordinate tasks?"

**How it works:**
- Agent Card (at `.well-known/agent-card.json`) advertises functional capabilities
- Defines skills: what tasks the agent can perform
- Specifies I/O modes: text, JSON, images, audio
- Provides endpoint URLs and protocol features (streaming, push notifications)

**Example:** Shopping Assistant's Agent Card says: "I can search products, compare prices, check inventory. I accept text input and return JSON."

**Relationship to AIMS:**
- A2A answers: "What can this agent DO?" (functional capabilities)
- AIMS answers: "What IS this agent?" (provenance, licensing, biases)
- A2A handles task coordination
- AIMS handles trust and transparency
- Agents typically have both: A2A Card for interoperability + AIMS Manifest for trust
- AIMS verification can slot into A2A's authentication flow

**Key distinction:** A2A is about functional interface. AIMS is about transparency and licensing. You need both for secure agent collaboration.

### MCP (Model Context Protocol)

**What it does:** Standardizes how AI systems connect to tools and data sources

**Who uses it:** AI developers integrating external tools, databases, APIs

**Problem it solves:** "How do I give my AI system access to external data and tools in a standard way?"

**How it works:**
- Defines server/client protocol for AI-to-tool connections
- MCP servers expose tools, prompts, and data sources
- AI applications connect to multiple MCP servers
- Examples: filesystem access, database queries, API integrations, calendar access

**Example:** Claude Desktop connects to MCP servers for GitHub (read/write repos), filesystem (access local files), Postgres (query databases).

**Relationship to AIMS:**
- MCP is about HOW AI systems connect to tools
- AIMS is about WHAT AI systems can access and their rights to use it
- AIMS Content Access Layer can reference MCP server configurations
- Makes it transparent which MCP tools an AI system has access to
- MCP handles the connection; AIMS declares the access rights

**Key distinction:** MCP is plumbing for tool access. AIMS is transparency about what tools you have and what you're allowed to do with them.

### How They All Work Together

**Real-world scenario:** User's personal agent helps plan a trip

1. **A2A:** User's agent discovers airline's booking agent via Agent Card
   - Sees it offers "search flights" and "book tickets" skills
   - Establishes connection using A2A protocol

2. **AIMS:** User's agent checks airline agent's manifest
   - Verifies it's the legitimate airline agent (DID verification)
   - Sees it has access to real-time flight data
   - Notes bias: recommendations prioritize airline's own flights
   - Checks what content licenses it holds

3. **RSL:** Airline agent checks licensing before sharing content
   - User's agent requests flight details
   - Airline agent checks if user's agent has appropriate RSL licenses
   - Uses OLP to verify licensing status

4. **MCP:** Airline agent uses MCP to access backend systems
   - MCP server for flight inventory database
   - MCP server for booking API
   - MCP server for payment processing

**The stack:**
- **A2A:** Enables agent communication and task coordination
- **AIMS:** Provides trust, transparency, and licensing verification
- **RSL:** Declares content licensing terms
- **MCP:** Connects agents to their tools and data sources

### Quick Reference Table

| Standard | Side | Answers | Format |
|----------|------|---------|--------|
| **RSL** | Content | "What can you do with my content?" | XML licensing terms in HTTP headers/robots.txt |
| **AIMS** | AI System | "What trained me? What can I access?" | JSON-LD manifest with cryptographic signatures |
| **A2A** | Agent | "What tasks can I perform?" | JSON Agent Card + task protocol |
| **MCP** | Tool | "How do I connect to external systems?" | Server/client protocol for tool access |

---

## Appendix B: Related Standards Reference

| Standard | Organization | Publication | Relevance |
|----------|--------------|-------------|-----------|
| [Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/did-core/) | W3C | July 2022 | Core identifier format |
| [Verifiable Credentials v2.0](https://www.w3.org/TR/vc-data-model-2.0/) | W3C | May 2025 | Manifest signing and packaging |
| [Really Simple Licensing (RSL) v1.0](https://rslstandard.org/rsl) | RSL Collective | November 2025 | Content licensing |
| [Agent-to-Agent Protocol (A2A)](https://github.com/a2aproject/A2A) | Linux Foundation | June 2025 | Inter-agent communication |
| [Model Context Protocol (MCP)](https://modelcontextprotocol.io) | Anthropic | 2024 | Agent-to-tool connectivity |
| [C2PA Content Credentials v2.2](https://c2pa.org/specifications/) | C2PA | Current | Media asset provenance |
| [EU AI Act (2024/1689)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | European Union | July 2024 | Regulatory requirements |
| [Model Cards](https://arxiv.org/abs/1810.03993) | Google Research | 2018 | ML model documentation |

---

## Appendix C: Glossary

**AIMS:** OpenAttribution AI Manifest Standard, the specification defined in this document.

**Agent:** An AI system capable of autonomous action and interaction with other systems.

**Content Access Layer:** Manifest section describing runtime content access, licensing, and usage rights (Section 7).

**DID:** Decentralized Identifier, a W3C standard for globally unique, cryptographically verifiable identifiers.

**Fingerprint:** Colloquial term for the AIMS identifier (DID) of an AI system.

**Foundation Layer:** Manifest section describing base model training data provenance (Section 5).

**Manifest:** The complete transparency document for an AI system, comprising Foundation, Deployment Context, and Content Access layers.

**Manifest Store:** Registry where AI Manifests are published and retrieved.

**MCP:** Model Context Protocol, a standard for AI-to-tool connectivity developed by Anthropic.

**OLP:** Open License Protocol, part of RSL, for runtime license negotiation between agents.

**RSL:** Really Simple Licensing, a standard for machine-readable content licensing.

**Deployment Context Layer:** Manifest section describing commercial and operational biases (Section 6).

**Verifiable Credential:** A W3C standard for cryptographically signed, tamper-evident digital credentials.

---

## Appendix D: AIMS Scope Boundaries

This appendix clarifies what AIMS covers versus what other standards handle. AIMS is intentionally focused on licensing provenance, content access rights, and agent trust, not general model documentation.

### What AIMS Covers

| Area | AIMS Responsibility | Key Questions |
|------|-------------------|---------------|
| **Training Data Licensing** | Licensing status, RSL compliance, cryptographic commitments | "Is the training data licensed? Can you prove it?" |
| **Runtime Content Access** | Licensed content partnerships, access rights, redistribution policies | "What content can this system legally access at inference time?" |
| **Agent Identity & Trust** | Cryptographic identity verification, manifest integrity | "Is this the legitimate agent? Can I verify its identity?" |
| **Commercial Biases** | Brand affiliations, intentional commercial priorities | "Does this agent have commercial incentives that bias its behavior?" |
| **Audit Infrastructure** | Merkle commitments, audit endpoints for selective disclosure | "How can third parties verify licensing claims?" |

### What Other Standards Cover

| Standard | Responsibility | Key Questions | AIMS Relationship |
|----------|---------------|---------------|-------------------|
| **Model Cards** | Performance evaluation, ethical considerations, limitations, disaggregated metrics | "How well does it work? For whom? What are its limitations?" | AIMS references via `modelCardUrl` |
| **Dataset Cards** | Dataset composition, collection methodology, biases, statistics | "What's in the dataset? How was it collected?" | AIMS references via `datasetCard` URL |
| **A2A Agent Cards** | Functional capabilities, skills, I/O modes, endpoints | "What tasks can this agent perform?" | AIMS references via `agentCardUrl` |
| **MCP** | Tool/server connections, permissions, integration details | "How does this system connect to external tools?" | AIMS references via `mcpConfigUrl` |

### Clear Scope Divisions

#### Training Data: Dataset Cards + AIMS
- **Dataset Card:** Composition (temporal, language, domain distributions), collection methodology, annotation process
- **AIMS:** Licensing status, RSL compliance, licensing agreements, cryptographic commitments

#### Model Behavior: Model Cards + AIMS
- **Model Card:** Alignment methodology, safety training, content policies, ethical frameworks, performance metrics, limitations
- **AIMS:** Commercial/operational biases relevant to agent trust (brand affiliation, product prioritization)

#### Agent Capabilities: A2A + AIMS
- **A2A Agent Card:** Functional capabilities, skills, I/O modes, what the agent can DO
- **AIMS:** Content access rights, what the agent can legally ACCESS

#### Tool Integration: MCP + AIMS
- **MCP:** Connection details, server configurations, permissions, scopes
- **AIMS:** Licensing notes for tools that access licensed content

### What AIMS Explicitly Does NOT Cover

❌ **Model performance evaluation** → Use Model Cards
❌ **Disaggregated fairness metrics** → Use Model Cards
❌ **Dataset composition statistics** → Use Dataset Cards
❌ **General alignment methodology** → Use Model Cards
❌ **Safety training details** → Use Model Cards
❌ **Content policy specifics** → Use Model Cards
❌ **Functional capabilities** → Use A2A Agent Cards
❌ **Tool connection details** → Use MCP

### Implementation Guidance

**For AI System Publishers:**
1. Publish AIMS manifest for licensing/provenance transparency
2. Publish Model Card for performance/ethics transparency
3. Reference Dataset Cards for training data composition
4. Publish A2A Agent Card for functional interoperability
5. Link them all together via URL references

**For Content Creators/Publishers:**
- Query AIMS manifests to verify licensing compliance
- Model Cards won't tell you about licensing. That's AIMS territory.
- Check both Foundation Layer (training) and Content Access Layer (runtime)

**For Regulators:**
- AIMS provides licensing and provenance audit trails
- Model Cards provide performance and ethical evaluation
- Both are needed for comprehensive transparency

**For Agent Developers:**
- Use AIMS for trust decisions (licensing boundaries, commercial biases)
- Use A2A for capability discovery (what can this agent do?)
- Use Model Cards for risk assessment (what are the limitations?)

### Summary

**AIMS = Licensing + Provenance + Trust**

Everything else belongs in other standards. This focused scope makes AIMS:
- Easier to implement
- Less controversial (not prescribing ethics)
- More likely to be adopted
- Clearly differentiated from existing work
- Complementary rather than competitive
