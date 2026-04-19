"""
Semantic data types for the Arabic Cognitive Fractal Engine.

Defines data structures for the semantic kernel layer:
SemanticVector, RootSemanticKernel, PatternSemanticTransform,
FormSemanticProfile, SemanticTransferResult, and SemanticCost.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from .enums_gate import ClosureStatus


# ---------------------------------------------------------------------------
# SemanticVector — the foundational mathematical structure
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SemanticVector:
    """An immutable vector in a named semantic space.

    Each component corresponds to a named dimension (e.g. ENTITY, EVENT).
    All vector arithmetic is built-in with no external dependencies.
    """

    values: tuple[float, ...]
    dimension_names: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.dimension_names and len(self.dimension_names) != len(self.values):
            raise ValueError(
                f"dimension_names length ({len(self.dimension_names)}) "
                f"must match values length ({len(self.values)})"
            )

    @property
    def dim(self) -> int:
        """Number of dimensions in this vector."""
        return len(self.values)

    def dot(self, other: SemanticVector) -> float:
        """Compute the dot product with another vector."""
        if self.dim != other.dim:
            raise ValueError(
                f"Cannot dot vectors of different dimensions: {self.dim} vs {other.dim}"
            )
        return sum(a * b for a, b in zip(self.values, other.values))

    def norm(self) -> float:
        """Compute the L2 norm of this vector."""
        return math.sqrt(sum(v * v for v in self.values))

    def cosine_similarity(self, other: SemanticVector) -> float:
        """Compute cosine similarity with another vector.

        Returns 0.0 if either vector has zero norm.
        """
        n1 = self.norm()
        n2 = other.norm()
        if n1 == 0.0 or n2 == 0.0:
            return 0.0
        return self.dot(other) / (n1 * n2)

    def add(self, other: SemanticVector) -> SemanticVector:
        """Element-wise addition with another vector."""
        if self.dim != other.dim:
            raise ValueError(
                f"Cannot add vectors of different dimensions: {self.dim} vs {other.dim}"
            )
        return SemanticVector(
            values=tuple(a + b for a, b in zip(self.values, other.values)),
            dimension_names=self.dimension_names or other.dimension_names,
        )

    def scale(self, factor: float) -> SemanticVector:
        """Multiply every component by a scalar factor."""
        return SemanticVector(
            values=tuple(v * factor for v in self.values),
            dimension_names=self.dimension_names,
        )


# ---------------------------------------------------------------------------
# RootSemanticKernel — 𝒦_root
# ---------------------------------------------------------------------------

@dataclass
class RootSemanticKernel:
    """Semantic kernel of a root — converts a root from morphological
    material into a computable semantic core.

    Attributes:
        root_id: Unique identifier for this root kernel.
        root_text: The root letters (e.g. "ك ت ب").
        phonological_signature: Phonological signature string.
        structural_signature: Structural/ordering signature string.
        semantic_vector: 13-dimensional semantic vector (one per SemanticDimension).
        identity_score: How much identity is preserved across transformations.
        transformability_score: How amenable the root is to pattern transforms.
    """

    root_id: str = ""
    root_text: str = ""
    phonological_signature: str = ""
    structural_signature: str = ""
    semantic_vector: SemanticVector = field(
        default_factory=lambda: SemanticVector(values=())
    )
    identity_score: float = 0.0
    transformability_score: float = 0.0


# ---------------------------------------------------------------------------
# PatternSemanticTransform — الوزن كمؤثر تحويلي
# ---------------------------------------------------------------------------

@dataclass
class PatternSemanticTransform:
    """Semantic transform of a pattern/weight — converts the pattern from
    a surface template into a semantic transformation operator.

    Attributes:
        pattern_id: Unique identifier for this pattern.
        pattern_code: The canonical pattern code (e.g. "فَعَلَ").
        surface_template: The surface realization template.
        semantic_transform_vector: 12-dimensional transform vector
            (one per PatternSemanticDimension).
        closure_index: How completely the pattern closes the root meaning.
        morphological_cost: Morphological cost of this pattern.
    """

    pattern_id: str = ""
    pattern_code: str = ""
    surface_template: str = ""
    semantic_transform_vector: SemanticVector = field(
        default_factory=lambda: SemanticVector(values=())
    )
    closure_index: float = 0.0
    morphological_cost: float = 0.0


# ---------------------------------------------------------------------------
# FormSemanticProfile — الملف الدلالي للصيغة
# ---------------------------------------------------------------------------

@dataclass
class FormSemanticProfile:
    """Semantic profile of a grammatical form.

    Attributes:
        form_id: Unique identifier for this form.
        pattern_id: Which pattern this form belongs to.
        form_semantic_vector: 9-dimensional form vector
            (one per FormSemanticDimension).
    """

    form_id: str = ""
    pattern_id: str = ""
    form_semantic_vector: SemanticVector = field(
        default_factory=lambda: SemanticVector(values=())
    )


# ---------------------------------------------------------------------------
# SemanticTransferResult — نتيجة نقل حمولة المعنى
# ---------------------------------------------------------------------------

@dataclass
class SemanticTransferResult:
    """Result of the semantic transfer operation: K_F = W_r·r + W_p·p + W_f·f + Δ_ctx.

    Attributes:
        transfer_id: Unique identifier for this transfer.
        root_kernel: The input root semantic kernel.
        pattern_transform: The pattern semantic transform applied.
        form_profile: The form semantic profile applied.
        input_kernel: The root's semantic vector (input to the transfer).
        output_kernel: The form-level semantic kernel 𝒦_form (output).
        transformation_score: Cosine similarity between input and output.
        compatibility_score: Root–pattern compatibility score.
        closure: Closure status of this transfer result.
    """

    transfer_id: str = ""
    root_kernel: RootSemanticKernel = field(default_factory=RootSemanticKernel)
    pattern_transform: PatternSemanticTransform = field(
        default_factory=PatternSemanticTransform
    )
    form_profile: FormSemanticProfile = field(default_factory=FormSemanticProfile)
    input_kernel: SemanticVector = field(
        default_factory=lambda: SemanticVector(values=())
    )
    output_kernel: SemanticVector = field(
        default_factory=lambda: SemanticVector(values=())
    )
    transformation_score: float = 0.0
    compatibility_score: float = 0.0
    closure: ClosureStatus = ClosureStatus.OPEN


# ---------------------------------------------------------------------------
# SemanticCost — الكلفة الإجمالية
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SemanticCost:
    """Multi-dimensional cost of a semantic transfer.

    Cost(x) = Cost_phon + Cost_morph + Cost_cog + Cost_sem
    """

    phonological_cost: float = 0.0
    morphological_cost: float = 0.0
    cognitive_cost: float = 0.0
    semantic_ambiguity_cost: float = 0.0

    @property
    def total(self) -> float:
        """Total cost across all dimensions."""
        return (
            self.phonological_cost
            + self.morphological_cost
            + self.cognitive_cost
            + self.semantic_ambiguity_cost
        )
