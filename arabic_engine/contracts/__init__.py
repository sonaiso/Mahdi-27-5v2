"""
Contracts package — نواة العقود.

Implements enforceable contracts:
  - Adjacency checks
  - Invariant validation
  - Anti-jump enforcement
  - State mapping
"""

from .adjacency import AdjacencyContract  # noqa: F401
from .invariants import InvariantChecker  # noqa: F401
from .anti_jump import AntiJumpContract  # noqa: F401
from .state_mapping import StateMapper  # noqa: F401
