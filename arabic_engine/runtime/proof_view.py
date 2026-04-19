"""
Proof view — generates a proof/audit trail from the master chain.

Provides a verifiable chain of evidence for every gate decision.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from arabic_engine.core.types_gate import GateResult
from arabic_engine.trace.replay import TraceReplayer

from .master_chain import MasterChain


@dataclass(frozen=True)
class ProofRecord:
    """A single proof record linking a gate result to its position."""

    index: int
    layer_name: str
    verdict: str
    reason: str
    missing_condition: str


class ProofView:
    """Generates a verifiable proof trail from the master chain."""

    @staticmethod
    def generate(chain: MasterChain) -> list[ProofRecord]:
        """Generate proof records for all gate results."""
        records: list[ProofRecord] = []
        for i, result in enumerate(chain.state.all_results):
            records.append(ProofRecord(
                index=i,
                layer_name=result.layer.name,
                verdict=result.verdict.name,
                reason=result.reason,
                missing_condition=result.missing_condition,
            ))
        return records

    @staticmethod
    def generate_trace_summary(chain: MasterChain) -> list[str]:
        """Generate a human-readable trace summary."""
        return TraceReplayer.replay(chain.tracer.log)
