"""
Singular package — نواة المفرد.

Implements the three singular closure layers:
  Layer 1: Perception (التصور المفرد)
  Layer 2: Information (المعلومة المفردة)
  Layer 3: Concept (المفهوم المفرد)
"""

from .perception import PerceptionGate  # noqa: F401
from .information import InformationGate  # noqa: F401
from .concept import ConceptGate  # noqa: F401
from .closure import SingularClosureEngine  # noqa: F401
