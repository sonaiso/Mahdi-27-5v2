"""
Runtime view — a runtime adapter over the master chain state.

Provides a simplified read-only view of the current processing state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.enums_gate import ClosureStatus

from .master_chain import MasterChain


@dataclass(frozen=True)
class RuntimeSnapshot:
    """Immutable snapshot of the master chain state."""

    current_layer: Layer
    closed_layers: frozenset[Layer]
    singular_closed: bool
    weight_closed: bool
    composition_closed: bool
    proposition_closed: bool
    judgement_closed: bool
    qiyas_closed: bool
    language_closed: bool
    total_gate_results: int
    total_errors: int


class RuntimeView:
    """Read-only adapter over the master chain."""

    @staticmethod
    def snapshot(chain: MasterChain) -> RuntimeSnapshot:
        """Take a snapshot of the current chain state."""
        state = chain.state
        return RuntimeSnapshot(
            current_layer=state.current_layer,
            closed_layers=frozenset(state.closed_layers),
            singular_closed=Layer.SINGULAR_CONCEPTUAL in state.closed_layers,
            weight_closed=Layer.WEIGHT_MIZAN in state.closed_layers,
            composition_closed=Layer.COMPOSITIONAL_ROLES in state.closed_layers,
            proposition_closed=Layer.PROPOSITION in state.closed_layers,
            judgement_closed=Layer.JUDGEMENT in state.closed_layers,
            qiyas_closed=Layer.QIYAS in state.closed_layers,
            language_closed=Layer.LANGUAGE in state.closed_layers,
            total_gate_results=len(state.all_results),
            total_errors=sum(1 for r in state.all_results if not r.passed),
        )
