"""
Economy optimizer — selects the optimal form by minimizing total cost
subject to the minimum-completeness constraint.

    x* = argmin_x Cost(x) s.t. Complete_min(x) = 1

Cost(x) = Cost_phon + Cost_morph + Cost_cog + Cost_sem
"""

from __future__ import annotations

from arabic_engine.core.types_semantic import (
    SemanticCost,
    SemanticTransferResult,
)


class EconomyOptimizer:
    """Computes costs and selects the most economical transfer result."""

    @staticmethod
    def compute_cost(result: SemanticTransferResult) -> SemanticCost:
        """Compute the multi-dimensional cost of a semantic transfer result.

        Cost components:
        - phonological_cost: derived from pattern morphological cost
        - morphological_cost: derived from pattern morphological cost
        - cognitive_cost: inverse of compatibility score (higher compat = lower cost)
        - semantic_ambiguity_cost: inverse of transformation score
        """
        pat = result.pattern_transform

        # Phonological cost scales with morphological cost of the pattern
        phonological_cost = pat.morphological_cost * 0.5

        # Morphological cost is the pattern's direct cost
        morphological_cost = pat.morphological_cost

        # Cognitive cost — lower compatibility means higher cognitive load
        cognitive_cost = 1.0 - result.compatibility_score

        # Semantic ambiguity — lower transformation score means higher ambiguity
        semantic_ambiguity_cost = 1.0 - max(0.0, result.transformation_score)

        return SemanticCost(
            phonological_cost=phonological_cost,
            morphological_cost=morphological_cost,
            cognitive_cost=cognitive_cost,
            semantic_ambiguity_cost=semantic_ambiguity_cost,
        )

    @staticmethod
    def select_optimal(
        candidates: list[SemanticTransferResult],
    ) -> SemanticTransferResult | None:
        """Select the candidate with the lowest total cost.

        Implements: x* = argmin_x Cost(x) s.t. Complete_min(x) = 1

        The completeness constraint is assumed to have been checked
        before candidates are passed here. All candidates are assumed valid.

        Returns None if the candidate list is empty.
        """
        if not candidates:
            return None

        best: SemanticTransferResult | None = None
        best_cost = float("inf")

        for candidate in candidates:
            cost = EconomyOptimizer.compute_cost(candidate)
            if cost.total < best_cost:
                best_cost = cost.total
                best = candidate

        return best
