"""
Compatibility checker — validates root–pattern compatibility
and the minimum-completeness condition (الحد الأدنى المكتمل).

Complete_min(R,P,F) ⟺ ValidRoot(R) ∧ ValidPattern(P) ∧ Compatible(R,P) ∧ Realizable(F)

Uses a two-stage check:
  1. Dimension-overlap heuristic (fast pre-filter)
  2. Cosine-similarity on projected vectors (precise check)
"""

from __future__ import annotations

import math

from arabic_engine.core.enums_semantic import CompatibilityStatus
from arabic_engine.core.types_semantic import (
    FormSemanticProfile,
    PatternSemanticTransform,
    RootSemanticKernel,
    SemanticVector,
)
from .alignment import project_root_to_pattern_space

# Minimum match ratio (active pattern dims with non-zero root dims / active pattern dims)
# to consider root–pattern compatible.  A ratio ≥ 0.5 → COMPATIBLE, > 0.0 → PARTIAL.
_OVERLAP_COMPAT_RATIO = 0.5

# Cosine-similarity threshold: ≥ this value → COMPATIBLE, ≥ 0.0 → PARTIAL.
_COSINE_COMPAT_THRESHOLD = 0.0


class CompatibilityChecker:
    """Checks compatibility between root, pattern, and form."""

    @staticmethod
    def check_root_pattern(
        root_kernel: RootSemanticKernel,
        pattern_transform: PatternSemanticTransform,
    ) -> CompatibilityStatus:
        """Check whether a root is compatible with a pattern.

        Two-stage check:
          1. Dimension-overlap: counts how many non-zero pattern dimensions
             correspond to non-zero root dimensions (fast pre-filter).
          2. Cosine-similarity: projects root vector into pattern space and
             measures directional alignment (precise).

        Returns:
            CompatibilityStatus — COMPATIBLE, INCOMPATIBLE, or PARTIAL.
        """
        r_vec = root_kernel.semantic_vector
        p_vec = pattern_transform.semantic_transform_vector

        if r_vec.dim == 0 or p_vec.dim == 0:
            return CompatibilityStatus.INCOMPATIBLE

        # Check if root has any semantic content
        r_sum = sum(abs(v) for v in r_vec.values)
        if r_sum == 0.0:
            return CompatibilityStatus.INCOMPATIBLE

        # Check if pattern has any transform content
        p_sum = sum(abs(v) for v in p_vec.values)
        if p_sum == 0.0:
            # A zero-transform pattern is a neutral passthrough — always compatible
            return CompatibilityStatus.COMPATIBLE

        # Stage 1: Dimension-overlap heuristic (fast pre-filter)
        overlap_dim = min(r_vec.dim, p_vec.dim)
        active_pattern_dims = sum(
            1 for i in range(overlap_dim) if abs(p_vec.values[i]) > 0.0
        )
        matching_dims = sum(
            1 for i in range(overlap_dim)
            if abs(p_vec.values[i]) > 0.0 and abs(r_vec.values[i]) > 0.0
        )

        if active_pattern_dims == 0:
            return CompatibilityStatus.COMPATIBLE

        match_ratio = matching_dims / active_pattern_dims

        # If overlap check clearly rejects, no need for cosine
        if match_ratio == 0.0:
            return CompatibilityStatus.INCOMPATIBLE

        # Stage 2: Cosine-similarity on projected vectors
        r_projected = project_root_to_pattern_space(r_vec)
        cosine_sim = r_projected.cosine_similarity(p_vec)

        if match_ratio >= _OVERLAP_COMPAT_RATIO and cosine_sim >= _COSINE_COMPAT_THRESHOLD:
            return CompatibilityStatus.COMPATIBLE
        elif match_ratio > 0.0 or cosine_sim >= _COSINE_COMPAT_THRESHOLD:
            return CompatibilityStatus.PARTIAL
        else:
            return CompatibilityStatus.INCOMPATIBLE

    @staticmethod
    def cosine_compatibility_score(
        root_kernel: RootSemanticKernel,
        pattern_transform: PatternSemanticTransform,
    ) -> float:
        """Return the cosine-similarity score between projected root and pattern.

        Projects root vector into pattern space, then computes cosine similarity.
        Returns 0.0 if either vector is zero.
        """
        r_vec = root_kernel.semantic_vector
        p_vec = pattern_transform.semantic_transform_vector
        if r_vec.dim == 0 or p_vec.dim == 0:
            return 0.0
        r_projected = project_root_to_pattern_space(r_vec)
        return r_projected.cosine_similarity(p_vec)

    @staticmethod
    def valid_root(root_kernel: RootSemanticKernel) -> bool:
        """Check whether a root kernel is valid.

        A valid root must have:
        - Non-empty root text
        - A 13-dimensional semantic vector
        - At least one non-zero semantic dimension
        """
        if not root_kernel.root_text:
            return False
        if root_kernel.semantic_vector.dim != 13:
            return False
        if sum(abs(v) for v in root_kernel.semantic_vector.values) == 0.0:
            return False
        return True

    @staticmethod
    def valid_pattern(pattern_transform: PatternSemanticTransform) -> bool:
        """Check whether a pattern transform is valid.

        A valid pattern must have:
        - Non-empty pattern code
        - A 12-dimensional transform vector
        """
        if not pattern_transform.pattern_code:
            return False
        if pattern_transform.semantic_transform_vector.dim != 12:
            return False
        return True

    @staticmethod
    def realizable_form(form_profile: FormSemanticProfile) -> bool:
        """Check whether a form profile is realizable.

        A realizable form must have:
        - Non-empty pattern_id
        - A 9-dimensional form vector
        - At least one non-zero dimension
        """
        if not form_profile.pattern_id:
            return False
        if form_profile.form_semantic_vector.dim != 9:
            return False
        if sum(abs(v) for v in form_profile.form_semantic_vector.values) == 0.0:
            return False
        return True

    @staticmethod
    def check_complete_min(
        root_kernel: RootSemanticKernel,
        pattern_transform: PatternSemanticTransform,
        form_profile: FormSemanticProfile,
    ) -> bool:
        """Check the minimum-completeness condition.

        Complete_min(R,P,F) ⟺
            ValidRoot(R) ∧ ValidPattern(P) ∧ Compatible(R,P) ∧ Realizable(F)
        """
        if not CompatibilityChecker.valid_root(root_kernel):
            return False
        if not CompatibilityChecker.valid_pattern(pattern_transform):
            return False

        compat = CompatibilityChecker.check_root_pattern(
            root_kernel, pattern_transform
        )
        if compat is CompatibilityStatus.INCOMPATIBLE:
            return False

        if not CompatibilityChecker.realizable_form(form_profile):
            return False

        return True
