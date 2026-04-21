"""
Reference-predication matrix models for Σ1 -> Σ2 transition.

Implements a computable formalization of:
- Criterion (3): prerequisite validity for singular reference units (Σ1)
- Sentence-level matrix construction (Σ2) across khabar/condition/naskh/insha
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Union
from warnings import warn


class SentenceSpace(Enum):
    """Sentence-space families in Σ2."""

    KHABAR = "khabar"
    COND = "conditional"
    NASKH = "naskh"
    INSHA = "insha"


class MentalFactor(Enum):
    """High-level cognitive factor controlling sentence construction."""

    PRED = "A_pred"
    COND = "A_cond"
    NAS = "A_nas"
    MOD = "A_mod"
    REF = "A_ref"
    TEMP = "A_temp"


class PredicationType(Enum):
    """χ type for sentence-level reference predication."""

    PRED = "chi_pred"
    COND = "chi_cond"
    NASKH = "chi_naskh"
    INSHA = "chi_insha"
    REF = "chi_ref"
    CAUSE = "chi_cause"
    TEMP = "chi_temp"


class PropositionMode(Enum):
    """ζ type for proposition mode."""

    KHABAR = "zeta_k"
    INSHA = "zeta_i"


class OntologyClass(Enum):
    """Ontology identity class for expanded Σ1."""

    ENTITY = "entity"
    EVENT = "event"
    QUALITY = "quality"
    RELATION = "relation"
    UNKNOWN = "unknown"


class EgoReferenceMode(Enum):
    """Reference anchoring with respect to ego/source perspective."""

    SELF = "self"
    OTHER = "other"
    GENERIC = "generic"
    UNKNOWN = "unknown"


class GeneralityLevel(Enum):
    """Generality profile for reference determination."""

    PARTICULAR = "particular"
    GENERIC = "generic"
    UNIVERSAL = "universal"
    UNKNOWN = "unknown"


class GrammaticalRole(Enum):
    """Structured grammatical role for positional compatibility checks."""

    SUBJECT = "subject"
    PREDICATE = "predicate"
    QUALIFIER = "qualifier"
    RELATOR = "relator"
    TRANSFORMER = "transformer"


@dataclass(frozen=True)
class LegacySigma1ReferenceUnit:
    """Legacy reduced Σ1 state used for explicit compatibility adapters."""

    label: str
    j_p: float
    j_m: float
    j_sigma: float
    transition_capacity_nu: float
    reference_variance: float
    type_potential: TypePotential
    positional_potential: PositionalPotential
    purity_score: float


@dataclass(frozen=True)
class TypePotential:
    """Type-potential vector: noun/verb/particle."""

    noun: float
    verb: float
    particle: float

    @property
    def max_value(self) -> float:
        return max(self.noun, self.verb, self.particle)


@dataclass(frozen=True)
class PositionalPotential:
    """Positional eligibility vector L = <ls, lp, lq, lr, lj>."""

    subject: float
    predicate: float
    qualifier: float
    relator: float
    transformer: float

    @property
    def max_value(self) -> float:
        return max(
            self.subject,
            self.predicate,
            self.qualifier,
            self.relator,
            self.transformer,
        )


@dataclass(frozen=True)
class Sigma1ReferenceUnit:
    """Reduced Σ1 state required to enter sentence construction."""

    label: str
    j_p: float
    j_m: float
    j_sigma: float
    transition_capacity_nu: float
    reference_variance: float
    type_potential: TypePotential
    positional_potential: PositionalPotential
    purity_score: float
    ontology: OntologyClass = OntologyClass.UNKNOWN
    causality: float = 0.5
    ego_reference: EgoReferenceMode = EgoReferenceMode.UNKNOWN
    generality: GeneralityLevel = GeneralityLevel.UNKNOWN
    gender: str = "unspecified"
    temporality: str = "atemporal"
    spatiality: str = "unspecified"
    signifier: str = ""
    association: float = 0.0


@dataclass(frozen=True)
class Sigma1Thresholds:
    """Threshold bundle for Criterion (3) and Σ1 admission."""

    theta_sigma1: float = 0.70
    theta_p: float = 0.70
    theta_m: float = 0.70
    theta_t: float = 0.55
    theta_l: float = 0.55
    theta_purity: float = 0.70
    theta_nu: float = 0.65
    epsilon_rho: float = 0.20


@dataclass(frozen=True)
class Sigma1PrerequisiteReport:
    """Detailed prerequisite status for Σ1 -> Σ2 transition."""

    unit_label: str
    passes_j_sigma1: bool
    passes_j_p: bool
    passes_j_m: bool
    passes_type_resolution: bool
    passes_positional_resolution: bool
    passes_purity: bool
    passes_transition_capacity: bool
    passes_reference_stability: bool

    @property
    def is_admissible(self) -> bool:
        return all(
            (
                self.passes_j_sigma1,
                self.passes_j_p,
                self.passes_j_m,
                self.passes_type_resolution,
                self.passes_positional_resolution,
                self.passes_purity,
                self.passes_transition_capacity,
                self.passes_reference_stability,
            )
        )


@dataclass(frozen=True)
class RatioVector:
    """N = <Na, Nt, Nq> (predicative/embedding/restrictive)."""

    asnadi: float
    tadmini: float
    taqyidi: float
    independent: bool = False

    def is_valid(self, tolerance: float = 1e-9) -> bool:
        if self.independent:
            return True
        total = self.asnadi + self.tadmini + self.taqyidi
        return abs(total - 1.0) <= tolerance


@dataclass(frozen=True)
class PropositionConstraintVector:
    """Cp = <ch, ct, cq, cn, cm, cw, cr>."""

    khabari: float
    conditional: float
    insha_talabi_or_istifhami: float
    naskh: float
    emphatic_or_istidraki: float
    proximative_or_inceptive_or_hopeful: float
    connective_or_referential: float


@dataclass(frozen=True)
class ReferencePredicationVector2:
    """Sentence-level reference-predication vector S_r^(2)."""

    mu_1: str
    mu_2: str
    chi: PredicationType
    omega: str
    gamma: str
    eta: float
    theta: float
    zeta: PropositionMode
    varsigma: float


@dataclass(frozen=True)
class CaseImpactVector2:
    """Sentence-level case/structural effect vector I^(2)."""

    subject_mark: str
    predicate_mark: str
    causal_alignment: float
    referential_alignment: float
    grammatical_factor_code: str
    causal_trace: str
    referential_trace: str
    derivational_basis: str = "effect_not_input"


@dataclass(frozen=True)
class GrammaticalFactorGI:
    """Structured grammatical factor G_i used internally by Σ2."""

    code: str
    ontology_anchor: OntologyClass
    causality_score: float
    ego_mode: EgoReferenceMode
    generality: GeneralityLevel
    role: GrammaticalRole
    positional_validity: float

    @property
    def is_positionally_valid(self) -> bool:
        return self.positional_validity >= 0.55


@dataclass(frozen=True)
class Sigma2Matrix:
    """Σ2 matrix for sentence-level reference predication."""

    sigma1_first: Sigma1ReferenceUnit
    sigma1_second: Sigma1ReferenceUnit
    mental_factor: MentalFactor
    reference_predication: ReferencePredicationVector2
    ratios: RatioVector
    grammatical_factor: GrammaticalFactorGI
    case_impact: CaseImpactVector2
    proposition_constraint: PropositionConstraintVector
    sentence_space: SentenceSpace


class SigmaTransitionError(ValueError):
    """Raised when Σ1 units cannot transition into Σ2."""


class SigmaPrerequisiteChecker:
    """Evaluates Criterion (3) prerequisites for Σ1 units."""

    @staticmethod
    def evaluate(
        unit: Sigma1ReferenceUnit,
        thresholds: Sigma1Thresholds,
    ) -> Sigma1PrerequisiteReport:
        return Sigma1PrerequisiteReport(
            unit_label=unit.label,
            passes_j_sigma1=unit.j_sigma >= thresholds.theta_sigma1,
            passes_j_p=unit.j_p >= thresholds.theta_p,
            passes_j_m=unit.j_m >= thresholds.theta_m,
            passes_type_resolution=(
                unit.type_potential.max_value >= thresholds.theta_t
            ),
            passes_positional_resolution=(
                unit.positional_potential.max_value >= thresholds.theta_l
            ),
            passes_purity=unit.purity_score >= thresholds.theta_purity,
            passes_transition_capacity=(
                unit.transition_capacity_nu >= thresholds.theta_nu
            ),
            passes_reference_stability=(
                unit.reference_variance <= thresholds.epsilon_rho
            ),
        )


class SigmaCompatibilityAdapter:
    """Centralized compatibility adapters for Σ1 and G_i migration."""

    @staticmethod
    def legacy_sigma1_to_expanded(
        legacy: LegacySigma1ReferenceUnit,
    ) -> Sigma1ReferenceUnit:
        return Sigma1ReferenceUnit(
            label=legacy.label,
            j_p=legacy.j_p,
            j_m=legacy.j_m,
            j_sigma=legacy.j_sigma,
            transition_capacity_nu=legacy.transition_capacity_nu,
            reference_variance=legacy.reference_variance,
            type_potential=legacy.type_potential,
            positional_potential=legacy.positional_potential,
            purity_score=legacy.purity_score,
        )

    @staticmethod
    def _infer_role(code: str) -> GrammaticalRole:
        token = code.lower()
        if "pred" in token:
            return GrammaticalRole.PREDICATE
        if "cond" in token:
            return GrammaticalRole.PREDICATE
        if "nas" in token:
            return GrammaticalRole.TRANSFORMER
        if "qual" in token:
            return GrammaticalRole.QUALIFIER
        return GrammaticalRole.SUBJECT

    @staticmethod
    def _role_score(unit: Sigma1ReferenceUnit, role: GrammaticalRole) -> float:
        if role is GrammaticalRole.SUBJECT:
            return unit.positional_potential.subject
        if role is GrammaticalRole.PREDICATE:
            return unit.positional_potential.predicate
        if role is GrammaticalRole.QUALIFIER:
            return unit.positional_potential.qualifier
        if role is GrammaticalRole.RELATOR:
            return unit.positional_potential.relator
        return unit.positional_potential.transformer

    @staticmethod
    def legacy_grammatical_factor_to_gi(
        legacy_grammatical_factor: str,
        first: Sigma1ReferenceUnit,
        second: Sigma1ReferenceUnit,
    ) -> GrammaticalFactorGI:
        role = SigmaCompatibilityAdapter._infer_role(legacy_grammatical_factor)
        positional_validity = max(
            SigmaCompatibilityAdapter._role_score(first, role),
            SigmaCompatibilityAdapter._role_score(second, role),
        )
        return GrammaticalFactorGI(
            code=legacy_grammatical_factor,
            ontology_anchor=first.ontology,
            causality_score=Sigma2Builder._clamp((first.causality + second.causality) / 2.0),
            ego_mode=first.ego_reference,
            generality=first.generality,
            role=role,
            positional_validity=positional_validity,
        )

    @staticmethod
    def normalize_grammatical_factor(
        grammatical_factor: Union[str, GrammaticalFactorGI],
        first: Sigma1ReferenceUnit,
        second: Sigma1ReferenceUnit,
    ) -> GrammaticalFactorGI:
        if isinstance(grammatical_factor, GrammaticalFactorGI):
            return grammatical_factor
        warn(
            "Passing string grammatical_factor is deprecated; pass GrammaticalFactorGI instead.",
            DeprecationWarning,
            stacklevel=3,
        )
        return SigmaCompatibilityAdapter.legacy_grammatical_factor_to_gi(
            grammatical_factor,
            first,
            second,
        )


class Sigma2Builder:
    """Builds Σ2 from two admissible Σ1 units plus governing factors."""

    _SPACE_DEFAULTS: dict[SentenceSpace, tuple[PredicationType, PropositionMode]] = {
        SentenceSpace.KHABAR: (PredicationType.PRED, PropositionMode.KHABAR),
        SentenceSpace.COND: (PredicationType.COND, PropositionMode.INSHA),
        SentenceSpace.NASKH: (PredicationType.NASKH, PropositionMode.KHABAR),
        SentenceSpace.INSHA: (PredicationType.INSHA, PropositionMode.INSHA),
    }

    @staticmethod
    def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
        return max(low, min(high, value))

    @staticmethod
    def _case_marks_are_causally_consistent(
        *,
        causal_alignment: float,
        sentence_space: SentenceSpace,
        subject_mark: str,
        predicate_mark: str,
    ) -> bool:
        # Low causal alignment cannot carry strong khabari raf/raf fixation.
        if (
            sentence_space is SentenceSpace.KHABAR
            and subject_mark == "raf"
            and predicate_mark == "raf"
            and causal_alignment < 0.50
        ):
            return False
        return True

    @staticmethod
    def build(
        first: Sigma1ReferenceUnit,
        second: Sigma1ReferenceUnit,
        *,
        sentence_space: SentenceSpace,
        mental_factor: MentalFactor,
        grammatical_factor: Union[str, GrammaticalFactorGI],
        ratios: RatioVector,
        proposition_constraint: PropositionConstraintVector,
        thresholds: Sigma1Thresholds | None = None,
        omega: str = "omega_d",
        gamma: str = "present",
        varsigma: float = 1.0,
        subject_mark: str = "raf",
        predicate_mark: str = "raf",
    ) -> Sigma2Matrix:
        thresholds = thresholds or Sigma1Thresholds()

        first_report = SigmaPrerequisiteChecker.evaluate(first, thresholds)
        second_report = SigmaPrerequisiteChecker.evaluate(second, thresholds)
        if not first_report.passes_j_m or not second_report.passes_j_m:
            raise SigmaTransitionError("Cannot build Σ2 when J_m prerequisite fails")

        if not first_report.is_admissible:
            raise SigmaTransitionError(
                f"Σ1 unit '{first.label}' is not admissible for Σ2 transition"
            )
        if not second_report.is_admissible:
            raise SigmaTransitionError(
                f"Σ1 unit '{second.label}' is not admissible for Σ2 transition"
            )
        if not ratios.is_valid():
            raise SigmaTransitionError("Ratio vector N is invalid")

        chi, zeta = Sigma2Builder._SPACE_DEFAULTS[sentence_space]
        g_i = SigmaCompatibilityAdapter.normalize_grammatical_factor(
            grammatical_factor=grammatical_factor,
            first=first,
            second=second,
        )
        if not g_i.is_positionally_valid:
            raise SigmaTransitionError(
                f"G_i '{g_i.code}' is inconsistent with positional eligibility"
            )

        s2 = ReferencePredicationVector2(
            mu_1=first.label,
            mu_2=second.label,
            chi=chi,
            omega=omega,
            gamma=gamma,
            eta=ratios.tadmini,
            theta=ratios.taqyidi,
            zeta=zeta,
            varsigma=varsigma,
        )

        causal_alignment = Sigma2Builder._clamp(
            (first.j_m + second.j_m + first.causality + second.causality) / 4.0
        )
        referential_alignment = Sigma2Builder._clamp(
            1.0
            - (
                (
                    first.reference_variance
                    + second.reference_variance
                    + abs(first.association - second.association)
                )
                / 3.0
            ),
        )
        if not Sigma2Builder._case_marks_are_causally_consistent(
            causal_alignment=causal_alignment,
            sentence_space=sentence_space,
            subject_mark=subject_mark,
            predicate_mark=predicate_mark,
        ):
            raise SigmaTransitionError(
                "Case marks contradict the underlying causal structure"
            )
        if (
            sentence_space is SentenceSpace.KHABAR
            and subject_mark == "raf"
            and predicate_mark == "raf"
            and (
                first.reference_variance > thresholds.epsilon_rho / 2.0
                or second.reference_variance > thresholds.epsilon_rho / 2.0
            )
        ):
            raise SigmaTransitionError(
                "Unstable reference cannot enter fixed khabari predication"
            )

        case_impact = CaseImpactVector2(
            subject_mark=subject_mark,
            predicate_mark=predicate_mark,
            causal_alignment=causal_alignment,
            referential_alignment=referential_alignment,
            grammatical_factor_code=g_i.code,
            causal_trace=f"jm:{(first.j_m + second.j_m)/2.0:.3f}|c:{(first.causality + second.causality)/2.0:.3f}",
            referential_trace=(
                f"var:{(first.reference_variance + second.reference_variance)/2.0:.3f}"
                f"|assoc_delta:{abs(first.association - second.association):.3f}"
            ),
        )

        return Sigma2Matrix(
            sigma1_first=first,
            sigma1_second=second,
            mental_factor=mental_factor,
            reference_predication=s2,
            ratios=ratios,
            grammatical_factor=g_i,
            case_impact=case_impact,
            proposition_constraint=proposition_constraint,
            sentence_space=sentence_space,
        )
