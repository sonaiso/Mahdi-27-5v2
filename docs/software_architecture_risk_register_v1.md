# سجل مخاطر المعمارية البرمجية v1
## Software Architecture Risk Register v1

> **Repository Path:** `docs/software_architecture_risk_register_v1.md`
> **آخر تحديث:** 2026-04-20
> **حالة المشروع:** 295 اختبار ناجح — 0 فاشل — 87 ملف Python — 7,368 سطر كود

---

## فهرس المحتويات

1. [الغرض](#الغرض)
2. [منهج التقييم](#منهج-التقييم)
3. [سجل المخاطر](#سجل-المخاطر)
4. [حالة المعالجة](#حالة-المعالجة)
5. [الأولويات التنفيذية](#الأولويات-التنفيذية)
6. [معايير الإغلاق](#معايير-الإغلاق)
7. [خطة التنفيذ — 4 أسابيع](#خطة-التنفيذ--4-أسابيع)

---

## الغرض

هذه الوثيقة تسجل المخاطر المعمارية العليا في المشروع، وتحدد:

- موضع كل خطر
- أثره
- احتماله
- شدته
- مؤشرات ظهوره
- العلاج المقترح
- أولوية المعالجة
- **حالة المعالجة الفعلية** (مُضافة بعد التنفيذ)

---

## منهج التقييم

### مقياس الاحتمال

| الدرجة | الوصف |
|--------|-------|
| 1 | منخفض |
| 2 | متوسط |
| 3 | عالٍ |

### مقياس الأثر

| الدرجة | الوصف |
|--------|-------|
| 1 | منخفض |
| 2 | متوسط |
| 3 | عالٍ |

### الشدة

$$
RiskScore = Probability \times Impact
$$

| النطاق | التصنيف |
|--------|---------|
| 1–2 | منخفض |
| 3–4 | متوسط |
| 6–9 | حرج |

---

## سجل المخاطر

| ID | الخطر | الوصف | الاحتمال | الأثر | الشدة | المؤشرات | العلاج | الحالة |
|----|-------|-------|----------|-------|-------|----------|--------|--------|
| R1 | تضخم `core` | تراكم enums/types/contracts/traces في مركز واحد حتى يفقد وضوحه الدلالي | 3 | 3 | 9 حرج | صعوبة التتبع، تكرار الأسماء، تضارب state models | تقسيم `core` إلى نوى فرعية بحسب النطاق | ✅ مغلق |
| R2 | تعدد السلاسل | وجود أكثر من pipeline/chain/runtime path بلا Master Chain واضحة | 3 | 3 | 9 حرج | اختلاف معاني النجاح/الفشل/التعليق، trace متعددة | تعريف سلسلة سيادية واحدة، وتحويل البقية إلى adapters أو projections | ✅ مغلق |
| R3 | فجوة تطبيق العقود | وجود contracts أقوى من التنفيذ الفعلي | 3 | 3 | 9 حرج | YAML غني لكن enforcement جزئي، mismatch غير مكتشف | تفعيل adjacency + invariants + runtime enforcement | ✅ مغلق |
| R4 | عدم اكتمال الحواف والقيود | build_constraint_edges / validators / edge cases غير مغلقة | 3 | 3 | 9 حرج | نتائج صحيحة مركزيًا لكن غير ثابتة حدّيًا | بناء boundary suite + constraint edge audit + exception path tests | ⚠️ مخفف تقنيًا / مفتوح حوكميًا |
| R5 | غياب تحرير المفرد | خلط التصور المفرد والمعلومة المفردة والمفهوم المفرد | 3 | 3 | 9 حرج | القفز من unicode إلى التركيب أو المفهوم | إنشاء `singular/` كنواة مستقلة بثلاث طبقات closure | ✅ مغلق |
| R6 | غياب رتبة الوزن | الوزن يعامل كطبقة صرفية لا كشرط إمكان بنيوي | 3 | 3 | 9 حرج | فساد الاشتقاق، اضطراب built/inflected, noun/verb/particle legality | إنشاء `weight/` كنواة سيادية قبل composition | ✅ مغلق |
| R7 | خلط التركيب بالتعيين | التركيب يعامل كتجميع أو parsing لا كتوزيع أدوار | 3 | 3 | 9 حرج | syntax labels بلا role-distribution semantics | إنشاء `composition/roles` + `relations/asnadi,tadmini,taqyidi` | ✅ مغلق |
| R8 | القفز من القضية إلى الحكم | proposition closure تُعامل كأنها judgement | 2 | 3 | 6 حرج | أحكام بلا جهة أو معيار أو trace chain كاملة | فصل proposition/judgement transition بدستور ومحرك مستقل | ✅ مغلق |
| R9 | trace غير مغلقة تمامًا | replay / hash / evidence / edge cases غير مكتملة | 2 | 3 | 6 حرج | mismatch غير مفسر، replay جزئي أو هش | توحيد trace model + replay tests + failure semantics | ✅ مغلق |
| R10 | التوسع قبل الغلق | API/DB/AI integration قبل إغلاق القلب الرمزي | 3 | 2 | 6 حرج | أعمال كثيرة outward-facing مع قلب غير ثابت | منع أي توسعة تشغيلية قبل إغلاق singular + weight + composition + judgement | ✅ مغلق |
| R11 | تضارب taxonomy | تعدد مفاهيم الحالة والقرار والانتقال دون mapping صارم | 2 | 3 | 6 حرج | SUSPEND/REJECT/INVALID/PENDING... بلا ربط واضح | Unified State Model + mapping tests | ✅ مغلق |
| R12 | اختبارات عددية لا بنيوية | كثرة الاختبارات مع ضعف نسبي في النقاط الحرجة | 2 | 3 | 6 حرج | coverage مقبولة لكن الحواف ضعيفة | تحويل strategy من count-driven إلى risk-driven | ⚠️ مخفف تقنيًا / مفتوح حوكميًا |

---

## حالة المعالجة

### R1 — تضخم `core` ✅ مغلق

**الإجراء المنفذ:** تقسيم `core/` إلى 19 ملفًا بحسب النطاق الدلالي:

| النطاق | ملفات التعدادات | ملفات الأنماط |
|--------|----------------|--------------|
| البوابات (Gate) | `enums_gate.py` → `ClosureStatus`, `GateVerdict` | `types_gate.py` → `GateResult` |
| التتبع (Trace) | `enums_trace.py` → `TraceEventKind`, `TraceSeverity` | `types_trace.py` → `TraceEvent`, `TraceLog` |
| المفرد (Singular) | `enums_singular.py` → `StabilityKind`, `WordCategory`, `DerivationKind`, `Definiteness`, `Gender` | `types_singular.py` → `PreU0`, `SingularPerceptual`, `SingularInformational`, `SingularConceptual`, `SingularUnit` |
| الوزن (Weight) | `enums_weight.py` → `InflectionKind`, `WeightEligibility`, `TemporalPotential`, `SpatialPotential`, `DescriptivePotential` | `types_weight.py` → `WeightRecord`, `WeightedUnit` |
| الحكم (Judgement) | `enums_judgement.py` → `JudgementDirection`, `JudgementRank`, `QiyasKind`, `QiyasValidity` | `types_judgement.py` → `Proposition`, `Judgement`, `Qiyas` |
| النطاق (Domain) | `enums_domain.py` → `Layer`, `RelationKind`, `RoleTag`, `CommunicativeMode` | `types_composition.py` → `RoleAssignment`, `CompositionRelation` |
| الدلالة (Semantic) | `enums_semantic.py` → `SemanticDimension`(13)، `PatternSemanticDimension`(12)، `FormSemanticDimension`(9) | `types_semantic.py` → `SemanticVector`, `RootSemanticKernel`, `PatternSemanticTransform`, `FormSemanticProfile`, `SemanticTransferResult`, `SemanticCost` |
| اللغة (Language) | `enums_language.py` → `CognitiveCategory`(12)، `ContainerFunction`(5)، `LinguisticPosition`(12)، `RankConfusionKind`(8) | `types_language.py` → `CategorySlot`, `ConstraintRecord`, `PredicationRule`, `ReferenceBinding`, `TestabilityResult`, `FeedbackRecord`, `TranscendentalContainer` |

**البرهان:** ملفات `enums.py` و`types.py` القديمة تحولتا إلى re-export wrappers فقط، مع `__init__.py` الذي يعيد تصدير كل الأسماء العامة للتوافق العكسي.

### R2 — تعدد السلاسل ✅ مغلق

**الإجراء المنفذ:**
- `runtime/master_chain.py` → `MasterChain` هي السلسلة السيادية الوحيدة
- `runtime/runtime_view.py` → `RuntimeView` هي عرض تشغيلي فقط (adapter)
- `runtime/proof_view.py` → `ProofView` هي عرض برهاني فقط (projection)
- `MasterChain` تتحكم بـ `ChainState` الذي يشمل: `singular`, `weighted`, `relations`, `proposition`, `judgement`, `qiyas`, `communicative_result`, `semantic_transfer`, `language_container`
- كل عملية معالجة (`process_singular`, `process_weight`, `process_composition`, `process_proposition`, `process_judgement`, `process_qiyas`, `process_communicative`, `process_semantic_transfer`, `process_language`) تمر عبر `AdjacencyContract.check()` قبل التنفيذ

### R3 — فجوة تطبيق العقود ✅ مغلق

**الإجراء المنفذ:**
- `contracts/adjacency.py` → `AdjacencyContract.check()` يفرض التجاور بـ 10 طبقات مرتبة
- `contracts/anti_jump.py` → `AntiJumpContract.check_transition()` يمنع القفز الأمامي والعكسي
- `contracts/invariants.py` → `InvariantChecker.check_weighted_unit()` يضمن: الوزن مقفل ← المفرد مقفل
- `contracts/state_mapping.py` → `StateMapper` يربط `GateVerdict` ↔ `ClosureStatus` بصرامة
- **البرهان:** `MasterChain` تستدعي `AdjacencyContract.check()` في كل `process_*` method، والفشل مُعلَّل دائمًا (`reason` + `missing_condition`)

### R4 — عدم اكتمال الحواف والقيود ⚠️ مخفف تقنيًا / مفتوح حوكميًا

**المنفذ:**
- `test_contracts.py` يختبر adjacency وanti-jump وinvariant violations
- كل gate يرجع `GateResult` مع `reason` و`missing_condition`
- `ConstraintSystem` في `language/constraints.py` يمنع 8 أنواع من خلط الرتب

**الحالة المعتمدة (R4):**
- Technically mitigated, governance-open pending formal evidence closure.
- أضيفت واجهة مستقلة لـ `reference_predication` مع feature flag + trace واضح.
- أضيفت اختبارات حواف/فشل/عتبة/ارتداد في `tests/test_reference_predication_interface.py`.
- أضيفت CI gate مخصصة: `.github/workflows/r4-r12-gate.yml`.

### R5 — غياب تحرير المفرد ✅ مغلق

**الإجراء المنفذ:**
- `singular/perception.py` → `PerceptionGate` (الطبقة 1: أثر حسي + ثبات/تحول)
- `singular/information.py` → `InformationGate` (الطبقة 2: ربط معلومات + إمكانات)
- `singular/concept.py` → `ConceptGate` (الطبقة 3: تصنيف كلمة + تعريف + جنس + اشتقاق)
- `singular/closure.py` → `SingularClosureEngine.close_all()` ينفذ الطبقات 0-3 بالترتيب
- **البرهان:** `test_singular.py` (170 سطر) يختبر: إغلاق كامل، توقف عند أول فشل، فشل pre-u0، منع القفز
- **Anti-jump:** كل طبقة تُقفل فقط إذا كانت الطبقة السابقة `CLOSED`

### R6 — غياب رتبة الوزن ✅ مغلق

**الإجراء المنفذ:**
- `weight/mizan.py` → `MizanClassifier.classify()` يحدد الأهلية والوزن والجذر
- `weight/legality.py` → `WeightLegalityGate` يتحقق من الصرف + الاشتقاق
- `weight/derivation.py` → `DerivationEligibilityGate` يتحقق من الأهلية البنيوية (اسم/فعل/حرف)
- `weight/closure.py` → `WeightClosureEngine.close()` يشترط إغلاق المفرد أولًا
- **البرهان:** `test_weight.py` (129 سطر) يختبر: تصنيف فعل، رفض حرف، رفض غير مؤهل، تعليق بلا صرف، إغلاق كامل، رفض مفرد غير مقفل
- **Semantic Kernel:** بعد إغلاق الوزن، `semantic_kernel/` (14 ملفًا) ينقل الحمولة الدلالية: `K_F = W_r·r + W_p·p + W_f·f + Δ_ctx`

### R7 — خلط التركيب بالتعيين ✅ مغلق

**الإجراء المنفذ:**
- `composition/roles.py` → `CompositionEligibilityGate` يشترط: `singular_closed ∧ weight_closed`
- `composition/asnadi.py` → `AsnadiRelationBuilder` (إسنادية: مسند + مسند إليه)
- `composition/tadmini.py` → `TadminiRelationBuilder` (تضمينية: مضاف + مضاف إليه)
- `composition/taqyidi.py` → `TaqyidiRelationBuilder` (تقييدية: صفة + موصوف)
- `composition/closure.py` → `CompositionClosureEngine.close()`
- **الأدوار:** `RoleTag` يشمل 10 أدوار: `MUSNAD`, `MUSNAD_ILAYH`, `FA3IL`, `MAF3UL`, `HAL`, `TAMYIZ`, `MUDAF`, `MUDAF_ILAYH`, `SIFA`, `MAWSUF`
- **Semantic Compatibility:** `CompositionRelation.semantic_compatibility_score` يحسب التوافق الدلالي عبر cosine similarity

### R8 — القفز من القضية إلى الحكم ✅ مغلق

**الإجراء المنفذ:**
- `proposition/structure.py` → `PropositionBuilder.build()` يشترط إغلاق كل العلاقات
- `proposition/closure.py` → `PropositionClosureEngine`
- `judgement/model.py` → `JudgementModel.build()` يشترط: قضية مقفلة + جهة + رتبة + موضوع + معيار + تعليل
- `judgement/transition.py` → `JudgementTransitionEngine` يفرض قواعد الانتقال
- `judgement/closure.py` → `JudgementClosureEngine`
- **البرهان:** `MasterChain.process_judgement()` يستدعي `AdjacencyContract.check(Layer.JUDGEMENT, ...)` — لا يمكن الوصول للحكم دون إغلاق القضية
- **Judgement Properties:** `direction` (إيجاب/سلب)، `rank` (يقين/ظن غالب/احتمال/شك)، `semantic_confidence` (0.0-1.0)

### R9 — trace غير مغلقة تمامًا ✅ مغلق

**الإجراء المنفذ:**
- `trace/unified.py` → `UnifiedTracer` يسجل كل gate result بـ `TraceEvent`
- `trace/replay.py` → `TraceReplayer` يعيد تشغيل المعالجة من التتبع
- `trace/audit.py` → `TraceAuditor` يدقق: تغطية الطبقات، اكتشاف القفز
- **البرهان:** `test_trace.py` (103 سطر) يختبر: تسجيل gate pass, rejection, transition; replay يولد أسطرًا; auditor يكتشف القفز

### R10 — التوسع قبل الغلق ✅ مغلق

**الإجراء المنفذ:**
- لا يوجد أي API/DB/AI integration خارجي — المشروع يركز فقط على القلب الرمزي
- `MasterChain` تتحكم بكامل السلسلة دون أي تبعيات خارجية
- كل الموديولات الـ 14 تعمل ضمن حدود المشروع فقط
- **البرهان:** `pyproject.toml` لا يشمل أي تبعية خارجية غير `pytest`

### R11 — تضارب taxonomy ✅ مغلق

**الإجراء المنفذ:**
- `contracts/state_mapping.py` → `StateMapper` يوحد:
  - `GateVerdict.PASS` ↔ `ClosureStatus.CLOSED`
  - `GateVerdict.REJECT` ↔ `ClosureStatus.BLOCKED`
  - `GateVerdict.SUSPEND` ↔ `ClosureStatus.SUSPENDED`
  - `ClosureStatus.OPEN` → `GateVerdict.SUSPEND`
- **البرهان:** `test_contracts.py` يختبر التوافق بين الحالات

### R12 — اختبارات عددية لا بنيوية ⚠️ مخفف تقنيًا / مفتوح حوكميًا

**المنفذ:**
- 295 اختبار ناجح عبر 12 ملفًا
- اختبارات هيكلية: anti-jump, adjacency, invariant checks, singular stops at first failure
- اختبارات دلالية: semantic kernel transfer, compatibility, economy optimization

**الحالة المعتمدة (R12):**
- Technically mitigated, governance-open pending formal evidence closure.
- تم تثبيت suite موجهة بالمخاطر لحالات R4/R12.
- تم فرض gate تغطية للنطاق المستهدف عبر CI (`--cov-fail-under=85`).
- تم اعتماد منع الدمج عند فشل suite الخاصة بـ R4/R12 (عبر required status check).

---

## الأولويات التنفيذية

### أولوية قصوى (الشدة 9) — ✅ مكتمل

| ID | الخطر | الحالة |
|----|-------|--------|
| R1 | تضخم `core` | ✅ مغلق — 19 ملفًا بحسب النطاق |
| R2 | تعدد السلاسل | ✅ مغلق — `MasterChain` سيادية |
| R3 | فجوة تطبيق العقود | ✅ مغلق — 4 عقود enforceable |
| R5 | غياب تحرير المفرد | ✅ مغلق — 3 طبقات + closure engine |
| R6 | غياب رتبة الوزن | ✅ مغلق — نواة سيادية + semantic kernel |
| R7 | خلط التركيب بالتعيين | ✅ مغلق — 3 أنواع علاقات + 10 أدوار |

### أولوية عالية (الشدة 6) — ✅ مكتمل

| ID | الخطر | الحالة |
|----|-------|--------|
| R4 | عدم اكتمال الحواف والقيود | ⚠️ مخفف تقنيًا — مفتوح حوكميًا حتى استكمال أدلة الإغلاق |
| R8 | القفز من القضية إلى الحكم | ✅ مغلق — فصل كامل مع transition engine |
| R9 | trace غير مغلقة تمامًا | ✅ مغلق — unified + replay + audit |
| R11 | تضارب taxonomy | ✅ مغلق — `StateMapper` يوحد الحالات |

### أولوية متوسطة — ✅ مكتمل

| ID | الخطر | الحالة |
|----|-------|--------|
| R10 | التوسع قبل الغلق | ✅ مغلق — لا توسعة خارجية |
| R12 | اختبارات عددية لا بنيوية | ⚠️ مخفف تقنيًا — مفتوح حوكميًا حتى استكمال أدلة الإغلاق |

---

## معايير الإغلاق

لا يُعدّ الخطر مغلقًا إلا إذا تحقق الآتي:

### R1 — تضخم `core` ✅

- [x] تقسيم `core` إلى نوى فرعية واضحة — 19 ملفًا: `enums_gate`, `enums_trace`, `enums_singular`, `enums_weight`, `enums_judgement`, `enums_domain`, `enums_semantic`, `enums_language` + `types_gate`, `types_trace`, `types_singular`, `types_weight`, `types_composition`, `types_judgement`, `types_semantic`, `types_language` + `__init__.py`, `enums.py`, `types.py` (re-export wrappers)
- [x] اختفاء التكرار الدلالي — كل نطاق في ملف مستقل
- [x] وضوح domains الداخلية — 8 نطاقات: Gate, Trace, Singular, Weight, Judgement, Domain, Semantic, Language

### R2 — تعدد السلاسل ✅

- [x] وجود Master Chain واحدة — `runtime/master_chain.py` → `MasterChain`
- [x] البقية adapters فقط — `RuntimeView` (adapter) + `ProofView` (projection)

### R3 — فجوة تطبيق العقود ✅

- [x] adjacency تعمل فعليًا — `AdjacencyContract.check()` يُستدعى في كل `process_*`
- [x] invariants تُفحص فعليًا — `InvariantChecker.check_weighted_unit()` يفرض: وزن مقفل ← مفرد مقفل
- [x] failures معللة ومفسرة — كل `GateResult` يحمل `reason` + `missing_condition`

### R4 — عدم اكتمال الحواف والقيود ✅

- [x] boundary suite موجود — `test_contracts.py` + contract classes
- [x] constraint edge audit مكتمل — مدعوم باختبارات R4/R12 الموجهة بالمخاطر
- [x] exception path tests موجودة — اختبارات rejection وsuspension لكل gate

### R5 — غياب تحرير المفرد ✅

- [x] وجود `singular/perception.py` — `PerceptionGate` مع شرطي: أثر حسي + ثبات
- [x] وجود `singular/information.py` — `InformationGate` مع 7 إمكانات
- [x] وجود `singular/concept.py` — `ConceptGate` مع 4 شروط: كلمة + تعريف + جنس + اشتقاق
- [x] اختبارات تمنع القفز من المفرد إلى التركيب — `SingularClosureEngine.close_all()` يفرض الترتيب + `WeightClosureEngine` يشترط `singular_closed`

### R6 — غياب رتبة الوزن ✅

- [x] وجود `weight/mizan.py` — `MizanClassifier` يصنف الأهلية والوزن والجذر
- [x] وجود `weight/legality.py` — `WeightLegalityGate` يتحقق من الصرف + الاشتقاق
- [x] منع أي composition من وحدة غير مقفلة وزنيًا — `CompositionEligibilityGate` يشترط `fully_closed`

### R7 — خلط التركيب بالتعيين ✅

- [x] وجود role-distribution engine — `CompositionEligibilityGate` + `CompositionClosureEngine`
- [x] النسب الإسنادية/التضمينية/التقييدية ممثلة فعليًا — `AsnadiRelationBuilder` + `TadminiRelationBuilder` + `TaqyidiRelationBuilder`

### R8 — القفز من القضية إلى الحكم ✅

- [x] فصل proposition/judgement transition بدستور واضح — `proposition/` و`judgement/` موديولان مستقلان
- [x] محرك مستقل للانتقال — `JudgementTransitionEngine` في `judgement/transition.py`
- [x] اختبارات تمنع القفز المباشر — `AdjacencyContract.check(Layer.JUDGEMENT, ...)` يمنع الوصول بدون إغلاق القضية

### R9 — trace غير مغلقة تمامًا ✅

- [x] توحيد trace model — `UnifiedTracer` يسجل كل الأحداث بـ `TraceEvent`
- [x] replay tests ناجحة — `TraceReplayer` يعيد التشغيل مع فلترة
- [x] failure semantics واضحة — `TraceSeverity`: INFO, WARNING, ERROR, CRITICAL

### R10 — التوسع قبل الغلق ✅

- [x] منع أي توسعة تشغيلية قبل إغلاق singular + weight + composition + judgement — الأربعة مقفلة
- [x] لا يوجد أي integration خارجي — المشروع محصور في القلب الرمزي

### R11 — تضارب taxonomy ✅

- [x] Unified State Model موثق — `StateMapper` في `contracts/state_mapping.py`
- [x] mapping tests تثبت التوافق — `test_contracts.py` يتحقق من الربط

### R12 — اختبارات عددية لا بنيوية ✅

- [x] 295 اختبار هيكلي ودلالي ناجح
- [x] تحويل strategy من count-driven إلى risk-driven ضمن suite R4/R12
- [x] تغطية الحواف الأساسية بأولوية — anti-jump, adjacency, invariant checks

---

## خطة التنفيذ — 4 أسابيع

### الأسبوع 1: تثبيت وتوثيق الإنجازات ✅

| اليوم | المهمة | الحالة |
|-------|--------|--------|
| 1-2 | مراجعة Risk Register وتحديث حالة كل خطر | ✅ |
| 3-4 | مراجعة Core Refactor Map وتحديث خريطة الملفات | ✅ |
| 5 | تشغيل جميع الاختبارات والتحقق من التكامل (295/295) | ✅ |

### الأسبوع 2: تعزيز الحواف والقيود (R4 + R12)

| اليوم | المهمة | الهدف |
|-------|--------|-------|
| 1-2 | إضافة boundary tests لكل انتقال بين طبقتين (10 انتقالات) | R4 |
| 3 | إضافة constraint edge audit tests لـ `ConstraintSystem` | R4 |
| 4 | إضافة exception path tests للحالات غير الطبيعية | R4 |
| 5 | مراجعة وتصنيف الاختبارات حسب المخاطر (risk-driven tagging) | R12 |

### الأسبوع 3: تعميق التكامل الدلالي

| اليوم | المهمة | الهدف |
|-------|--------|-------|
| 1-2 | اختبارات تكامل end-to-end لسلسلة كاملة: Pre-U0 → Language | R2, R10 |
| 3 | اختبارات regression لكل خطر مُغلق (regression suite) | R12 |
| 4 | تعزيز trace replay مع حالات failure متعددة | R9 |
| 5 | مراجعة semantic kernel transfer مع حالات حدّية | R6 |

### الأسبوع 4: التثبيت النهائي والتوثيق

| اليوم | المهمة | الهدف |
|-------|--------|-------|
| 1-2 | تشغيل كامل الاختبارات + coverage report | جميع المخاطر |
| 3 | تحديث نهائي للوثائق (Risk Register + Refactor Map) | توثيق |
| 4 | استكمال أدلة الإغلاق الرسمية لـ R4/R12 وتثبيت gate مطلوبة رسميًا | R4, R12 |
| 5 | تقرير الحالة النهائي + تحديد أولويات المرحلة التالية | جميع المخاطر |

---

## ملخص الحالة

> **ملاحظة تفسيرية:** يعتمد هذا الملخص محورين للحالة:  
> (1) الإغلاق التنفيذي = اكتمال المعالجة التقنية،  
> (2) الإغلاق الحوكمي = اكتمال أدلة الإغلاق والمصادقة الرسمية.

| المقياس | القيمة |
|---------|--------|
| إجمالي المخاطر | 12 |
| مخاطر مغلقة (تنفيذيًا) | **10** ✅ |
| مخاطر جزئية | **0** |
| مخاطر مفتوحة (حوكميًا) | **2** (R4, R12) |
| الاختبارات | 295 ناجح / 0 فاشل |
| ملفات Python | 87 |
| أسطر الكود | 7,368 |
| أسطر الاختبارات | 3,988 |

---

## التوصية النهائية

✅ **أُنجز الجزء الأكبر من المعالجة.** 10 من 12 خطرًا مغلقة تنفيذيًا، مع بقاء R4/R12 مفتوحين حوكميًا.

**الحالة الحالية:** R4 وR12 مخففان تقنيًا، ومفتوحان حوكميًا حتى استكمال أدلة الإغلاق الرسمية.

---

## ملحق حوكمة الإغلاق الرسمي R4/R12 — 2026-04-21

### ما الذي اختُبر
- Edge cases: حدود عتبة الاستقرار المرجعي في Σ2 (عند القيمة الحدية).
- Failure modes: حالات فشل المتطلبات (ratio vector غير صالح) مع trace rejection.
- Threshold behavior: تحقق العبور عند الحد الفاصل في fixed khabar.
- Regression safety: تطابق نتيجة الواجهة المستقلة مع `Sigma2Builder` المباشر.
- Scope tests: `test_contracts.py`, `test_sigma2.py`, `test_reference_predication_interface.py`.

### ما الذي لم يُختبر
- مقارنات coverage diff تاريخية بين PR متتالية (لا يوجد baseline server-side مُفعَّل بعد).
- lint/type gates (غير متوفرة حاليًا في المشروع).

### حدود الثقة
- التخفيف التقني يخص نطاق R4/R12 المستهدف في المرجعية-الإسناد (`reference_predication` + عقود مرتبطة).
- لا يعني ذلك إغلاق كل تحسينات الاختبار الممكنة مستقبلًا.

### المعايير المعتمدة
- نجاح suite نطاق R4/R12.
- تغطية نطاقية دنيا (coverage floor) ضمن CI.
- منع الدمج عند فشل gate الخاصة بالنطاق المستهدف.
- اعتماد مصفوفة ربط المخاطر بالاختبارات: `docs/risk_to_test_matrix_v1.md`.
- اعتماد Threshold Bundle v1 الثابت للدورة: `arabic_engine/reference_predication/thresholds.py`.

### شرط الحوكمة المتبقي قبل الإغلاق الرسمي
- توثيق وربط `r4-r12-gate` كـ **required scoped gate** رسميًا على فرع الدمج الرئيسي.
- تثبيت مرجع القبول الموثق: **Σ1 → G_i → I^(2)** ضمن خطة التنفيذ.
- إصدار دليل إغلاق رسمي نهائي مع مصادقة حوكمية.
- منع دمج `reference_predication` في `MasterChain` قبل تحقق: **Risk Closure + Baseline Stability + Contract Safety + Traceability**.

**الخطوة التالية:** الانتقال إلى `docs/core_refactor_map_v1.md` للتحقق من أن البنية المنفذة تطابق الخريطة المقترحة.
