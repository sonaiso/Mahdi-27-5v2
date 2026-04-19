"""
Composition package — نواة التركيب والأدوار.

Implements Layer 5: Compositional Roles
  - Role distribution
  - Asnadi (predicative) relations
  - Tadmini (embedding) relations
  - Taqyidi (restrictive) relations
"""

from .roles import CompositionEligibilityGate  # noqa: F401
from .asnadi import AsnadiRelationBuilder  # noqa: F401
from .tadmini import TadminiRelationBuilder  # noqa: F401
from .taqyidi import TaqyidiRelationBuilder  # noqa: F401
from .closure import CompositionClosureEngine  # noqa: F401
