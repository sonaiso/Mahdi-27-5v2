# خريطة إعادة تشكيل القلب v1
## Core Refactor Map v1

> **Repository Path:** `docs/core_refactor_map_v1.md`
> **آخر تحديث:** 2026-04-20
> **حالة المشروع:** 295 اختبار ناجح — 87 ملف Python — 14 موديول — 7,368 سطر

---

## فهرس المحتويات

1. [الغرض](#الغرض)
2. [المبدأ الحاكم](#المبدأ-الحاكم)
3. [ما يبقى كما هو](#ما-يبقى-كما-هو)
4. [ما يفكك](#ما-يفكك)
5. [ما يفصل إلى نوى مستقلة](#ما-يفصل-إلى-نوى-مستقلة)
6. [الترتيب التنفيذي](#الترتيب-التنفيذي)
7. [خريطة الملفات المقترحة والفعلية](#خريطة-الملفات-المقترحة-والفعلية)
8. [معايير النجاح](#معايير-النجاح)
9. [خطة التنفيذ — 4 أسابيع](#خطة-التنفيذ--4-أسابيع)

---

## الغرض

هذه الوثيقة تحدد:

- ما الذي يجب الحفاظ عليه
- ما الذي يجب تفكيكه
- ما الذي يجب فصله إلى package مستقلة
- ما الترتيب الصحيح لإعادة الهيكلة
- **ما الذي تحقق فعليًا** (مُضاف بعد التنفيذ)

---

## المبدأ الحاكم

لا نعيد البناء من الصفر بمحو كل شيء، ولا نرقع الهيكل القديم.
بل نتبع هذا القانون:

> **نُبقي الرصيد المعرفي والتنفيذي النافع، ونفصل النوى السيادية التي اختلطت، ثم نعيد ربطها تحت سلسلة واحدة.**

---

## ما يبقى كما هو

### 1. الرصيد الاختباري ✅

يبقى مع إعادة التوزيع حسب المخاطر.

**الحالة الفعلية:** 295 اختبار في 12 ملفًا (3,988 سطر) — جميعها ناجحة.

| ملف الاختبار | الأسطر | التغطية |
|-------------|--------|---------|
| `test_singular.py` | 170 | إغلاق المفرد (الطبقات 0-3) |
| `test_weight.py` | 129 | إغلاق الوزن (الطبقة 4) |
| `test_semantic_kernel.py` | 601 | مكونات الحمولة الدلالية |
| `test_semantic_phases.py` | 833 | مراحل النقل الدلالي |
| `test_semantic_integration.py` | 437 | تكامل الحمولة الدلالية |
| `test_chain.py` | 296 | تنسيق السلسلة الرئيسية |
| `test_communicative.py` | 279 | تصنيف الخبر والإنشاء |
| `test_language.py` | 792 | نظام الوعاء الترنسندنتالي |
| `test_qiyas.py` | 245 | القياس |
| `test_trace.py` | 103 | نظام التتبع |
| `test_contracts.py` | 103 | تنفيذ العقود |

### 2. الرصيد الوثائقي الدستوري ✅

يبقى ويصبح مرجعًا للتصميم:

- `docs/software_architecture_risk_register_v1.md` — سجل المخاطر (هذه الوثيقة الشقيقة)
- `docs/semantic_kernel_architecture_v1.md` — معمارية الحمولة الدلالية
- `docs/language_transcendental_container_v1.md` — الوعاء الترنسندنتالي
- `docs/weight_and_mizan_fractal_constitution_v1.md` — دستور الوزن والميزان

### 3. النماذج المفيدة الحالية ✅

يبقى ما يصلح من:

- gate logic — `GateResult`, `GateVerdict`, `ClosureStatus`
- trace logic — `TraceEvent`, `TraceLog`, `UnifiedTracer`
- judgement records — `Judgement`, `JudgementModel`, `JudgementTransitionEngine`
- closure verification — `*ClosureEngine` في كل موديول
- بعض وحدات root/pattern/ontology/evaluation — `semantic_kernel/root_kernel.py`, `semantic_kernel/pattern_transform.py`

### 4. لغة المشروع العربية ✅

تبقى سمة أساسية — كل `reason` في `GateResult` مكتوب بالعربية.

---

## ما يفكك

### 1. `core/enums.py` ✅ مُنفَّذ

فُكِّك إلى 8 ملفات بحسب النطاق الدلالي:

| الملف الجديد | المحتوى | الحالة |
|-------------|---------|--------|
| `core/enums_gate.py` | `ClosureStatus`, `GateVerdict` | ✅ |
| `core/enums_trace.py` | `TraceEventKind`, `TraceSeverity` | ✅ |
| `core/enums_singular.py` | `StabilityKind`, `WordCategory`, `DerivationKind`, `Definiteness`, `Gender` | ✅ |
| `core/enums_weight.py` | `InflectionKind`, `WeightEligibility`, `TemporalPotential`, `SpatialPotential`, `DescriptivePotential` | ✅ |
| `core/enums_judgement.py` | `JudgementDirection`, `JudgementRank`, `QiyasKind`, `QiyasValidity` | ✅ |
| `core/enums_domain.py` | `Layer`, `RelationKind`, `RoleTag`, `CommunicativeMode` | ✅ |
| `core/enums_semantic.py` | `SemanticDimension`(13), `PatternSemanticDimension`(12), `FormSemanticDimension`(9), `CompatibilityStatus` | ✅ (إضافة) |
| `core/enums_language.py` | `CognitiveCategory`(12), `ContainerFunction`(5), `LinguisticPosition`(12), `RankConfusionKind`(8), `ContainerValidityStatus` | ✅ (إضافة) |

**ملاحظة:** ملف `enums.py` القديم تحول إلى re-export wrapper للتوافق العكسي.

### 2. `core/types.py` ✅ مُنفَّذ

فُكِّك إلى 8 ملفات بحسب النطاق الدلالي:

| الملف الجديد | المحتوى | الحالة |
|-------------|---------|--------|
| `core/types_gate.py` | `GateResult` | ✅ |
| `core/types_trace.py` | `TraceEvent`, `TraceLog` | ✅ |
| `core/types_singular.py` | `PreU0`, `SingularPerceptual`, `SingularInformational`, `SingularConceptual`, `SingularUnit` | ✅ |
| `core/types_weight.py` | `WeightRecord`, `WeightedUnit` | ✅ |
| `core/types_composition.py` | `RoleAssignment`, `CompositionRelation` | ✅ |
| `core/types_judgement.py` | `Proposition`, `Judgement`, `Qiyas` | ✅ |
| `core/types_semantic.py` | `SemanticVector`, `RootSemanticKernel`, `PatternSemanticTransform`, `FormSemanticProfile`, `SemanticTransferResult`, `SemanticCost` | ✅ (إضافة) |
| `core/types_language.py` | `CategorySlot`, `ConstraintRecord`, `PredicationRule`, `ReferenceBinding`, `TestabilityResult`, `FeedbackRecord`, `TranscendentalContainer` | ✅ (إضافة) |

**ملاحظة:** ملف `types.py` القديم تحول إلى re-export wrapper للتوافق العكسي.

### 3. السلاسل المتعددة ✅ مُنفَّذ

تفككت من حيث السيادة:

- **Master Chain** → `runtime/master_chain.py` — السلسلة السيادية الوحيدة
- **RuntimeView** → `runtime/runtime_view.py` — عرض تشغيلي (adapter)
- **ProofView** → `runtime/proof_view.py` — عرض برهاني (projection)

---

## ما يفصل إلى نوى مستقلة

### النواة 1: Singular Core — نواة المفرد ✅

| المكون | الوصف | الملف | الحالة |
|--------|-------|-------|--------|
| `perception` | التصور المفرد (الطبقة 1) | `singular/perception.py` → `PerceptionGate` | ✅ |
| `information` | المعلومة المفردة (الطبقة 2) | `singular/information.py` → `InformationGate` | ✅ |
| `concept` | المفهوم المفرد (الطبقة 3) | `singular/concept.py` → `ConceptGate` | ✅ |
| `closure` | محرك الإغلاق | `singular/closure.py` → `SingularClosureEngine` | ✅ |

### النواة 2: Weight/Mizan Core — نواة الوزن والميزان ✅

| المكون | الوصف | الملف | الحالة |
|--------|-------|-------|--------|
| `weight classification` | تصنيف الوزن | `weight/mizan.py` → `MizanClassifier` | ✅ |
| `legality` | مشروعية الاشتقاق | `weight/legality.py` → `WeightLegalityGate` | ✅ |
| `derivational eligibility` | أهلية الاشتقاق | `weight/derivation.py` → `DerivationEligibilityGate` | ✅ |
| `built/inflected relation` | العلاقة بين المبني والمعرب | `InflectionKind.MABNI` / `MU3RAB` في `enums_weight.py` | ✅ |
| `lexical structural eligibility` | الأهلية البنيوية المعجمية | `noun_eligible`, `verb_eligible`, `particle_eligible` في `WeightRecord` | ✅ |
| `closure` | محرك الإغلاق | `weight/closure.py` → `WeightClosureEngine` | ✅ |

### النواة 2+: Semantic Kernel Core — نواة الحمولة الدلالية ✅ (إضافة)

| المكون | الوصف | الملف | الحالة |
|--------|-------|-------|--------|
| `root kernel` | النواة الدلالية للجذر (13 بُعدًا) | `semantic_kernel/root_kernel.py` → `RootKernelBuilder` | ✅ |
| `pattern transform` | مؤثر الوزن الدلالي (12 بُعدًا) | `semantic_kernel/pattern_transform.py` → `PatternTransformBuilder` | ✅ |
| `form profile` | ملف الصيغة الدلالي (9 أبعاد) | `semantic_kernel/form_profile.py` → `FormProfileBuilder` | ✅ |
| `transfer` | محرك النقل الدلالي: `K_F = W_r·r + W_p·p + W_f·f + Δ_ctx` | `semantic_kernel/transfer.py` → `SemanticTransferEngine` | ✅ |
| `compatibility` | فحص التوافق (جذر ↔ وزن) | `semantic_kernel/compatibility.py` → `CompatibilityChecker` | ✅ |
| `alignment` | إسقاط المتجهات بين الأبعاد | `semantic_kernel/alignment.py` | ✅ |
| `context` | حساب `Δ_ctx` | `semantic_kernel/context.py` → `ContextDeltaBuilder` | ✅ |
| `economy` | تحسين تكلفة النقل | `semantic_kernel/economy.py` → `EconomyOptimizer` | ✅ |
| `weight scheduler` | جدولة الأوزان | `semantic_kernel/weight_scheduler.py` → `WeightScheduler` | ✅ |
| `phonotactics` | فحص الصوتيات | `semantic_kernel/phonotactics.py` → `PhonotacticChecker` | ✅ |
| `metrics` | قياسات النقل | `semantic_kernel/metrics.py` → `TransferMetrics` | ✅ |
| `seed data` | بيانات مرجعية | `semantic_kernel/seed_data.py` | ✅ |
| `closure` | محرك الإغلاق | `semantic_kernel/closure.py` → `SemanticKernelClosureEngine` | ✅ |

### النواة 3: Compositional Role Core — نواة التركيب والأدوار ✅

| المكون | الوصف | الملف | الحالة |
|--------|-------|-------|--------|
| `role distribution` | توزيع الأدوار (10 أدوار) | `composition/roles.py` → `CompositionEligibilityGate` | ✅ |
| `asnadi relations` | العلاقات الإسنادية | `composition/asnadi.py` → `AsnadiRelationBuilder` | ✅ |
| `tadmini relations` | العلاقات التضمينية | `composition/tadmini.py` → `TadminiRelationBuilder` | ✅ |
| `taqyidi relations` | العلاقات التقييدية | `composition/taqyidi.py` → `TaqyidiRelationBuilder` | ✅ |
| `عامل/معمول models` | نماذج العامل والمعمول | `RoleTag`: `FA3IL`, `MAF3UL`, `MUSNAD`, `MUSNAD_ILAYH` | ✅ |
| `closure` | محرك الإغلاق | `composition/closure.py` → `CompositionClosureEngine` | ✅ |

### النواة 4: Proposition Core — نواة القضية ✅

| المكون | الوصف | الملف | الحالة |
|--------|-------|-------|--------|
| `proposition structure` | بنية القضية | `proposition/structure.py` → `PropositionBuilder` | ✅ |
| `proposition closure` | إغلاق القضية | `proposition/closure.py` → `PropositionClosureEngine` | ✅ |

### النواة 5: Communicative/Stylistic Core — نواة التواصل والأسلوب ✅

| المكون | الوصف | الملف | الحالة |
|--------|-------|-------|--------|
| `khabar/insha classification` | تصنيف الخبر والإنشاء | `communicative/khabar_insha.py` → `KhabarInshaClassifier` | ✅ |
| `communicative closure` | الإغلاق التواصلي | `communicative/closure.py` → `CommunicativeClosureEngine` | ✅ |
| `stylistic closure` | الإغلاق الأسلوبي | `communicative/stylistic.py` → `StylisticGate` | ✅ |

### النواة 6: Judgement Core — نواة الحكم ✅

| المكون | الوصف | الملف | الحالة |
|--------|-------|-------|--------|
| `subject` | الموضوع | `subject: str` في `Judgement` | ✅ |
| `direction` | الجهة (إيجاب/سلب) | `direction: JudgementDirection` في `Judgement` | ✅ |
| `criterion` | المعيار | `criterion: str` في `Judgement` | ✅ |
| `content` | المحتوى | `proposition: Proposition` في `Judgement` | ✅ |
| `rank` | الرتبة (يقين/ظن غالب/احتمال/شك) | `rank: JudgementRank` في `Judgement` | ✅ |
| `reason` | التعليل | `reason: str` في `Judgement` | ✅ |
| `trace` | التتبع | `semantic_confidence: float` + `UnifiedTracer` | ✅ |
| `model` | نموذج الحكم | `judgement/model.py` → `JudgementModel` | ✅ |
| `transition` | محرك الانتقال | `judgement/transition.py` → `JudgementTransitionEngine` | ✅ |
| `closure` | محرك الإغلاق | `judgement/closure.py` → `JudgementClosureEngine` | ✅ |

### النواة 6+: Qiyas Core — نواة القياس ✅ (إضافة)

| المكون | الوصف | الملف | الحالة |
|--------|-------|-------|--------|
| `model` | نموذج القياس (4 أركان) | `qiyas/model.py` → `QiyasModel` | ✅ |
| `transition` | محرك الانتقال | `qiyas/transition.py` → `QiyasTransitionEngine` | ✅ |
| `closure` | محرك الإغلاق | `qiyas/closure.py` → `QiyasClosureEngine` | ✅ |

### النواة 7: Trace Core — نواة التتبع ✅

| المكون | الوصف | الملف | الحالة |
|--------|-------|-------|--------|
| `unified trace` | التتبع الموحد | `trace/unified.py` → `UnifiedTracer` | ✅ |
| `replay` | إعادة التشغيل | `trace/replay.py` → `TraceReplayer` | ✅ |
| `audit` | التدقيق | `trace/audit.py` → `TraceAuditor` | ✅ |
| `mismatch diagnosis` | تشخيص التعارض | `TraceAuditor.check_layer_coverage()` + `check_jumps()` | ✅ |

### النواة 8: Contracts Core — نواة العقود ✅

| المكون | الوصف | الملف | الحالة |
|--------|-------|-------|--------|
| `adjacency` | التجاور (10 طبقات) | `contracts/adjacency.py` → `AdjacencyContract` | ✅ |
| `invariants` | الثوابت | `contracts/invariants.py` → `InvariantChecker` | ✅ |
| `anti-jump` | منع القفز | `contracts/anti_jump.py` → `AntiJumpContract` | ✅ |
| `state mapping` | ربط الحالات | `contracts/state_mapping.py` → `StateMapper` | ✅ |

### النواة 9: Language Core — نواة الوعاء الترنسندنتالي ✅ (إضافة)

| المكون | الوصف | الملف | الحالة |
|--------|-------|-------|--------|
| `categories` | سجل المقولات (12 مقولة) | `language/categories.py` → `CategoryRegistry` | ✅ |
| `container` | بناء الوعاء الترنسندنتالي | `language/container.py` → `TranscendentalContainerBuilder` | ✅ |
| `constraints` | نظام القيود (8 أنواع خلط) | `language/constraints.py` → `ConstraintSystem` | ✅ |
| `predication` | محرك الحمل | `language/predication.py` → `PredicationEngine` | ✅ |
| `reference` | نظام الإحالة | `language/reference.py` → `ReferenceSystem` | ✅ |
| `testability` | واجهة الاختبارية | `language/testability.py` → `TestabilityInterface` | ✅ |
| `feedback` | حلقة التغذية الراجعة | `language/feedback.py` → `FeedbackLoop` | ✅ |
| `closure` | محرك الإغلاق | `language/closure.py` → `LanguageClosureEngine` | ✅ |

---

## الترتيب التنفيذي

```
المرحلة 1 ──▶ المرحلة 2 ──▶ المرحلة 3 ──▶ المرحلة 4 ──▶ المرحلة 5 ──▶ المرحلة 6 ──▶ المرحلة 7
```

| المرحلة | العمل | المخاطر المعالجة | الحالة |
|---------|-------|-----------------|--------|
| **المرحلة 1** | فصل Singular Core | R5 | ✅ مكتمل |
| **المرحلة 2** | فصل Weight/Mizan Core + Semantic Kernel | R6 | ✅ مكتمل |
| **المرحلة 3** | فصل Compositional Role Core | R7 | ✅ مكتمل |
| **المرحلة 4** | تحديد Master Chain | R2 | ✅ مكتمل |
| **المرحلة 5** | فصل Proposition → Communicative → Judgement → Qiyas transition | R8 | ✅ مكتمل |
| **المرحلة 6** | توحيد Trace و Contracts | R3, R9, R11 | ✅ مكتمل |
| **المرحلة 7** | إعادة ربط runtime و API لاحقًا فقط | R10 | ✅ مكتمل (لا API حتى إغلاق القلب) |

---

## خريطة الملفات المقترحة والفعلية

```text
arabic_engine/                              # الحالة
├── __init__.py                              # ✅
├── core/                                    # ✅ 19 ملف (8 enums + 8 types + __init__ + 2 re-export)
│   ├── __init__.py                          # ✅ يعيد تصدير كل الأسماء العامة
│   ├── enums.py                             # ✅ re-export wrapper (توافق عكسي)
│   ├── enums_gate.py                        # ✅ ClosureStatus, GateVerdict
│   ├── enums_trace.py                       # ✅ TraceEventKind, TraceSeverity
│   ├── enums_singular.py                    # ✅ StabilityKind, WordCategory, DerivationKind, Definiteness, Gender
│   ├── enums_weight.py                      # ✅ InflectionKind, WeightEligibility, TemporalPotential, ...
│   ├── enums_judgement.py                   # ✅ JudgementDirection, JudgementRank, QiyasKind, QiyasValidity
│   ├── enums_domain.py                      # ✅ Layer, RelationKind, RoleTag, CommunicativeMode
│   ├── enums_semantic.py                    # ✅ SemanticDimension(13), PatternSemanticDimension(12), ...
│   ├── enums_language.py                    # ✅ CognitiveCategory(12), ContainerFunction(5), ...
│   ├── types.py                             # ✅ re-export wrapper (توافق عكسي)
│   ├── types_gate.py                        # ✅ GateResult
│   ├── types_trace.py                       # ✅ TraceEvent, TraceLog
│   ├── types_singular.py                    # ✅ PreU0, SingularPerceptual, SingularInformational, ...
│   ├── types_weight.py                      # ✅ WeightRecord, WeightedUnit
│   ├── types_composition.py                 # ✅ RoleAssignment, CompositionRelation
│   ├── types_judgement.py                   # ✅ Proposition, Judgement, Qiyas
│   ├── types_semantic.py                    # ✅ SemanticVector, RootSemanticKernel, ...
│   └── types_language.py                    # ✅ CategorySlot, TranscendentalContainer, ...
│
├── singular/                                # ✅ نواة المفرد (5 ملفات)
│   ├── __init__.py                          # ✅
│   ├── perception.py                        # ✅ PerceptionGate
│   ├── information.py                       # ✅ InformationGate
│   ├── concept.py                           # ✅ ConceptGate
│   └── closure.py                           # ✅ SingularClosureEngine
│
├── weight/                                  # ✅ نواة الوزن (5 ملفات)
│   ├── __init__.py                          # ✅
│   ├── mizan.py                             # ✅ MizanClassifier
│   ├── legality.py                          # ✅ WeightLegalityGate
│   ├── derivation.py                        # ✅ DerivationEligibilityGate
│   └── closure.py                           # ✅ WeightClosureEngine
│
├── semantic_kernel/                         # ✅ نواة الحمولة الدلالية (14 ملفًا) — إضافة
│   ├── __init__.py                          # ✅
│   ├── root_kernel.py                       # ✅ RootKernelBuilder (13-dim)
│   ├── pattern_transform.py                 # ✅ PatternTransformBuilder (12-dim)
│   ├── form_profile.py                      # ✅ FormProfileBuilder (9-dim)
│   ├── transfer.py                          # ✅ SemanticTransferEngine (K_F equation)
│   ├── compatibility.py                     # ✅ CompatibilityChecker
│   ├── alignment.py                         # ✅ Projection functions
│   ├── context.py                           # ✅ ContextDeltaBuilder
│   ├── economy.py                           # ✅ EconomyOptimizer
│   ├── weight_scheduler.py                  # ✅ WeightScheduler
│   ├── phonotactics.py                      # ✅ PhonotacticChecker
│   ├── metrics.py                           # ✅ TransferMetrics
│   ├── seed_data.py                         # ✅ Reference data
│   └── closure.py                           # ✅ SemanticKernelClosureEngine
│
├── composition/                             # ✅ نواة التركيب والأدوار (6 ملفات)
│   ├── __init__.py                          # ✅
│   ├── roles.py                             # ✅ CompositionEligibilityGate
│   ├── asnadi.py                            # ✅ AsnadiRelationBuilder
│   ├── tadmini.py                           # ✅ TadminiRelationBuilder
│   ├── taqyidi.py                           # ✅ TaqyidiRelationBuilder
│   └── closure.py                           # ✅ CompositionClosureEngine
│
├── proposition/                             # ✅ نواة القضية (3 ملفات)
│   ├── __init__.py                          # ✅
│   ├── structure.py                         # ✅ PropositionBuilder
│   └── closure.py                           # ✅ PropositionClosureEngine
│
├── communicative/                           # ✅ نواة التواصل والأسلوب (4 ملفات)
│   ├── __init__.py                          # ✅
│   ├── khabar_insha.py                      # ✅ KhabarInshaClassifier
│   ├── stylistic.py                         # ✅ StylisticGate
│   └── closure.py                           # ✅ CommunicativeClosureEngine
│
├── judgement/                               # ✅ نواة الحكم (4 ملفات)
│   ├── __init__.py                          # ✅
│   ├── model.py                             # ✅ JudgementModel
│   ├── transition.py                        # ✅ JudgementTransitionEngine
│   └── closure.py                           # ✅ JudgementClosureEngine
│
├── qiyas/                                   # ✅ نواة القياس (4 ملفات) — إضافة
│   ├── __init__.py                          # ✅
│   ├── model.py                             # ✅ QiyasModel
│   ├── transition.py                        # ✅ QiyasTransitionEngine
│   └── closure.py                           # ✅ QiyasClosureEngine
│
├── language/                                # ✅ نواة الوعاء الترنسندنتالي (8 ملفات) — إضافة
│   ├── __init__.py                          # ✅
│   ├── categories.py                        # ✅ CategoryRegistry
│   ├── container.py                         # ✅ TranscendentalContainerBuilder
│   ├── constraints.py                       # ✅ ConstraintSystem
│   ├── predication.py                       # ✅ PredicationEngine
│   ├── reference.py                         # ✅ ReferenceSystem
│   ├── testability.py                       # ✅ TestabilityInterface
│   ├── feedback.py                          # ✅ FeedbackLoop
│   └── closure.py                           # ✅ LanguageClosureEngine
│
├── trace/                                   # ✅ نواة التتبع (4 ملفات)
│   ├── __init__.py                          # ✅
│   ├── unified.py                           # ✅ UnifiedTracer
│   ├── replay.py                            # ✅ TraceReplayer
│   └── audit.py                             # ✅ TraceAuditor
│
├── contracts/                               # ✅ نواة العقود (5 ملفات)
│   ├── __init__.py                          # ✅
│   ├── adjacency.py                         # ✅ AdjacencyContract
│   ├── invariants.py                        # ✅ InvariantChecker
│   ├── anti_jump.py                         # ✅ AntiJumpContract
│   └── state_mapping.py                     # ✅ StateMapper
│
└── runtime/                                 # ✅ السلسلة السيادية (4 ملفات)
    ├── __init__.py                          # ✅
    ├── master_chain.py                      # ✅ MasterChain (السلسلة الوحيدة)
    ├── runtime_view.py                      # ✅ RuntimeView (adapter)
    └── proof_view.py                        # ✅ ProofView (projection)
```

**الإحصاء الفعلي:**

| الموديول | عدد الملفات | الوصف |
|----------|-------------|-------|
| `core/` | 19 | تعدادات + أنماط مقسمة بحسب النطاق |
| `singular/` | 5 | نواة المفرد (الطبقات 0-3) |
| `weight/` | 5 | نواة الوزن (الطبقة 4) |
| `semantic_kernel/` | 14 | نواة الحمولة الدلالية |
| `composition/` | 6 | نواة التركيب والأدوار (الطبقة 5) |
| `proposition/` | 3 | نواة القضية (الطبقة 6) |
| `communicative/` | 4 | نواة التواصل والأسلوب |
| `judgement/` | 4 | نواة الحكم (الطبقة 7) |
| `qiyas/` | 4 | نواة القياس (الطبقة 8) |
| `language/` | 8 | نواة الوعاء الترنسندنتالي (الطبقة 9) |
| `trace/` | 4 | نواة التتبع |
| `contracts/` | 5 | نواة العقود |
| `runtime/` | 4 | السلسلة السيادية |
| **المجموع** | **87** | **7,368 سطر** |

---

## معايير النجاح

يُعدّ الـ refactor ناجحًا **فقط** إذا تحقق الآتي:

| # | المعيار | الحالة | البرهان |
|---|---------|--------|---------|
| 1 | لم يعد `core` عنق زجاجة معرفي | ✅ | 19 ملفًا مقسمة بحسب 8 نطاقات دلالية |
| 2 | أصبحت هناك Master Chain واحدة | ✅ | `MasterChain` في `runtime/master_chain.py` — `RuntimeView` و`ProofView` views فقط |
| 3 | صارت رتبة المفرد مستقلة وصريحة | ✅ | `singular/` نواة مستقلة بـ 3 طبقات + closure engine + anti-jump |
| 4 | صار الوزن نواة سيادية لا helper | ✅ | `weight/` + `semantic_kernel/` (14 ملفًا) — الوزن شرط إمكان لا أداة مساعدة |
| 5 | صار التركيب توزيع أدوار لا مجرد parsing | ✅ | `composition/` بـ 3 أنواع علاقات + 10 أدوار + semantic compatibility |
| 6 | صار الانتقال إلى الحكم مرحلة مستقلة | ✅ | `judgement/transition.py` + `AdjacencyContract` يفرض: قضية مقفلة → حكم |
| 7 | صارت العقود والتتبع enforceable لا وصفية فقط | ✅ | 4 عقود فعلية + `MasterChain` تستدعيها في كل خطوة |
| 8 | بقي الرصيد الحالي محفوظًا ولم يُهدم بلا ضرورة | ✅ | 295 اختبار ناجح — التوافق العكسي محفوظ عبر re-export wrappers |

---

## خريطة التبعيات بين الموديولات

```text
singular → core (types + enums)
weight → core + singular
semantic_kernel → core + weight (optional)
composition → core + weight + semantic_kernel
proposition → core + composition
communicative → core + judgement
judgement → core + composition + proposition
qiyas → core + judgement
language → core (all types)
trace → core
contracts → core + singular + weight + composition + proposition + judgement + qiyas
runtime → all modules (orchestrator)
```

---

## خطة التنفيذ — 4 أسابيع

### الأسبوع 1: تثبيت وتوثيق الإنجازات ✅ مكتمل

- [x] مراجعة Risk Register وتحديث حالة كل خطر (10/12 مغلق)
- [x] مراجعة Core Refactor Map وتحديث خريطة الملفات (87 ملف)
- [x] تشغيل جميع الاختبارات (295/295 ناجح)
- [x] توثيق النوى الإضافية: Semantic Kernel, Qiyas, Language

### الأسبوع 2: تعزيز الحواف والقيود

- [ ] إضافة boundary tests لكل انتقال بين طبقتين (10 انتقالات × 2 حالة = 20 اختبار)
- [ ] إضافة constraint edge audit tests لـ `ConstraintSystem` (8 أنواع خلط)
- [ ] إضافة exception path tests للحالات غير الطبيعية
- [ ] تصنيف الاختبارات حسب المخاطر (risk-driven tagging)

### الأسبوع 3: تعميق التكامل الدلالي

- [ ] اختبارات تكامل end-to-end لسلسلة كاملة: Pre-U0 → Language
- [ ] اختبارات regression لكل خطر مُغلق
- [ ] تعزيز trace replay مع حالات failure متعددة
- [ ] مراجعة semantic kernel transfer مع حالات حدّية

### الأسبوع 4: التثبيت النهائي

- [ ] تشغيل كامل الاختبارات + coverage report
- [ ] تحديث نهائي للوثائق
- [ ] إغلاق R4 وR12 رسميًا
- [ ] تقرير الحالة النهائي

---

## التوصية النهائية

✅ **إعادة تشكيل القلب مكتملة.** جميع معايير النجاح الثمانية تحققت.

**البنية الفعلية تتجاوز الخريطة المقترحة** بإضافة 3 نوى لم تكن في التصميم الأصلي:
1. **Language Core** (8 ملفات) — الوعاء الترنسندنتالي كطبقة تاسعة
2. **Qiyas Core** (4 ملفات) — القياس كطبقة ثامنة
3. **Semantic Kernel** (14 ملفًا) — Extension / Transitional Core Review حتى تثبيت مركزيته النهائية

**المتبقي:** تعزيز الحواف (R4) وتحويل استراتيجية الاختبار (R12) — عمليات تحسينية.
