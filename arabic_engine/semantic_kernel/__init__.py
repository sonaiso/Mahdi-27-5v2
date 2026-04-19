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
  - closure: SemanticKernelClosureEngine, ClosureTrace
  - alignment: Semantic dimension alignment mappings
  - context: ContextDeltaBuilder, ContextFeatures
  - weight_scheduler: WeightScheduler, BlendingWeights
  - phonotactics: PhonotacticChecker, RootType
  - metrics: TransferMetrics
  - seed_data: Reference data for common roots and patterns
"""

from .root_kernel import RootKernelBuilder  # noqa: F401
from .pattern_transform import PatternTransformBuilder  # noqa: F401
from .form_profile import FormProfileBuilder  # noqa: F401
from .transfer import SemanticTransferEngine  # noqa: F401
from .compatibility import CompatibilityChecker  # noqa: F401
from .economy import EconomyOptimizer  # noqa: F401
from .closure import SemanticKernelClosureEngine, ClosureTrace  # noqa: F401
from .alignment import (  # noqa: F401
    project_root_to_pattern_space,
    project_root_to_form_space,
    project_pattern_to_form_space,
    project_to_common_space,
)
from .context import ContextDeltaBuilder, ContextFeatures  # noqa: F401
from .weight_scheduler import WeightScheduler, BlendingWeights  # noqa: F401
from .phonotactics import PhonotacticChecker, RootType  # noqa: F401
from .metrics import TransferMetrics  # noqa: F401
