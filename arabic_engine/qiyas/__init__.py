"""
Qiyas package — نواة القياس.

Implements Layer 8: Analogical reasoning (القياس).
  - QiyasModel: builds a qiyas from a closed judgement
  - QiyasTransitionEngine: validates the judgement-to-qiyas transition
  - QiyasClosureEngine: orchestrates closure
"""

from .model import QiyasModel  # noqa: F401
from .transition import QiyasTransitionEngine  # noqa: F401
from .closure import QiyasClosureEngine  # noqa: F401
