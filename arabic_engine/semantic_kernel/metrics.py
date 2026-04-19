"""
Performance metrics for the semantic kernel layer.

Collects timing, throughput, and vector-operation counters for
profiling and diagnostics.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class TransferMetrics:
    """Aggregate metrics for semantic transfer operations."""

    transfer_count: int = 0
    total_transfer_time_ms: float = 0.0
    closure_pass_count: int = 0
    closure_fail_count: int = 0
    economy_total_cost: float = 0.0
    _timestamps: list[float] = field(default_factory=list, repr=False)

    @property
    def avg_transfer_time_ms(self) -> float:
        """Average time per transfer operation in milliseconds."""
        if self.transfer_count == 0:
            return 0.0
        return self.total_transfer_time_ms / self.transfer_count

    @property
    def closure_pass_rate(self) -> float:
        """Fraction of closures that pass (0.0-1.0)."""
        total = self.closure_pass_count + self.closure_fail_count
        if total == 0:
            return 0.0
        return self.closure_pass_count / total

    @property
    def avg_economy_cost(self) -> float:
        """Average economy cost per transfer."""
        if self.transfer_count == 0:
            return 0.0
        return self.economy_total_cost / self.transfer_count

    def record_transfer(self, duration_ms: float) -> None:
        """Record a completed transfer operation."""
        self.transfer_count += 1
        self.total_transfer_time_ms += duration_ms
        self._timestamps.append(time.monotonic())

    def record_closure(self, passed: bool) -> None:
        """Record a closure outcome."""
        if passed:
            self.closure_pass_count += 1
        else:
            self.closure_fail_count += 1

    def record_cost(self, cost: float) -> None:
        """Record an economy cost observation."""
        self.economy_total_cost += cost

    def reset(self) -> None:
        """Reset all metrics to zero."""
        self.transfer_count = 0
        self.total_transfer_time_ms = 0.0
        self.closure_pass_count = 0
        self.closure_fail_count = 0
        self.economy_total_cost = 0.0
        self._timestamps.clear()

    def summary(self) -> dict[str, float]:
        """Return a summary dictionary of all metrics."""
        return {
            "transfer_count": float(self.transfer_count),
            "avg_transfer_time_ms": self.avg_transfer_time_ms,
            "closure_pass_rate": self.closure_pass_rate,
            "avg_economy_cost": self.avg_economy_cost,
        }
