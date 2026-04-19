# Arabic Cognitive Fractal Engine

محرك عربي معرفي فراكتالي — يثبت أن Unicode هو أدنى أثر حسابي لمدخل لغوي-معرفي.

## Architecture

```
arabic_engine/
├── core/              # Enumerations, types, gate logic (split by domain)
├── singular/          # Layers 0-3: Perception → Information → Concept
├── weight/            # Layer 4: Weight/Mizan fractal
├── composition/       # Layer 5: Role distribution (asnadi/tadmini/taqyidi)
├── proposition/       # Layer 6: Proposition structure and closure
├── communicative/     # Khabar/Insha classification, stylistic closure
├── judgement/         # Layer 7: Judgement model, transition, closure
├── trace/             # Unified trace, replay, audit
├── contracts/         # Adjacency, invariants, anti-jump, state mapping
└── runtime/           # Master chain, runtime view, proof view
```

## The Nine Mandatory Layers

| Layer | Name | Description |
|-------|------|-------------|
| 0 | Pre-U0 Admissibility | الحضور والتمييز والقبول الأولي |
| 1 | Singular Perceptual | الأثر الحسي والثبات/التحول الأولي |
| 2 | Singular Informational | الربط بالمعلومات السابقة والسببية والزمن |
| 3 | Singular Conceptual | التعريف والتذكير والاسم/الفعل/الحرف |
| 4 | Weight / Mizan | القابلية الوزنية والتصنيف والشرعية الاشتقاقية |
| 5 | Compositional Roles | توزيع الأدوار والنسب |
| 6 | Proposition | القضية |
| 7 | Judgement | الحكم |
| 8 | Qiyas | القياس |

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
