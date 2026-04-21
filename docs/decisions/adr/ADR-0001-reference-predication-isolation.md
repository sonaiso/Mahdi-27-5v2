# ADR-0001 / قرار معماري: Reference-Predication Isolation

Document Type: ADR  
Status: Accepted  
Owner: Architecture  
Version: v1  
Last Reviewed: 2026-04-21  
Source of Authority: Executive Decision ED-2026-04  
Related Tests: tests/test_sigma2.py, tests/test_reference_predication_interface.py  
Related Risks: R4, R12  
Related Decisions: ED-2026-04-ready-for-controlled-semantic-expansion

## Decision
`reference_predication` remains isolated in current phase via stable interface and feature-flagged activation.

## Consequence
Integration into `MasterChain` requires a formal checkpoint after Phase B.
