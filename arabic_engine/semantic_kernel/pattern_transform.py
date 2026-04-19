"""
Pattern transform builder — converts a weight/pattern from a surface
template into a semantic transformation operator.

The pattern is no longer just a phonological template (فَعَلَ);
it becomes a 12-dimensional transform vector that shifts root meaning.
"""

from __future__ import annotations

import math
import uuid

from arabic_engine.core.enums_semantic import PatternSemanticDimension
from arabic_engine.core.types_semantic import PatternSemanticTransform, SemanticVector

# Number of dimensions in a pattern transform vector
PATTERN_SEMANTIC_DIM = len(PatternSemanticDimension)

# Canonical dimension names (ordered by enum value)
PATTERN_DIMENSION_NAMES = tuple(d.name for d in PatternSemanticDimension)


class PatternTransformBuilder:
    """Builds a PatternSemanticTransform from raw pattern data.

    Converts the pattern from a phonological template into a computable
    semantic transformation operator.
    """

    @staticmethod
    def build(
        pattern_code: str,
        surface_template: str = "",
        transform_values: tuple[float, ...] = (),
        morphological_cost: float = 0.0,
        pattern_id: str = "",
    ) -> PatternSemanticTransform:
        """Build a pattern semantic transform.

        Args:
            pattern_code: The canonical pattern (e.g. "فَعَلَ").
            surface_template: The surface realization template.
            transform_values: 12-element tuple of float values,
                one per PatternSemanticDimension.
            morphological_cost: Cost of this pattern.
            pattern_id: Optional unique ID; auto-generated if empty.

        Returns:
            A fully populated PatternSemanticTransform.

        Raises:
            ValueError: If transform_values does not have exactly 12 elements.
        """
        if len(transform_values) != PATTERN_SEMANTIC_DIM:
            raise ValueError(
                f"transform_values must have exactly {PATTERN_SEMANTIC_DIM} elements, "
                f"got {len(transform_values)}"
            )

        vec = SemanticVector(
            values=transform_values,
            dimension_names=PATTERN_DIMENSION_NAMES,
        )

        closure_index = PatternTransformBuilder._compute_closure_index(vec)

        return PatternSemanticTransform(
            pattern_id=pattern_id or f"pat-{uuid.uuid4().hex[:8]}",
            pattern_code=pattern_code,
            surface_template=surface_template or pattern_code,
            semantic_transform_vector=vec,
            closure_index=closure_index,
            morphological_cost=morphological_cost,
        )

    @staticmethod
    def _compute_closure_index(vec: SemanticVector) -> float:
        """Compute closure index — how strongly the pattern closes meaning.

        A pattern with large transform magnitudes has a higher closure index.
        Defined as: norm(vec) / sqrt(dim), clamped to [0, 1].
        """
        n = vec.norm()
        max_possible = math.sqrt(vec.dim)  # if all values were 1.0
        if max_possible == 0.0:
            return 0.0
        return min(n / max_possible, 1.0)
