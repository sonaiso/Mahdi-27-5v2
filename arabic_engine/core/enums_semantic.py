"""
Semantic enumerations for the Arabic Cognitive Fractal Engine.

Defines dimensional categories for the semantic kernel layer:
root semantic dimensions, pattern transform dimensions, form dimensions,
and compatibility status.
"""

from enum import Enum, auto


class SemanticDimension(Enum):
    """The thirteen semantic dimensions of a root (الأبعاد الدلالية للجذر).

    Each dimension captures one facet of the root's semantic potential.
    """

    ENTITY = auto()           # كيان — denotes an entity
    EVENT = auto()            # حدث — denotes an event
    QUALITY = auto()          # صفة — denotes a quality
    RELATION = auto()         # علاقة — denotes a relation
    AGENCY = auto()           # فاعلية — agency potential
    PATIENTHOOD = auto()      # مفعولية — patient potential
    CAUSALITY = auto()        # سببية — causal potential
    RESULTATIVITY = auto()    # نتيجية — resultative potential
    TEMPORALITY = auto()      # زمنية — temporal potential
    SPATIALITY = auto()       # مكانية — spatial potential
    EMBODIMENT = auto()       # تجسيد — embodiment / concreteness
    ABSTRACTION = auto()      # تجريد — abstraction
    TRANSFERABILITY = auto()  # قابلية النقل — transferability


class PatternSemanticDimension(Enum):
    """The twelve semantic transform dimensions of a pattern/weight (أبعاد التحويل الدلالي للوزن).

    Each dimension captures a shift the pattern imposes on root meaning.
    """

    EVENT_SHIFT = auto()          # تحويل حدثي
    AGENCY_SHIFT = auto()         # تحويل فاعلي
    TRANSITIVITY_SHIFT = auto()   # تحويل تعدية
    CAUSATIVE_SHIFT = auto()      # تحويل سببي
    REFLEXIVE_SHIFT = auto()      # تحويل انعكاسي
    INTENSIFICATION = auto()      # تكثيف
    ITERATIVITY = auto()          # تكرار
    STATIVE_SHIFT = auto()        # تحويل ثباتي
    NOMINALIZATION = auto()       # تسمية
    INSTRUMENTALITY = auto()      # آلية
    LOCATIVITY = auto()           # مكانية
    TEMPORALITY_SHIFT = auto()    # تحويل زمني


class FormSemanticDimension(Enum):
    """The nine semantic dimensions of a grammatical form (أبعاد الصيغة).

    Each dimension captures a grammatical feature of the realized form.
    """

    CATEGORY = auto()         # تصنيف — noun/verb/particle
    TENSE = auto()            # زمن
    ASPECT = auto()           # جهة
    VOICE = auto()            # بناء — active/passive
    NUMBER = auto()           # عدد — singular/dual/plural
    GENDER = auto()           # جنس — masculine/feminine
    DEFINITENESS = auto()     # تعريف/تنكير
    SYNTACTIC_LOAD = auto()   # الحمل النحوي
    REFERENTIALITY = auto()   # إحالية


class CompatibilityStatus(Enum):
    """Compatibility between root and pattern (حالة التوافق)."""

    COMPATIBLE = auto()     # متوافق — root and pattern are fully compatible
    INCOMPATIBLE = auto()   # غير متوافق — root and pattern are incompatible
    PARTIAL = auto()        # جزئي — partially compatible
