"""Tests for the trace package (unified tracer, replayer, auditor)."""

from arabic_engine.core.enums_gate import GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.enums_trace import TraceEventKind, TraceSeverity
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_trace import TraceEvent, TraceLog

from arabic_engine.trace.unified import UnifiedTracer
from arabic_engine.trace.replay import TraceReplayer
from arabic_engine.trace.audit import TraceAuditor


def test_tracer_records_gate_pass():
    tracer = UnifiedTracer()
    result = GateResult(verdict=GateVerdict.PASS, layer=Layer.SINGULAR_PERCEPTUAL)
    tracer.record_gate(result)
    assert len(tracer.log.events) == 1
    assert tracer.log.events[0].severity is TraceSeverity.INFO


def test_tracer_records_rejection():
    tracer = UnifiedTracer()
    result = GateResult(
        verdict=GateVerdict.REJECT,
        layer=Layer.WEIGHT_MIZAN,
        reason="test rejection",
    )
    tracer.record_gate(result)
    assert tracer.log.events[0].severity is TraceSeverity.ERROR
    assert tracer.log.has_errors


def test_tracer_records_transition():
    tracer = UnifiedTracer()
    tracer.record_transition(Layer.SINGULAR_CONCEPTUAL, Layer.WEIGHT_MIZAN)
    assert tracer.log.events[0].kind is TraceEventKind.LAYER_TRANSITION


def test_replayer_produces_lines():
    log = TraceLog()
    log.append(TraceEvent(
        kind=TraceEventKind.GATE_CHECK,
        layer=Layer.SINGULAR_PERCEPTUAL,
        severity=TraceSeverity.INFO,
        reason="test",
    ))
    lines = TraceReplayer.replay(log)
    assert len(lines) == 1
    assert "SINGULAR_PERCEPTUAL" in lines[0]


def test_replayer_filters_errors():
    log = TraceLog()
    log.append(TraceEvent(
        kind=TraceEventKind.GATE_CHECK,
        layer=Layer.SINGULAR_PERCEPTUAL,
        severity=TraceSeverity.INFO,
    ))
    log.append(TraceEvent(
        kind=TraceEventKind.REJECTION,
        layer=Layer.WEIGHT_MIZAN,
        severity=TraceSeverity.ERROR,
        reason="test error",
    ))
    errors = TraceReplayer.replay_errors(log)
    assert len(errors) == 1


def test_auditor_layer_coverage():
    log = TraceLog()
    for layer in [
        Layer.PRE_U0_ADMISSIBILITY,
        Layer.SINGULAR_PERCEPTUAL,
        Layer.SINGULAR_INFORMATIONAL,
        Layer.SINGULAR_CONCEPTUAL,
        Layer.WEIGHT_MIZAN,
        Layer.COMPOSITIONAL_ROLES,
        Layer.PROPOSITION,
        Layer.JUDGEMENT,
        Layer.QIYAS,
        Layer.LANGUAGE,
    ]:
        log.append(TraceEvent(
            kind=TraceEventKind.GATE_CHECK,
            layer=layer,
        ))
    coverage = TraceAuditor.audit_layer_coverage(log)
    assert all(coverage.values())


def test_auditor_detects_jump():
    log = TraceLog()
    log.append(TraceEvent(
        kind=TraceEventKind.LAYER_TRANSITION,
        layer=Layer.SINGULAR_PERCEPTUAL,
    ))
    log.append(TraceEvent(
        kind=TraceEventKind.LAYER_TRANSITION,
        layer=Layer.WEIGHT_MIZAN,  # skips informational and conceptual
    ))
    violations = TraceAuditor.audit_no_jump(log)
    assert len(violations) > 0
