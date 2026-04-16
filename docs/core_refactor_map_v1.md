# خريطة إعادة تشكيل القلب v1
## Core Refactor Map v1

> **Repository Path:** `docs/core_refactor_map_v1.md`

---

## فهرس المحتويات

1. [الغرض](#الغرض)
2. [المبدأ الحاكم](#المبدأ-الحاكم)
3. [ما يبقى كما هو](#ما-يبقى-كما-هو)
4. [ما يفكك](#ما-يفكك)
5. [ما يفصل إلى نوى مستقلة](#ما-يفصل-إلى-نوى-مستقلة)
6. [الترتيب التنفيذي](#الترتيب-التنفيذي)
7. [خريطة الملفات المقترحة](#خريطة-الملفات-المقترحة)
8. [معايير النجاح](#معايير-النجاح)

---

## الغرض

هذه الوثيقة تحدد:

- ما الذي يجب الحفاظ عليه
- ما الذي يجب تفكيكه
- ما الذي يجب فصله إلى package مستقلة
- ما الترتيب الصحيح لإعادة الهيكلة

---

## المبدأ الحاكم

لا نعيد البناء من الصفر بمحو كل شيء، ولا نرقع الهيكل القديم.
بل نتبع هذا القانون:

> **نُبقي الرصيد المعرفي والتنفيذي النافع، ونفصل النوى السيادية التي اختلطت، ثم نعيد ربطها تحت سلسلة واحدة.**

---

## ما يبقى كما هو

### 1. الرصيد الاختباري

يبقى مع إعادة التوزيع حسب المخاطر.

### 2. الرصيد الوثائقي الدستوري

يبقى ويصبح مرجعًا للتصميم:

- project goals
- unicode admissibility
- weight/mizan
- communicative/stylistic closure
- proposition-to-judgement transition

### 3. النماذج المفيدة الحالية

يبقى ما يصلح من:

- gate logic
- trace logic
- judgement records
- closure verification
- بعض وحدات root/pattern/ontology/evaluation

### 4. لغة المشروع العربية

تبقى سمة أساسية.

---

## ما يفكك

### 1. `core/enums.py`

يفكك إلى:

| الملف الجديد | المحتوى |
|-------------|---------|
| `core/enums_gate.py` | تعدادات البوابات |
| `core/enums_trace.py` | تعدادات التتبع |
| `core/enums_singular.py` | تعدادات المفرد |
| `core/enums_weight.py` | تعدادات الوزن |
| `core/enums_judgement.py` | تعدادات الحكم |
| `core/enums_domain.py` | تعدادات النطاقات |

### 2. `core/types.py`

يفكك إلى:

| الملف الجديد | المحتوى |
|-------------|---------|
| `core/types_gate.py` | أنماط البوابات |
| `core/types_trace.py` | أنماط التتبع |
| `core/types_singular.py` | أنماط المفرد |
| `core/types_weight.py` | أنماط الوزن |
| `core/types_composition.py` | أنماط التركيب |
| `core/types_judgement.py` | أنماط الحكم |

### 3. السلاسل المتعددة

تفكك من حيث السيادة، لا من حيث الحذف:

- واحدة تصبح **Master Chain**
- البقية **wrappers / runtime views / proof views**

---

## ما يفصل إلى نوى مستقلة

### النواة 1: Singular Core — نواة المفرد

| المكون | الوصف |
|--------|-------|
| `perception` | التصور المفرد |
| `information` | المعلومة المفردة |
| `concept` | المفهوم المفرد |

### النواة 2: Weight/Mizan Core — نواة الوزن والميزان

| المكون | الوصف |
|--------|-------|
| `weight classification` | تصنيف الوزن |
| `legality` | مشروعية الاشتقاق |
| `derivational eligibility` | أهلية الاشتقاق |
| `built/inflected relation` | العلاقة بين المبني والمعرب |
| `lexical structural eligibility` | الأهلية البنيوية المعجمية |

### النواة 3: Compositional Role Core — نواة التركيب والأدوار

| المكون | الوصف |
|--------|-------|
| `role distribution` | توزيع الأدوار |
| `asnadi relations` | العلاقات الإسنادية |
| `tadmini relations` | العلاقات التضمينية |
| `taqyidi relations` | العلاقات التقييدية |
| `عامل/معمول models` | نماذج العامل والمعمول |

### النواة 4: Proposition Core — نواة القضية

| المكون | الوصف |
|--------|-------|
| `proposition structure` | بنية القضية |
| `proposition closure` | إغلاق القضية |

### النواة 5: Communicative/Stylistic Core — نواة التواصل والأسلوب

| المكون | الوصف |
|--------|-------|
| `khabar/insha classification` | تصنيف الخبر والإنشاء |
| `communicative closure` | الإغلاق التواصلي |
| `stylistic closure` | الإغلاق الأسلوبي |

### النواة 6: Judgement Core — نواة الحكم

| المكون | الوصف |
|--------|-------|
| `subject` | الموضوع |
| `direction` | الجهة |
| `criterion` | المعيار |
| `content` | المحتوى |
| `rank` | الرتبة |
| `reason` | التعليل |
| `trace` | التتبع |

### النواة 7: Trace Core — نواة التتبع

| المكون | الوصف |
|--------|-------|
| `unified trace` | التتبع الموحد |
| `replay` | إعادة التشغيل |
| `audit` | التدقيق |
| `mismatch diagnosis` | تشخيص التعارض |

### النواة 8: Contracts Core — نواة العقود

| المكون | الوصف |
|--------|-------|
| `adjacency` | التجاور |
| `invariants` | الثوابت |
| `anti-jump` | منع القفز |
| `state mapping` | ربط الحالات |

---

## الترتيب التنفيذي

```
المرحلة 1 ──▶ المرحلة 2 ──▶ المرحلة 3 ──▶ المرحلة 4 ──▶ المرحلة 5 ──▶ المرحلة 6 ──▶ المرحلة 7
```

| المرحلة | العمل | المخاطر المعالجة |
|---------|-------|-----------------|
| **المرحلة 1** | فصل Singular Core | R5 |
| **المرحلة 2** | فصل Weight/Mizan Core | R6 |
| **المرحلة 3** | فصل Compositional Role Core | R7 |
| **المرحلة 4** | تحديد Master Chain | R2 |
| **المرحلة 5** | فصل Proposition → Communicative → Judgement transition | R8 |
| **المرحلة 6** | توحيد Trace و Contracts | R3, R9, R11 |
| **المرحلة 7** | إعادة ربط runtime و API لاحقًا فقط | R10 |

---

## خريطة الملفات المقترحة

```text
arabic_engine/
├── core/
│   ├── enums_gate.py
│   ├── enums_trace.py
│   ├── enums_singular.py
│   ├── enums_weight.py
│   ├── enums_judgement.py
│   ├── enums_domain.py
│   ├── types_gate.py
│   ├── types_trace.py
│   ├── types_singular.py
│   ├── types_weight.py
│   ├── types_composition.py
│   ├── types_judgement.py
│   └── __init__.py
│
├── singular/
│   ├── perception.py
│   ├── information.py
│   ├── concept.py
│   └── closure.py
│
├── weight/
│   ├── mizan.py
│   ├── classifier.py
│   ├── legality.py
│   ├── derivation.py
│   └── closure.py
│
├── composition/
│   ├── roles.py
│   ├── asnadi.py
│   ├── tadmini.py
│   ├── taqyidi.py
│   └── closure.py
│
├── proposition/
│   ├── structure.py
│   └── closure.py
│
├── communicative/
│   ├── khabar_insha.py
│   ├── stylistic.py
│   └── closure.py
│
├── judgement/
│   ├── model.py
│   ├── transition.py
│   └── closure.py
│
├── trace/
│   ├── unified.py
│   ├── replay.py
│   └── audit.py
│
├── contracts/
│   ├── adjacency.py
│   ├── invariants.py
│   ├── anti_jump.py
│   └── state_mapping.py
│
└── runtime/
    ├── master_chain.py
    ├── runtime_view.py
    └── proof_view.py
```

---

## معايير النجاح

يُعدّ الـ refactor ناجحًا **فقط** إذا تحقق الآتي:

| # | المعيار | الحالة |
|---|---------|--------|
| 1 | لم يعد `core` عنق زجاجة معرفي | ⬜ |
| 2 | أصبحت هناك Master Chain واحدة | ⬜ |
| 3 | صارت رتبة المفرد مستقلة وصريحة | ⬜ |
| 4 | صار الوزن نواة سيادية لا helper | ⬜ |
| 5 | صار التركيب توزيع أدوار لا مجرد parsing | ⬜ |
| 6 | صار الانتقال إلى الحكم مرحلة مستقلة | ⬜ |
| 7 | صارت العقود والتتبع enforceable لا وصفية فقط | ⬜ |
| 8 | بقي الرصيد الحالي محفوظًا ولم يُهدم بلا ضرورة | ⬜ |

---

## التوصية النهائية

**ابدؤوا بـ `Software Architecture Risk Register v1` أولًا، ثم `Core Refactor Map v1` مباشرة بعده.**
لأن الأولى تضبط **لماذا** نعيد التشكيل، والثانية تضبط **كيف** نعيده.

الخطوة التالية الأنسب: تحويل هاتين الوثيقتين إلى **خطة تنفيذ من 4 أسابيع** بأولويات أسبوعية واضحة.
