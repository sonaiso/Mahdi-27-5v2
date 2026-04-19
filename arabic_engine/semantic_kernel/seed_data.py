"""
Seed data for common Arabic roots and patterns.

Provides reference semantic vectors for the most fundamental roots and
pattern transforms, enabling immediate testing and demonstration.

Each root vector has 13 dimensions (SemanticDimension):
    ENTITY, EVENT, QUALITY, RELATION, AGENCY, PATIENTHOOD,
    CAUSALITY, RESULTATIVITY, TEMPORALITY, SPATIALITY,
    EMBODIMENT, ABSTRACTION, TRANSFERABILITY

Each pattern transform vector has 12 dimensions (PatternSemanticDimension):
    EVENT_SHIFT, AGENCY_SHIFT, TRANSITIVITY_SHIFT, CAUSATIVE_SHIFT,
    REFLEXIVE_SHIFT, INTENSIFICATION, ITERATIVITY, STATIVE_SHIFT,
    NOMINALIZATION, INSTRUMENTALITY, LOCATIVITY, TEMPORALITY_SHIFT

Each form vector has 9 dimensions (FormSemanticDimension):
    CATEGORY, TENSE, ASPECT, VOICE, NUMBER, GENDER,
    DEFINITENESS, SYNTACTIC_LOAD, REFERENTIALITY
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Seed Root Vectors (13-dimensional)
# ---------------------------------------------------------------------------

#: ك ت ب — كتابة (writing): Event-high, Agency-high
SEED_ROOT_KTB = (
    0.2,   # ENTITY
    0.9,   # EVENT
    0.1,   # QUALITY
    0.3,   # RELATION
    0.8,   # AGENCY
    0.5,   # PATIENTHOOD
    0.3,   # CAUSALITY
    0.6,   # RESULTATIVITY
    0.4,   # TEMPORALITY
    0.1,   # SPATIALITY
    0.5,   # EMBODIMENT
    0.4,   # ABSTRACTION
    0.7,   # TRANSFERABILITY
)

#: ع ل م — علم (knowledge): Quality-high, Abstraction-high
SEED_ROOT_3LM = (
    0.3,   # ENTITY
    0.4,   # EVENT
    0.8,   # QUALITY
    0.5,   # RELATION
    0.6,   # AGENCY
    0.3,   # PATIENTHOOD
    0.2,   # CAUSALITY
    0.4,   # RESULTATIVITY
    0.2,   # TEMPORALITY
    0.1,   # SPATIALITY
    0.2,   # EMBODIMENT
    0.9,   # ABSTRACTION
    0.6,   # TRANSFERABILITY
)

#: ق ت ل — قتل (killing): Event-high, Causality-high
SEED_ROOT_QTL = (
    0.1,   # ENTITY
    0.9,   # EVENT
    0.1,   # QUALITY
    0.2,   # RELATION
    0.9,   # AGENCY
    0.8,   # PATIENTHOOD
    0.9,   # CAUSALITY
    0.8,   # RESULTATIVITY
    0.5,   # TEMPORALITY
    0.3,   # SPATIALITY
    0.8,   # EMBODIMENT
    0.1,   # ABSTRACTION
    0.3,   # TRANSFERABILITY
)

#: ح س ن — حسن (beauty/goodness): Quality-high, Embodiment-medium
SEED_ROOT_HSN = (
    0.4,   # ENTITY
    0.1,   # EVENT
    0.9,   # QUALITY
    0.3,   # RELATION
    0.1,   # AGENCY
    0.2,   # PATIENTHOOD
    0.0,   # CAUSALITY
    0.1,   # RESULTATIVITY
    0.1,   # TEMPORALITY
    0.1,   # SPATIALITY
    0.5,   # EMBODIMENT
    0.6,   # ABSTRACTION
    0.4,   # TRANSFERABILITY
)

#: خ ر ج — خروج (going out): Event-high, Spatiality-high
SEED_ROOT_XRJ = (
    0.2,   # ENTITY
    0.9,   # EVENT
    0.1,   # QUALITY
    0.3,   # RELATION
    0.7,   # AGENCY
    0.3,   # PATIENTHOOD
    0.2,   # CAUSALITY
    0.5,   # RESULTATIVITY
    0.5,   # TEMPORALITY
    0.9,   # SPATIALITY
    0.7,   # EMBODIMENT
    0.2,   # ABSTRACTION
    0.4,   # TRANSFERABILITY
)

#: ف ع ل — فعل (doing/action): Event-high, Agency-high, maximally generic
SEED_ROOT_F3L = (
    0.3,   # ENTITY
    0.9,   # EVENT
    0.2,   # QUALITY
    0.4,   # RELATION
    0.9,   # AGENCY
    0.5,   # PATIENTHOOD
    0.5,   # CAUSALITY
    0.5,   # RESULTATIVITY
    0.5,   # TEMPORALITY
    0.3,   # SPATIALITY
    0.4,   # EMBODIMENT
    0.4,   # ABSTRACTION
    0.8,   # TRANSFERABILITY
)

#: ج ل س — جلوس (sitting): Event-medium, Spatiality-high, Stative
SEED_ROOT_JLS = (
    0.3,   # ENTITY
    0.5,   # EVENT
    0.2,   # QUALITY
    0.2,   # RELATION
    0.5,   # AGENCY
    0.2,   # PATIENTHOOD
    0.1,   # CAUSALITY
    0.3,   # RESULTATIVITY
    0.4,   # TEMPORALITY
    0.7,   # SPATIALITY
    0.8,   # EMBODIMENT
    0.1,   # ABSTRACTION
    0.3,   # TRANSFERABILITY
)

#: ف ت ح — فتح (opening): Event-high, Causality-medium
SEED_ROOT_FTH = (
    0.2,   # ENTITY
    0.8,   # EVENT
    0.1,   # QUALITY
    0.3,   # RELATION
    0.7,   # AGENCY
    0.5,   # PATIENTHOOD
    0.6,   # CAUSALITY
    0.7,   # RESULTATIVITY
    0.3,   # TEMPORALITY
    0.4,   # SPATIALITY
    0.6,   # EMBODIMENT
    0.2,   # ABSTRACTION
    0.5,   # TRANSFERABILITY
)

#: ن ظ ر — نظر (looking/seeing): Event-high, Perception-oriented
SEED_ROOT_NZR = (
    0.2,   # ENTITY
    0.8,   # EVENT
    0.3,   # QUALITY
    0.4,   # RELATION
    0.7,   # AGENCY
    0.3,   # PATIENTHOOD
    0.1,   # CAUSALITY
    0.3,   # RESULTATIVITY
    0.3,   # TEMPORALITY
    0.2,   # SPATIALITY
    0.4,   # EMBODIMENT
    0.6,   # ABSTRACTION
    0.5,   # TRANSFERABILITY
)

#: ش ر ب — شرب (drinking): Event-high, Embodiment-high
SEED_ROOT_SHR_B = (
    0.1,   # ENTITY
    0.9,   # EVENT
    0.1,   # QUALITY
    0.2,   # RELATION
    0.8,   # AGENCY
    0.4,   # PATIENTHOOD
    0.2,   # CAUSALITY
    0.5,   # RESULTATIVITY
    0.3,   # TEMPORALITY
    0.1,   # SPATIALITY
    0.9,   # EMBODIMENT
    0.1,   # ABSTRACTION
    0.3,   # TRANSFERABILITY
)

#: ق ر أ — قراءة (reading): Event-high, Abstraction-high
SEED_ROOT_QR2 = (
    0.2,   # ENTITY
    0.8,   # EVENT
    0.2,   # QUALITY
    0.4,   # RELATION
    0.7,   # AGENCY
    0.4,   # PATIENTHOOD
    0.2,   # CAUSALITY
    0.5,   # RESULTATIVITY
    0.4,   # TEMPORALITY
    0.1,   # SPATIALITY
    0.3,   # EMBODIMENT
    0.7,   # ABSTRACTION
    0.7,   # TRANSFERABILITY
)

#: ذ ه ب — ذهاب (going): Event-high, Spatiality-high
SEED_ROOT_DHB = (
    0.1,   # ENTITY
    0.9,   # EVENT
    0.1,   # QUALITY
    0.2,   # RELATION
    0.8,   # AGENCY
    0.1,   # PATIENTHOOD
    0.1,   # CAUSALITY
    0.3,   # RESULTATIVITY
    0.5,   # TEMPORALITY
    0.9,   # SPATIALITY
    0.6,   # EMBODIMENT
    0.1,   # ABSTRACTION
    0.3,   # TRANSFERABILITY
)

#: ح ك م — حكم (judging/ruling): Event-high, Abstraction-high, Relation-high
SEED_ROOT_HKM = (
    0.3,   # ENTITY
    0.7,   # EVENT
    0.4,   # QUALITY
    0.8,   # RELATION
    0.8,   # AGENCY
    0.5,   # PATIENTHOOD
    0.4,   # CAUSALITY
    0.6,   # RESULTATIVITY
    0.3,   # TEMPORALITY
    0.1,   # SPATIALITY
    0.2,   # EMBODIMENT
    0.8,   # ABSTRACTION
    0.6,   # TRANSFERABILITY
)

#: ص ن ع — صنع (making/crafting): Event-high, Embodiment-high, Causality-high
SEED_ROOT_SN3 = (
    0.4,   # ENTITY
    0.8,   # EVENT
    0.2,   # QUALITY
    0.3,   # RELATION
    0.8,   # AGENCY
    0.4,   # PATIENTHOOD
    0.7,   # CAUSALITY
    0.8,   # RESULTATIVITY
    0.3,   # TEMPORALITY
    0.2,   # SPATIALITY
    0.8,   # EMBODIMENT
    0.2,   # ABSTRACTION
    0.4,   # TRANSFERABILITY
)

#: أ ك ل — أكل (eating): Event-high, Embodiment-high
SEED_ROOT_2KL = (
    0.1,   # ENTITY
    0.9,   # EVENT
    0.1,   # QUALITY
    0.2,   # RELATION
    0.8,   # AGENCY
    0.4,   # PATIENTHOOD
    0.2,   # CAUSALITY
    0.5,   # RESULTATIVITY
    0.3,   # TEMPORALITY
    0.1,   # SPATIALITY
    0.9,   # EMBODIMENT
    0.0,   # ABSTRACTION
    0.3,   # TRANSFERABILITY
)

#: و ج د — وجد (finding/existence): Quality-medium, Abstraction-high
SEED_ROOT_WJD = (
    0.5,   # ENTITY
    0.6,   # EVENT
    0.5,   # QUALITY
    0.4,   # RELATION
    0.5,   # AGENCY
    0.3,   # PATIENTHOOD
    0.2,   # CAUSALITY
    0.4,   # RESULTATIVITY
    0.3,   # TEMPORALITY
    0.2,   # SPATIALITY
    0.3,   # EMBODIMENT
    0.7,   # ABSTRACTION
    0.5,   # TRANSFERABILITY
)

#: ر ج ع — رجع (returning): Event-high, Spatiality-medium
SEED_ROOT_RJ3 = (
    0.1,   # ENTITY
    0.8,   # EVENT
    0.1,   # QUALITY
    0.3,   # RELATION
    0.7,   # AGENCY
    0.2,   # PATIENTHOOD
    0.1,   # CAUSALITY
    0.4,   # RESULTATIVITY
    0.5,   # TEMPORALITY
    0.7,   # SPATIALITY
    0.5,   # EMBODIMENT
    0.2,   # ABSTRACTION
    0.4,   # TRANSFERABILITY
)

#: ك ب ر — كبر (growing/being great): Quality-high, Embodiment-medium
SEED_ROOT_KBR = (
    0.4,   # ENTITY
    0.3,   # EVENT
    0.8,   # QUALITY
    0.3,   # RELATION
    0.2,   # AGENCY
    0.2,   # PATIENTHOOD
    0.1,   # CAUSALITY
    0.3,   # RESULTATIVITY
    0.4,   # TEMPORALITY
    0.2,   # SPATIALITY
    0.6,   # EMBODIMENT
    0.5,   # ABSTRACTION
    0.4,   # TRANSFERABILITY
)

#: ص ل ح — صلح (being good/righteous): Quality-high, Abstraction-high
SEED_ROOT_SLH = (
    0.3,   # ENTITY
    0.2,   # EVENT
    0.9,   # QUALITY
    0.4,   # RELATION
    0.2,   # AGENCY
    0.2,   # PATIENTHOOD
    0.1,   # CAUSALITY
    0.3,   # RESULTATIVITY
    0.2,   # TEMPORALITY
    0.1,   # SPATIALITY
    0.3,   # EMBODIMENT
    0.7,   # ABSTRACTION
    0.5,   # TRANSFERABILITY
)

#: س م ع — سمع (hearing): Event-high, Perception-oriented
SEED_ROOT_SM3 = (
    0.2,   # ENTITY
    0.8,   # EVENT
    0.3,   # QUALITY
    0.4,   # RELATION
    0.6,   # AGENCY
    0.4,   # PATIENTHOOD
    0.1,   # CAUSALITY
    0.3,   # RESULTATIVITY
    0.3,   # TEMPORALITY
    0.1,   # SPATIALITY
    0.5,   # EMBODIMENT
    0.5,   # ABSTRACTION
    0.5,   # TRANSFERABILITY
)

#: د خ ل — دخل (entering): Event-high, Spatiality-high
SEED_ROOT_DXL = (
    0.1,   # ENTITY
    0.9,   # EVENT
    0.1,   # QUALITY
    0.2,   # RELATION
    0.7,   # AGENCY
    0.2,   # PATIENTHOOD
    0.1,   # CAUSALITY
    0.4,   # RESULTATIVITY
    0.4,   # TEMPORALITY
    0.9,   # SPATIALITY
    0.6,   # EMBODIMENT
    0.1,   # ABSTRACTION
    0.3,   # TRANSFERABILITY
)

#: ز ل ز ل — زلزال (earthquake): Event-high, Spatiality-high, quadriliteral
SEED_ROOT_ZLZL = (
    0.3,   # ENTITY
    0.9,   # EVENT
    0.1,   # QUALITY
    0.1,   # RELATION
    0.3,   # AGENCY (natural phenomenon, low agency)
    0.6,   # PATIENTHOOD
    0.7,   # CAUSALITY
    0.8,   # RESULTATIVITY
    0.4,   # TEMPORALITY
    0.9,   # SPATIALITY
    0.9,   # EMBODIMENT
    0.1,   # ABSTRACTION
    0.2,   # TRANSFERABILITY
)


# ---------------------------------------------------------------------------
# Seed Pattern Transform Vectors (12-dimensional)
# ---------------------------------------------------------------------------

#: فَعَلَ — base trilateral (neutral transform)
SEED_PATTERN_FA3ALA = (
    0.0,   # EVENT_SHIFT
    0.0,   # AGENCY_SHIFT
    0.0,   # TRANSITIVITY_SHIFT
    0.0,   # CAUSATIVE_SHIFT
    0.0,   # REFLEXIVE_SHIFT
    0.0,   # INTENSIFICATION
    0.0,   # ITERATIVITY
    0.0,   # STATIVE_SHIFT
    0.0,   # NOMINALIZATION
    0.0,   # INSTRUMENTALITY
    0.0,   # LOCATIVITY
    0.0,   # TEMPORALITY_SHIFT
)

#: فَعَّلَ — intensive/causative (تَفْعِيل)
SEED_PATTERN_FA33ALA = (
    0.2,   # EVENT_SHIFT
    0.3,   # AGENCY_SHIFT
    0.4,   # TRANSITIVITY_SHIFT
    0.8,   # CAUSATIVE_SHIFT
    0.0,   # REFLEXIVE_SHIFT
    0.9,   # INTENSIFICATION
    0.3,   # ITERATIVITY
    0.0,   # STATIVE_SHIFT
    0.0,   # NOMINALIZATION
    0.0,   # INSTRUMENTALITY
    0.0,   # LOCATIVITY
    0.1,   # TEMPORALITY_SHIFT
)

#: أَفْعَلَ — causative/transitivizer (إِفْعَال)
SEED_PATTERN_AF3ALA = (
    0.1,   # EVENT_SHIFT
    0.2,   # AGENCY_SHIFT
    0.8,   # TRANSITIVITY_SHIFT
    0.7,   # CAUSATIVE_SHIFT
    0.0,   # REFLEXIVE_SHIFT
    0.3,   # INTENSIFICATION
    0.0,   # ITERATIVITY
    0.0,   # STATIVE_SHIFT
    0.0,   # NOMINALIZATION
    0.0,   # INSTRUMENTALITY
    0.0,   # LOCATIVITY
    0.1,   # TEMPORALITY_SHIFT
)

#: اِنْفَعَلَ — reflexive/affected (اِنْفِعَال)
SEED_PATTERN_INFA3ALA = (
    0.1,   # EVENT_SHIFT
    -0.3,  # AGENCY_SHIFT (reduced agency)
    -0.4,  # TRANSITIVITY_SHIFT (intransitivizer)
    0.0,   # CAUSATIVE_SHIFT
    0.8,   # REFLEXIVE_SHIFT
    0.0,   # INTENSIFICATION
    0.0,   # ITERATIVITY
    0.6,   # STATIVE_SHIFT
    0.0,   # NOMINALIZATION
    0.0,   # INSTRUMENTALITY
    0.0,   # LOCATIVITY
    0.0,   # TEMPORALITY_SHIFT
)

#: اِسْتَفْعَلَ — seeking/requesting (اِسْتِفْعَال)
SEED_PATTERN_ISTAF3ALA = (
    0.3,   # EVENT_SHIFT
    0.7,   # AGENCY_SHIFT (high seeking agency)
    0.2,   # TRANSITIVITY_SHIFT
    0.1,   # CAUSATIVE_SHIFT
    0.0,   # REFLEXIVE_SHIFT
    0.4,   # INTENSIFICATION
    0.0,   # ITERATIVITY
    0.0,   # STATIVE_SHIFT
    0.0,   # NOMINALIZATION
    0.0,   # INSTRUMENTALITY
    0.0,   # LOCATIVITY
    0.2,   # TEMPORALITY_SHIFT
)

#: تَفَاعَلَ — reciprocal/mutual (تَفَاعُل)
SEED_PATTERN_TAFA3ALA = (
    0.2,   # EVENT_SHIFT
    0.1,   # AGENCY_SHIFT
    0.0,   # TRANSITIVITY_SHIFT
    0.0,   # CAUSATIVE_SHIFT
    0.5,   # REFLEXIVE_SHIFT
    0.2,   # INTENSIFICATION
    0.7,   # ITERATIVITY
    0.0,   # STATIVE_SHIFT
    0.0,   # NOMINALIZATION
    0.0,   # INSTRUMENTALITY
    0.0,   # LOCATIVITY
    0.1,   # TEMPORALITY_SHIFT
)

#: فاعِل — active participle (اسم الفاعل)
SEED_PATTERN_FA3IL = (
    -0.3,  # EVENT_SHIFT (less event, more entity)
    0.6,   # AGENCY_SHIFT
    0.0,   # TRANSITIVITY_SHIFT
    0.0,   # CAUSATIVE_SHIFT
    0.0,   # REFLEXIVE_SHIFT
    0.0,   # INTENSIFICATION
    0.0,   # ITERATIVITY
    0.0,   # STATIVE_SHIFT
    0.9,   # NOMINALIZATION
    0.0,   # INSTRUMENTALITY
    0.0,   # LOCATIVITY
    0.0,   # TEMPORALITY_SHIFT
)

#: مَفْعُول — passive participle (اسم المفعول)
SEED_PATTERN_MAF3UL = (
    -0.3,  # EVENT_SHIFT (less event, more entity)
    -0.4,  # AGENCY_SHIFT (reduced agency)
    0.0,   # TRANSITIVITY_SHIFT
    0.0,   # CAUSATIVE_SHIFT
    0.0,   # REFLEXIVE_SHIFT
    0.0,   # INTENSIFICATION
    0.0,   # ITERATIVITY
    0.6,   # STATIVE_SHIFT
    0.9,   # NOMINALIZATION
    0.0,   # INSTRUMENTALITY
    0.0,   # LOCATIVITY
    0.0,   # TEMPORALITY_SHIFT
)

#: تَفَعَّلَ — gradual/self-reflexive (تَفَعُّل), Form V
SEED_PATTERN_TAFA33ALA = (
    0.2,   # EVENT_SHIFT
    0.0,   # AGENCY_SHIFT
    -0.2,  # TRANSITIVITY_SHIFT (intransitive tendency)
    0.0,   # CAUSATIVE_SHIFT
    0.6,   # REFLEXIVE_SHIFT
    0.5,   # INTENSIFICATION
    0.3,   # ITERATIVITY (gradual)
    0.2,   # STATIVE_SHIFT
    0.0,   # NOMINALIZATION
    0.0,   # INSTRUMENTALITY
    0.0,   # LOCATIVITY
    0.1,   # TEMPORALITY_SHIFT
)

#: اِفْتَعَلَ — middle/reflexive (اِفْتِعَال), Form VIII
SEED_PATTERN_IFTA3ALA = (
    0.1,   # EVENT_SHIFT
    0.2,   # AGENCY_SHIFT
    -0.1,  # TRANSITIVITY_SHIFT
    0.0,   # CAUSATIVE_SHIFT
    0.4,   # REFLEXIVE_SHIFT
    0.3,   # INTENSIFICATION
    0.0,   # ITERATIVITY
    0.2,   # STATIVE_SHIFT
    0.0,   # NOMINALIZATION
    0.0,   # INSTRUMENTALITY
    0.0,   # LOCATIVITY
    0.0,   # TEMPORALITY_SHIFT
)

#: مِفْعَال — instrument noun (اسم الآلة)
SEED_PATTERN_MIF3AL = (
    -0.5,  # EVENT_SHIFT (entity, not event)
    0.0,   # AGENCY_SHIFT
    0.0,   # TRANSITIVITY_SHIFT
    0.0,   # CAUSATIVE_SHIFT
    0.0,   # REFLEXIVE_SHIFT
    0.0,   # INTENSIFICATION
    0.0,   # ITERATIVITY
    0.0,   # STATIVE_SHIFT
    0.8,   # NOMINALIZATION
    0.9,   # INSTRUMENTALITY
    0.0,   # LOCATIVITY
    0.0,   # TEMPORALITY_SHIFT
)

#: مَفْعَل — place noun (اسم المكان)
SEED_PATTERN_MAF3AL = (
    -0.5,  # EVENT_SHIFT (entity, not event)
    0.0,   # AGENCY_SHIFT
    0.0,   # TRANSITIVITY_SHIFT
    0.0,   # CAUSATIVE_SHIFT
    0.0,   # REFLEXIVE_SHIFT
    0.0,   # INTENSIFICATION
    0.0,   # ITERATIVITY
    0.0,   # STATIVE_SHIFT
    0.8,   # NOMINALIZATION
    0.0,   # INSTRUMENTALITY
    0.9,   # LOCATIVITY
    0.0,   # TEMPORALITY_SHIFT
)


# ---------------------------------------------------------------------------
# Seed Form Vectors (9-dimensional)
# ---------------------------------------------------------------------------

#: Active verb, past tense, masculine singular
SEED_FORM_VERB_PAST_MS = (
    1.0,   # CATEGORY (verb)
    1.0,   # TENSE (past)
    0.5,   # ASPECT (perfective)
    1.0,   # VOICE (active)
    0.3,   # NUMBER (singular)
    1.0,   # GENDER (masculine)
    0.0,   # DEFINITENESS (N/A for verbs)
    0.7,   # SYNTACTIC_LOAD
    0.5,   # REFERENTIALITY
)

#: Active participle noun, indefinite masculine singular
SEED_FORM_NOUN_INDEF_MS = (
    0.0,   # CATEGORY (noun)
    0.0,   # TENSE (N/A)
    0.0,   # ASPECT (N/A)
    0.5,   # VOICE (neutral)
    0.3,   # NUMBER (singular)
    1.0,   # GENDER (masculine)
    0.0,   # DEFINITENESS (indefinite)
    0.5,   # SYNTACTIC_LOAD
    0.7,   # REFERENTIALITY
)

#: Definite noun, masculine singular
SEED_FORM_NOUN_DEF_MS = (
    0.0,   # CATEGORY (noun)
    0.0,   # TENSE (N/A)
    0.0,   # ASPECT (N/A)
    0.5,   # VOICE (neutral)
    0.3,   # NUMBER (singular)
    1.0,   # GENDER (masculine)
    1.0,   # DEFINITENESS (definite)
    0.6,   # SYNTACTIC_LOAD
    0.9,   # REFERENTIALITY
)

#: Active verb, present tense, masculine singular
SEED_FORM_VERB_PRESENT_MS = (
    1.0,   # CATEGORY (verb)
    0.5,   # TENSE (present)
    0.7,   # ASPECT (imperfective)
    1.0,   # VOICE (active)
    0.3,   # NUMBER (singular)
    1.0,   # GENDER (masculine)
    0.0,   # DEFINITENESS (N/A)
    0.7,   # SYNTACTIC_LOAD
    0.5,   # REFERENTIALITY
)

#: Passive verb, past tense, masculine singular
SEED_FORM_VERB_PASSIVE_PAST_MS = (
    1.0,   # CATEGORY (verb)
    1.0,   # TENSE (past)
    0.5,   # ASPECT (perfective)
    0.0,   # VOICE (passive)
    0.3,   # NUMBER (singular)
    1.0,   # GENDER (masculine)
    0.0,   # DEFINITENESS (N/A)
    0.6,   # SYNTACTIC_LOAD
    0.4,   # REFERENTIALITY
)

#: Indefinite noun, feminine singular
SEED_FORM_NOUN_INDEF_FS = (
    0.0,   # CATEGORY (noun)
    0.0,   # TENSE (N/A)
    0.0,   # ASPECT (N/A)
    0.5,   # VOICE (neutral)
    0.3,   # NUMBER (singular)
    0.0,   # GENDER (feminine)
    0.0,   # DEFINITENESS (indefinite)
    0.5,   # SYNTACTIC_LOAD
    0.7,   # REFERENTIALITY
)

#: Definite noun, masculine dual
SEED_FORM_NOUN_DEF_MD = (
    0.0,   # CATEGORY (noun)
    0.0,   # TENSE (N/A)
    0.0,   # ASPECT (N/A)
    0.5,   # VOICE (neutral)
    0.5,   # NUMBER (dual)
    1.0,   # GENDER (masculine)
    1.0,   # DEFINITENESS (definite)
    0.6,   # SYNTACTIC_LOAD
    0.9,   # REFERENTIALITY
)

#: Definite noun, masculine plural
SEED_FORM_NOUN_DEF_MP = (
    0.0,   # CATEGORY (noun)
    0.0,   # TENSE (N/A)
    0.0,   # ASPECT (N/A)
    0.5,   # VOICE (neutral)
    1.0,   # NUMBER (plural)
    1.0,   # GENDER (masculine)
    1.0,   # DEFINITENESS (definite)
    0.7,   # SYNTACTIC_LOAD
    0.9,   # REFERENTIALITY
)

#: Imperative verb, masculine singular
SEED_FORM_VERB_IMPERATIVE_MS = (
    1.0,   # CATEGORY (verb)
    0.0,   # TENSE (N/A — imperative)
    0.8,   # ASPECT (perfective in command)
    1.0,   # VOICE (active)
    0.3,   # NUMBER (singular)
    1.0,   # GENDER (masculine)
    0.0,   # DEFINITENESS (N/A)
    0.8,   # SYNTACTIC_LOAD (high — directive)
    0.3,   # REFERENTIALITY (low — non-referential)
)
