"""
Weight package — نواة الوزن والميزان.

Implements the weight/mizan fractal layer (Layer 4):
  - Weight classification (mizan)
  - Weight legality
  - Derivational eligibility
  - Weight closure engine
"""

from .mizan import MizanClassifier  # noqa: F401
from .legality import WeightLegalityGate  # noqa: F401
from .derivation import DerivationEligibilityGate  # noqa: F401
from .closure import WeightClosureEngine  # noqa: F401
