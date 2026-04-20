"""
Master chain — the single sovereign pipeline.

Orchestrates the full processing chain from Pre-U0 through Language,
enforcing adjacency and anti-jump contracts at every step.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer, CommunicativeMode
from arabic_engine.core.enums_judgement import JudgementDirection, JudgementRank
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_singular import SingularUnit
from arabic_engine.core.types_weight import WeightRecord, WeightedUnit
from arabic_engine.core.types_composition import CompositionRelation
from arabic_engine.core.types_judgement import Proposition, Judgement
from arabic_engine.core.types_semantic import (
    FormSemanticProfile,
    PatternSemanticTransform,
    RootSemanticKernel,
    SemanticTransferResult,
)
from arabic_engine.core.types_language import (
    ReferenceBinding,
    TranscendentalContainer,
)

from arabic_engine.singular.closure import SingularClosureEngine
from arabic_engine.weight.closure import WeightClosureEngine
from arabic_engine.composition.closure import CompositionClosureEngine
from arabic_engine.proposition.structure import PropositionBuilder
from arabic_engine.judgement.model import JudgementModel
from arabic_engine.trace.unified import UnifiedTracer
from arabic_engine.contracts.adjacency import AdjacencyContract


@dataclass
class ChainState:
    """Current state of the master chain."""

    singular: Optional[SingularUnit] = None
    weighted: Optional[WeightedUnit] = None
    relations: list[CompositionRelation] = field(default_factory=list)
    proposition: Optional[Proposition] = None
    judgement: Optional[Judgement] = None
    semantic_transfer: Optional[SemanticTransferResult] = None
    language_container: Optional[TranscendentalContainer] = None
    current_layer: Layer = Layer.PRE_U0_ADMISSIBILITY
    closed_layers: set[Layer] = field(default_factory=set)
    all_results: list[GateResult] = field(default_factory=list)


class MasterChain:
    """The single sovereign processing pipeline.

    Processes a linguistic unit through all nine layers in strict order.
    """

    def __init__(self) -> None:
        self._state = ChainState()
        self._tracer = UnifiedTracer()

    @property
    def state(self) -> ChainState:
        return self._state

    @property
    def tracer(self) -> UnifiedTracer:
        return self._tracer

    def process_singular(self, unit: SingularUnit) -> list[GateResult]:
        """Process layers 0-3 (singular closure)."""
        self._state.singular = unit
        results = SingularClosureEngine.close_all(unit)

        for r in results:
            self._tracer.record_gate(r)
            self._state.all_results.append(r)

        if unit.singular_closed:
            self._state.closed_layers.update([
                Layer.PRE_U0_ADMISSIBILITY,
                Layer.SINGULAR_PERCEPTUAL,
                Layer.SINGULAR_INFORMATIONAL,
                Layer.SINGULAR_CONCEPTUAL,
            ])

        return results

    def process_weight(
        self,
        weight: WeightRecord,
        semantic_values: tuple[float, ...] | None = None,
        pattern_transform_values: tuple[float, ...] | None = None,
        form_values: tuple[float, ...] | None = None,
    ) -> list[GateResult]:
        """Process layer 4 (weight closure).

        When ``semantic_values``, ``pattern_transform_values``, and
        ``form_values`` are all provided, the semantic transfer step is
        automatically chained after weight closure succeeds.
        """
        if self._state.singular is None:
            r = GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.WEIGHT_MIZAN,
                reason="لم تُعالج المفردات بعد",
                missing_condition="singular_processed",
            )
            self._state.all_results.append(r)
            return [r]

        # Adjacency check
        adj = AdjacencyContract.check(Layer.WEIGHT_MIZAN, self._state.closed_layers)
        if not adj.passed:
            self._state.all_results.append(adj)
            return [adj]

        weighted = WeightedUnit(
            singular=self._state.singular,
            weight=weight,
        )
        self._state.weighted = weighted

        results = WeightClosureEngine.close(weighted)
        for r in results:
            self._tracer.record_gate(r)
            self._state.all_results.append(r)

        if weighted.fully_closed:
            self._state.closed_layers.add(Layer.WEIGHT_MIZAN)

        # Auto-chain semantic transfer when all semantic inputs are provided
        if (
            weighted.fully_closed
            and semantic_values is not None
            and pattern_transform_values is not None
            and form_values is not None
        ):
            from arabic_engine.semantic_kernel.root_kernel import (
                RootKernelBuilder,
                ROOT_SEMANTIC_DIM,
            )
            from arabic_engine.semantic_kernel.pattern_transform import (
                PatternTransformBuilder,
                PATTERN_SEMANTIC_DIM,
            )
            from arabic_engine.semantic_kernel.form_profile import (
                FormProfileBuilder,
                FORM_SEMANTIC_DIM,
            )

            # Validate dimension counts before building
            if (
                len(semantic_values) == ROOT_SEMANTIC_DIM
                and len(pattern_transform_values) == PATTERN_SEMANTIC_DIM
                and len(form_values) == FORM_SEMANTIC_DIM
            ):
                root_kernel = RootKernelBuilder.build(
                    root_text=weight.root,
                    semantic_values=semantic_values,
                )
                pat_transform = PatternTransformBuilder.build(
                    pattern_code=weight.pattern,
                    transform_values=pattern_transform_values,
                )
                form_profile = FormProfileBuilder.build(
                    pattern_id=pat_transform.pattern_id,
                    form_values=form_values,
                )
                sem_results = self.process_semantic_transfer(
                    root_kernel=root_kernel,
                    pattern_transform=pat_transform,
                    form_profile=form_profile,
                )
                results.extend(sem_results)

        return results

    def process_composition(
        self, relations: list[CompositionRelation]
    ) -> list[GateResult]:
        """Process layer 5 (composition closure)."""
        adj = AdjacencyContract.check(
            Layer.COMPOSITIONAL_ROLES, self._state.closed_layers
        )
        if not adj.passed:
            self._state.all_results.append(adj)
            return [adj]

        self._state.relations = relations
        results = CompositionClosureEngine.close(relations)
        for r in results:
            self._tracer.record_gate(r)
            self._state.all_results.append(r)

        if all(r.passed for r in results):
            self._state.closed_layers.add(Layer.COMPOSITIONAL_ROLES)

        return results

    def process_proposition(self) -> GateResult:
        """Process layer 6 (proposition)."""
        adj = AdjacencyContract.check(Layer.PROPOSITION, self._state.closed_layers)
        if not adj.passed:
            self._state.all_results.append(adj)
            return adj

        prop, result = PropositionBuilder.build(self._state.relations)
        self._tracer.record_gate(result)
        self._state.all_results.append(result)

        if result.passed and prop is not None:
            self._state.proposition = prop
            self._state.closed_layers.add(Layer.PROPOSITION)

        return result

    def process_judgement(
        self,
        direction: JudgementDirection,
        rank: JudgementRank,
        subject: str,
        criterion: str,
        reason: str = "",
    ) -> GateResult:
        """Process layer 7 (judgement)."""
        adj = AdjacencyContract.check(Layer.JUDGEMENT, self._state.closed_layers)
        if not adj.passed:
            self._state.all_results.append(adj)
            return adj

        if self._state.proposition is None:
            r = GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.JUDGEMENT,
                reason="لا توجد قضية",
                missing_condition="proposition",
            )
            self._state.all_results.append(r)
            return r

        judgement, result = JudgementModel.build(
            proposition=self._state.proposition,
            direction=direction,
            rank=rank,
            subject=subject,
            criterion=criterion,
            reason=reason,
        )
        self._tracer.record_gate(result)
        self._state.all_results.append(result)

        if result.passed and judgement is not None:
            self._state.judgement = judgement
            self._state.closed_layers.add(Layer.JUDGEMENT)

        return result

    def process_semantic_transfer(
        self,
        root_kernel: RootSemanticKernel,
        pattern_transform: PatternSemanticTransform,
        form_profile: FormSemanticProfile,
    ) -> list[GateResult]:
        """Process semantic transfer (requires weight closure).

        Runs the semantic transfer engine and the semantic kernel closure
        pipeline. The result is stored in the chain state and linked to
        the weight record only when closure succeeds.
        """
        # Weight must be closed
        if (
            self._state.weighted is None
            or not self._state.weighted.weight.weight_closed
        ):
            r = GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.WEIGHT_MIZAN,
                reason="الوزن غير مقفل — لا يجوز نقل الحمولة الدلالية",
                missing_condition="weight_closed",
            )
            self._state.all_results.append(r)
            return [r]

        # Consistency check: root_kernel must match the weight record's root
        weight = self._state.weighted.weight
        if root_kernel.root_text and weight.root and root_kernel.root_text != weight.root:
            r = GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.WEIGHT_MIZAN,
                reason=(
                    "تناقض بين نواة الجذر والوزن — "
                    f"الجذر الدلالي '{root_kernel.root_text}' "
                    f"لا يطابق جذر الوزن '{weight.root}'"
                ),
                missing_condition="root_consistency",
            )
            self._state.all_results.append(r)
            return [r]

        # Consistency check: pattern_transform must match the weight record's pattern
        if (
            pattern_transform.pattern_code
            and weight.pattern
            and pattern_transform.pattern_code != weight.pattern
        ):
            r = GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.WEIGHT_MIZAN,
                reason=(
                    "تناقض بين مؤثر الوزن والوزن — "
                    f"رمز الوزن الدلالي '{pattern_transform.pattern_code}' "
                    f"لا يطابق وزن السجل '{weight.pattern}'"
                ),
                missing_condition="pattern_consistency",
            )
            self._state.all_results.append(r)
            return [r]

        from arabic_engine.semantic_kernel.transfer import SemanticTransferEngine
        from arabic_engine.semantic_kernel.closure import (
            SemanticKernelClosureEngine,
        )

        # Run transfer
        transfer_result = SemanticTransferEngine.transfer(
            root_kernel=root_kernel,
            pattern_transform=pattern_transform,
            form_profile=form_profile,
        )

        # Run closure
        results = SemanticKernelClosureEngine.close(transfer_result)
        for r in results:
            self._tracer.record_gate(r)
            self._state.all_results.append(r)

        # Persist semantic transfer only after semantic closure succeeds
        if transfer_result.closure == ClosureStatus.CLOSED:
            self._state.semantic_transfer = transfer_result
            self._state.weighted.weight.semantic_transfer = transfer_result
            self._state.weighted.weight.semantic_kernel = root_kernel

        return results

    def process_language(
        self,
        reference_bindings: list[ReferenceBinding] | None = None,
    ) -> list[GateResult]:
        """Process the language layer (transcendental container).

        Builds the complete transcendental container Lang_tr and runs
        closure.  Requires all preceding layers to be closed.

        Parameters
        ----------
        reference_bindings : list[ReferenceBinding] | None
            Optional reference bindings for the reference system.
        """
        adj = AdjacencyContract.check(Layer.LANGUAGE, self._state.closed_layers)
        if not adj.passed:
            self._state.all_results.append(adj)
            return [adj]

        from arabic_engine.language.container import TranscendentalContainerBuilder
        from arabic_engine.language.closure import LanguageClosureEngine

        container = TranscendentalContainerBuilder.build(
            reference_bindings=reference_bindings,
        )
        self._state.language_container = container

        results = LanguageClosureEngine.close(container)
        for r in results:
            self._tracer.record_gate(r)
            self._state.all_results.append(r)

        if container.closure == ClosureStatus.CLOSED:
            self._state.closed_layers.add(Layer.LANGUAGE)

        return results
