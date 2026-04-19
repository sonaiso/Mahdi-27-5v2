"""
Semantic transfer engine — the core of the semantic kernel layer.

Implements the semantic transfer equation:

    K_F = W_r · r_sem + W_p · p_sem + W_f · f_sem + Δ_ctx

This is the function that transports meaning from root to form.
Vectors are projected into a common 13-dim root space using semantic
alignment mappings before blending.
"""

from __future__ import annotations

import uuid
from typing import Optional

from arabic_engine.core.enums_gate import ClosureStatus
from arabic_engine.core.enums_semantic import CompatibilityStatus
from arabic_engine.core.types_semantic import (
    FormSemanticProfile,
    PatternSemanticTransform,
    RootSemanticKernel,
    SemanticTransferResult,
    SemanticVector,
)

from .alignment import project_to_common_space
from .compatibility import CompatibilityChecker

# Default blending weights for the transfer equation
DEFAULT_W_ROOT = 0.50     # Weight of root semantic vector
DEFAULT_W_PATTERN = 0.30  # Weight of pattern transform vector
DEFAULT_W_FORM = 0.15     # Weight of form semantic vector
DEFAULT_W_CONTEXT = 0.05  # Weight of context delta


class SemanticTransferEngine:
    """Transfers semantic meaning from root through pattern to form.

    The transfer equation:
        K_F = W_r · r_sem + W_p · p_sem + W_f · f_sem + Δ_ctx

    where:
        r_sem = root semantic vector (13-dim)
        p_sem = pattern transform vector (12-dim)
        f_sem = form semantic vector (9-dim)
        Δ_ctx = context adjustment vector

    All vectors are projected into a common 13-dim root space using
    semantic alignment mappings before blending.
    """

    @staticmethod
    def transfer(
        root_kernel: RootSemanticKernel,
        pattern_transform: PatternSemanticTransform,
        form_profile: FormSemanticProfile,
        context_delta: Optional[SemanticVector] = None,
        w_root: float = DEFAULT_W_ROOT,
        w_pattern: float = DEFAULT_W_PATTERN,
        w_form: float = DEFAULT_W_FORM,
        w_context: float = DEFAULT_W_CONTEXT,
        transfer_id: str = "",
    ) -> SemanticTransferResult:
        """Execute the semantic transfer.

        Args:
            root_kernel: The root semantic kernel.
            pattern_transform: The pattern semantic transform.
            form_profile: The form semantic profile.
            context_delta: Optional context adjustment vector.
            w_root: Weight for root contribution.
            w_pattern: Weight for pattern contribution.
            w_form: Weight for form contribution.
            w_context: Weight for context contribution.
            transfer_id: Optional unique ID; auto-generated if empty.

        Returns:
            A SemanticTransferResult with the computed output kernel.
        """
        # Project all vectors into the common 13-dim root space
        # using semantic alignment mappings
        r_proj, p_proj, f_proj = project_to_common_space(
            root_kernel.semantic_vector,
            pattern_transform.semantic_transform_vector,
            form_profile.form_semantic_vector,
        )

        out_dim = r_proj.dim  # always 13

        # Context delta
        if context_delta is not None:
            ctx_proj = SemanticTransferEngine._project(context_delta, out_dim)
        else:
            ctx_proj = SemanticVector(values=tuple(0.0 for _ in range(out_dim)))

        # K_F = W_r · r_sem + W_p · p_sem + W_f · f_sem + Δ_ctx
        output = (
            r_proj.scale(w_root)
            .add(p_proj.scale(w_pattern))
            .add(f_proj.scale(w_form))
            .add(ctx_proj.scale(w_context))
        )

        # Compute transformation score (cosine similarity between input and output)
        transformation_score = r_proj.cosine_similarity(output)

        # Compute compatibility score
        compat = CompatibilityChecker.check_root_pattern(
            root_kernel, pattern_transform
        )
        if compat is CompatibilityStatus.COMPATIBLE:
            compatibility_score = 1.0
        elif compat is CompatibilityStatus.PARTIAL:
            compatibility_score = 0.5
        else:
            compatibility_score = 0.0

        return SemanticTransferResult(
            transfer_id=transfer_id or f"xfer-{uuid.uuid4().hex[:8]}",
            root_kernel=root_kernel,
            pattern_transform=pattern_transform,
            form_profile=form_profile,
            input_kernel=root_kernel.semantic_vector,
            output_kernel=output,
            transformation_score=transformation_score,
            compatibility_score=compatibility_score,
            closure=ClosureStatus.OPEN,
        )

    @staticmethod
    def _project(vec: SemanticVector, target_dim: int) -> SemanticVector:
        """Project a vector to a target dimension by padding or truncating."""
        if vec.dim == target_dim:
            return vec
        if vec.dim < target_dim:
            # Pad with zeros
            padded = vec.values + tuple(0.0 for _ in range(target_dim - vec.dim))
            return SemanticVector(values=padded)
        # Truncate
        return SemanticVector(values=vec.values[:target_dim])
