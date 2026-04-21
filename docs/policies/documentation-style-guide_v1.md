# Documentation Style Guide v1

Document Type: Policy  
Status: Approved  
Owner: Architecture  
Version: v1  
Last Reviewed: 2026-04-21  
Source of Authority: ED-2026-04-ready-for-controlled-semantic-expansion  
Related Tests: tests/test_contracts.py  
Related Risks: R12  
Related Decisions: ADR-0002, DL-2026-04-contract-surface-policy

## Language Policy
- Foundations and conceptual docs: Arabic-first with standardized English terms at first occurrence.
- Operational, engineering, contract docs: English-first with short Arabic summary when needed.
- Shared governance docs (ADR/Decision Log/Risk Register): bilingual title and core metadata fields only.

**Rule:** Arabic-first conceptually, English-stable operationally.

## Naming Convention
- `<domain>_<document-purpose>_v<version>.md`

## Required Header (all docs)
- Document Type
- Status
- Owner
- Version
- Last Reviewed
- Source of Authority
- Supersedes / Superseded by
- Related Tests
- Related Risks
- Related Decisions

## Duplication Policy
- Each topic has one authoritative document.
- Other documents must reference it; they must not restate full policy text.
