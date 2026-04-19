"""
Core module — enumerations, types, and gate logic for the Arabic Cognitive Fractal Engine.

This __init__ re-exports every public name from the split sub-modules so that
existing ``from arabic_engine.core import X`` imports continue to work.
"""

# --- Enums (split files) ---------------------------------------------------
from .enums_gate import ClosureStatus, GateVerdict  # noqa: F401
from .enums_trace import TraceEventKind, TraceSeverity  # noqa: F401
from .enums_singular import (  # noqa: F401
    StabilityKind,
    WordCategory,
    DerivationKind,
    Definiteness,
    Gender,
)
from .enums_weight import (  # noqa: F401
    InflectionKind,
    WeightEligibility,
    TemporalPotential,
    SpatialPotential,
    DescriptivePotential,
)
from .enums_judgement import JudgementDirection, JudgementRank  # noqa: F401
from .enums_domain import (  # noqa: F401
    Layer,
    RelationKind,
    RoleTag,
    CommunicativeMode,
)

# --- Types (split files) ---------------------------------------------------
from .types_gate import GateResult  # noqa: F401
from .types_trace import TraceEvent, TraceLog  # noqa: F401
from .types_singular import (  # noqa: F401
    PreU0,
    SingularPerceptual,
    SingularInformational,
    SingularConceptual,
    SingularUnit,
)
from .types_weight import WeightRecord, WeightedUnit  # noqa: F401
from .types_composition import RoleAssignment, CompositionRelation  # noqa: F401
from .types_judgement import Proposition, Judgement, Qiyas  # noqa: F401
