# Arabic Cognitive Fractal Engine

محرك عربي معرفي فراكتالي — يثبت أن Unicode هو أدنى أثر حسابي لمدخل لغوي-معرفي.

## Architecture

```
arabic_engine/
├── core/              # Enumerations, types, gate logic (split by domain)
├── singular/          # Layers 0-3: Perception → Information → Concept
├── weight/            # Layer 4: Weight/Mizan fractal
├── semantic_kernel/   # Semantic kernel: 𝒦_root → 𝒦_form transfer layer
├── composition/       # Layer 5: Role distribution (asnadi/tadmini/taqyidi)
├── proposition/       # Layer 6: Proposition structure and closure
├── communicative/     # Khabar/Insha classification, stylistic closure
├── judgement/         # Layer 7: Judgement model, transition, closure
├── language/          # Layer 9: Transcendental container (Lang_tr)
├── trace/             # Unified trace, replay, audit
├── contracts/         # Adjacency, invariants, anti-jump, state mapping
└── runtime/           # Master chain, runtime view, proof view
```

## The Ten Mandatory Layers

| Layer | Name | Description |
|-------|------|-------------|
| 0 | Pre-U0 Admissibility | الحضور والتمييز والقبول الأولي |
| 1 | Singular Perceptual | الأثر الحسي والثبات/التحول الأولي |
| 2 | Singular Informational | الربط بالمعلومات السابقة والسببية والزمن |
| 3 | Singular Conceptual | التعريف والتذكير والاسم/الفعل/الحرف |
| 4 | Weight / Mizan | القابلية الوزنية والتصنيف والشرعية الاشتقاقية |
| 4+ | Semantic Kernel | نقل حمولة المعنى من الجذر إلى الصيغة (𝒦_root → 𝒦_form) |
| 5 | Compositional Roles | توزيع الأدوار والنسب |
| 6 | Proposition | القضية |
| 7 | Judgement | الحكم |
| 8 | Qiyas | القياس |
| 9 | Language | الوعاء الترنسندنتالي — Lang_tr = Proj(Con(Ord(Rel(𝒦)))) |

## Installation

```bash
pip install -e .
```

## Testing

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## Intellectual Leadership

- **al-Nabhani**: cognitive ordering, conception, subject liberation, judgement, anti-jump logic
- **Sibawayh**: Arabic structural precision, grammatical roles, internal language architecture
- **Kant** (conditions of possibility): language as transcendental container for cognitive categories

## Semantic Kernel (𝒦_root → 𝒦_form)

The semantic kernel layer transforms roots from morphological strings into
computable semantic vectors and transports meaning through pattern and form:

```
K_F = W_r · r_sem + W_p · p_sem + W_f · f_sem + Δ_ctx
```

See [`docs/semantic_kernel_architecture_v1.md`](docs/semantic_kernel_architecture_v1.md)
for the full mathematical specification.

## Language as Transcendental Container (Lang_tr)

Language is not the origin of reason but the transcendental container that
collects cognitive categories after they form in the mind, prevents their
confusion, and renders them expressible, predicable, referable, and testable.

```
Lang_tr = Proj(Con(Ord(Rel(𝒦))))

𝒦 = {Entity, Quality, Event, Relation, Cause, Condition,
      Negation, Quantity, Limitation, Reference, Temporality, Spatiality}

Lang_tr = ⟨Lexicon, CategorySystem, PredicationRules,
          ConstraintSystem, ReferenceSystem, TestabilityInterface⟩
```

See [`docs/language_transcendental_container_v1.md`](docs/language_transcendental_container_v1.md)
for the full specification.
