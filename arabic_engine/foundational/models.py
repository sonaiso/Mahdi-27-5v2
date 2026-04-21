"""
Foundational types for additive Layer 1/2 (symbolic + ontological baseline).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict


class FoundationalLayer(Enum):
    """Additive foundational layers for v1."""

    SYMBOLIC_ENCODING = auto()
    ONTOLOGICAL_PROPERTY = auto()


class SymbolKind(Enum):
    """Supported foundational symbol kinds in v1 scope."""

    LETTER = auto()
    DIACRITIC = auto()


@dataclass(frozen=True)
class FoundationalGateResult:
    """Gate verdict for foundational layers."""

    verdict: GateVerdict
    layer: FoundationalLayer
    reason: str = ""
    missing_condition: str = ""
    trace_id: str = ""

    @property
    def passed(self) -> bool:
        return self.verdict is GateVerdict.PASS


@dataclass
class SymbolicToken:
    """Layer 1 symbolic token model for letter/diacritic identity."""

    symbol: str = ""
    codepoint: int = 0
    kind: SymbolKind = SymbolKind.LETTER
    normalization_form: str = "NFC"
    visual_glyph: str = ""

    normalized_symbol: str = ""
    canonical_form: str = ""
    compatibility_form: str = ""
    representational_stability: bool = False
    closure: ClosureStatus = ClosureStatus.OPEN


@dataclass
class OntologicalPropertyProfile:
    """Layer 2 ontological profile split into essential/contextual domains."""

    letter_essential: dict[str, bool] = field(default_factory=dict)
    diacritic_essential: dict[str, bool] = field(default_factory=dict)
    contextual: dict[str, str] = field(default_factory=dict)
    closure: ClosureStatus = ClosureStatus.OPEN


@dataclass
class FoundationalUnit:
    """Foundational aggregate for v1 scope (letter + optional diacritic)."""

    letter: SymbolicToken | None = None
    diacritic: SymbolicToken | None = None
    ontology: OntologicalPropertyProfile = field(default_factory=OntologicalPropertyProfile)

