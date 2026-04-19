"""
Adjacency contract — enforces that layers are processed in strict order.

No layer N may be entered unless layer N-1 is closed.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult


class AdjacencyContract:
    """Enforces adjacency — no skipping layers."""

    # Ordered list of layers that must be processed in sequence
    LAYER_ORDER = [
        Layer.PRE_U0_ADMISSIBILITY,
        Layer.SINGULAR_PERCEPTUAL,
        Layer.SINGULAR_INFORMATIONAL,
        Layer.SINGULAR_CONCEPTUAL,
        Layer.WEIGHT_MIZAN,
        Layer.COMPOSITIONAL_ROLES,
        Layer.PROPOSITION,
        Layer.JUDGEMENT,
        Layer.QIYAS,
    ]

    @staticmethod
    def check(
        target_layer: Layer,
        closed_layers: set[Layer],
    ) -> GateResult:
        """Check whether *target_layer* may be entered given *closed_layers*.

        Every layer preceding *target_layer* in LAYER_ORDER must be in
        *closed_layers*.
        """
        target_idx = AdjacencyContract.LAYER_ORDER.index(target_layer)

        for i in range(target_idx):
            required = AdjacencyContract.LAYER_ORDER[i]
            if required not in closed_layers:
                return GateResult(
                    verdict=GateVerdict.REJECT,
                    layer=target_layer,
                    reason=f"الطبقة {required.name} غير مقفلة — لا يجوز الدخول في {target_layer.name}",
                    missing_condition=f"{required.name}_closed",
                )

        return GateResult(
            verdict=GateVerdict.PASS,
            layer=target_layer,
        )
