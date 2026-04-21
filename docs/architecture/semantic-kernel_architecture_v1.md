# Semantic Kernel Architecture v1

## هندسة النواة الدلالية — النسخة الأولى

---

## 1. المبدأ الأعلى

> **بعد الوصول إلى الوزن لا يكفي أن نستخرج البنية الصرفية، بل يجب أن نبني
> طبقةً ناقلةً لحمولة المعنى من الجذر إلى الصيغة بحيث تدخل في قلب النظام
> البرمجي بوصفها بنيةً قابلةً للحساب، لا شرحًا خارجيًا.**

---

## 2. الفرضية الفراكتالية بصيغة صورية

العربية نظام توليدي متعدد الطبقات يعيد إنتاج نمط بنيوي واحد عبر مستويات
مختلفة مع حفظ قدر من الهوية وتحويل قدر من الوظيفة:

```
𝒜 = {X₀, X₁, X₂, …, X₉}
```

حيث:
- X₀: الطبقة الذرية (Pre-U0)
- X₁: طبقة التمييز الصوتي (Perceptual)
- X₂: الحركة/المقطع (Informational)
- X₃: الجذر (Conceptual)
- X₄: الوزن (Weight/Mizan)
- X₅: الصيغة (Compositional)
- X₆: الحمل النحوي (Proposition)
- X₇: الحمل الدلالي (Judgement)
- X₈: الحكم (Qiyas)

مؤثرات الانتقال:

```
T_n : X_n → X_{n+1}

Id(T_n(X_n), X_n) ≥ ε      (حفظ الهوية)
StructSim(T_n(X_n), X_n) ≥ λ  (تشابه بنيوي متعدد المقاييس)
```

---

## 3. هندسة الطبقات الخمس

### الطبقة الأولى: الطبقة الترميزية

```
Text → Unicode → SymbolUnits
```

وحدات: حرف، حركة، شدة، سكون، موضع، ترتيب.

### الطبقة الثانية: الطبقة الصرفية

```
SymbolUnits → Syllable → Root → Pattern → Form
```

### الطبقة الثالثة: طبقة النواة الدلالية (𝒦_root)

```
Root → 𝒦_root
```

حيث 𝒦_root ليست معنى قاموسيًا فقط بل متجهًا دلاليًا منظمًا من 13 بُعدًا.

### الطبقة الرابعة: طبقة نقل الحمولة

```
𝒦_root + Pattern + FormFeatures → 𝒦_form
```

### الطبقة الخامسة: طبقة الحكم والاختبار

```
𝒦_form + Syntax + Context → J_p → Test
```

---

## 4. تمثيل الجذر كمتجه دلالي

```
R = ⟨r_phon, r_struct, r_sem⟩
```

حيث r_sem متجه من 13 بُعدًا:

```python
r_sem = ⟨Entity, Event, Quality, Relation, Agency, Patienthood,
         Causality, Resultativity, Temporality, Spatiality,
         Embodiment, Abstraction, Transferability⟩
```

**مقياسات مشتقة:**
- `identity_score`: مقدار التركيز الدلالي للجذر (1 - H_norm)
- `transformability_score`: قابلية الجذر للتحويل (4·H_norm·(1-H_norm))

---

## 5. معادلة نقل حمولة المعنى

```
K_F = W_r · r_sem + W_p · p_sem + W_f · f_sem + Δ_ctx
```

حيث:
- `W_r = 0.50` — وزن الجذر
- `W_p = 0.30` — وزن الوزن
- `W_f = 0.15` — وزن الصيغة
- `Δ_ctx = 0.05` — تعديل السياق

### معنى المعادلة

| المكوّن | الدور |
|---------|-------|
| الجذر | يحمل الحمولة الأولية |
| الوزن | يعيد توجيه الحمولة |
| الصيغة | تضيف جهة استعمالية ونحوية |
| السياق | يعدّل النتيجة |

---

## 6. تمثيل الوزن دلاليًا

المتجه التحويلي للوزن من 12 بُعدًا:

```python
p_sem = ⟨EventShift, AgencyShift, TransitivityShift, CausativeShift,
         ReflexiveShift, Intensification, Iterativity, StativeShift,
         Nominalization, Instrumentality, Locativity, TemporalityShift⟩
```

**أمثلة:**
- **فَعَّلَ**: Intensification↑, CausativeShift↑
- **اِسْتَفْعَلَ**: AgencyShift↑ (seeking)
- **اِنْفَعَلَ**: ReflexiveShift↑, StativeShift↑

---

## 7. تمثيل الصيغة

المتجه الدلالي للصيغة من 9 أبعاد:

```python
f_sem = ⟨Category, Tense, Aspect, Voice, Number, Gender,
         Definiteness, SyntacticLoad, Referentiality⟩
```

---

## 8. شرط الحد الأدنى المكتمل

```
Complete_min(R, P, F) ⟺
    ValidRoot(R) ∧ ValidPattern(P) ∧ Compatible(R,P) ∧ Realizable(F)
```

---

## 9. معادلة الاقتصاد

```
x* = argmin_x Cost(x) s.t. Complete_min(x) = 1

Cost(x) = Cost_phon + Cost_morph + Cost_cog + Cost_sem
```

---

## 10. بوابات الإغلاق (Closure Gates)

تتبع نفس نمط Gate → Closure → Trace المستخدم في كل الطبقات:

1. **بوابة التوافق** — الجذر والوزن متوافقان
2. **بوابة الحد الأدنى المكتمل** — Complete_min(R,P,F) = 1
3. **بوابة الاقتصاد** — الكلفة منتهية ومعقولة

---

