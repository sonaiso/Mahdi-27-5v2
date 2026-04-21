"""
Non-invasive integration hooks for semantic_kernel and language.
"""

from __future__ import annotations

from .models import FoundationalUnit


class SemanticKernelFoundationalHook:
    """Hook payload for future semantic_kernel attachment."""

    @staticmethod
    def payload(unit: FoundationalUnit) -> dict[str, object]:
        return {
            "attachment_point": "semantic_kernel",
            "scope": "letter+diacritic",
            "symbolic": {
                "letter_codepoint": unit.letter.codepoint if unit.letter else None,
                "diacritic_codepoint": unit.diacritic.codepoint if unit.diacritic else None,
                "letter_normalized": unit.letter.normalized_symbol if unit.letter else "",
                "diacritic_normalized": unit.diacritic.normalized_symbol if unit.diacritic else "",
            },
            "trace_id": "foundational.hook.semantic-kernel",
        }


class LanguageFoundationalHook:
    """Hook payload for future language attachment."""

    @staticmethod
    def payload(unit: FoundationalUnit) -> dict[str, object]:
        return {
            "attachment_point": "language",
            "scope": "letter+diacritic",
            "ontology": {
                "letter_essential": dict(unit.ontology.letter_essential),
                "diacritic_essential": dict(unit.ontology.diacritic_essential),
                "contextual": dict(unit.ontology.contextual),
            },
            "trace_id": "foundational.hook.language",
        }


class FoundationalIntegrationBridge:
    """Produces traceable, integration-ready mapping without runtime wiring."""

    @staticmethod
    def traceability_mapping(unit: FoundationalUnit) -> dict[str, object]:
        return {
            "model_scope": "v1-letter-diacritic-foundation",
            "future_attachment_points": [
                "arabic_engine.semantic_kernel.foundational_hook",
                "arabic_engine.language.foundational_hook",
            ],
            "contracts": [
                "symbolic_identity_invariant",
                "normalization_invariant",
                "ontological_property_completeness_invariant",
                "essential_contextual_separation_invariant",
            ],
            "hooks": [
                SemanticKernelFoundationalHook.payload(unit),
                LanguageFoundationalHook.payload(unit),
            ],
            "trace_id": "foundational.traceability.mapping",
        }

