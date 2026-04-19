"""
Root kernel builder — converts a root from morphological material
into a computable semantic core (𝒦_root).

The root is no longer just a string of letters; it becomes a
13-dimensional semantic vector encoding the root's essential meaning.
"""

from __future__ import annotations

import math
import uuid

from arabic_engine.core.enums_semantic import SemanticDimension
from arabic_engine.core.types_semantic import RootSemanticKernel, SemanticVector

# Number of dimensions in a root semantic vector
ROOT_SEMANTIC_DIM = len(SemanticDimension)

# Canonical dimension names (ordered by enum value)
ROOT_DIMENSION_NAMES = tuple(d.name for d in SemanticDimension)


class RootKernelBuilder:
    """Builds a RootSemanticKernel from raw root data.

    Converts the root from a morphological string into a computable
    semantic vector with identity and transformability scores.
    """

    @staticmethod
    def build(
        root_text: str,
        phonological_sig: str = "",
        structural_sig: str = "",
        semantic_values: tuple[float, ...] = (),
        root_id: str = "",
    ) -> RootSemanticKernel:
        """Build a root semantic kernel.

        Args:
            root_text: The root letters (e.g. "ك ت ب").
            phonological_sig: Phonological signature.
            structural_sig: Structural/ordering signature.
            semantic_values: 13-element tuple of float values,
                one per SemanticDimension.
            root_id: Optional unique ID; auto-generated if empty.

        Returns:
            A fully populated RootSemanticKernel.

        Raises:
            ValueError: If semantic_values does not have exactly 13 elements.
        """
        if len(semantic_values) != ROOT_SEMANTIC_DIM:
            raise ValueError(
                f"semantic_values must have exactly {ROOT_SEMANTIC_DIM} elements, "
                f"got {len(semantic_values)}"
            )

        vec = SemanticVector(
            values=semantic_values,
            dimension_names=ROOT_DIMENSION_NAMES,
        )

        identity_score = RootKernelBuilder._compute_identity_score(vec)
        transformability_score = RootKernelBuilder._compute_transformability_score(vec)

        return RootSemanticKernel(
            root_id=root_id or f"root-{uuid.uuid4().hex[:8]}",
            root_text=root_text,
            phonological_signature=phonological_sig,
            structural_signature=structural_sig,
            semantic_vector=vec,
            identity_score=identity_score,
            transformability_score=transformability_score,
        )

    @staticmethod
    def _compute_identity_score(vec: SemanticVector) -> float:
        """Compute identity score — how concentrated the root's meaning is.

        A root with one dominant dimension has high identity;
        a root spread evenly across dimensions has lower identity.
        Uses normalized entropy: 1 - H(v)/log(dim).
        """
        total = sum(abs(v) for v in vec.values)
        if total == 0.0:
            return 0.0

        probs = [abs(v) / total for v in vec.values]
        entropy = -sum(p * math.log(p) if p > 0 else 0.0 for p in probs)
        max_entropy = math.log(vec.dim)
        if max_entropy == 0.0:
            return 1.0

        return 1.0 - (entropy / max_entropy)

    @staticmethod
    def _compute_transformability_score(vec: SemanticVector) -> float:
        """Compute transformability — how amenable the root is to pattern shifts.

        Roots with moderate spread across dimensions (not too concentrated,
        not too uniform) are most transformable.
        Uses: 4 * H_norm * (1 - H_norm) where H_norm = H/log(dim).
        This peaks at H_norm = 0.5.
        """
        total = sum(abs(v) for v in vec.values)
        if total == 0.0:
            return 0.0

        probs = [abs(v) / total for v in vec.values]
        entropy = -sum(p * math.log(p) if p > 0 else 0.0 for p in probs)
        max_entropy = math.log(vec.dim)
        if max_entropy == 0.0:
            return 0.0

        h_norm = entropy / max_entropy
        return 4.0 * h_norm * (1.0 - h_norm)
