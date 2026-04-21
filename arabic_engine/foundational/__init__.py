"""
Foundational package — additive Layer 1/2 baseline for letter+diacritic identity.

This package is intentionally non-invasive and does not wire into MasterChain.
It provides:
  - Layer 1: SymbolicEncodingGate
  - Layer 2: OntologicalPropertyGate
  - Contracts/invariants for foundational v1
  - Integration-ready hooks for semantic_kernel and language
"""

from .models import (  # noqa: F401
    FoundationalGateResult,
    FoundationalLayer,
    FoundationalUnit,
    OntologicalPropertyProfile,
    SymbolKind,
    SymbolicToken,
)
from .symbolic_encoding import SymbolicEncodingGate  # noqa: F401
from .ontological_property import OntologicalPropertyGate  # noqa: F401
from .contracts import FoundationalInvariantContract  # noqa: F401
from .integration import (  # noqa: F401
    FoundationalIntegrationBridge,
    LanguageFoundationalHook,
    SemanticKernelFoundationalHook,
)
