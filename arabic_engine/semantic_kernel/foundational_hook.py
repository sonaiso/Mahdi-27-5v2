"""
semantic_kernel-side adapter for foundational v1 integration hooks.

Non-invasive by design: exposes payload adapters only.
"""

from __future__ import annotations

from arabic_engine.foundational.integration import SemanticKernelFoundationalHook
from arabic_engine.foundational.models import FoundationalUnit


class SemanticKernelFoundationalAdapter:
    """Adapter namespace for semantic_kernel future attachment."""

    @staticmethod
    def from_foundational(unit: FoundationalUnit) -> dict[str, object]:
        return SemanticKernelFoundationalHook.payload(unit)

