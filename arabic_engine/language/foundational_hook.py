"""
language-side adapter for foundational v1 integration hooks.

Non-invasive by design: exposes payload adapters only.
"""

from __future__ import annotations

from arabic_engine.foundational.integration import LanguageFoundationalHook
from arabic_engine.foundational.models import FoundationalUnit


class LanguageFoundationalAdapter:
    """Adapter namespace for language future attachment."""

    @staticmethod
    def from_foundational(unit: FoundationalUnit) -> dict[str, object]:
        return LanguageFoundationalHook.payload(unit)

