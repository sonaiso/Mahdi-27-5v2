"""
Context delta builder — constructs contextual adjustment vectors (Δ_ctx).

The context delta modifies the semantic transfer equation output:

    K_F = W_r · r_sem + W_p · p_sem + W_f · f_sem + Δ_ctx

Δ_ctx captures adjustments from:
  - syntactic_position: where the word appears in the sentence
  - discourse_role: the word's role in discourse (topic, focus, etc.)
  - collocational_bias: frequency-based bias from common collocations
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

from arabic_engine.core.types_semantic import SemanticVector


# Common dimension count for context vectors (matches root's 13-dim space)
_CONTEXT_DIM = 13


@dataclass(frozen=True)
class ContextFeatures:
    """Raw context features that influence the semantic transfer.

    Attributes:
        syntactic_position: Normalized position in the sentence [0.0, 1.0].
            0.0 = sentence-initial, 1.0 = sentence-final.
        discourse_role: Discourse role weight.
            Higher values for topicalized or focused elements.
        collocational_bias: Bias vector from common collocations.
            Optional 13-dim vector of adjustment values.
        negation: Whether the context is negated (flips agency/causality).
        emphasis: Emphasis level [0.0, 1.0].
            Higher values for emphatic constructions.
    """

    syntactic_position: float = 0.5
    discourse_role: float = 0.0
    collocational_bias: Optional[tuple[float, ...]] = None
    negation: bool = False
    emphasis: float = 0.0


class ContextDeltaBuilder:
    """Builds a context delta vector (Δ_ctx) from contextual features.

    The context delta adjusts the semantic transfer to account for
    pragmatic and syntactic context that morphology alone cannot capture.
    """

    @staticmethod
    def build(features: ContextFeatures) -> SemanticVector:
        """Build a context delta vector from features.

        The delta is constructed as:
          - Sentence-initial position boosts AGENCY (+0.1)
          - Sentence-final position boosts RESULTATIVITY (+0.1)
          - Discourse role boosts TRANSFERABILITY
          - Negation inverts AGENCY and CAUSALITY components
          - Emphasis amplifies EVENT and QUALITY components
          - Collocational bias is added directly if provided

        Returns:
            A 13-dim SemanticVector representing Δ_ctx.
        """
        values = [0.0] * _CONTEXT_DIM

        # Syntactic position effects
        # Sentence-initial → boost agency (index 4)
        if features.syntactic_position < 0.3:
            values[4] += 0.1 * (0.3 - features.syntactic_position) / 0.3
        # Sentence-final → boost resultativity (index 7)
        if features.syntactic_position > 0.7:
            values[7] += 0.1 * (features.syntactic_position - 0.7) / 0.3

        # Discourse role → boost transferability (index 12)
        values[12] += features.discourse_role * 0.15

        # Negation → invert agency (4) and causality (6)
        if features.negation:
            values[4] -= 0.2
            values[6] -= 0.2

        # Emphasis → amplify event (1) and quality (2)
        if features.emphasis > 0.0:
            values[1] += features.emphasis * 0.1
            values[2] += features.emphasis * 0.1

        # Collocational bias — direct addition (validated)
        if features.collocational_bias is not None:
            for i in range(min(len(features.collocational_bias), _CONTEXT_DIM)):
                val = features.collocational_bias[i]
                if math.isfinite(val):
                    values[i] += val

        return SemanticVector(values=tuple(values))

    @staticmethod
    def zero() -> SemanticVector:
        """Return a zero context delta (no adjustment)."""
        return SemanticVector(values=tuple(0.0 for _ in range(_CONTEXT_DIM)))
