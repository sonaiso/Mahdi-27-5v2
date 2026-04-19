"""
Mizan classifier — determines weight eligibility and pattern.

Answers: Is this unit eligible for a morphological weight?
What is its canonical pattern and root?
"""

from __future__ import annotations

from typing import Optional

from arabic_engine.core.enums_weight import WeightEligibility
from arabic_engine.core.enums_singular import WordCategory
from arabic_engine.core.types_weight import WeightRecord
from arabic_engine.core.types_singular import SingularUnit


class MizanClassifier:
    """Classifies a singular unit's weight ontology (eligibility, pattern, root)."""

    @staticmethod
    def classify(
        unit: SingularUnit,
        pattern: str = "",
        root: str = "",
        semantic_values: Optional[tuple[float, ...]] = None,
    ) -> WeightRecord:
        """Produce a WeightRecord with ontology fields populated.

        Particles are never weight-eligible.  Nouns and verbs require
        a non-empty pattern to be considered eligible.

        If semantic_values is provided (a 13-element tuple), a
        RootSemanticKernel is built and attached to the record.
        """
        record = WeightRecord()

        category = unit.conceptual.word_category
        if category is WordCategory.HARF:
            record.eligibility = WeightEligibility.NOT_ELIGIBLE
            return record

        if not pattern:
            record.eligibility = WeightEligibility.NOT_ELIGIBLE
            return record

        record.eligibility = WeightEligibility.ELIGIBLE
        record.pattern = pattern
        record.root = root

        # Build semantic kernel if values are provided
        if semantic_values is not None:
            from arabic_engine.semantic_kernel.root_kernel import (
                RootKernelBuilder,
                ROOT_SEMANTIC_DIM,
            )
            if len(semantic_values) != ROOT_SEMANTIC_DIM:
                # Graceful degradation: invalid length → skip kernel construction
                pass
            else:
                record.semantic_kernel = RootKernelBuilder.build(
                    root_text=root,
                    semantic_values=semantic_values,
                )

        return record