## 11. البرهان الصوري على إمكان الفراكتال

### المسلمات

1. يوجد نمط أولي مولد x₀ (متجه الجذر الدلالي)
2. يوجد مؤثر انتقال T_n (SemanticTransferEngine)
3. يحفظ الانتقال قدرًا من الهوية: Id(T_n(x_n), x_n) ≥ ε
4. يعيد إنتاج بنية متشابهة: StructSim(T_n(x_n), x_n) ≥ λ
5. يتحقق عبر أكثر من مستوى: Root → Pattern → Form → Judgement

### النتيجة

إذا ثبتت هذه الشروط تجريبيًا على عدد كافٍ من المستويات، جاز وصف العربية
بأنها ذات بنية فراكتالية توليدية.

---

## 12. بنية البيانات

### جدول الجذور

| الحقل | النوع | الوصف |
|-------|-------|-------|
| root_id | str | معرّف فريد |
| root_text | str | نص الجذر |
| phonological_signature | str | التوقيع الصوتي |
| structural_signature | str | التوقيع البنيوي |
| semantic_vector | SemanticVector(13) | المتجه الدلالي |
| identity_score | float | درجة حفظ الهوية |
| transformability_score | float | قابلية التحويل |

### جدول الأوزان

| الحقل | النوع | الوصف |
|-------|-------|-------|
| pattern_id | str | معرّف فريد |
| pattern_code | str | رمز الوزن |
| surface_template | str | القالب السطحي |
| semantic_transform_vector | SemanticVector(12) | متجه التحويل |
| closure_index | float | مؤشر الإغلاق |
| morphological_cost | float | الكلفة الصرفية |

### جدول الصيغ

| الحقل | النوع | الوصف |
|-------|-------|-------|
| form_id | str | معرّف فريد |
| pattern_id | str | معرّف الوزن |
| form_semantic_vector | SemanticVector(9) | المتجه الدلالي للصيغة |

### جدول النقل الدلالي

| الحقل | النوع | الوصف |
|-------|-------|-------|
| transfer_id | str | معرّف فريد |
| input_kernel | SemanticVector | النواة الداخلية |
| output_kernel | SemanticVector | النواة الخارجية (𝒦_form) |
| transformation_score | float | درجة التحويل |
| compatibility_score | float | درجة التوافق |
| closure | ClosureStatus | حالة الإغلاق |

---

## 13. الجدول البحثي النهائي

| Variable | Arabic Term | Layer | Mathematical Role | Data Type | Testability |
|----------|------------|-------|-------------------|-----------|-------------|
| r_sem | المتجه الدلالي للجذر | 𝒦_root | النمط الأولي المولد | SemanticVector(13) | قابل للقياس |
| p_sem | المتجه التحويلي للوزن | 𝒦_root→𝒦_form | المؤثر الانتقالي | SemanticVector(12) | قابل للقياس |
| f_sem | المتجه الدلالي للصيغة | 𝒦_form | طبقة التوجيه | SemanticVector(9) | قابل للقياس |
| K_F | نواة المعنى | 𝒦_form | المخرج النهائي | SemanticVector | قابل للقياس |
| W_r | وزن الجذر | Transfer | معامل المزج | float | قابل للضبط |
| W_p | وزن الوزن | Transfer | معامل المزج | float | قابل للضبط |
| W_f | وزن الصيغة | Transfer | معامل المزج | float | قابل للضبط |
| Δ_ctx | تعديل السياق | Transfer | تصحيح سياقي | SemanticVector | قابل للقياس |
| Complete_min | الحد الأدنى المكتمل | Gate | شرط القبول | bool | قابل للاختبار |
| Cost | الكلفة الإجمالية | Economy | دالة التحسين | SemanticCost | قابل للقياس |
| Id(T_n) | حفظ الهوية | Fractal | مقياس التشابه | float ∈ [0,1] | قابل للاختبار |
| StructSim | التشابه البنيوي | Fractal | مقياس الفراكتالية | float ∈ [0,1] | قابل للاختبار |
| CompatibilityStatus | حالة التوافق | Gate | شرط القبول | Enum | قابل للاختبار |

---

## 14. خريطة الملفات

```
arabic_engine/
├── core/
│   ├── enums_semantic.py          ← تعدادات الأبعاد الدلالية
│   ├── types_semantic.py          ← أنماط البيانات الدلالية
│   ├── types_weight.py            ← + حقول دلالية اختيارية
│   └── types.py                   ← + حقول دلالية اختيارية
│
├── semantic_kernel/               ← حزمة النواة الدلالية
│   ├── __init__.py
│   ├── root_kernel.py             ← بناء نواة الجذر الدلالية
│   ├── pattern_transform.py       ← بناء مؤثر الوزن التحويلي
│   ├── form_profile.py            ← بناء الملف الدلالي للصيغة
│   ├── transfer.py                ← محرك نقل حمولة المعنى (لب المشروع)
│   ├── compatibility.py           ← فحص التوافق والحد الأدنى المكتمل
│   ├── economy.py                 ← محسّن الاقتصاد
│   ├── closure.py                 ← محرك إغلاق النواة الدلالية
│   └── seed_data.py               ← بيانات مرجعية للجذور والأوزان
│
├── weight/
│   ├── mizan.py                   ← + دعم اختياري للمتجهات الدلالية
│   └── closure.py                 ← + بوابة دلالية اختيارية
│
└── runtime/
    └── master_chain.py            ← + process_semantic_transfer()

tests/
├── test_semantic_kernel.py        ← 57 اختبارًا وحدويًا
└── test_semantic_integration.py   ← 9 اختبارات تكاملية
```
