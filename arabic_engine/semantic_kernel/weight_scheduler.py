"""
Adaptive weight scheduler — adjusts blending weights based on root/pattern properties.

Default weights (W_r=0.50, W_p=0.30, W_f=0.15, W_ctx=0.05) work well for
prototypical triliteral verbs, but can be adapted to produce better results
for different root types, pattern classes, and contexts.

Strategy:
  - Roots with high transformability_score → lower W_r, higher W_p
    (the root readily transforms, so the pattern matters more)
  - Roots with high identity_score → higher W_r, lower W_p
    (the root resists transformation, so it dominates)
  - Nominalizing patterns → higher W_f
    (the form's grammatical features matter more for nouns)
"""

from __future__ import annotations

from dataclasses import dataclass

from arabic_engine.core.types_semantic import (
    FormSemanticProfile,
    PatternSemanticTransform,
    RootSemanticKernel,
)


@dataclass(frozen=True)
class BlendingWeights:
    """A set of blending weights for the transfer equation.

    K_F = w_root · r_sem + w_pattern · p_sem + w_form · f_sem + w_context · Δ_ctx
    """

    w_root: float = 0.50
    w_pattern: float = 0.30
    w_form: float = 0.15
    w_context: float = 0.05


# The default weights
DEFAULT_WEIGHTS = BlendingWeights()


class WeightScheduler:
    """Adapts blending weights based on root/pattern/form properties.

    Instead of using fixed weights, the scheduler examines the root's
    identity and transformability scores, the pattern's closure index,
    and the form's characteristics to produce context-appropriate weights.
    """

    @staticmethod
    def schedule(
        root_kernel: RootSemanticKernel,
        pattern_transform: PatternSemanticTransform,
        form_profile: FormSemanticProfile,
    ) -> BlendingWeights:
        """Compute adaptive blending weights.

        The adjustment strategy:
        1. Start from default weights (0.50, 0.30, 0.15, 0.05)
        2. If root has high transformability → shift weight from root to pattern
        3. If root has high identity → shift weight from pattern to root
        4. If pattern has high closure_index (strong nominalization) → boost form
        5. Normalize so total sums to 1.0

        Args:
            root_kernel: The root semantic kernel with scores.
            pattern_transform: The pattern with closure index.
            form_profile: The form profile.

        Returns:
            Adapted BlendingWeights.
        """
        w_r = 0.50
        w_p = 0.30
        w_f = 0.15
        w_ctx = 0.05

        # Adjustment based on root transformability
        # High transformability → root yields to pattern
        t_score = root_kernel.transformability_score
        if t_score > 0.6:
            shift = (t_score - 0.6) * 0.25  # max shift ≈ 0.10
            w_r -= shift
            w_p += shift

        # Adjustment based on root identity
        # High identity → root dominates
        i_score = root_kernel.identity_score
        if i_score > 0.5:
            shift = (i_score - 0.5) * 0.15  # max shift ≈ 0.075
            w_r += shift
            w_p -= shift

        # Adjustment based on pattern closure index
        # High closure → pattern strongly shapes meaning, boost form to compensate
        c_index = pattern_transform.closure_index
        if c_index > 0.4:
            shift = (c_index - 0.4) * 0.10  # max shift ≈ 0.06
            w_f += shift
            w_p -= shift * 0.5
            w_r -= shift * 0.5

        # Clamp all weights to [0.01, 0.95] to avoid extremes
        w_r = max(0.01, min(0.95, w_r))
        w_p = max(0.01, min(0.95, w_p))
        w_f = max(0.01, min(0.95, w_f))
        w_ctx = max(0.01, min(0.95, w_ctx))

        # Normalize to sum to 1.0
        total = w_r + w_p + w_f + w_ctx
        if total > 0.0:
            w_r /= total
            w_p /= total
            w_f /= total
            w_ctx /= total

        return BlendingWeights(
            w_root=w_r,
            w_pattern=w_p,
            w_form=w_f,
            w_context=w_ctx,
        )
