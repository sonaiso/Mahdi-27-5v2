"""
Language-layer enumerations for the Arabic Cognitive Fractal Engine.

Defines the twelve cognitive categories (𝒦) that the transcendental
container must hold, the five container functions, and validity status.

Reference:
    𝒦 = {Entity, Quality, Event, Relation, Cause, Condition,
          Negation, Quantity, Limitation, Reference, Temporality, Spatiality}

    Lang_tr = ⟨Lexicon, CategorySystem, PredicationRules,
              ConstraintSystem, ReferenceSystem, TestabilityInterface⟩
"""

from enum import Enum, auto


class CognitiveCategory(Enum):
    """The twelve cognitive categories (المقولات العقلية) that language
    must contain after they form in the mind.

    These are not created by language but *carried* by it in an ordered
    manner (لا تُخلق في اللغة بل تُحمل فيها حملًا منظمًا).
    """

    ENTITY = auto()        # الذات — denotes a substance / entity
    QUALITY = auto()       # الصفة — denotes a quality / attribute
    EVENT = auto()         # الحدث — denotes an event / action
    RELATION = auto()      # العلاقة — denotes a relation
    CAUSE = auto()         # السببية — denotes causation
    CONDITION = auto()     # الشرطية — denotes a condition
    NEGATION = auto()      # النفي — denotes negation
    QUANTITY = auto()       # العدد/الكم — denotes quantity / number
    LIMITATION = auto()    # التقييد — denotes restriction / limitation
    REFERENCE = auto()     # الإحالة — denotes reference / deixis
    TEMPORALITY = auto()   # الزمان — denotes temporality
    SPATIALITY = auto()    # المكان — denotes spatiality


class ContainerFunction(Enum):
    """The five functions of the transcendental container (وظائف الوعاء الترنسندنتالي).

    Each function describes *what* the container does to the categories it holds.
    """

    COLLECTION = auto()     # الجمع — collects categories into one system
    PREVENTION = auto()     # المنع — prevents rank confusion
    CARRYING = auto()       # الحمل — carries meaning from mind to expression
    DESIGNATION = auto()    # التعيين — assigns each category its proper position
    TESTABILITY = auto()    # الاختبار — makes judgement testable for truth/falsity


class LinguisticPosition(Enum):
    """The canonical linguistic positions where categories are housed.

    Maps each cognitive category to its proper Arabic grammatical home.
    """

    ISM = auto()                # الاسم — noun (for Entity)
    NA3T_SIFA_HAL = auto()      # النعت/الصفة/الحال — attribute positions (for Quality)
    FI3L_MASDAR = auto()        # الفعل/المصدر — verb or verbal noun (for Event)
    HARF_ADAWAT_NISAB = auto()  # الحروف/الأدوات/النسب — particles/tools (for Relation)
    ADAWAT_SABAB = auto()       # أدوات السبب — causal particles (for Cause)
    ADAWAT_SHART = auto()       # أدوات الشرط — conditional particles (for Condition)
    ADAWAT_NAFY = auto()        # أدوات النفي — negation particles (for Negation)
    ADAWAT_ADAD = auto()        # أدوات العدد — number words (for Quantity)
    ADAWAT_TAQYID = auto()      # أدوات التقييد — restrictive particles (for Limitation)
    DAMIR_ISHARA_MAWSUL = auto()  # الضمائر/الإشارة/الموصولات — reference (for Reference)
    ADAWAT_ZAMAN = auto()       # أدوات الزمان — temporal expressions (for Temporality)
    ADAWAT_MAKAN = auto()       # أدوات المكان — spatial expressions (for Spatiality)


class RankConfusionKind(Enum):
    """Types of rank confusion the constraint system must prevent.

    Each kind represents a specific confusion the transcendental
    container's prevention function (المنع) guards against.
    """

    ENTITY_AS_QUALITY = auto()          # معاملة الذات كصفة
    QUALITY_AS_ENTITY = auto()          # معاملة الصفة كذات مستقلة
    EVENT_AS_STATIC = auto()            # معاملة الحدث كثابت
    CAUSE_AS_CONDITION = auto()         # معاملة السبب كشرط
    GENERAL_AS_ABSOLUTE = auto()        # معاملة العام كالمطلق
    SINGULAR_CONCEPT_AS_JUDGEMENT = auto()  # معاملة المفهوم المفرد كحكم كامل
    PREDICATE_AS_SUBJECT = auto()       # خلط المسند بالمسند إليه
    KHABAR_AS_INSHA = auto()            # خلط الخبر بالإنشاء


class ContainerValidityStatus(Enum):
    """Validity status of a category placement within the container.

    Valid(x) ⟺ Category(x) ∧ ProperRole(x) ∧ NoRankConfusion(x)
    """

    VALID = auto()         # صالح — category is properly placed
    INVALID = auto()       # غير صالح — rank confusion detected
    PARTIAL = auto()       # جزئي — some conditions met, others pending
