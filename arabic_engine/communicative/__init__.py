"""
Communicative package — نواة التواصل والأسلوب.

Implements communicative and stylistic closure:
  - Khabar/Insha classification (خبر/إنشاء)
  - Stylistic closure
"""

from .khabar_insha import KhabarInshaClassifier  # noqa: F401
from .stylistic import StylisticGate  # noqa: F401
from .closure import CommunicativeClosureEngine  # noqa: F401
