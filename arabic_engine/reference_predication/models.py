"""
Reference-predication matrix models for Σ1 -> Σ2 transition.

Implements a computable formalization of:
- Criterion (3): prerequisite validity for singular reference units (Σ1)
- Sentence-level matrix construction (Σ2) across khabar/condition/naskh/insha
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


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


@dataclass(frozen=True)
class Sigma2Matrix:
    """Σ2 matrix for sentence-level reference predication."""

    sigma1_first: Sigma1ReferenceUnit
    sigma1_second: Sigma1ReferenceUnit
    mental_factor: MentalFactor
    reference_predication: ReferencePredicationVector2
    ratios: RatioVector
    grammatical_factor: str
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
    def build(
        first: Sigma1ReferenceUnit,
        second: Sigma1ReferenceUnit,
        *,
        sentence_space: SentenceSpace,
        mental_factor: MentalFactor,
        grammatical_factor: str,
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

        case_impact = CaseImpactVector2(
            subject_mark=subject_mark,
            predicate_mark=predicate_mark,
            causal_alignment=Sigma2Builder._clamp((first.j_m + second.j_m) / 2.0),
            referential_alignment=Sigma2Builder._clamp(
                1.0 - ((first.reference_variance + second.reference_variance) / 2.0),
            ),
        )

        return Sigma2Matrix(
            sigma1_first=first,
            sigma1_second=second,
            mental_factor=mental_factor,
            reference_predication=s2,
            ratios=ratios,
            grammatical_factor=grammatical_factor,
            case_impact=case_impact,
            proposition_constraint=proposition_constraint,
            sentence_space=sentence_space,
        )
