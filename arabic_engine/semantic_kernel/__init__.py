"""
Semantic Kernel package — نواة الدلالة المحوسبة.

Implements the semantic kernel layer that transforms roots from
morphological material into computable semantic cores, applies
pattern transforms, and produces form-level meaning kernels (𝒦_form).

Components:
  - root_kernel: RootKernelBuilder
  - pattern_transform: PatternTransformBuilder
  - form_profile: FormProfileBuilder
  - transfer: SemanticTransferEngine (core of the project)
  - compatibility: CompatibilityChecker
  - economy: EconomyOptimizer
  - closure: SemanticKernelClosureEngine
  - seed_data: Reference data for common roots and patterns
"""

from .root_kernel import RootKernelBuilder  # noqa: F401
from .pattern_transform import PatternTransformBuilder  # noqa: F401
from .form_profile import FormProfileBuilder  # noqa: F401
from .transfer import SemanticTransferEngine  # noqa: F401
from .compatibility import CompatibilityChecker  # noqa: F401
from .economy import EconomyOptimizer  # noqa: F401
from .closure import SemanticKernelClosureEngine  # noqa: F401
